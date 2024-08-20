// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"path/filepath"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/stretchr/testify/assert"
)

func TestCustomizeImageOverlays(t *testing.T) {
	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	testTempDir := filepath.Join(tmpDir, "TestCustomizeImageOverlays")
	buildDir := filepath.Join(testTempDir, "build")
	outImageFilePath := filepath.Join(testTempDir, "image.raw")
	configFile := filepath.Join(testDir, "overlays-config.yaml")

	// Customize image.
	err := CustomizeImageWithConfigFile(buildDir, configFile, baseImage, nil, outImageFilePath, "raw", "", true, false)
	if !assert.NoError(t, err) {
		return
	}

	// Connect to customized image.
	imageConnection, err := connectToCoreEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	verifyOverlays(t, imageConnection.chroot.RootDir())
}

func verifyOverlays(t *testing.T, rootPath string) {
	// Verify fstab for Overlays.
	fstabPath := filepath.Join(rootPath, "/etc/fstab")
	fstabContents, err := file.Read(fstabPath)
	if !assert.NoError(t, err) {
		return
	}

	// Check for specific overlay configurations in fstab
	assert.Contains(t, fstabContents,
		"overlay /etc overlay lowerdir=/sysroot/etc:/sysroot/home,"+
			"upperdir=/sysroot/var/overlays/etc/upper,workdir=/sysroot/var/overlays/etc/work,"+
			"x-systemd.requires=/sysroot/var,x-initrd.mount 0 0")

	assert.Contains(t, fstabContents,
		"overlay /media overlay lowerdir=/media,"+
			"upperdir=/var/overlays/media/upper,workdir=/var/overlays/media/work 0 0")

	// Verify that overlays are correctly mounted using the mount command.
	mountOutput, err := shell.Execute("mount")
	if !assert.NoError(t, err) {
		return
	}

	// Check that the overlays are mounted with the correct options
	assert.Regexp(t,
		`overlay on /etc type overlay \((.*)lowerdir=/sysroot/etc:/sysroot/home,`+
			`upperdir=/sysroot/var/overlays/etc/upper,workdir=/sysroot/var/overlays/etc/work(.*)\)`,
		mountOutput)

	assert.Regexp(t,
		`overlay on /media type overlay \((.*)lowerdir=/media,`+
			`upperdir=/var/overlays/media/upper,workdir=/var/overlays/media/work\)`,
		mountOutput)
}
