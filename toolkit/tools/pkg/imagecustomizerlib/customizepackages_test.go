// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCustomizeImagePackagesAddOfflineDir(t *testing.T) {
	testTmpDir := filepath.Join(tmpDir, "TestCustomizeImagePackagesAddOfflineDir")

	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)
	downloadedRpmsDir := getDownloadedRpmsDir(t, "2.0")

	testCustomizeImagePackagesAddHelper(t, testTmpDir, baseImage, false, /*useBaseImageRpmRepos*/
		[]string{downloadedRpmsDir})
}

func TestCustomizeImagePackagesAddOfflineLocalRepo(t *testing.T) {
	testTmpDir := filepath.Join(tmpDir, "TestCustomizeImagePackagesAddOfflineLocalRepo")

	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)
	downloadedRpmsRepoFile := getDownloadedRpmsRepoFile(t, "2.0")

	testCustomizeImagePackagesAddHelper(t, testTmpDir, baseImage, false, /*useBaseImageRpmRepos*/
		[]string{downloadedRpmsRepoFile})
}

func testCustomizeImagePackagesAddHelper(t *testing.T, testTmpDir string, baseImage string, useBaseImageRpmRepos bool,
	rpmSources []string,
) {
	buildDir := filepath.Join(testTmpDir, "build")

	outImageFilePath := filepath.Join(testTmpDir, "image.raw")
	configFile := filepath.Join(testDir, "packages-add-config.yaml")

	// Customize image.
	err := CustomizeImageWithConfigFile(buildDir, configFile, baseImage, rpmSources, outImageFilePath, "raw", "",
		useBaseImageRpmRepos, false /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	imageConnection, err := connectToCoreEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Ensure packages were installed.
	ensureFilesExist(t, imageConnection,
		"/usr/bin/jq",
		"/usr/bin/go",
	)
}

func TestCustomizeImagePackagesUpdate(t *testing.T) {
	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	testTmpDir := filepath.Join(tmpDir, "TestCustomizeImagePackagesUpdate")
	buildDir := filepath.Join(testTmpDir, "build")

	outImageFilePath := filepath.Join(testTmpDir, "image.raw")
	configFile := filepath.Join(testDir, "packages-update-config.yaml")

	// Customize image.
	err := CustomizeImageWithConfigFile(buildDir, configFile, baseImage, nil, outImageFilePath, "raw", "",
		true /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	imageConnection, err := connectToCoreEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Ensure packages were installed.
	ensureFilesExist(t, imageConnection,
		"/usr/bin/jq",
		"/usr/bin/go",
	)

	// Ensure packages were removed.
	ensureFilesNotExist(t, imageConnection,
		"/usr/bin/which")
}

func TestCustomizeImagePackagesDiskSpace(t *testing.T) {
	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	testTmpDir := filepath.Join(tmpDir, "TestCustomizeImagePackagesDiskSpace")
	buildDir := filepath.Join(testTmpDir, "build")

	outImageFilePath := filepath.Join(testTmpDir, "image.raw")
	configFile := filepath.Join(testDir, "install-package-disk-space.yaml")

	// Customize image.
	err := CustomizeImageWithConfigFile(buildDir, configFile, baseImage, nil, outImageFilePath, "raw", "",
		true /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	assert.ErrorContains(t, err, "failed to customize raw image")
	assert.ErrorContains(t, err, "failed to install package (gcc)")
}
