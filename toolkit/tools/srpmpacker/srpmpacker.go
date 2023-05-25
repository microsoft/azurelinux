// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"bufio"
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
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/retry"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/rpm"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/spectosrpm"
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
	defaultWorkerCount = "0"
	// rpmbuild usually sits doing nothing most of the time, so we can run multiple instances of it in parallel.
	defaultWorkerCountMultiplier = 8
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
	keepListFile = app.Flag("keep-list", "Path to a list of SPECs to keep. If empty will keep all SPECs.").ExistingFile()
	doTidy       = app.Flag("tidy", "Whether or not to tidy the SRPMs before packing.").Bool()
	summaryFile  = app.Flag("summary-file", "Path to a file to write a summary of the SRPMs created.").String()
	runCheck     = app.Flag("run-check", "Whether or not to run the spec file's check section during package build.").Bool()

	workers          = app.Flag("workers", "Number of concurrent goroutines to parse with.").Default(defaultWorkerCount).Int()
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

	// rpmbuild is fairly light and single-threaded, so we can run multiple instances of it in parallel.
	if *workers <= 0 {
		*workers = runtime.NumCPU() * defaultWorkerCountMultiplier
		logger.Log.Debugf("No worker count supplied, running %d workers per logical CPUs (total= %d).", defaultWorkerCountMultiplier, *workers)
	}

	if *workers <= 0 {
		logger.Log.Fatalf("Value in --workers must be greater than zero. Found %d", *workers)
	}

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
	packList, err := parsePackListFile(*packListFile)
	logger.PanicOnError(err)

	// A keep list may be provided. It will be combined with the pack list to decide
	// which SRPMS to keep. If it is empty all packages will be kept (but only the
	// most recent version of each).
	keepList := map[string]bool{}
	if *keepListFile != "" {
		keepList, err = parsePackListFile(*keepListFile)
		for spec := range packList {
			keepList[spec] = true
		}
		logger.PanicOnError(err)
	}

	packagedSRPMs, tidiedSRPMs, err := createAllSRPMsWrapper(*specsDir, *distTag, *buildDir, *outDir, *workerTar, *workers, *nestedSourcesDir, *repackAll, *runCheck, packList, keepList, *doTidy, templateSrcConfig)
	logger.PanicOnError(err)

	// Create empty summary file if one was specified and get a file handle to it for writing.
	if *summaryFile != "" {
		summaryFileHandle, err := os.Create(*summaryFile)
		logger.PanicOnError(err)
		defer summaryFileHandle.Close()

		// Write each SRPM to the summary file.
		for _, srpm := range tidiedSRPMs {
			_, err = summaryFileHandle.WriteString(fmt.Sprintf("%s: %s\n", "Deleted", srpm))
			logger.PanicOnError(err)
		}
		// Write each SRPM to the summary file.
		for _, srpm := range packagedSRPMs {
			_, err = summaryFileHandle.WriteString(fmt.Sprintf("%s: %s\n", "Packed", srpm))
			logger.PanicOnError(err)
		}
	}
}

// parsePackListFile will parse a list of packages to pack if one is specified.
// Duplicate list entries in the file will be removed.
func parsePackListFile(packListFile string) (packList map[string]bool, err error) {
	timestamp.StartEvent("parse list", nil)
	defer timestamp.StopEvent(nil)

	if packListFile == "" {
		return
	}

	packList = make(map[string]bool)

	file, err := os.Open(packListFile)
	if err != nil {
		return
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line != "" {
			packList[line] = true
		}
	}

	if len(packList) == 0 {
		err = fmt.Errorf("cannot have empty pack list (%s)", packListFile)
	}

	return
}

// createAllSRPMsWrapper wraps createAllSRPMs to conditionally run it inside a chroot.
// If workerTar is non-empty, packing will occur inside a chroot, otherwise it will run on the host system.
func createAllSRPMsWrapper(specsDir, distTag, buildDir, outDir, workerTar string, workers int, nestedSourcesDir, repackAll, runCheck bool, packList, keepList map[string]bool, doTidy bool, templateSrcConfig sourceRetrievalConfiguration) (packagedSRPMs, tidiedSRPMs []string, err error) {
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
		return createAllSRPMs(specsDir, distTag, buildDir, outDir, workers, nestedSourcesDir, repackAll, runCheck, packList, keepList, doTidy, templateSrcConfig, &packagedSRPMs, &tidiedSRPMs)
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
func createAllSRPMs(specsDir, distTag, buildDir, outDir string, workers int, nestedSourcesDir, repackAll, runCheck bool, packList, keepList map[string]bool, doTidy bool, templateSrcConfig sourceRetrievalConfiguration, packagedSRPMs, tidiedSRPMs *[]string) (err error) {
	logger.Log.Infof("Finding all SPEC files")
	timestamp.StartEvent("packing SRPMS", nil)
	defer timestamp.StopEvent(nil)

	timestamp.StartEvent("determining specs to pack", nil)
	var specFilesToKeep []string
	var specStates []*spectosrpm.SpecState
	if doTidy {
		timestamp.StartEvent("calculating specs that need tidying", nil)
		// First pass to remove any SPECs that should not be packed and are stale.
		specFilesToKeep, err = spectosrpm.FindSPECFiles(specsDir, keepList)
		if err != nil {
			return
		}

		specStates, err = spectosrpm.CalculateSPECsToRepack(specFilesToKeep, distTag, outDir, false, false, true, runCheck, workers)
		if err != nil {
			return fmt.Errorf("error calculating SRPM states: %w", err)
		}

		var srpmsToKeepMap map[string]bool
		// Convert the results to a map of SRPMs to keep
		srpmsToKeepMap, err = convertSpecStatesToMap(specStates)
		if err != nil {
			return fmt.Errorf("error calculating SRPM states: %w", err)
		}

		*tidiedSRPMs, err = deleteStaleSRPMs(srpmsToKeepMap, distTag, outDir, workers)
		if err != nil {
			err = fmt.Errorf("error deleting stale SRPMs: %w", err)
			return
		}
		timestamp.StopEvent(nil) // calculating specs that need tidying
	} else {
		*tidiedSRPMs = []string{}
	}

	// Second pass to actually check the any SPECs that need to be packed for stale sources.
	specFilesToPackage, err := spectosrpm.FindSPECFiles(specsDir, packList)
	if err != nil {
		return
	}

	specStates, err = spectosrpm.CalculateSPECsToRepack(specFilesToPackage, distTag, outDir, false, false, false, runCheck, workers)
	if err != nil {
		return fmt.Errorf("error calculating SRPM states: %w", err)
	}
	timestamp.StopEvent(nil) // determining specs to pack

	*packagedSRPMs, err = packSRPMs(specStates, distTag, buildDir, templateSrcConfig, workers)
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

func deleteStaleSRPMs(srpmsToKeep map[string]bool, distTag, outDir string, workers int) (packagedSRPMs []string, err error) {
	// Scan every file in outDir and delete any that are not in srpmsToKeep.
	err = filepath.Walk(outDir, func(path string, info os.FileInfo, err error) error {
		// Skip the root directory, and any file that isn't .src.rpm.
		if path == outDir || !strings.HasSuffix(path, ".src.rpm") {
			return nil
		}
		if !srpmsToKeep[path] {
			// Delete the file.
			logger.Log.Infof("Deleting stale SRPM %s", path)
			err := os.Remove(path)
			if err != nil {
				return fmt.Errorf("error deleting stale SRPM %s: %w", path, err)
			}
		}
		return nil
	})
	if err != nil {
		err = fmt.Errorf("error deleting stale SRPMs: %w", err)
	}

	return
}

// packSRPMs will pack any SPEC files that have been marked as `toPack`.
func packSRPMs(specStates []*spectosrpm.SpecState, distTag, buildDir string, templateSrcConfig sourceRetrievalConfiguration, workers int) (packagedSRPMs []string, err error) {
	tsRoot, _ := timestamp.StartEvent("packing SRPMs", nil)
	defer timestamp.StopEvent(nil)
	var wg sync.WaitGroup

	allSpecStates := make(chan *spectosrpm.SpecState, len(specStates))
	results := make(chan *packResult, len(specStates))
	cancel := make(chan struct{})
	packagedSRPMs = make([]string, 0, len(specStates))

	// Start the workers now so they begin working as soon as a new job is buffered.
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go packSRPMWorker(allSpecStates, results, cancel, &wg, distTag, buildDir, templateSrcConfig, tsRoot)
	}

	for _, state := range specStates {
		allSpecStates <- state
	}

	// Signal to the workers that there are no more new spec files
	close(allSpecStates)

	for i := 0; i < len(specStates); i++ {
		result := <-results

		if result.err != nil {
			logger.Log.Errorf("Failed to pack (%s). Error: %s", result.specFile, result.err)
			err = result.err
			close(cancel)
			break
		}

		// Skip results for states that were not packed by request
		if result.srpmFile == "" {
			continue
		}

		packagedSRPMs = append(packagedSRPMs, result.srpmFile)
		logger.Log.Infof("Packed (%s) -> (%s)", filepath.Base(result.specFile), filepath.Base(result.srpmFile))
	}

	logger.Log.Debug("Waiting for outstanding workers to finish")
	wg.Wait()

	return
}

// packSRPMWorker will process a channel of SPECs and pack any that are marked as toPack.
func packSRPMWorker(allSpecStates <-chan *spectosrpm.SpecState, results chan<- *packResult, cancel <-chan struct{}, wg *sync.WaitGroup, distTag, buildDir string, templateSrcConfig sourceRetrievalConfiguration, tsRoot *timestamp.TimeStamp) {
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
			specFile: specState.SpecFile,
		}

		// Its a no-op if the SPEC does not need to be packed
		if !specState.ToPack {
			results <- result
			timestamp.StopEvent(ts)
			continue
		}

		// Setup a source retrieval configuration based on the provided template
		signaturesFilePath := specPathToSignaturesPath(specState.SpecFile)
		srcConfig, err := initializeSourceConfig(templateSrcConfig, signaturesFilePath)
		if err != nil {
			result.err = err
			results <- result
			continue
		}

		fullOutDirPath := filepath.Dir(specState.SrpmFile)
		err = os.MkdirAll(fullOutDirPath, os.ModePerm)
		if err != nil {
			result.err = err
			results <- result
			continue
		}

		outputPath, err := packSingleSPEC(specState.SpecFile, specState.SrpmFile, signaturesFilePath, buildDir, fullOutDirPath, distTag, srcConfig)
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

func convertSpecStatesToMap(specStates []*spectosrpm.SpecState) (srpmsToKeep map[string]bool, err error) {
	srpmsToKeep = make(map[string]bool)
	for _, state := range specStates {
		if state.ToPack {
			srpmsToKeep[state.SrpmFile] = true
		}
	}
	return
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
func packSingleSPEC(specFile, srpmFile, signaturesFile, buildDir, outDir, distTag string, srcConfig sourceRetrievalConfiguration) (outputPath string, err error) {
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
	err = hydrateFiles(fileTypePatch, specFile, workingDir, srcConfig, currentSignatures, defines)
	if err != nil {
		return
	}

	// Hydrate all sources. Download any missing ones not in `sourceDir`
	err = hydrateFiles(fileTypeSource, specFile, workingDir, srcConfig, currentSignatures, defines)
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
func hydrateFiles(fileTypeToHydrate fileType, specFile, workingDir string, srcConfig sourceRetrievalConfiguration, currentSignatures, defines map[string]string) (err error) {
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
		hydrateFromRemoteSource(fileHydrationState, newSourceDir, srcConfig, skipSignatureHandling, currentSignatures)
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
				logger.Log.Warn(err.Error())
				return nil
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
func hydrateFromRemoteSource(fileHydrationState map[string]bool, newSourceDir string, srcConfig sourceRetrievalConfiguration, skipSignatureHandling bool, currentSignatures map[string]string) {
	const (
		downloadRetryAttempts = 3
		downloadRetryDuration = time.Second
	)

	for fileName, alreadyHydrated := range fileHydrationState {
		if alreadyHydrated {
			continue
		}

		destinationFile := filepath.Join(newSourceDir, fileName)

		url := network.JoinURL(srcConfig.sourceURL, fileName)

		err := retry.Run(func() error {
			err := network.DownloadFile(url, destinationFile, srcConfig.caCerts, srcConfig.tlsCerts)
			if err != nil {
				logger.Log.Warnf("Failed to download (%s). Error: %s", url, err)
			}

			return err
		}, downloadRetryAttempts, downloadRetryDuration)

		if err != nil {
			continue
		}

		if !skipSignatureHandling {
			err = validateSignature(destinationFile, srcConfig, currentSignatures)
			if err != nil {
				logger.Log.Warn(err.Error())

				// If the delete fails, just warn as there will be another cleanup
				// attempt when exiting the program.
				err = os.Remove(destinationFile)
				if err != nil {
					logger.Log.Warnf("Failed to delete file (%s). Error: %s", destinationFile, err)
				}

				continue
			}
		}

		fileHydrationState[fileName] = true
		logger.Log.Debugf("Hydrated (%s) from (%s)", fileName, url)
	}
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
