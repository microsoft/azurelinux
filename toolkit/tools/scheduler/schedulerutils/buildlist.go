// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"

	"github.com/juliangruber/go-intersect"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/installutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/sliceutils"
)

// ParseAndGeneratePackageList parses the common package request arguments and generates a list of packages to build based on the given dependency graph.
// - dependencyGraph: the dependency graph of all packages. Used to convert package/spec names to PackageVers.
// - pkgsToBuild: a list of package/spec names to build. If empty, all packages will be built.
// - pkgsToRebuild: a list of package/spec names to always rebuild.
// - pkgsToIgnore: a list of package/spec names to ignore.
// - imageConfig: the path to the image config file. Used to extract additional packages to build.
// - baseDirPath: the path to the base directory for the image. Used to resolve relative paths in the image config.
func ParseAndGeneratePackageList(dependencyGraph *pkggraph.PkgGraph, pkgsToBuild, pkgsToRebuild, pkgsToIgnore []string, imageConfig, baseDirPath string) (finalPackagesToBuild, packagesToRebuild, packagesToIgnore []*pkgjson.PackageVer, err error) {
	// Generate the list of packages that need to be built.
	// If none are requested then all packages will be built.
	packagesToBuild, err := PackageNamesToBuiltPackages(pkgsToBuild, dependencyGraph)
	if err != nil {
		err = fmt.Errorf("unable to find build nodes for the packages to build, error:\n%s", err)
		return
	}

	packagesToRebuild, err = PackageNamesToBuiltPackages(pkgsToRebuild, dependencyGraph)
	if err != nil {
		err = fmt.Errorf("unable to find build nodes for the packages to rebuild, error:\n%s", err)
		return
	}

	prunedIgnoredPackageNames, unknownNames, err := PruneUnknownPackages(pkgsToIgnore, dependencyGraph)
	if err != nil {
		err = fmt.Errorf("failed to prune unknown package/spec names from the ignored list, error:\n%s", err)
		return
	}

	if len(unknownNames) != 0 {
		logger.Log.Warnf("The following ignored items matched neither a spec nor a package name: %v.", unknownNames)
	}

	packagesToIgnore, err = PackageNamesToBuiltPackages(prunedIgnoredPackageNames, dependencyGraph)
	if err != nil {
		err = fmt.Errorf("unable to find build nodes for the ignored packages, error:\n%s", err)
		return
	}

	ignoredAndRebuiltPackages := intersect.Hash(packagesToIgnore, packagesToRebuild)
	if len(ignoredAndRebuiltPackages) != 0 {
		err = fmt.Errorf("can't ignore and force a rebuild of a package at the same time. Abusing packages: %v", ignoredAndRebuiltPackages)
		return
	}

	finalPackagesToBuild, err = CalculatePackagesToBuild(packagesToBuild, packagesToRebuild, imageConfig, baseDirPath, dependencyGraph)
	if err != nil {
		err = fmt.Errorf("unable to generate package build list, error:\n%s", err)
		return
	}
	return
}

// CalculatePackagesToBuild generates a comprehensive list of all PackageVers that the scheduler should attempt to build.
// The build list is a superset of:
//   - packagesNamesToBuild,
//   - packagesNamesToRebuild,
//   - local packages listed in the image config, and
//   - kernels in the image config (if built locally).
func CalculatePackagesToBuild(packagesNamesToBuild, packagesNamesToRebuild []*pkgjson.PackageVer, imageConfig, baseDirPath string, dependencyGraph *pkggraph.PkgGraph) (packageVersToBuild []*pkgjson.PackageVer, err error) {
	packageVersToBuild = append(packagesNamesToBuild, packagesNamesToRebuild...)

	packageVersFromConfig, err := extractPackagesFromConfig(imageConfig, baseDirPath)
	if err != nil {
		err = fmt.Errorf("failed to extract packages from the image config, error:\n%w", err)
		return
	}

	packageVersFromConfig, err = filterLocalPackagesOnly(packageVersFromConfig, dependencyGraph)
	if err != nil {
		err = fmt.Errorf("failed to filter local packages from the image config, error:\n%w", err)
		return
	}

	packageVersToBuild = append(packageVersToBuild, packageVersFromConfig...)
	packageVersToBuild = sliceutils.RemoveDuplicatesFromSlice(packageVersToBuild)

	return
}

// PackageNamesToBuiltPackages converts the input strings to PackageVer structures that are understood by the graph.
// If a string is a spec name, it will convert it to all packages built from that spec.
// If the string is NOT a spec name, it will check, if the string is a package present in the graph.
// If the package is not present in the graph, it will return an error.
// All packages without a build node are considered invalid.
//
// Note: since "SRPM_PACK_LIST" can work only with spec names, spec names take priority over package names
// so that passing "X" to "SRPM_PACK_LIST", "PACKAGE_IGNORE_LIST", and "*_BUILD_LIST" arguments targets the same set of packages.
func PackageNamesToBuiltPackages(packageOrSpecNames []string, dependencyGraph *pkggraph.PkgGraph) (packageVers []*pkgjson.PackageVer, err error) {
	logger.Log.Debugf("Converting package/spec names to build nodes' PackageVers: %v", packageOrSpecNames)

	specToPackageNodes := make(map[string][]*pkggraph.PkgNode)
	for _, node := range dependencyGraph.AllBuildNodes() {
		specToPackageNodes[node.SpecName()] = append(specToPackageNodes[node.SpecName()], node)
	}

	packageVersMap := make(map[*pkgjson.PackageVer]bool)
	for _, packageOrSpecName := range packageOrSpecNames {
		if nodes, ok := specToPackageNodes[packageOrSpecName]; ok {
			logger.Log.Debugf("Name '%s' matched a spec name. Adding all packages built from this spec to the list.", packageOrSpecName)
			for _, pkg := range nodes {
				packageVersMap[pkg.VersionedPkg] = true
			}
		} else {
			logger.Log.Debugf("Name '%s' not found among known spec names. Searching among known package names.", packageOrSpecName)
			foundNode, err := dependencyGraph.FindBestPkgNode(&pkgjson.PackageVer{Name: packageOrSpecName})
			if err != nil {
				err = fmt.Errorf("failed while searching the dependency graph for package '%s', error:\n%w", packageOrSpecName, err)
				return nil, err
			}
			if foundNode == nil {
				err = fmt.Errorf("couldn't find package '%s' in the dependency graph", packageOrSpecName)
				return nil, err
			}
			if foundNode.BuildNode == nil {
				err = fmt.Errorf("found package '%s' but it is not a locally-built package", packageOrSpecName)
				return nil, err
			}

			logger.Log.Debugf("Name '%s' matched a package name. Adding it to the list.", packageOrSpecName)
			packageVersMap[foundNode.BuildNode.VersionedPkg] = true
		}
	}

	packageVers = sliceutils.PackageVersSetToSlice(packageVersMap)

	return
}

// PruneUnknownPackages removes all packages from the input list that do not have a build node in the graph.
// The function also returns a slice with the unknown package names.
func PruneUnknownPackages(packageOrSpecNames []string, dependencyGraph *pkggraph.PkgGraph) (prunedNames, unknownNames []string, err error) {
	logger.Log.Debugf("Pruning unknown packages from the following list: %v", packageOrSpecNames)

	specNames := make(map[string]bool)
	for _, node := range dependencyGraph.AllBuildNodes() {
		specNames[node.SpecName()] = true
	}

	for _, packageOrSpecName := range packageOrSpecNames {
		if specNames[packageOrSpecName] {
			logger.Log.Tracef("Name '%s' matched a spec name, keeping it in the list.", packageOrSpecName)
			prunedNames = append(prunedNames, packageOrSpecName)
		} else {
			logger.Log.Debugf("Name '%s' not found among known spec names. Searching among known package names.", packageOrSpecName)
			foundNode, err := dependencyGraph.FindBestPkgNode(&pkgjson.PackageVer{Name: packageOrSpecName})
			if err != nil {
				err = fmt.Errorf("failed while searching the dependency graph for package '%s', error:\n%w", packageOrSpecName, err)
				return nil, nil, err
			}

			if (foundNode == nil) || (foundNode.BuildNode == nil) {
				logger.Log.Tracef("Couldn't find package '%s' in the dependency graph. Pruning from the list.", packageOrSpecName)
				unknownNames = append(unknownNames, packageOrSpecName)
				continue
			}

			logger.Log.Debugf("Name '%s' matched a package name, keeping it in the list.", packageOrSpecName)
			prunedNames = append(prunedNames, packageOrSpecName)
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

// extractPackagesFromConfig reads configuration file and returns a package list required for the said configuration
// Package list is assembled from packageList and KernelOptions.
func extractPackagesFromConfig(configFile, baseDirPath string) (packageList []*pkgjson.PackageVer, err error) {
	if configFile == "" {
		return
	}

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
func filterLocalPackagesOnly(packageVersionsInConfig []*pkgjson.PackageVer, dependencyGraph *pkggraph.PkgGraph) (filteredPackages []*pkgjson.PackageVer, err error) {
	logger.Log.Debug("Filtering out external packages from list of packages extracted from the image config file.")

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
