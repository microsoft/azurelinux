// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package toolchain

import (
	"fmt"
	"path/filepath"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
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

func (o *OfficialScript) BuildOfficialToolchainRpms() error {
	onStdout := func(args ...interface{}) {
		line := args[0].(string)
		logger.Log.Infof("Official Toolchain: %s", line)
	}
	onStdErr := func(args ...interface{}) {
		line := args[0].(string)
		logger.Log.Warnf("Official Toolchain: %s", line)
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

	err := shell.ExecuteLiveWithCallbackInDirectory(onStdout, onStdErr, false, script, o.WorkingDir, args...)
	if err != nil {
		return fmt.Errorf("failed to execute bootstrap script. Error:\n%w", err)
	}

	return nil
}
