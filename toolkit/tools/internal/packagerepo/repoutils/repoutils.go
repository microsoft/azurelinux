// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package repoutils

import (
	"fmt"
	"path/filepath"

	"microsoft.com/pkggen/internal/file"
	"microsoft.com/pkggen/internal/jsonutils"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/packagerepo/repocloner"
	"microsoft.com/pkggen/internal/pkgjson"
)

// RestoreClonedRepoContents restores a cloner's repo contents using a JSON file at `srcFile`.
// Will convert the cloned content into a repo and verify its content is correct.
//
// This routine requires a clean build environment. If there are already packages in the
// cache (with exception of the toolchain packages) then this routine will return an error.
// This is done to ensure the cache only contains the desired packages.
func RestoreClonedRepoContents(cloner repocloner.RepoCloner, srcFile string) (err error) {
	const (
		cloneDeps        = false
		packageCondition = "="
	)

	logger.Log.Infof("Restoring cloned repository contents from (%s)", srcFile)

	var repo *repocloner.RepoContents
	err = jsonutils.ReadJSONFile(srcFile, &repo)
	if err != nil {
		return
	}

	for _, pkg := range repo.Repo {
		// Setup a PackageVer that points at the exact package to clone with the version and distribution tag included.
		pkgVer := &pkgjson.PackageVer{
			Name:      pkg.Name,
			Version:   fmt.Sprintf("%s.%s", pkg.Version, pkg.Distribution),
			Condition: packageCondition,
		}

		// Skip packages that are already present, this is expected for the toolchain
		rpmName := fmt.Sprintf("%s-%s.%s.rpm", pkgVer.Name, pkgVer.Version, pkg.Architecture)
		expectedFile := filepath.Join(cloner.CloneDirectory(), pkg.Architecture, rpmName)
		logger.Log.Infof("Restoring (%s)", rpmName)

		exists, _ := file.PathExists(expectedFile)
		if exists {
			logger.Log.Debugf("%s already exists, skipping clone", rpmName)
			continue
		}
		_, err = cloner.Clone(cloneDeps, pkgVer)
		if err != nil {
			return err
		}
	}

	// Covert the packages into a repo so that they can be compared against the expected state.
	err = cloner.ConvertDownloadedPackagesIntoRepo()
	if err != nil {
		return
	}

	// Verify the cloned contents are as expected.
	logger.Log.Infof("Verify cloned repo contents")
	clonedRepo, err := cloner.ClonedRepoContents()
	if err != nil {
		return
	}

	if len(repo.Repo) != len(clonedRepo.Repo) {
		return fmt.Errorf("cloned repo (%s) has %d packages, expected %d", cloner.CloneDirectory(), len(repo.Repo), len(clonedRepo.Repo))
	}

	for i, expectedPkg := range repo.Repo {
		clonedPkg := clonedRepo.Repo[i]

		if expectedPkg.Name != clonedPkg.Name ||
			expectedPkg.Version != clonedPkg.Version ||
			expectedPkg.Architecture != clonedPkg.Architecture ||
			expectedPkg.Distribution != clonedPkg.Distribution {

			return fmt.Errorf("package mismatch, have (%v), expected (%v)", clonedPkg, expectedPkg)
		}
	}

	return
}

// SaveClonedRepoContents saves a cloner's repo contents to a JSON file at `dstFile`.
func SaveClonedRepoContents(cloner repocloner.RepoCloner, dstFile string) (err error) {
	logger.Log.Infof("Saving cloned repository contents to (%s)", dstFile)

	repo, err := cloner.ClonedRepoContents()
	if err != nil {
		return
	}

	err = jsonutils.WriteJSONFile(dstFile, repo)
	return
}
