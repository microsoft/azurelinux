// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package toolchain

import (
	"fmt"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/systemdependency"
)

const bootstrapName = "bootstrap"

// Type defining the bootstrap script
type BootstrapScript struct {
	OutputFile     string   // Path to the generated bootstrap file
	ScriptPath     string   // Path to the bootstrap script
	WorkingDir     string   // Path to the working directory
	BuildDir       string   // Path to the build directory
	SpecsDir       string   // Path to the specs directory
	SourceURL      string   // URL to the source code
	UseIncremental bool     // Use incremental build mode
	ArchiveTool    string   // Path to the archive tool
	InputFiles     []string // List of input files to hash for validating the cache
}

func (b *BootstrapScript) CheckCache(cacheDir string) (string, bool, error) {
	return checkCache(bootstrapName, b.InputFiles, cacheDir)
}

func (b *BootstrapScript) RestoreFromCache(cacheDir string) error {
	return restoreFromCache(bootstrapName, b.InputFiles, b.OutputFile, cacheDir)
}

func (b *BootstrapScript) AddToCache(cacheDir string) (string, error) {
	return addToCache(bootstrapName, b.InputFiles, b.OutputFile, cacheDir)
}

func (b *BootstrapScript) Bootstrap() (err error) {
	onStdout := func(args ...interface{}) {
		line := args[0].(string)
		logger.Log.Infof("Raw Bootstrap: %s", line)
	}
	onStdErr := func(args ...interface{}) {
		line := args[0].(string)
		logger.Log.Warnf("Raw Bootstrap: %s", line)
	}
	gzipTool, err := systemdependency.GzipTool()
	if err != nil {
		err = fmt.Errorf("failed to get gzip tool. Error:\n%w", err)
		return
	}

	script := b.ScriptPath
	incrementalArg := "n"
	if b.UseIncremental {
		incrementalArg = "y"
	}
	args := []string{
		b.BuildDir,
		b.SpecsDir,
		b.SourceURL,
		incrementalArg,
		gzipTool,
	}

	err = shell.ExecuteLiveWithCallbackInDirectory(onStdout, onStdErr, false, script, b.WorkingDir, args...)
	if err != nil {
		err = fmt.Errorf("failed to execute bootstrap script. Error:\n%w", err)
		return
	}

	return
}
