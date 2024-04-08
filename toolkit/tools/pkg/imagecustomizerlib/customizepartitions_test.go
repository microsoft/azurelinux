// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCustomizeImagePartitions(t *testing.T) {
	var err error

	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	buildDir := filepath.Join(tmpDir, "TestCustomizeImageCopyFiles")
	configFile := filepath.Join(testDir, "partitions-config.yaml")
	outImageFilePath := filepath.Join(buildDir, "image.qcow2")

	// Customize image.
	err = CustomizeImageWithConfigFile(buildDir, configFile, baseImage, nil, outImageFilePath, "raw", "", true, false)
	if !assert.NoError(t, err) {
		return
	}

	// Check output file type.
	checkFileType(t, outImageFilePath, "raw")

	imageConnection, err := connectToImage(buildDir, outImageFilePath, []mountPoint{
		{
			PartitionNum:   3,
			Path:           "/",
			FileSystemType: "xfs",
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
			FileSystemType: "xfs",
		},
	})
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Check for key files/directories on the partitions.
	_, err = os.Stat(filepath.Join(imageConnection.Chroot().RootDir(), "/etc/fstab"))
	assert.NoError(t, err, "check for /etc/fstab")

	_, err = os.Stat(filepath.Join(imageConnection.Chroot().RootDir(), "/usr/bin/bash"))
	assert.NoError(t, err, "check for /usr/bin/bash")

	_, err = os.Stat(filepath.Join(imageConnection.Chroot().RootDir(), "/boot/grub2/grub.cfg"))
	assert.NoError(t, err, "check for /boot/grub2/grub2.cfg")

	_, err = os.Stat(filepath.Join(imageConnection.Chroot().RootDir(), "/boot/efi/boot/grub2/grub.cfg"))
	assert.NoError(t, err, "check for /boot/efi/boot/grub2/grub2.cfg")

	_, err = os.Stat(filepath.Join(imageConnection.Chroot().RootDir(), "/var/log"))
	assert.NoError(t, err, "check for /var/log")
}
