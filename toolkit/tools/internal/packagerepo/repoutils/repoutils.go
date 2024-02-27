// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package repoutils

import (
	"fmt"
	"path/filepath"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repocloner"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
)

// RestoreClonedRepoContents restores a cloner's repo contents using a JSON file at `srcFile`.
// Will convert the cloned content into a repo and verify its content is correct.
//
// This routine requires a clean build environment. If there are already packages in the
// cache (with exception of the toolchain packages) then this routine will return an error.
// This is done to ensure the cache only contains the desired packages.
func RestoreClonedRepoContents(cloner repocloner.RepoCloner, srcFile string) (err error) {
	const cloneDeps = false

	timestamp.StartEvent("restoring cloned repo", nil)
	defer timestamp.StopEvent(nil)

	logger.Log.Infof("Restoring cloned repository contents from (%s).", srcFile)

	var repo *repocloner.RepoContents
	err = jsonutils.ReadJSONFile(srcFile, &repo)
	if err != nil {
		return
	}

	uniquePackages := removePackageDuplicates(repo.Repo)
	packagesToDownload := filterOutDownloadedPackage(uniquePackages, cloner.CloneDirectory())

	_, err = cloner.CloneByPackageVer(cloneDeps, packagesToDownload...)
	if err != nil {
		return err
	}

	// Covert the packages into a repo so that they can be compared against the expected state.
	err = cloner.ConvertDownloadedPackagesIntoRepo()
	if err != nil {
		return
	}

	// Verify the cloned contents are as expected.
	clonedRepo, err := cloner.ClonedRepoContents()
	if err != nil {
		return
	}

	return verifyClonedRepoContents(clonedRepo.Repo, uniquePackages)
}

// SaveClonedRepoContents saves a cloner's repo contents to a JSON file at `dstFile`.
func SaveClonedRepoContents(cloner repocloner.RepoCloner, dstFile string) (err error) {
	timestamp.StartEvent("saving cloned repo contents", nil)
	defer timestamp.StopEvent(nil)

	repo, err := cloner.ClonedRepoContents()
	if err != nil {
		return
	}

	err = jsonutils.WriteJSONFile(dstFile, repo)
	return
}

func removePackageDuplicates(packages []*repocloner.RepoPackage) []*repocloner.RepoPackage {
	index := 0
	seen := make(map[string]bool)
	uniquePackages := make([]*repocloner.RepoPackage, len(packages))

	for _, pkg := range packages {
		packageID := pkg.ID()
		if !seen[packageID] {
			seen[packageID] = true
			uniquePackages[index] = pkg
			index++
		}
	}

	return uniquePackages[:index]
}

func filterOutDownloadedPackage(packages []*repocloner.RepoPackage, cloneDirectory string) []*pkgjson.PackageVer {
	const packageCondition = "="

	packageVers := make([]*pkgjson.PackageVer, len(packages))
	index := 0
	for _, pkg := range packages {
		pkgVersion := fmt.Sprintf("%s.%s", pkg.Version, pkg.Distribution)

		// Skip packages that are already present, this is expected for the toolchain
		rpmName := fmt.Sprintf("%s-%s.%s.rpm", pkg.Name, pkgVersion, pkg.Architecture)
		expectedFile := filepath.Join(cloneDirectory, rpmName)

		exists, _ := file.PathExists(expectedFile)
		if exists {
			logger.Log.Debugf("Package (%s) already cloned, skipping restoration.", rpmName)
			continue
		}

		logger.Log.Infof("Found missing package to restore: %s.", rpmName)

		// Setup a PackageVer that points at the exact package to clone with the pkgVersion and distribution tag included.
		packageVers[index] = &pkgjson.PackageVer{
			Name:      pkg.Name,
			Version:   pkgVersion,
			Condition: packageCondition,
		}
		index++
	}

	return packageVers[:index]
}

func verifyClonedRepoContents(clonedRepoContents, expectedPackages []*repocloner.RepoPackage) (err error) {
	logger.Log.Infof("Verifying cloned repo contents.")

	if len(expectedPackages) != len(clonedRepoContents) {
		return fmt.Errorf("cloned repo has %d packages, expected %d", len(expectedPackages), len(clonedRepoContents))
	}

	expectedPackagesSet := map[string]bool{}
	clonedPackagesSet := map[string]bool{}
	for i := 0; i < len(expectedPackages); i++ {
		expectedPackagesSet[expectedPackages[i].ID()] = true
		clonedPackagesSet[clonedRepoContents[i].ID()] = true
	}

	extraPackages := []string{}
	missingPackages := []string{}
	for clonedPackage := range clonedPackagesSet {
		if !expectedPackagesSet[clonedPackage] {
			extraPackages = append(extraPackages, clonedPackage)
		}
	}

	for expectedPackage := range expectedPackagesSet {
		if !clonedPackagesSet[expectedPackage] {
			missingPackages = append(missingPackages, expectedPackage)
		}
	}

	if (len(extraPackages) > 0) || (len(missingPackages) > 0) {
		return fmt.Errorf("packages mismatch. Unexpected extra packages: %v.\n Expected missing packages: %v", extraPackages, missingPackages)
	}

	logger.Log.Infof("Cloned repo contents verified successfully.")

	return
}
