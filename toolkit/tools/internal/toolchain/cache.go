// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package toolchain

import (
	"encoding/hex"
	"fmt"
	"path/filepath"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/marinertoolusers"
)

func checkCache(name string, inputs []string, cacheDir string) (cachedFile string, cacheOk bool, err error) {
	cachedFile, err = cacheFilePath(name, inputs, cacheDir)
	if err != nil {
		return "", false, fmt.Errorf("unable to get cache file path:\n%w", err)
	}
	// Check if the cached file exists
	if exists, err := file.PathExists(cachedFile); exists && err == nil {
		cacheOk = true
	}

	return
}

func restoreFromCache(name string, inputFiles []string, outputFile, cacheDir string) (err error) {
	cachedFile, cacheOk, err := checkCache(name, inputFiles, cacheDir)
	if err != nil {
		err = fmt.Errorf("unable to check cache:\n%w", err)
		return
	}
	filesSame, err := file.ContentsAreSame(outputFile, cachedFile)
	if err != nil {
		err = fmt.Errorf("unable to compare files:\n%w", err)
		return
	}

	if cacheOk && !filesSame {
		// Move the cached file to the output file
		err = file.Copy(cachedFile, outputFile)
		if err != nil {
			err = fmt.Errorf("unable to restore from cache:\n%w", err)
			return
		}
		logger.Log.Infof("Cache restored '%s' to '%s'", cachedFile, outputFile)
	}
	return
}

func cacheFilePath(name string, inputs []string, cacheDir string) (cachedFile string, err error) {
	// Generate a running hash of the input files to check the a cached file against
	hash, err := file.CalculateSHA256Bytes(inputs)
	if err != nil {
		return "", fmt.Errorf("unable to calculate hash:\n%w", err)
	}

	fileName := fmt.Sprintf("%s-%s.tar.gz", name, hex.EncodeToString(hash))
	cachedFile = filepath.Join(cacheDir, name, fileName)
	return
}

func addToCache(name string, inputs []string, srcFile, cacheDir string) (cachedFile string, err error) {
	cachedFile, err = cacheFilePath(name, inputs, cacheDir)
	if err != nil {
		return "", fmt.Errorf("unable to get cache file path:\n%w", err)
	}

	err = file.CopyWithUser(srcFile, cachedFile, marinertoolusers.GetMarinerBuildUser())
	if err != nil {
		return "", fmt.Errorf("unable to move bootstrap file to cache:\n%w", err)
	}

	logger.Log.Infof("Cache updated '%s' to '%s'", srcFile, cachedFile)

	return
}
