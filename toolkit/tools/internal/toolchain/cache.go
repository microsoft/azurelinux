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
	if cacheOk {
		// Move the cached file to the output file
		err = file.Move(cachedFile, outputFile)
		if err != nil {
			err = fmt.Errorf("unable to restore from cache:\n%w", err)
			return
		}
	}
	return
}

func cacheFilePath(name string, inputs []string, cacheDir string) (cachedFile string, err error) {
	// Generate a running hash of the input files to check the a cached file against
	hash, err := calculateHash(inputs)
	if err != nil {
		return "", fmt.Errorf("unable to calculate hash:\n%w", err)
	}

	fileName := fmt.Sprintf("%s-%s.tar.gz", name, hash)
	cachedFile = filepath.Join(cacheDir, name, fileName)
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

func addToCache(name string, inputs []string, srcFile, cacheDir string) (cachedFile string, err error) {
	cachedFile, err = cacheFilePath(name, inputs, cacheDir)
	if err != nil {
		return "", fmt.Errorf("unable to get cache file path:\n%w", err)
	}

	err = file.Move(srcFile, cachedFile)
	if err != nil {
		return "", fmt.Errorf("unable to move bootstrap file to cache:\n%w", err)
	}

	return
}
