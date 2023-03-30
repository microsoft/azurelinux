// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"bufio"
	"os"
	"path/filepath"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/installutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/pkgjson"
)

// CalculatePackagesToBuild generates a comprehensive list of all PackageVers that the scheduler should attempt to build.
// The build list is a superset of:
//   - packagesNamesToBuild,
//   - packagesNamesToRebuild,
//   - local packages listed in the image config, and
//   - kernels in the image config (if built locally).
func CalculatePackagesToBuild(packagesNamesToBuild, packagesNamesToRebuild []string, inputGraphFile, imageConfig, baseDirPath string) (packageVersToBuild []*pkgjson.PackageVer, err error) {
	packageVersToBuild = convertPackageNamesIntoPackageVers(packagesNamesToBuild)
	packageVersToBuild = append(packageVersToBuild, convertPackageNamesIntoPackageVers(packagesNamesToRebuild)...)

	if imageConfig == "" {
		return
	}

	packageVersFromConfig, err := extractPackagesFromConfig(imageConfig, baseDirPath)
	if err != nil {
		return
	}

	packageVersFromConfig, err = filterLocalPackagesOnly(packageVersFromConfig, inputGraphFile)
	if err != nil {
		return
	}

	packageVersToBuild = append(packageVersToBuild, packageVersFromConfig...)
	return
}

// convertPackageNamesIntoPackageVers converts a slice of package names into PackageVer structures that
// are understood by the graph.
func convertPackageNamesIntoPackageVers(packageNames []string) (packageVers []*pkgjson.PackageVer) {
	packageVers = make([]*pkgjson.PackageVer, len(packageNames))
	for i, pkg := range packageNames {
		packageVers[i] = &pkgjson.PackageVer{
			Name: pkg,
		}
	}

	return
}

// extractPackagesFromConfig reads configuration file and returns a package list required for the said configuration
// Package list is assembled from packageList and KernelOptions.
func extractPackagesFromConfig(configFile, baseDirPath string) (packageList []*pkgjson.PackageVer, err error) {
	cfg, err := configuration.LoadWithAbsolutePaths(configFile, baseDirPath)
	if err != nil {
		logger.Log.Errorf("Failed to load config file (%s) with base directory (%s) for package list generation", configFile, baseDirPath)
		return
	}

	packageList, err = installutils.PackageNamesFromConfig(cfg)
	if err != nil {
		return
	}

	// Add kernel packages from KernelOptions
	packageList = append(packageList, installutils.KernelPackages(cfg)...)

	return
}

// filterLocalPackagesOnly returns the subset of packageVersionsInConfig that only contains local packages.
func filterLocalPackagesOnly(packageVersionsInConfig []*pkgjson.PackageVer, inputGraph string) (filteredPackages []*pkgjson.PackageVer, err error) {
	logger.Log.Debug("Filtering out external packages from list of packages extracted from the image config file.")

	dependencyGraph := pkggraph.NewPkgGraph()
	err = pkggraph.ReadDOTGraphFile(dependencyGraph, inputGraph)
	if err != nil {
		return
	}

	for _, pkgVer := range packageVersionsInConfig {
		pkgNode, _ := dependencyGraph.FindBestPkgNode(pkgVer)

		// A pkgNode for a local package has the following characteristics:
		// 1) The pkgNode exists in the graph (is not nil).
		// 2) The pkgNode doesn't have the 'StateUnresolved' or 'StateCached' state. These are reserved for external dependencies nodes.
		if pkgNode != nil && pkgNode.RunNode.State != pkggraph.StateUnresolved && pkgNode.RunNode.State != pkggraph.StateCached {
			filteredPackages = append(filteredPackages, pkgVer)
		} else {
			logger.Log.Debugf("Found external package to filter out: %v.", pkgVer)
		}
	}

	return
}

// ReadReservedFilesList reads the list of reserved files (such as toolchain RPMs) from the manifest file passed in.
// Entries will be returned in the form '<rpm>-<version>-<release>.rpm' with any preceding path removed. If the file path is
// empty, an empty list will be returned.
func ReadReservedFilesList(path string) (reservedFiles []string, err error) {
	// If the path is empty, return an empty list.
	if len(path) == 0 {
		return reservedFiles, nil
	}

	file, err := os.Open(path)
	if err != nil {
		logger.Log.Errorf("Failed to open file manifest %s with error %s", path, err)
		return nil, err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		strippedPath := filepath.Base(scanner.Text())
		reservedFiles = append(reservedFiles, strippedPath)
	}

	err = scanner.Err()
	if err != nil {
		logger.Log.Errorf("Failed to scan file manifest %s with error %s", path, err)
		return nil, err
	}

	return reservedFiles, nil
}

// IsReservedFile determines if a given file path or filename is found in a list of reserved RPMs.
// reservedRPMs may be a list of filenames or paths to reserved files. (e.g. 'foo-1.0.0-1.cm1.x86_64.rpm' or
// '/path/to/foo-1.0.0-1.cm1.x86_64.rpm').
func IsReservedFile(rpmPath string, reservedRPMs []string) bool {
	base := filepath.Base(rpmPath)
	for _, reservedRPM := range reservedRPMs {
		reservedBase := filepath.Base(reservedRPM)
		if reservedBase == base {
			return true
		}
	}
	return false
}
