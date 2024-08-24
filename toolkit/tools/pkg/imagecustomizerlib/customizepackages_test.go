// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"
	"github.com/stretchr/testify/assert"
)

func TestCustomizeImagePackagesAddOfflineDir(t *testing.T) {
	testTmpDir := filepath.Join(tmpDir, "TestCustomizeImagePackagesAddOfflineDir")

	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)
	downloadedRpmsDir := getDownloadedRpmsDir(t, "2.0")

	buildDir := filepath.Join(testTmpDir, "build")
	outImageFilePath := filepath.Join(testTmpDir, "image.raw")

	downloadedRpmsTmpDir := filepath.Join(testTmpDir, "rpms")

	// Create a copy of the RPMs directory, but without the golang package.
	err := copyRpms(downloadedRpmsDir, downloadedRpmsTmpDir, []string{"golang-"})
	if !assert.NoError(t, err) {
		return
	}

	// Install jq package.
	config := imagecustomizerapi.Config{
		OS: &imagecustomizerapi.OS{
			Packages: imagecustomizerapi.Packages{
				Install: []string{"jq"},
			},
		},
	}

	err = CustomizeImage(buildDir, testDir, &config, baseImage, []string{downloadedRpmsTmpDir}, outImageFilePath,
		"raw", "", false /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	imageConnection, err := connectToCoreEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Ensure jq was installed.
	ensureFilesExist(t, imageConnection,
		"/usr/bin/jq",
	)

	err = imageConnection.CleanClose()
	if !assert.NoError(t, err) {
		return
	}

	// Create a copy of the RPMs directory, but without the jq package.
	// This ensures that the package repo metadata is refreshed between runs.
	err = os.RemoveAll(downloadedRpmsTmpDir)
	if !assert.NoError(t, err) {
		return
	}

	err = copyRpms(downloadedRpmsDir, downloadedRpmsTmpDir, []string{"jq-"})
	if !assert.NoError(t, err) {
		return
	}

	// Install jq package.
	config = imagecustomizerapi.Config{
		OS: &imagecustomizerapi.OS{
			Packages: imagecustomizerapi.Packages{
				InstallLists: []string{"lists/golang.yaml"},
			},
		},
	}

	err = CustomizeImage(buildDir, testDir, &config, outImageFilePath, []string{downloadedRpmsTmpDir}, outImageFilePath,
		"raw", "", false /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	imageConnection, err = connectToCoreEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Ensure go was installed.
	ensureFilesExist(t, imageConnection,
		"/usr/bin/jq",
		"/usr/bin/go",
	)
}

func copyRpms(sourceDir string, targetDir string, excludePrefixes []string) error {
	sourceFiles, err := os.ReadDir(sourceDir)
	if err != nil {
		return fmt.Errorf("failed to read source directory (%s):\n%w", sourceDir, err)
	}

	for _, sourceFile := range sourceFiles {
		if sourceFile.IsDir() {
			continue
		}

		exclude := sliceutils.ContainsFunc(excludePrefixes, func(prefix string) bool {
			return strings.HasPrefix(sourceFile.Name(), prefix)
		})
		if exclude {
			continue
		}

		err := file.Copy(filepath.Join(sourceDir, sourceFile.Name()), filepath.Join(targetDir, sourceFile.Name()))
		if err != nil {
			return err
		}
	}

	return nil
}

func TestCustomizeImagePackagesAddOfflineLocalRepo(t *testing.T) {
	testTmpDir := filepath.Join(tmpDir, "TestCustomizeImagePackagesAddOfflineLocalRepo")

	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	downloadedRpmsRepoFile := getDownloadedRpmsRepoFile(t, "2.0")
	rpmSources := []string{downloadedRpmsRepoFile}

	buildDir := filepath.Join(testTmpDir, "build")
	outImageFilePath := filepath.Join(testTmpDir, "image.raw")
	configFile := filepath.Join(testDir, "packages-add-config.yaml")

	// Customize image.
	err := CustomizeImageWithConfigFile(buildDir, configFile, baseImage, rpmSources, outImageFilePath, "raw", "",
		false /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
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
