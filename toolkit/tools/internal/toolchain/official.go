// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package toolchain

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/sliceutils"
)

const officialName = "official"

var toolchainMountPoints = []string{"dev", "dev/pts", "proc", "sys", "run"}

type OfficialScript struct {
	OutputFile           string   // Path to the generated bootstrap file
	ScriptPath           string   // Path to the bootstrap script
	WorkingDir           string   // Path to the working directory
	DistTag              string   // Dist tag for the rpms
	BuildNumber          string   // Build number for the rpms
	ReleaseVersion       string   // Release version for the rpms
	BuildDir             string   // Path to the build directory
	RpmsDir              string   // Path to the rpms directory
	SpecsDir             string   // Path to the specs directory
	RunCheck             bool     // Run check
	UseIncremental       bool     // Use incremental build mode
	IntermediateSrpmsDir string   // Path to the intermediate srpms directory
	OutputSrpmsDir       string   // Path to the output srpms directory
	ToolchainFromRepos   string   // Path to the toolchain from repos
	ToolchainManifest    string   // Path to the toolchain manifest
	BldTracker           string   // Path to the bld tracker
	TimestampFile        string   // Path to the timestamp file
	InputFiles           []string // List of input files to hash for validating the cache

	// Internal state
	buildDone      bool
	unmountsQueued bool
	progress       int
}

func (o *OfficialScript) populatedToolchainDir() string {
	return filepath.Join(o.BuildDir, "toolchain", "populated_toolchain")
}

func (o *OfficialScript) CheckCache(cacheDir string) (string, bool, error) {
	return checkCache(officialName, o.InputFiles, cacheDir)
}

func (o *OfficialScript) RestoreFromCache(cacheDir string) error {
	return restoreFromCache(officialName, o.InputFiles, o.OutputFile, cacheDir)
}

func (o *OfficialScript) AddToCache(cacheDir string) (string, error) {
	return addToCache(officialName, o.InputFiles, o.OutputFile, cacheDir)
}

func (o *OfficialScript) PrepIncrementalRpms(downloadDir string, toolchainRPMs []string) (err error) {
	logger.Log.Info("Preparing incremental rpms for delta build")

	incrementalRpmsPath := filepath.Join(o.populatedToolchainDir(), "usr", "src", "mariner", "RPMS")
	_, err = CleanToolchainRpms(incrementalRpmsPath, toolchainRPMs)
	if err != nil {
		err = fmt.Errorf("unable to clean toolchain rpms:\n%w", err)
		return
	}

	for _, rpm := range toolchainRPMs {
		var fileExists bool
		srcPath := filepath.Join(downloadDir, rpm)
		dstPath := filepath.Join(o.ToolchainFromRepos, rpm)
		fileExists, err = file.PathExists(srcPath)

		if err != nil {
			return fmt.Errorf("unable to check if rpm exists: %w", err)
		}
		if !fileExists {
			// Just touch an empty file in the delta directory
			dstFile, fileErr := os.Create(dstPath)
			if fileErr != nil {
				err = fmt.Errorf("unable to create delta rpm file: %w", fileErr)
				return
			}
			dstFile.Close()
		} else {
			err = file.Copy(srcPath, dstPath)
			if err != nil {
				err = fmt.Errorf("unable to restore from cache:\n%w", err)
				return
			}
		}
	}
	return
}

func (o *OfficialScript) CleanIncrementalRpms() (err error) {
	logger.Log.Info("Cleaning incremental rpms")
	err = os.RemoveAll(o.ToolchainFromRepos)
	if err != nil {
		err = fmt.Errorf("unable to clean incremental rpms:\n%w", err)
		return
	}

	err = o.cleanMountDirs()
	if err != nil {
		err = fmt.Errorf("unable to clean mount dirs:\n%w", err)
		return
	}
	err = os.RemoveAll(o.populatedToolchainDir())
	if err != nil {
		err = fmt.Errorf("unable to clean populated toolchain dir:\n%w", err)
		return
	}

	return
}

func (o *OfficialScript) cleanMountDirs() (err error) {
	// Mounts are taken from 'chroot_mount()' in 'build_official_toolchain_rpms.sh'
	fullPaths := []string{}
	for _, mount := range toolchainMountPoints {
		fullPaths = append(fullPaths, filepath.Join(o.populatedToolchainDir(), mount))
	}
	failed := safechroot.CleanupUnsafeMounts(fullPaths)
	if failed {
		err = fmt.Errorf("failed to unmount some mount points")
		return
	}

	// Register the unmounts so they can be cleaned up if the process is killed
	if !o.unmountsQueued {
		for _, mountPath := range fullPaths {
			safechroot.RegisterUnsafeUnmount(mountPath)
		}
		o.unmountsQueued = true
	}
	return
}

func (o *OfficialScript) updateProgress(done chan bool) {
	const delay = time.Duration(5) * time.Second
	var (
		logFile    = filepath.Join(o.BuildDir, "logs", "toolchain", "build_list.txt")
		scriptFile = filepath.Join(o.WorkingDir, "./build_official_toolchain_rpms.sh")
	)
	script, err := file.ReadLines(scriptFile)
	if err != nil {
		logger.Log.Warnf("Failed to read script file '%s'. Error:\n%s", scriptFile, err)
		return
	}
	buildLines := sliceutils.FindMatches(script, func(line string) bool {
		// Lines that start with 'build_rpm_in_chroot_no_install' are the ones we want
		return strings.HasPrefix(line, "build_rpm_in_chroot_no_install")
	})

	for {
		select {
		case <-done:
			return
		case <-time.After(delay):
			exists, err := file.PathExists(logFile)
			if err != nil {
				logger.Log.Warnf("Failed to check if log file '%s' exists. Error:\n%s", logFile, err)
				return
			}
			if !exists {
				// Log not created yet, keep waiting
				continue
			}
			numBuilt, err := file.ReadLines(logFile)
			if err != nil {
				logger.Log.Warnf("Failed to read log file '%s'. Error:\n%s", logFile, err)
				return
			}
			o.progress = (len(numBuilt) * 100) / len(buildLines)
		}
	}
}

func (o *OfficialScript) BuildOfficialToolchainRpms() (builtRpms []string, err error) {
	err = o.cleanMountDirs()
	if err != nil {
		err = fmt.Errorf("failed to clean mount dirs. Error:\n%w", err)
		return
	}

	onStdout := func(args ...interface{}) {
		line := args[0].(string)
		logger.Log.Infof("Official Toolchain %3d%%: %s", o.progress, line)
	}
	// Generally stderr is just set -x output, so we don't need to log it to console
	onStdErr := func(args ...interface{}) {
		line := args[0].(string)
		logger.Log.Debugf("Official Toolchain: %s", line)
	}

	script := o.ScriptPath
	incrementalArg := "n"
	if o.UseIncremental {
		incrementalArg = "y"
	}
	runCheckArg := "n"
	if o.RunCheck {
		runCheckArg = "y"
	}
	args := []string{
		o.DistTag,
		o.BuildNumber,
		o.ReleaseVersion,
		o.BuildDir,
		o.RpmsDir,
		o.SpecsDir,
		runCheckArg,
		filepath.Dir(o.ToolchainManifest),
		incrementalArg,
		o.IntermediateSrpmsDir,
		o.OutputSrpmsDir,
		o.ToolchainFromRepos,
		o.ToolchainManifest,
		o.BldTracker,
		o.TimestampFile,
	}

	done := make(chan bool)
	defer close(done)
	go o.updateProgress(done)

	err = shell.ExecuteLiveWithCallbackInDirectory(onStdout, onStdErr, false, script, o.WorkingDir, args...)
	if err != nil {
		err = fmt.Errorf("failed to execute bootstrap script. Error:\n%w", err)
		return
	}

	o.buildDone = true
	builtRpmPaths, err := o.getBuiltRpms()
	if err != nil {
		err = fmt.Errorf("failed to get built rpms. Error:\n%w", err)
		return
	}
	for _, rpm := range builtRpmPaths {
		rpm = filepath.Join(o.RpmsDir, rpm)
		builtRpms = append(builtRpms, fmt.Sprintf("Built: %s", rpm))
	}
	return
}

func (o *OfficialScript) getBuiltRpms() (rpms []string, err error) {
	logsDir := filepath.Join(o.BuildDir, "logs", "toolchain")
	builtRpmsFile := filepath.Join(logsDir, "built_rpms_list.txt")

	if !o.buildDone {
		err = fmt.Errorf("can't check built rpms, no build completed")
		return
	}

	exists, err := file.PathExists(builtRpmsFile)
	if err != nil {
		err = fmt.Errorf("failed to check if built rpms file exists. Error:\n%w", err)
		return
	}
	if !exists {
		logger.Log.Debug("No built rpms file found, built no rpms?")
	}

	rpms, err = file.ReadLines(builtRpmsFile)
	if err != nil {
		err = fmt.Errorf("failed to read built rpms file. Error:\n%w", err)
		return
	}
	return
}

func (o *OfficialScript) TransferBuiltRpms() (rpmsMoved []string, err error) {
	builtRpms, err := o.getBuiltRpms()
	if err != nil {
		err = fmt.Errorf("can't copy built rpms. Error:\n%w", err)
		return
	}

	for _, rpm := range builtRpms {
		builtRpmsDir := filepath.Join(o.BuildDir, "toolchain", "built_rpms_all")
		src := filepath.Join(builtRpmsDir, rpm)
		dst := filepath.Join(o.RpmsDir, rpm)

		srcExists, fErr := file.PathExists(src)
		if fErr != nil {
			err = fmt.Errorf("failed to check if rpm exists. Error:\n%w", fErr)
			return
		}
		if !srcExists {
			err = fmt.Errorf("can't copy output rpm, '%s' doesn't exist", src)
			return
		}

		isSame, fErr := file.ContentsAreSame(src, dst)
		if fErr != nil {
			err = fmt.Errorf("failed to compare files. Error:\n%w", fErr)
			return
		}
		if !isSame {
			err = file.Copy(src, dst)
			if err != nil {
				err = fmt.Errorf("failed to copy file. Error:\n%w", err)
				return
			}
			rpmsMoved = append(rpmsMoved, fmt.Sprintf("Copied: %s", dst))
		}
	}
	return
}
