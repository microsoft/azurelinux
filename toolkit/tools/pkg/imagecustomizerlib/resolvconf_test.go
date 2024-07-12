// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/stretchr/testify/assert"
)

func TestCustomizeImageResolvConf(t *testing.T) {
	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	testTmpDir := filepath.Join(tmpDir, "TestCustomizeImageResolvConf")
	buildDir := filepath.Join(testTmpDir, "build")
	outImageFilePath := filepath.Join(testTmpDir, "image.raw")

	// Customize image.
	config := imagecustomizerapi.Config{
		OS: &imagecustomizerapi.OS{
			Services: imagecustomizerapi.Services{
				Disable: []string{"systemd-resolved"},
			},
		},
	}

	err := CustomizeImage(buildDir, testDir, &config, baseImage, nil, outImageFilePath, "raw", "",
		false /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	imageConnection, err := connectToCoreEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Ensure resolv.conf does not exist.
	imageResolvConfPath := filepath.Join(imageConnection.Chroot().RootDir(), resolvConfPath)
	exists, err := file.PathExists(imageResolvConfPath)
	if !assert.NoError(t, err) {
		return
	}
	assert.False(t, exists)

	// Create a resolv.conf file.
	fakeResolvConfContents := "abcdef"
	err = file.Write(fakeResolvConfContents, imageResolvConfPath)
	if !assert.NoError(t, err) {
		return
	}

	err = imageConnection.CleanClose()
	if !assert.NoError(t, err) {
		return
	}

	// Customize image.
	config = imagecustomizerapi.Config{
		OS: &imagecustomizerapi.OS{},
	}

	err = CustomizeImage(buildDir, testDir, &config, outImageFilePath, nil, outImageFilePath, "raw", "",
		false /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	imageConnection, err = connectToCoreEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Ensure resolv.conf file was restored.
	imageResolvConfPath = filepath.Join(imageConnection.Chroot().RootDir(), resolvConfPath)
	actualResolvConfContents, err := file.Read(imageResolvConfPath)
	if !assert.NoError(t, err) {
		return
	}

	assert.Equal(t, fakeResolvConfContents, actualResolvConfContents)

	// Delete resolv.conf file.
	err = os.Remove(imageResolvConfPath)
	if !assert.NoError(t, err) {
		return
	}

	// Create a resolv.conf symlink.
	fakeResolvConfSymlinkPath := "../fake/resolv.conf"
	err = os.Symlink(fakeResolvConfSymlinkPath, imageResolvConfPath)
	if !assert.NoError(t, err) {
		return
	}

	err = imageConnection.CleanClose()
	if !assert.NoError(t, err) {
		return
	}

	// Customize image.
	err = CustomizeImage(buildDir, testDir, &config, outImageFilePath, nil, outImageFilePath, "raw", "",
		false /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	imageConnection, err = connectToCoreEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Ensure resolv.conf symlink was restored.
	imageResolvConfPath = filepath.Join(imageConnection.Chroot().RootDir(), resolvConfPath)
	actualResolvConfSymlinkPath, err := os.Readlink(imageResolvConfPath)
	if !assert.NoError(t, err) {
		return
	}

	assert.Equal(t, fakeResolvConfSymlinkPath, actualResolvConfSymlinkPath)

	// Delete resolv.conf file.
	err = os.Remove(imageResolvConfPath)
	if !assert.NoError(t, err) {
		return
	}

	err = imageConnection.CleanClose()
	if !assert.NoError(t, err) {
		return
	}

	// Customize image.
	config = imagecustomizerapi.Config{
		OS: &imagecustomizerapi.OS{
			Services: imagecustomizerapi.Services{
				Enable: []string{"systemd-resolved"},
			},
		},
	}

	err = CustomizeImage(buildDir, testDir, &config, outImageFilePath, nil, outImageFilePath, "raw", "",
		false /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	imageConnection, err = connectToCoreEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Ensure resolv.conf symlink was set to systemd-resolved.
	imageResolvConfPath = filepath.Join(imageConnection.Chroot().RootDir(), resolvConfPath)
	actualResolvConfSymlinkPath, err = os.Readlink(imageResolvConfPath)
	if !assert.NoError(t, err) {
		return
	}

	assert.Equal(t, resolvSystemdStubPath, actualResolvConfSymlinkPath)
}
