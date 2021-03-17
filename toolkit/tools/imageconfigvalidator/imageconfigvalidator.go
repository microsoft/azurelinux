// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// An image configuration validator

package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"gopkg.in/alecthomas/kingpin.v2"
	"microsoft.com/pkggen/imagegen/configuration"
	"microsoft.com/pkggen/imagegen/installutils"
	"microsoft.com/pkggen/internal/exe"
	"microsoft.com/pkggen/internal/logger"
)

var (
	app = kingpin.New("imageconfigvalidator", "A tool for validating image configuration files")

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)

	input       = exe.InputStringFlag(app, "Path to the image config file.")
	baseDirPath = exe.InputDirFlag(app, "Base directory for relative file paths from the config.")
)

func main() {
	const returnCodeOnError = 1

	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	inPath, err := filepath.Abs(*input)
	logger.PanicOnError(err, "Error when calculating input path")
	baseDir, err := filepath.Abs(*baseDirPath)
	logger.PanicOnError(err, "Error when calculating input directory")

	logger.Log.Infof("Reading configuration file (%s)", inPath)
	config, err := configuration.LoadWithAbsolutePaths(inPath, baseDir)
	if err != nil {
		logger.Log.Fatalf("Failed while loading image configuration '%s': %s", inPath, err)
	}

	// Basic validation will occur during load, but we can add additional checking here.
	err = ValidateConfiguration(config)
	if err != nil {
		// Log an error here as opposed to panicing to keep the output simple
		// and only contain the error with the config file.
		logger.Log.Fatalf("Invalid configuration '%s': %s", inPath, err)
	}

	return
}

// ValidateConfiguration will run sanity checks on a configuration structure
func ValidateConfiguration(config configuration.Config) (err error) {
	err = config.IsValid()
	if err != nil {
		return
	}
	err = validatePackages(config)
	return
}

func validatePackages(config configuration.Config) (err error) {
	const (
		validateError      = "failed to validate package lists in config"
		verityPkgName      = "verity-read-only-root"
		verityDebugPkgName = "verity-read-only-root-debug-tools"
		dracutFipsPkgName  = "dracut-fips"
		fipsKernelCmdLine  = "fips=1"
	)
	for _, systemConfig := range config.SystemConfigs {
		packageList, err := installutils.PackageNamesFromSingleSystemConfig(systemConfig)
		if err != nil {
			return fmt.Errorf("%s: %w", validateError, err)
		}
		foundVerityInitramfsPackage := false
		foundVerityInitramfsDebugPackage := false
		foundDracutFipsPackage := false
		kernelCmdLineString := systemConfig.KernelCommandLine.ExtraCommandLine
		for _, pkg := range packageList {
			if pkg == "kernel" {
				return fmt.Errorf("%s: kernel should not be included in a package list, add via config file's [KernelOptions] entry", validateError)
			}
			if pkg == verityPkgName {
				foundVerityInitramfsPackage = true
			}
			if pkg == verityDebugPkgName {
				foundVerityInitramfsDebugPackage = true
			}
			if pkg == dracutFipsPkgName {
				foundDracutFipsPackage = true
			}
		}
		if systemConfig.ReadOnlyVerityRoot.Enable {
			if !foundVerityInitramfsPackage {
				return fmt.Errorf("%s: [ReadOnlyVerityRoot] selected, but '%s' package is not included in the package lists", validateError, verityPkgName)
			}
			if systemConfig.ReadOnlyVerityRoot.TmpfsOverlayDebugEnabled && !foundVerityInitramfsDebugPackage {
				return fmt.Errorf("%s: [ReadOnlyVerityRoot] and [TmpfsOverlayDebugEnabled] selected, but '%s' package is not included in the package lists", validateError, verityDebugPkgName)
			}
		}
		if strings.Contains(kernelCmdLineString, fipsKernelCmdLine) {
			if !foundDracutFipsPackage {
				return fmt.Errorf("%s: 'fips=1' provided on kernel cmdline, but '%s' package is not included in the package lists", validateError, dracutFipsPkgName)
			}
		}
	}
	return
}
