// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package toolchain

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"os"
	"path/filepath"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

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

func CheckBootstrapCache(bootstrapScript BootstrapScript, cacheDir string) (cachedFile string, cacheOk bool, err error) {
	cachedFile, err = cacheFilePath(bootstrapScript, cacheDir)
	if err != nil {
		return "", false, fmt.Errorf("unable to get cache file path:\n%w", err)
	}
	// Check if the cached file exists
	if exists, err := file.PathExists(cachedFile); exists && err != nil {
		cacheOk = true
	}

	return
}

func RestoreFromCache(bootstrapScript BootstrapScript, cacheDir string) (restored bool, err error) {
	cachedFile, cacheOk, err := CheckBootstrapCache(bootstrapScript, cacheDir)
	if err != nil {
		err = fmt.Errorf("unable to check cache:\n%w", err)
		return
	}
	if cacheOk {
		// Move the cached file to the output file
		err = file.Move(cachedFile, bootstrapScript.OutputFile)
		if err != nil {
			err = fmt.Errorf("unable to restore from cache:\n%w", err)
			return
		}
		restored = true
	}
	return
}

func cacheFilePath(bootstrapScript BootstrapScript, cacheDir string) (cachedFile string, err error) {
	// Generate a running hash of the input files to check the a cached file against
	hash, err := calculateHash(bootstrapScript.InputFiles)
	if err != nil {
		return "", fmt.Errorf("unable to calculate hash:\n%w", err)
	}

	fileName := fmt.Sprintf("bootstrap-%s.tar.gz", hash)
	cachedFile = filepath.Join(cacheDir, "bootstrap", fileName)
	return
}

func calculateHash(inputFiles []string) (hash string, err error) {
	fileHasher := sha256.New()
	for _, inputFile := range inputFiles {
		// Read the file, and pass into the hasher
		r, err := os.ReadFile(inputFile)
		if err != nil {
			return "", fmt.Errorf("unable to read input file:\n%w", err)
		}
		_, err = fileHasher.Write(r)
		if err != nil {
			return "", fmt.Errorf("unable to hash file:\n%w", err)
		}
	}
	hash = hex.EncodeToString(fileHasher.Sum(nil))
	return
}

func AddToCache(bootstrapScript BootstrapScript, cacheDir string) (cachedFile string, err error) {
	srcFile := bootstrapScript.OutputFile
	cachedFile, err = cacheFilePath(bootstrapScript, cacheDir)
	if err != nil {
		return "", fmt.Errorf("unable to get cache file path:\n%w", err)
	}

	err = file.Move(srcFile, cachedFile)
	if err != nil {
		return "", fmt.Errorf("unable to move bootstrap file to cache:\n%w", err)
	}

	return
}

func Bootstrap(bootstrapScript BootstrapScript) error {
	onStdout := func(args ...interface{}) {
		const bootstrapPrefix = "Raw Bootstrap"
		line := args[0].(string)
		logger.Log.Infof("Raw Bootstrap: %s", line)
	}
	onStdErr := func(args ...interface{}) {
		const bootstrapPrefix = "Raw Bootstrap"
		line := args[0].(string)
		logger.Log.Warnf("Raw Bootstrap: %s", line)
	}

	script := bootstrapScript.ScriptPath
	incrementalArg := "n"
	if bootstrapScript.UseIncremental {
		incrementalArg = "y"
	}
	args := []string{
		bootstrapScript.BuildDir,
		bootstrapScript.SpecsDir,
		bootstrapScript.SourceURL,
		incrementalArg,
		bootstrapScript.ArchiveTool,
	}

	err := shell.ExecuteLiveWithCallbackInDirectory(onStdout, onStdErr, false, script, bootstrapScript.WorkingDir, args...)
	if err != nil {
		return fmt.Errorf("failed to execute bootstrap script. Error:\n%w", err)
	}

	return nil
}
