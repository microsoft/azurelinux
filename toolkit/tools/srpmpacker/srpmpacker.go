// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"crypto/tls"
	"crypto/x509"
	"fmt"
	"io/ioutil"
	"os"
	"path"
	"path/filepath"
	"reflect"
	"runtime"
	"strings"
	"sync"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/buildpipeline"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/directory"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/network"
	packagelist "github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packlist"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/retry"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/rpm"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/profile"

	"gopkg.in/alecthomas/kingpin.v2"
)

type fileSignaturesWrapper struct {
	FileSignatures map[string]string `json:"Signatures"`
}

const (
	srpmOutDir     = "SRPMS"
	srpmSPECDir    = "SPECS"
	srpmSOURCESDir = "SOURCES"
)

type fileType int

const (
	fileTypePatch  fileType = iota
	fileTypeSource fileType = iota
)

type signatureHandlingType int

const (
	signatureEnforce   signatureHandlingType = iota
	signatureSkipCheck signatureHandlingType = iota
	signatureUpdate    signatureHandlingType = iota
)

const (
	signatureEnforceString   = "enforce"
	signatureSkipCheckString = "skip"
	signatureUpdateString    = "update"
)

const (
	defaultBuildDir    = "./build/SRPMS"
	defaultWorkerCount = "80"
	defaultNetOpsCount = "10"
)

// sourceRetrievalConfiguration holds information on where to hydrate files from.
type sourceRetrievalConfiguration struct {
	localSourceDir string
	sourceURL      string
	caCerts        *x509.CertPool
	tlsCerts       []tls.Certificate

	signatureHandling signatureHandlingType
	signatureLookup   map[string]string
}

// packResult holds the worker results from packing a SPEC file into an SRPM.
type packResult struct {
	specFile string
	srpmFile string
	err      error
}

// specState holds the state of a SPEC file: if it should be packed and the resulting SRPM if it is.
type specState struct {
	specFile string
	srpmFile string
	toPack   bool
	err      error
}

var (
	app = kingpin.New("srpmpacker", "A tool to package a SRPM.")

	specsDir      = exe.InputDirFlag(app, "Path to the SPEC directory to create SRPMs from.")
	outDir        = exe.OutputDirFlag(app, "Directory to place the output SRPM.")
	logFile       = exe.LogFileFlag(app)
	logLevel      = exe.LogLevelFlag(app)
	profFlags     = exe.SetupProfileFlags(app)
	timestampFile = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()

	buildDir     = app.Flag("build-dir", "Directory to store temporary files while building.").Default(defaultBuildDir).String()
	distTag      = app.Flag("dist-tag", "The distribution tag SRPMs will be built with.").Required().String()
	packListFile = app.Flag("pack-list", "Path to a list of SPECs to pack. If empty will pack all SPECs.").ExistingFile()
	runCheck     = app.Flag("run-check", "Whether or not to run the spec file's check section during package build.").Bool()

	workers          = app.Flag("workers", "Number of concurrent goroutines to parse with.").Default(defaultWorkerCount).Uint()
	concurrentNetOps = app.Flag("concurrent-net-ops", "Number of concurrent network operations to perform.").Default(defaultNetOpsCount).Uint()
	repackAll        = app.Flag("repack", "Rebuild all SRPMs, even if already built.").Bool()
	nestedSourcesDir = app.Flag("nested-sources", "Set if for a given SPEC, its sources are contained in a SOURCES directory next to the SPEC file.").Bool()

	// Use String() and not ExistingFile() as the Makefile may pass an empty string if the user did not specify any of these options
	sourceURL     = app.Flag("source-url", "URL to a source server to download SPEC sources from.").String()
	caCertFile    = app.Flag("ca-cert", "Root certificate authority to use when downloading files.").String()
	tlsClientCert = app.Flag("tls-cert", "TLS client certificate to use when downloading files.").String()
	tlsClientKey  = app.Flag("tls-key", "TLS client key to use when downloading files.").String()

	workerTar = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz. If this argument is empty, SRPMs will be packed in the host environment.").ExistingFile()

	validSignatureLevels = []string{signatureEnforceString, signatureSkipCheckString, signatureUpdateString}
	signatureHandling    = app.Flag("signature-handling", "Specifies how to handle signature mismatches for source files.").Default(signatureEnforceString).PlaceHolder(exe.PlaceHolderize(validSignatureLevels)).Enum(validSignatureLevels...)
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	prof, err := profile.StartProfiling(profFlags)
	if err != nil {
		logger.Log.Warnf("Could not start profiling: %s", err)
	}
	defer prof.StopProfiler()

	timestamp.BeginTiming("srpmpacker", *timestampFile)
	defer timestamp.CompleteTiming()

	timestamp.StartEvent("configuring packer", nil)

	// Create a template configuration that all packed SRPM will be based on.
	var templateSrcConfig sourceRetrievalConfiguration

	switch *signatureHandling {
	case signatureEnforceString:
		templateSrcConfig.signatureHandling = signatureEnforce
	case signatureSkipCheckString:
		logger.Log.Warn("Skipping signature enforcement")
		templateSrcConfig.signatureHandling = signatureSkipCheck
	case signatureUpdateString:
		logger.Log.Warn("Will update signature files as needed")
		templateSrcConfig.signatureHandling = signatureUpdate
	default:
		logger.Log.Fatalf("Invalid signature handling encountered: %s. Allowed: %s", *signatureHandling, validSignatureLevels)
	}

	// Setup remote source configuration
	templateSrcConfig.sourceURL = *sourceURL
	templateSrcConfig.caCerts, err = x509.SystemCertPool()
	logger.PanicOnError(err, "Received error calling x509.SystemCertPool(). Error: %v", err)
	if *caCertFile != "" {
		newCACert, err := ioutil.ReadFile(*caCertFile)
		if err != nil {
			logger.Log.Panicf("Invalid CA certificate (%s), error: %s", *caCertFile, err)
		}

		templateSrcConfig.caCerts.AppendCertsFromPEM(newCACert)
	}

	if *tlsClientCert != "" && *tlsClientKey != "" {
		cert, err := tls.LoadX509KeyPair(*tlsClientCert, *tlsClientKey)
		if err != nil {
			logger.Log.Panicf("Invalid TLS client key pair (%s) (%s), error: %s", *tlsClientCert, *tlsClientKey, err)
		}

		templateSrcConfig.tlsCerts = append(templateSrcConfig.tlsCerts, cert)
	}

	timestamp.StopEvent(nil)

	// A pack list may be provided, if so only pack this subset.
	// If non is provided, pack all srpms.
	packList, err := packagelist.ParsePackageListFile(*packListFile)
	logger.PanicOnError(err)

	err = createAllSRPMsWrapper(*specsDir, *distTag, *buildDir, *outDir, *workerTar, *workers, *concurrentNetOps, *nestedSourcesDir, *repackAll, *runCheck, packList, templateSrcConfig)
	logger.PanicOnError(err)
}

// createAllSRPMsWrapper wraps createAllSRPMs to conditionally run it inside a chroot.
// If workerTar is non-empty, packing will occur inside a chroot, otherwise it will run on the host system.
func createAllSRPMsWrapper(specsDir, distTag, buildDir, outDir, workerTar string, workers, concurrentNetOps uint, nestedSourcesDir, repackAll, runCheck bool, packList map[string]bool, templateSrcConfig sourceRetrievalConfiguration) (err error) {
	var chroot *safechroot.Chroot
	originalOutDir := outDir
	if workerTar != "" {
		const leaveFilesOnDisk = false
		chroot, buildDir, outDir, specsDir, err = createChroot(workerTar, buildDir, outDir, specsDir)
		if err != nil {
			return
		}
		defer chroot.Close(leaveFilesOnDisk)
	}

	doCreateAll := func() error {
		return createAllSRPMs(specsDir, distTag, buildDir, outDir, workers, concurrentNetOps, nestedSourcesDir, repackAll, runCheck, packList, templateSrcConfig)
	}

	if chroot != nil {
		logger.Log.Info("Packing SRPMs inside a chroot environment")
		err = chroot.Run(doCreateAll)
	} else {
		logger.Log.Info("Packing SRPMs in the host environment")
		err = doCreateAll()
	}

	if err != nil {
		return
	}

	// If this is container build then the bind mounts will not have been created.
	// Copy the chroot output to host output folder.
	if !buildpipeline.IsRegularBuild() {
		srpmsInChroot := filepath.Join(chroot.RootDir(), outDir)
		err = directory.CopyContents(srpmsInChroot, originalOutDir)
	}

	return
}

// createAllSRPMs will find all SPEC files in specsDir and pack SRPMs for them if needed.
func createAllSRPMs(specsDir, distTag, buildDir, outDir string, workers, concurrentNetOps uint, nestedSourcesDir, repackAll, runCheck bool, packList map[string]bool, templateSrcConfig sourceRetrievalConfiguration) (err error) {
	logger.Log.Infof("Finding all SPEC files")
	timestamp.StartEvent("packing SRPMS", nil)
	defer timestamp.StopEvent(nil)

	timestamp.StartEvent("determining specs to pack", nil)
	specFiles, err := findSPECFiles(specsDir, packList)
	if err != nil {
		return
	}

	specStates, err := calculateSPECsToRepack(specFiles, distTag, outDir, nestedSourcesDir, repackAll, runCheck, workers)
	if err != nil {
		return
	}
	timestamp.StopEvent(nil)

	err = packSRPMs(specStates, distTag, buildDir, templateSrcConfig, workers, concurrentNetOps)
	return
}

// findSPECFiles finds all SPEC files that should be considered for packing.
// Takes into consideration a packList if provided.
func findSPECFiles(specsDir string, packList map[string]bool) (specFiles []string, err error) {
	if len(packList) == 0 {
		specSearch := filepath.Join(specsDir, "**/*.spec")
		specFiles, err = filepath.Glob(specSearch)
	} else {
		for specName := range packList {
			var specFile []string

			specSearch := filepath.Join(specsDir, fmt.Sprintf("**/%s.spec", specName))
			specFile, err = filepath.Glob(specSearch)

			// If a SPEC is in the pack list, it must be packed.
			if err != nil {
				return
			}
			if len(specFile) != 1 {
				if strings.HasPrefix(specName, "msopenjdk-11") {
					logger.Log.Debugf("Ignoring missing match for '%s', which is externally-provided and thus doesn't have a local spec.", specName)
					continue
				} else {
					err = fmt.Errorf("unexpected number of matches (%d) for spec file (%s)", len(specFile), specName)
					return
				}
			}

			specFiles = append(specFiles, specFile[0])
		}
	}

	return
}

// createChroot creates a chroot to pack SRPMs inside of.
func createChroot(workerTar, buildDir, outDir, specsDir string) (chroot *safechroot.Chroot, newBuildDir, newOutDir, newSpecsDir string, err error) {
	const (
		chrootName       = "srpmpacker_chroot"
		existingDir      = false
		leaveFilesOnDisk = false

		outMountPoint    = "/output"
		specsMountPoint  = "/specs"
		buildDirInChroot = "/build"
	)
	timestamp.StartEvent("create chroot", nil)
	defer timestamp.StopEvent(nil)

	extraMountPoints := []*safechroot.MountPoint{
		safechroot.NewMountPoint(outDir, outMountPoint, "", safechroot.BindMountPointFlags, ""),
		safechroot.NewMountPoint(specsDir, specsMountPoint, "", safechroot.BindMountPointFlags, ""),
	}

	extraDirectories := []string{
		buildDirInChroot,
	}

	newBuildDir = buildDirInChroot
	newOutDir = outMountPoint
	newSpecsDir = specsMountPoint

	chrootDir := filepath.Join(buildDir, chrootName)
	chroot = safechroot.NewChroot(chrootDir, existingDir)

	err = chroot.Initialize(workerTar, extraDirectories, extraMountPoints)
	if err != nil {
		return
	}

	defer func() {
		if err != nil {
			closeErr := chroot.Close(leaveFilesOnDisk)
			if closeErr != nil {
				logger.Log.Errorf("Failed to close chroot, err: %s", closeErr)
			}
		}
	}()

	// If this is container build then the bind mounts will not have been created.
	if !buildpipeline.IsRegularBuild() {
		// Copy in all of the SPECs so they can be packed.
		specsInChroot := filepath.Join(chroot.RootDir(), newSpecsDir)
		err = directory.CopyContents(specsDir, specsInChroot)
		if err != nil {
			return
		}

		// Copy any prepacked srpms so they will not be repacked.
		srpmsInChroot := filepath.Join(chroot.RootDir(), newOutDir)
		err = directory.CopyContents(outDir, srpmsInChroot)
		if err != nil {
			return
		}
	}

	// Networking support is needed to download sources.
	files := []safechroot.FileToCopy{
		{Src: "/etc/resolv.conf", Dest: "/etc/resolv.conf"},
	}

	err = chroot.AddFiles(files...)
	return
}

// calculateSPECsToRepack will check which SPECs should be packed.
// If the resulting SRPM does not exist, or is older than a modification to
// one of the files used by the SPEC then it is repacked.
func calculateSPECsToRepack(specFiles []string, distTag, outDir string, nestedSourcesDir, repackAll, runCheck bool, workers uint) (states []*specState, err error) {
	var wg sync.WaitGroup

	requests := make(chan string, len(specFiles))
	results := make(chan *specState, len(specFiles))
	cancel := make(chan struct{})

	logger.Log.Infof("Calculating SPECs to repack")

	arch, err := rpm.GetRpmArch(runtime.GOARCH)
	if err != nil {
		return
	}

	// Start the workers now so they begin working as soon as a new job is buffered.
	for i := uint(0); i < workers; i++ {
		wg.Add(1)
		go specsToPackWorker(requests, results, cancel, &wg, distTag, outDir, arch, nestedSourcesDir, repackAll, runCheck)
	}

	for _, specFile := range specFiles {
		requests <- specFile
	}

	// Signal to the workers that there are no more new spec files
	close(requests)

	// Transfer the results from the channel into states.
	//
	// While the channel itself could be returned and passed to the consumer of
	// the results, additional functionality would have to be added to limit the total workers
	// in use at any given time.
	//
	// Since this worker pool and future worker pools in the application are opening file descriptors
	// if too many are active at once it can exhaust the file descriptor limit.
	// Currently all functions that employ workers pool of size `workers` are serialized,
	// resulting in `workers` being the upper capacity at any given time.
	totalToRepack := 0
	states = make([]*specState, len(specFiles))
	for i := 0; i < len(specFiles); i++ {
		result := <-results
		states[i] = result

		if result.err != nil {
			logger.Log.Errorf("Failed to check (%s). Error: %s", result.specFile, result.err)
			err = result.err
			close(cancel)
			break
		}

		if result.toPack {
			totalToRepack++
		}
	}

	logger.Log.Debug("Waiting for outstanding workers to finish")
	wg.Wait()

	if err != nil {
		return
	}

	logger.Log.Infof("Packing %d/%d SPECs", totalToRepack, len(specFiles))
	return
}

// specsToPackWorker will process a channel of spec files that should be checked if packing is needed.
func specsToPackWorker(requests <-chan string, results chan<- *specState, cancel <-chan struct{}, wg *sync.WaitGroup, distTag, outDir string, arch string, nestedSourcesDir, repackAll, runCheck bool) {
	const (
		queryFormat         = `%{NAME}-%{VERSION}-%{RELEASE}.src.rpm`
		nestedSourceDirName = "SOURCES"
	)

	const (
		srpmQueryResultsIndex   = iota
		expectedQueryResultsLen = iota
	)

	defer wg.Done()

	for specFile := range requests {
		select {
		case <-cancel:
			logger.Log.Debug("Cancellation signal received")
			return
		default:
		}

		result := &specState{
			specFile: specFile,
		}

		containingDir := filepath.Dir(specFile)

		// Find the SRPM that this SPEC will produce.
		defines := rpm.DefaultDefinesWithDist(runCheck, distTag)

		// Allow the user to configure if the SPEC sources are in a nested 'SOURCES' directory.
		// Otherwise assume source files are next to the SPEC file.
		sourceDir := containingDir
		if nestedSourcesDir {
			sourceDir = filepath.Join(sourceDir, nestedSourceDirName)
		}
		specQueryResults, err := rpm.QuerySPEC(specFile, sourceDir, queryFormat, arch, defines, rpm.QueryHeaderArgument)

		if err != nil {
			if err.Error() == rpm.NoCompatibleArchError {
				logger.Log.Infof("Skipping SPEC (%s) due to incompatible build architecture", specFile)
			} else {
				result.err = err
			}

			results <- result
			continue
		}

		if len(specQueryResults) != expectedQueryResultsLen {
			result.err = fmt.Errorf("unexpected query results, wanted (%d) results but got (%d), results: %v", expectedQueryResultsLen, len(specQueryResults), specQueryResults)
			results <- result
			continue
		}

		// Resolve the full path of the SRPM that would be packed from this SPEC file.
		producedSRPM := specQueryResults[srpmQueryResultsIndex]
		fullSRPMPath := filepath.Join(outDir, producedSRPM)
		result.srpmFile = fullSRPMPath

		if repackAll {
			result.toPack = true
			results <- result
			continue
		}

		// Sanity check that SRPMS is meant to be built for the machine architecture
		isCompatible, err := rpm.SpecArchIsCompatible(specFile, sourceDir, arch, defines)
		if err != nil {
			result.err = err
			results <- result
			continue
		}

		if !isCompatible {
			logger.Log.Infof(`Skipping (%s) since it cannot be built on current architecture.`, specFile)
			results <- result
			continue
		}

		// Check if the SRPM is already on disk and if so its modification time.
		srpmInfo, err := os.Stat(fullSRPMPath)
		if err != nil {
			logger.Log.Debugf("Updating (%s) since (%s) is not yet built", specFile, fullSRPMPath)
			result.toPack = true
			results <- result
			continue
		}

		// Check if a file used by the SPEC has been modified since the resulting SRPM was previously packed.
		specModTime, latestFile, err := directory.LastModifiedFile(containingDir)
		if err != nil {
			result.err = fmt.Errorf("failed to query modification time for SPEC (%s). Error: %s", specFile, err)
			results <- result
			continue
		}

		if specModTime.After(srpmInfo.ModTime()) {
			logger.Log.Debugf("Updating (%s) since (%s) has changed", specFile, latestFile)
			result.toPack = true
		}

		results <- result
	}
}

// packSRPMs will pack any SPEC files that have been marked as `toPack`.
func packSRPMs(specStates []*specState, distTag, buildDir string, templateSrcConfig sourceRetrievalConfiguration, workers, concurrentNetOps uint) (err error) {
	tsRoot, _ := timestamp.StartEvent("packing SRPMs", nil)
	defer timestamp.StopEvent(nil)
	var wg sync.WaitGroup

	allSpecStates := make(chan *specState, len(specStates))
	results := make(chan *packResult, len(specStates))
	cancel := make(chan struct{})
	netOpsSemaphore := make(chan struct{}, concurrentNetOps)

	// Start the workers now so they begin working as soon as a new job is buffered.
	for i := 0; uint(i) < workers; i++ {
		wg.Add(1)
		go packSRPMWorker(allSpecStates, results, cancel, netOpsSemaphore, &wg, distTag, buildDir, templateSrcConfig, tsRoot)
	}

	for _, state := range specStates {
		allSpecStates <- state
	}

	// Signal to the workers that there are no more new spec files
	close(allSpecStates)

	for i := 0; i < len(specStates); i++ {
		result := <-results

		if result.err != nil {
			logger.Log.Errorf("Failed to pack (%s). Cancelling outstanding workers. Error: %s", result.specFile, result.err)
			err = result.err
			close(cancel)
			break
		}

		// Skip results for states that were not packed by request
		if result.srpmFile == "" {
			continue
		}

		logger.Log.Infof("Packed (%s) -> (%s)", filepath.Base(result.specFile), filepath.Base(result.srpmFile))
	}

	logger.Log.Debug("Waiting for outstanding workers to finish")
	wg.Wait()

	return
}

// packSRPMWorker will process a channel of SPECs and pack any that are marked as toPack.
func packSRPMWorker(allSpecStates <-chan *specState, results chan<- *packResult, cancel <-chan struct{}, netOpsSemaphore chan struct{}, wg *sync.WaitGroup, distTag, buildDir string, templateSrcConfig sourceRetrievalConfiguration, tsRoot *timestamp.TimeStamp) {
	defer wg.Done()

	for specState := range allSpecStates {
		select {
		case <-cancel:
			logger.Log.Debug("Cancellation signal received")
			return
		default:
		}

		ts, _ := timestamp.StartEvent(filepath.Base(specState.specFile), tsRoot)

		result := &packResult{
			specFile: specState.specFile,
		}

		// Its a no-op if the SPEC does not need to be packed
		if !specState.toPack {
			results <- result
			timestamp.StopEvent(ts)
			continue
		}

		// Setup a source retrieval configuration based on the provided template
		signaturesFilePath := specPathToSignaturesPath(specState.specFile)
		srcConfig, err := initializeSourceConfig(templateSrcConfig, signaturesFilePath)
		if err != nil {
			result.err = err
			results <- result
			continue
		}

		fullOutDirPath := filepath.Dir(specState.srpmFile)
		err = os.MkdirAll(fullOutDirPath, os.ModePerm)
		if err != nil {
			result.err = err
			results <- result
			continue
		}

		outputPath, err := packSingleSPEC(specState.specFile, specState.srpmFile, signaturesFilePath, buildDir, fullOutDirPath, distTag, srcConfig, cancel, netOpsSemaphore)
		if err != nil {
			result.err = err
			results <- result
			continue
		}

		result.srpmFile = outputPath

		results <- result
		timestamp.StopEvent(ts)
	}
}

func specPathToSignaturesPath(specFilePath string) string {
	const (
		specSuffix          = ".spec"
		signatureFileSuffix = "signatures.json"
	)

	specName := strings.TrimSuffix(filepath.Base(specFilePath), specSuffix)
	signatureFileName := fmt.Sprintf("%s.%s", specName, signatureFileSuffix)
	signatureFileDirPath := filepath.Dir(specFilePath)

	return filepath.Join(signatureFileDirPath, signatureFileName)
}

func initializeSourceConfig(templateSrcConfig sourceRetrievalConfiguration, signaturesFilePath string) (srcConfig sourceRetrievalConfiguration, err error) {
	srcConfig = templateSrcConfig
	srcConfig.localSourceDir = filepath.Dir(signaturesFilePath)

	// Read the signatures file for the SPEC sources if applicable
	if srcConfig.signatureHandling != signatureSkipCheck {
		srcConfig.signatureLookup, err = readSignatures(signaturesFilePath)
	}

	return srcConfig, err
}

func readSignatures(signaturesFilePath string) (readSignatures map[string]string, err error) {
	var signaturesWrapper fileSignaturesWrapper
	signaturesWrapper.FileSignatures = make(map[string]string)

	err = jsonutils.ReadJSONFile(signaturesFilePath, &signaturesWrapper)
	if err != nil {
		if os.IsNotExist(err) {
			// Non-fatal as some SPECs may not have sources
			logger.Log.Debugf("The signatures file (%s) doesn't exist, will not pre-populate signatures.", signaturesFilePath)
			err = nil
		} else {
			logger.Log.Errorf("Failed to read the signatures file (%s): %v.", signaturesFilePath, err)
		}
	}

	return signaturesWrapper.FileSignatures, err
}

// packSingleSPEC will pack a given SPEC file into an SRPM.
func packSingleSPEC(specFile, srpmFile, signaturesFile, buildDir, outDir, distTag string, srcConfig sourceRetrievalConfiguration, cancel <-chan struct{}, netOpsSemaphore chan struct{}) (outputPath string, err error) {
	srpmName := filepath.Base(srpmFile)
	workingDir := filepath.Join(buildDir, srpmName)

	logger.Log.Debugf("Working directory: %s", workingDir)

	err = os.MkdirAll(workingDir, os.ModePerm)
	if err != nil {
		return
	}
	defer cleanupSRPMWorkingDir(workingDir)

	// Make the folder structure needed for rpmbuild
	err = createRPMBuildFolderStructure(workingDir)
	if err != nil {
		return
	}

	// Copy the SPEC file in
	srpmSpecFile := filepath.Join(workingDir, srpmSPECDir, filepath.Base(specFile))
	err = file.Copy(specFile, srpmSpecFile)
	if err != nil {
		return
	}

	// Track the current signatures of source files used by the SPEC.
	// This will only contain signatures that have either been validated or updated by this tool.
	currentSignatures := make(map[string]string)

	defines := rpm.DefaultDefines(*runCheck)
	if distTag != "" {
		defines[rpm.DistTagDefine] = distTag
	}

	// Hydrate all patches. Exclusively using `sourceDir`
	err = hydrateFiles(fileTypePatch, specFile, workingDir, srcConfig, currentSignatures, defines, nil, nil)
	if err != nil {
		return
	}

	// Hydrate all sources. Download any missing ones not in `sourceDir`
	err = hydrateFiles(fileTypeSource, specFile, workingDir, srcConfig, currentSignatures, defines, cancel, netOpsSemaphore)
	if err != nil {
		return
	}

	err = updateSignaturesIfApplicable(signaturesFile, srcConfig, currentSignatures)

	// Build the SRPM itself, using `workingDir` as the topdir
	err = rpm.GenerateSRPMFromSPEC(specFile, workingDir, defines)
	if err != nil {
		return
	}

	// Save the output of the build to `outDir`
	outputPath, err = copyOutput(workingDir, outDir)
	return
}

func updateSignaturesIfApplicable(signaturesFile string, srcConfig sourceRetrievalConfiguration, currentSignatures map[string]string) (err error) {
	if srcConfig.signatureHandling == signatureUpdate && !reflect.DeepEqual(srcConfig.signatureLookup, currentSignatures) {
		logger.Log.Infof("Updating (%s)", signaturesFile)

		outputSignatures := fileSignaturesWrapper{
			FileSignatures: currentSignatures,
		}

		err = jsonutils.WriteJSONFile(signaturesFile, outputSignatures)
		if err != nil {
			logger.Log.Warnf("Unable to update signatures file (%s)", signaturesFile)
			return
		}
	}

	return
}

func createRPMBuildFolderStructure(workingDir string) (err error) {
	dirsToCreate := []string{
		srpmSOURCESDir,
		srpmSPECDir,
		srpmOutDir,
	}

	for _, dir := range dirsToCreate {
		err = os.MkdirAll(path.Join(workingDir, dir), os.ModePerm)
		if err != nil {
			return
		}
	}

	return
}

// readSPECTagArray will return an array of tag values from the given specfile.
// (e.g. all SOURCE entries)
func readSPECTagArray(specFile, sourceDir, tag string, arch string, defines map[string]string) (tagValues []string, err error) {
	queryFormat := fmt.Sprintf(`[%%{%s}\n]`, tag)
	return rpm.QuerySPEC(specFile, sourceDir, queryFormat, arch, defines, rpm.QueryHeaderArgument)
}

// hydrateFiles will attempt to retrieve all sources needed to build an SRPM from a SPEC.
// Will alter `currentSignatures`,
func hydrateFiles(fileTypeToHydrate fileType, specFile, workingDir string, srcConfig sourceRetrievalConfiguration, currentSignatures, defines map[string]string, cancel <-chan struct{}, netOpsSemaphore chan struct{}) (err error) {
	const (
		downloadMissingPatchFiles = false
		skipPatchSignatures       = true

		downloadMissingSourceFiles = true
		skipSourceSignatures       = false

		patchTag  = "PATCH"
		sourceTag = "SOURCE"
	)

	var (
		specTag               string
		hydrateRemotely       bool
		skipSignatureHandling bool
	)

	switch fileTypeToHydrate {
	case fileTypePatch:
		specTag = patchTag
		hydrateRemotely = downloadMissingPatchFiles
		skipSignatureHandling = skipPatchSignatures
	case fileTypeSource:
		specTag = sourceTag
		hydrateRemotely = downloadMissingSourceFiles
		skipSignatureHandling = skipSourceSignatures
	default:
		return fmt.Errorf("invalid filetype (%d)", fileTypeToHydrate)
	}

	newSourceDir := filepath.Join(workingDir, srpmSOURCESDir)
	fileHydrationState := make(map[string]bool)

	// Only consult the current build system's arch
	// We don't care about the target arch since SRPMs should be packaged in an architecture agnostic manner
	arch, err := rpm.GetRpmArch(runtime.GOARCH)
	if err != nil {
		return
	}

	// Collect a list of files of type `specTag` needed for this SRPM
	filesNeeded, err := readSPECTagArray(specFile, srcConfig.localSourceDir, specTag, arch, defines)
	if err != nil {
		return
	}

	for _, fileNeeded := range filesNeeded {
		fileHydrationState[fileNeeded] = false
	}

	// If the user provided an existing source dir, prefer it over remote sources.
	if srcConfig.localSourceDir != "" {
		err = hydrateFromLocalSource(fileHydrationState, newSourceDir, srcConfig, skipSignatureHandling, currentSignatures)
		// On error warn and default to hydrating from an external server.
		if err != nil {
			logger.Log.Warnf("Error hydrating from local source directory (%s): %v", srcConfig.localSourceDir, err)
		}
	}

	if hydrateRemotely && srcConfig.sourceURL != "" {
		err = hydrateFromRemoteSource(fileHydrationState, newSourceDir, srcConfig, skipSignatureHandling, currentSignatures, cancel, netOpsSemaphore)
		if err != nil {
			return
		}
	}

	for fileNeeded, alreadyHydrated := range fileHydrationState {
		if !alreadyHydrated {
			err = fmt.Errorf("unable to hydrate file: %s", fileNeeded)
			logger.Log.Error(err)
		}
	}

	return
}

// hydrateFromLocalSource will update fileHydrationState.
// Will alter currentSignatures.
func hydrateFromLocalSource(fileHydrationState map[string]bool, newSourceDir string, srcConfig sourceRetrievalConfiguration, skipSignatureHandling bool, currentSignatures map[string]string) (err error) {
	err = filepath.Walk(srcConfig.localSourceDir, func(path string, info os.FileInfo, err error) error {
		isFile, _ := file.IsFile(path)
		if !isFile {
			return nil
		}

		fileName := filepath.Base(path)

		isHydrated, found := fileHydrationState[fileName]
		if !found {
			return nil
		}

		if isHydrated {
			logger.Log.Warnf("Duplicate matching file found at (%s), skipping", path)
			return nil
		}

		if !skipSignatureHandling {
			err = validateSignature(path, srcConfig, currentSignatures)
			if err != nil {
				return err
			}
		}

		err = file.Copy(path, filepath.Join(newSourceDir, fileName))
		if err != nil {
			logger.Log.Warnf("Failed to copy file (%s), skipping. Error: %s", path, err)
			return nil
		}

		logger.Log.Debugf("Hydrated (%s) from (%s)", fileName, path)

		fileHydrationState[fileName] = true
		return nil
	})

	return
}

// hydrateFromRemoteSource will update fileHydrationState.
// Will alter `currentSignatures`.
func hydrateFromRemoteSource(fileHydrationState map[string]bool, newSourceDir string, srcConfig sourceRetrievalConfiguration, skipSignatureHandling bool, currentSignatures map[string]string, cancel <-chan struct{}, netOpsSemaphore chan struct{}) (err error) {
	const (
		// With 5 attempts, initial delay of 1 second, and a backoff factor of 2.0 the total time spent retrying will be
		// ~30 seconds.
		downloadRetryAttempts = 5
		failureBackoffBase    = 2.0
		downloadRetryDuration = time.Second
	)
	errPackerCancelReceived := fmt.Errorf("packer cancel signal received")

	// Making sure we remove the hydrated file in case of signature validation failure.
	filesToRemove := []string{}
	defer func() {
		for _, fileToRemove := range filesToRemove {
			logger.Log.Debugf("Removing file (%s) after signature validation failure.", fileToRemove)
			removeErr := os.Remove(fileToRemove)
			if removeErr != nil {
				logger.Log.Errorf("Failed to delete file (%s) after signature validation failure. Error: %s", fileToRemove, removeErr)
			}
		}
	}()

	for fileName, alreadyHydrated := range fileHydrationState {
		if alreadyHydrated {
			continue
		}

		destinationFile := filepath.Join(newSourceDir, fileName)

		url := network.JoinURL(srcConfig.sourceURL, fileName)

		// Limit the number of concurrent network operations by pushing a struct{} into the channel. This will block until
		// another operation completes and removes the struct{} from the channel.
		if netOpsSemaphore != nil {
			select {
			case netOpsSemaphore <- struct{}{}:
			case <-cancel:
				logger.Log.Debug("Cancellation signal received at network operation semaphore")
				err = errPackerCancelReceived
				return
			}
		}

		cancelled, internalErr := retry.RunWithExpBackoff(func() error {
			downloadErr := network.DownloadFile(url, destinationFile, srcConfig.caCerts, srcConfig.tlsCerts)
			if downloadErr != nil {
				logger.Log.Debugf("Failed an attempt to download (%s). Error: %s", url, downloadErr)
			}

			return downloadErr
		}, downloadRetryAttempts, downloadRetryDuration, failureBackoffBase, cancel)

		if netOpsSemaphore != nil {
			// Clear the channel to allow another operation to start
			<-netOpsSemaphore
		}

		// We may intentionally fail early due to a cancellation signal, stop immediately if that is the case.
		if cancelled {
			err = errPackerCancelReceived
			return
		}

		if internalErr != nil {
			logger.Log.Errorf("Failed to download (%s). Error: %s", url, internalErr)
			continue
		}

		if !skipSignatureHandling {
			internalErr = validateSignature(destinationFile, srcConfig, currentSignatures)
			if internalErr != nil {
				logger.Log.Errorf("Signature validation for (%s) failed. Error: %s.", destinationFile, internalErr)
				filesToRemove = append(filesToRemove, destinationFile)
				continue
			}
		}

		fileHydrationState[fileName] = true
		logger.Log.Debugf("Hydrated (%s) from (%s)", fileName, url)
	}

	return
}

// validateSignature will compare the SHA256 of the file at path against the signature for it in srcConfig.signatureLookup
// Will skip if signature handling is set to skip.
// Will alter `currentSignatures`.
func validateSignature(path string, srcConfig sourceRetrievalConfiguration, currentSignatures map[string]string) (err error) {
	if srcConfig.signatureHandling == signatureSkipCheck {
		return
	}

	fileName := filepath.Base(path)
	expectedSignature, found := srcConfig.signatureLookup[fileName]
	if !found && srcConfig.signatureHandling != signatureUpdate {
		err = fmt.Errorf("no signature for file (%s) found. full path is (%s)", fileName, path)
		return
	}

	newSignature, err := file.GenerateSHA256(path)
	if err != nil {
		return
	}

	if strings.EqualFold(expectedSignature, newSignature) {
		currentSignatures[fileName] = newSignature
	} else {
		if srcConfig.signatureHandling == signatureUpdate {
			logger.Log.Warnf("Updating signature for (%s) from (%s) to (%s)", fileName, expectedSignature, newSignature)
			currentSignatures[fileName] = newSignature
		} else {
			return fmt.Errorf("file (%s) has mismatching signature: expected (%s) - actual (%s)", path, expectedSignature, newSignature)
		}
	}

	return
}

// copyOutput will copy the built SRPMs from workingDir to the specified output directory.
func copyOutput(workingDir, outDir string) (outputPath string, err error) {
	rpmbuildOutDir := filepath.Join(workingDir, srpmOutDir)
	err = filepath.Walk(rpmbuildOutDir, func(path string, info os.FileInfo, err error) error {
		isFile, _ := file.IsFile(path)
		if !isFile {
			return nil
		}
		outputPath = filepath.Join(outDir, filepath.Base(path))
		return file.Copy(path, outputPath)
	})

	return
}

// cleanupSRPMWorkingDir will delete the working directory for the SRPM build.
func cleanupSRPMWorkingDir(workingDir string) {
	err := os.RemoveAll(workingDir)
	if err != nil {
		logger.Log.Warnf("Unable to cleanup working directory: %s", workingDir)
	}
}
