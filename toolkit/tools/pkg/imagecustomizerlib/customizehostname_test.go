// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/stretchr/testify/assert"
)

func TestUpdateHostname(t *testing.T) {
	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses a chroot")
	}

	// Setup environment.
	proposedDir := filepath.Join(tmpDir, "TestUpdateHostname")
	chroot := safechroot.NewChroot(proposedDir, false)
	err := chroot.Initialize("", []string{}, []*safechroot.MountPoint{}, false)
	assert.NoError(t, err)
	defer chroot.Close(false)

	err = os.MkdirAll(filepath.Join(chroot.RootDir(), "etc"), os.ModePerm)
	assert.NoError(t, err)

	// Set hostname.
	expectedHostname := "testhostname"
	err = UpdateHostname(expectedHostname, chroot)
	assert.NoError(t, err)

	// Ensure hostname was correctly set.
	actualHostname, err := os.ReadFile(filepath.Join(chroot.RootDir(), "etc/hostname"))
	assert.NoError(t, err)
	assert.Equal(t, expectedHostname, string(actualHostname))
}

func TestCustomizeImageHostname(t *testing.T) {
	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	testTmpDir := filepath.Join(tmpDir, "TestCustomizeImageHostname")
	buildDir := filepath.Join(testTmpDir, "build")
	configFile := filepath.Join(testDir, "hostname-config.yaml")
	outImageFilePath := filepath.Join(buildDir, "image.qcow2")

	// Customize image.
	err := CustomizeImageWithConfigFile(buildDir, configFile, baseImage, nil, outImageFilePath, "raw", "",
		false /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	// Connect to customized image.
	imageConnection, err := connectToCoreEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Ensure hostname was correctly set.
	actualHostname, err := os.ReadFile(filepath.Join(imageConnection.Chroot().RootDir(), "etc/hostname"))
	assert.NoError(t, err)
	assert.Equal(t, "testname", string(actualHostname))
}
