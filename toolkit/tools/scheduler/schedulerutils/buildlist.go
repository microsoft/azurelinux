// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"microsoft.com/pkggen/imagegen/configuration"
	"microsoft.com/pkggen/imagegen/installutils"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkgjson"
)

// CalculatePackagesToBuild generates a comprehensive list of all PackageVers that the scheduler should attempt to build.
// The build list is a superset of packagesNamesToBuild, packagesNamesToRebuild, packages listed in the image config, and kernels in the image config.
func CalculatePackagesToBuild(packagesNamesToBuild, packagesNamesToRebuild []string, imageConfig, baseDirPath string) (packageVersToBuild []*pkgjson.PackageVer, err error) {
	packageVersToBuild = convertPackageNamesIntoPackageVers(packagesNamesToBuild)
	packageVersToBuild = append(packageVersToBuild, convertPackageNamesIntoPackageVers(packagesNamesToRebuild)...)

	if imageConfig == "" {
		return
	}

	packageVersFromConfig, err := extractPackagesFromConfig(imageConfig, baseDirPath)
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
