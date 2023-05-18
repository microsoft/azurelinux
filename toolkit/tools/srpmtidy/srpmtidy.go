// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/buildpipeline"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/directory"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/spectosrpm"

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
	defaultBuildDir    = "./build/SRPMS"
	defaultWorkerCount = "0"
	// rpmbuild usually sits doing nothing most of the time, so we can run multiple instances of it in parallel.
	defaultWorkerCountMultiplier = 8
)

var (
	app = kingpin.New("srpmpacker", "A tool to package a SRPM.")

	specsDir = exe.InputDirFlag(app, "Path to the SPEC directory to create SRPMs from.")
	outDir   = exe.OutputDirFlag(app, "Directory to place the output SRPM.")
	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)

	workers      = app.Flag("workers", "Number of concurrent goroutines to parse with.").Default(defaultWorkerCount).Int()
	buildDir     = app.Flag("build-dir", "Directory to store temporary files while building.").Default(defaultBuildDir).String()
	distTag      = app.Flag("dist-tag", "The distribution tag SRPMs will be built with.").Required().String()
	packListFile = app.Flag("pack-list", "Path to a list of SPECs to pack. If empty will pack all SPECs.").ExistingFile()
	summaryFile  = app.Flag("summary-file", "Path to a file to write a summary of the SRPMs created.").String()
	runCheck     = app.Flag("run-check", "Whether or not to run the spec file's check section during package build.").Bool()

	workerTar = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz. If this argument is empty, SRPMs will be packed in the host environment.").ExistingFile()
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	// rpmbuild is fairly light and single-threaded, so we can run multiple instances of it in parallel.
	if *workers <= 0 {
		*workers = runtime.NumCPU() * defaultWorkerCountMultiplier
		logger.Log.Debugf("No worker count supplied, running %d workers per logical CPUs (total= %d).", defaultWorkerCountMultiplier, *workers)
	}

	// A pack list may be provided, if so only pack this subset.
	// If non is provided, pack all srpms.
	packList, err := parsePackListFile(*packListFile)
	logger.PanicOnError(err)

	if len(*specsDir) == 0 {
		logger.PanicOnError(fmt.Errorf("no spec directory provided"))
	} else {
		logger.Log.Debugf("Spec directory: %s", *specsDir)
	}

	clearedSRPMs, err := tidyAllSRPMsWrapper(*specsDir, *distTag, *buildDir, *outDir, *workerTar, *workers, *runCheck, packList)
	logger.PanicOnError(err)

	// Create empty summary file if one was specified and get a file handle to it for writing.
	if *summaryFile != "" {
		summaryFileHandle, err := os.Create(*summaryFile)
		logger.PanicOnError(err)
		defer summaryFileHandle.Close()

		// Write each SRPM to the summary file.
		for _, srpm := range clearedSRPMs {
			_, err = summaryFileHandle.WriteString(srpm + "\n")
			logger.PanicOnError(err)
		}
	}
}

// removeDuplicateStrings will remove duplicate entries from a string slice
func removeDuplicateStrings(packList []string) (deduplicatedPackList []string) {
	var (
		packListSet = make(map[string]struct{})
		exists      = struct{}{}
	)

	for _, entry := range packList {
		packListSet[entry] = exists
	}

	for entry := range packListSet {
		deduplicatedPackList = append(deduplicatedPackList, entry)
	}

	return
}

// parsePackListFile will parse a list of packages to pack if one is specified.
// Duplicate list entries in the file will be removed.
func parsePackListFile(packListFile string) (packList []string, err error) {
	if packListFile == "" {
		return
	}

	file, err := os.Open(packListFile)
	if err != nil {
		return
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line != "" {
			packList = append(packList, line)
		}
	}

	if len(packList) == 0 {
		err = fmt.Errorf("cannot have empty pack list (%s)", packListFile)
	}

	packList = removeDuplicateStrings(packList)

	return
}

// createAllSRPMsWrapper wraps createAllSRPMs to conditionally run it inside a chroot.
// If workerTar is non-empty, packing will occur inside a chroot, otherwise it will run on the host system.
func tidyAllSRPMsWrapper(specsDir, distTag, buildDir, outDir, workerTar string, workers int, runCheck bool, packList []string) (cleanedSRPMs []string, err error) {
	var chroot *safechroot.Chroot

	// The specs dir may change if we're running inside a chroot or not.
	relativeSpecsDir := specsDir
	if workerTar != "" {
		const leaveFilesOnDisk = false
		chroot, relativeSpecsDir, err = createChroot(workerTar, buildDir, outDir, specsDir)
		if err != nil {
			return
		}
		defer chroot.Close(leaveFilesOnDisk)
	}

	SRPMsToKeepMap := make(map[string]bool)

	doTidyAll := func() error {
		return checkAllSRPMs(relativeSpecsDir, distTag, buildDir, outDir, workers, runCheck, packList, &SRPMsToKeepMap)
	}

	if chroot != nil {
		logger.Log.Info("Tidying SRPMs inside a chroot environment")
		err = chroot.Run(doTidyAll)
	} else {
		logger.Log.Info("Tidying SRPMs in the host environment")
		err = doTidyAll()
	}
	if err != nil {
		err = fmt.Errorf("error tidying SRPMs: %w", err)
		return
	}

	logger.Log.Errorf("%v", SRPMsToKeepMap)

	cleanedSRPMs, err = deleteStaleSRPMs(SRPMsToKeepMap, distTag, outDir, workers)
	if err != nil {
		err = fmt.Errorf("error deleting stale SRPMs: %w", err)
		return
	}

	return
}

// createAllSRPMs will find all SPEC files in specsDir and pack SRPMs for them if needed.
func checkAllSRPMs(specsDir, distTag, buildDir, outDir string, workers int, runCheck bool, packList []string, srpmsToKeep *map[string]bool) (err error) {
	logger.Log.Infof("Finding all SPEC files in %s", specsDir)

	specFiles, err := spectosrpm.FindSPECFiles(specsDir, packList)
	if err != nil {
		return fmt.Errorf("error finding SPEC files: %w", err)
	}

	specStates, err := spectosrpm.CalculateSPECsToRepack(specFiles, distTag, outDir, false, false, true, runCheck, workers)
	if err != nil {
		return fmt.Errorf("error calculating SRPM states: %w", err)
	}

	for _, state := range specStates {
		if state.Err != nil {
			err = fmt.Errorf("error calculating SRPM state for %s: %w", state.SpecFile, state.Err)
			return
		}
		if state.ToPack {
			(*srpmsToKeep)[state.SrpmFile] = true
		}
	}

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

// createChroot creates a chroot to pack SRPMs inside of.
func createChroot(workerTar, buildDir, outDir, specsDir string) (chroot *safechroot.Chroot, newSpecsDir string, err error) {
	const (
		chrootName       = "srpm_tidy_chroot"
		existingDir      = false
		leaveFilesOnDisk = false

		specsMountPoint = "/specs"
	)

	extraMountPoints := []*safechroot.MountPoint{
		safechroot.NewMountPoint(specsDir, specsMountPoint, "", safechroot.BindMountPointFlags, ""),
	}

	newSpecsDir = specsMountPoint

	chrootDir := filepath.Join(buildDir, chrootName)
	chroot = safechroot.NewChroot(chrootDir, existingDir)

	err = chroot.Initialize(workerTar, []string{}, extraMountPoints)
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
	}

	return
}
