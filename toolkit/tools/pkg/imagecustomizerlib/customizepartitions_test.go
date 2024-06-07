// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"os"
	"path/filepath"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/stretchr/testify/assert"
)

func TestCustomizeImagePartitions(t *testing.T) {
	var err error

	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	buildDir := filepath.Join(tmpDir, "TestCustomizeImageCopyFiles")
	configFile := filepath.Join(testDir, "partitions-config.yaml")
	outImageFilePath := filepath.Join(buildDir, "image.qcow2")

	// Customize image.
	err = CustomizeImageWithConfigFile(buildDir, configFile, baseImage, nil, outImageFilePath, "raw", "",
		false /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	// Check output file type.
	checkFileType(t, outImageFilePath, "raw")

	mountPoints := []mountPoint{
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
	}

	imageConnection, err := connectToImage(buildDir, outImageFilePath, mountPoints)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Check for key files/directories on the partitions.
	fstabPath := filepath.Join(imageConnection.Chroot().RootDir(), "/etc/fstab")
	_, err = os.Stat(fstabPath)
	assert.NoError(t, err, "check for /etc/fstab")

	_, err = os.Stat(filepath.Join(imageConnection.Chroot().RootDir(), "/usr/bin/bash"))
	assert.NoError(t, err, "check for /usr/bin/bash")

	grubCfgFilePath := filepath.Join(imageConnection.Chroot().RootDir(), "/boot/grub2/grub.cfg")
	_, err = os.Stat(grubCfgFilePath)
	assert.NoError(t, err, "check for /boot/grub2/grub2.cfg")

	_, err = os.Stat(filepath.Join(imageConnection.Chroot().RootDir(), "/boot/efi/boot/grub2/grub.cfg"))
	assert.NoError(t, err, "check for /boot/efi/boot/grub2/grub2.cfg")

	_, err = os.Stat(filepath.Join(imageConnection.Chroot().RootDir(), "/var/log"))
	assert.NoError(t, err, "check for /var/log")

	// Check that the fstab entries are correct.
	fstabEntries, err := diskutils.ReadFstabFile(fstabPath)
	assert.NoError(t, err, "read /etc/fstab")

	partitions, err := diskutils.GetDiskPartitions(imageConnection.Loopback().DevicePath())
	assert.NoError(t, err, "get disk partitions")

	assert.Equal(t, len(mountPoints), len(fstabEntries), "/etc/fstab entries count")

	for i := range mountPoints {
		mountPoint := mountPoints[i]
		fstabEntry := fstabEntries[i]
		partition := partitions[mountPoint.PartitionNum]

		assert.Equalf(t, mountPoint.FileSystemType, fstabEntry.FsType, "fstab [%d]: file system type", i)
		assert.Equalf(t, mountPoint.Path, fstabEntry.Target, "fstab [%d]: target path", i)

		expectedSource := fmt.Sprintf("PARTUUID=%s", partition.PartUuid)
		assert.Equalf(t, expectedSource, fstabEntry.Source, "fstab [%d]: source", i)
	}

	// Check that the extraCommandLine was added to the grub.cfg file.
	grubCfgContents, err := file.Read(grubCfgFilePath)
	assert.NoError(t, err, "read grub.cfg file")
	assert.Regexp(t, "linux.* console=tty0 console=ttyS0 ", grubCfgContents)
}

func TestCustomizeImageKernelCommandLine(t *testing.T) {
	var err error

	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	buildDir := filepath.Join(tmpDir, "TestCustomizeImageCopyFiles")
	configFile := filepath.Join(testDir, "extracommandline-config.yaml")
	outImageFilePath := filepath.Join(buildDir, "image.qcow2")

	// Customize image.
	err = CustomizeImageWithConfigFile(buildDir, configFile, baseImage, nil, outImageFilePath, "raw", "",
		false /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	imageConnection, err := connectToCoreEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Check that the extraCommandLine was added to the grub.cfg file.
	grubCfgFilePath := filepath.Join(imageConnection.Chroot().RootDir(), "/boot/grub2/grub.cfg")
	grubCfgContents, err := file.Read(grubCfgFilePath)
	assert.NoError(t, err, "read grub.cfg file")
	assert.Regexp(t, "linux.* console=tty0 console=ttyS0 ", grubCfgContents)
}
