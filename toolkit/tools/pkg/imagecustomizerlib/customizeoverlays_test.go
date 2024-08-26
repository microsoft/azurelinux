// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"path/filepath"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
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
	mountPoints := []mountPoint{
		{
			PartitionNum:   3,
			Path:           "/",
			FileSystemType: "ext4",
		},
		{
			PartitionNum:   2,
			Path:           "/boot",
			FileSystemType: "ext4",
		},
		{
			PartitionNum:   1,
			Path:           "/boot/efi",
			FileSystemType: "vfat",
		},
		{
			PartitionNum:   4,
			Path:           "/var",
			FileSystemType: "ext4",
		},
	}

	// Connect to customized image.
	imageConnection, err := connectToImage(buildDir, outImageFilePath, false /*includeDefaultMounts*/, mountPoints)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	verifyOverlays(t, imageConnection.chroot.RootDir())
}

func verifyOverlays(t *testing.T, rootPath string) {
	// Verify fstab for Overlays.
	fstabPath := filepath.Join(rootPath, "etc/fstab")
	fstabContents, err := file.Read(fstabPath)
	if !assert.NoError(t, err) {
		return
	}

	// Check for specific overlay configurations in fstab
	assert.Contains(t, fstabContents,
		"overlay /etc overlay lowerdir=/sysroot/etc,"+
			"upperdir=/sysroot/var/overlays/etc/upper,workdir=/sysroot/var/overlays/etc/work,"+
			"x-systemd.requires=/sysroot/var,x-initrd.mount,x-systemd.wanted-by=initrd-fs.target 0 0")

	assert.Contains(t, fstabContents,
		"overlay /media overlay lowerdir=/media:/home,"+
			"upperdir=/overlays/media/upper,workdir=/overlays/media/work 0 0")
}
