// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package toolchain

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/systemdependency"
)

const officialName = "official"

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
	buildDone bool
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

func (o *OfficialScript) BuildOfficialToolchainRpms() (err error) {
	onStdout := func(args ...interface{}) {
		line := args[0].(string)
		logger.Log.Infof("Official Toolchain: %s", line)
	}
	onStdErr := func(args ...interface{}) {
		line := args[0].(string)
		logger.Log.Debugf("Official Toolchain: %s", line)
	}

	script := o.ScriptPath
	incrementalArg := "n"
	if o.UseIncremental {
		incrementalArg = "y"
	}
	gzipTool, err := systemdependency.GzipTool()
	if err != nil {
		err = fmt.Errorf("failed to get gzip tool. Error:\n%w", err)
		return
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
		gzipTool,
		o.IntermediateSrpmsDir,
		o.OutputSrpmsDir,
		o.ToolchainFromRepos,
		o.ToolchainManifest,
		o.BldTracker,
		o.TimestampFile,
	}

	err = shell.ExecuteLiveWithCallbackInDirectory(onStdout, onStdErr, false, script, o.WorkingDir, args...)
	if err != nil {
		err = fmt.Errorf("failed to execute bootstrap script. Error:\n%w", err)
		return
	}

	o.buildDone = true
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

func (o *OfficialScript) TransferBuiltRpms() (err error) {
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
		}
	}
	return
}
