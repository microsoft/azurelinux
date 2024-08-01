// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safeloopback"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
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

	imageConnection, err := connectToImage(buildDir, outImageFilePath, false /*includeDefaultMounts*/, mountPoints)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	defaultPartitionName := diskutils.LegacyDefaultParitionName
	if partedSupportsEmptyString, _ := diskutils.PartedSupportsEmptyString(); partedSupportsEmptyString {
		defaultPartitionName = ""
	}

	partitions, err := diskutils.GetDiskPartitions(imageConnection.Loopback().DevicePath())
	if assert.NoError(t, err, "read partition table") {
		assert.Equal(t, defaultPartitionName, partitions[1].PartLabel)
		assert.Equal(t, defaultPartitionName, partitions[2].PartLabel)
		assert.Equal(t, "rootfs", partitions[3].PartLabel)
		assert.Equal(t, defaultPartitionName, partitions[4].PartLabel)
	}

	// Check for key files/directories on the partitions.
	_, err = os.Stat(filepath.Join(imageConnection.Chroot().RootDir(), "/usr/bin/bash"))
	assert.NoError(t, err, "check for /usr/bin/bash")

	_, err = os.Stat(filepath.Join(imageConnection.Chroot().RootDir(), "/var/log"))
	assert.NoError(t, err, "check for /var/log")

	partitions, err = diskutils.GetDiskPartitions(imageConnection.Loopback().DevicePath())
	assert.NoError(t, err, "get disk partitions")

	// Check that the fstab entries are correct.
	verifyFstabEntries(t, imageConnection, mountPoints, partitions)
	verifyBootloaderConfig(t, imageConnection, "console=tty0 console=ttyS0",
		partitions[mountPoints[1].PartitionNum].Uuid,
		partitions[mountPoints[0].PartitionNum].PartUuid)
}

func TestCustomizeImagePartitionsLegacy(t *testing.T) {
	var err error

	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	testTmpDir := filepath.Join(tmpDir, "TestCustomizeImagePartitionsLegacy")
	buildDir := filepath.Join(testTmpDir, "build")
	configFile := filepath.Join(testDir, "legacyboot-config.yaml")
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
			PartitionNum:   2,
			Path:           "/",
			FileSystemType: "ext4",
		},
	}

	imageConnection, err := connectToImage(buildDir, outImageFilePath, false /*includeDefaultMounts*/, mountPoints)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	partitions, err := diskutils.GetDiskPartitions(imageConnection.Loopback().DevicePath())
	assert.NoError(t, err, "get disk partitions")

	// Check that the fstab entries are correct.
	verifyFstabEntries(t, imageConnection, mountPoints, partitions)
	verifyBootGrubCfg(t, imageConnection, "",
		partitions[mountPoints[0].PartitionNum].Uuid,
		partitions[mountPoints[0].PartitionNum].PartUuid)
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

func TestCustomizeImageNewUUIDs(t *testing.T) {
	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	testTmpDir := filepath.Join(tmpDir, "TestCustomizeImageCopyFiles")
	buildDir := filepath.Join(testTmpDir, "build")
	configFile := filepath.Join(testDir, "newpartitionsuuids-config.yaml")
	tempRawBaseImage := filepath.Join(testTmpDir, "baseImage.raw")
	outImageFilePath := filepath.Join(testTmpDir, "image.raw")

	err := os.MkdirAll(buildDir, os.ModePerm)
	if !assert.NoError(t, err) {
		return
	}

	// Get the partitions from the base image.
	err = shell.ExecuteLiveWithErr(1, "qemu-img", "convert", "-O", "raw", baseImage, tempRawBaseImage)
	if !assert.NoError(t, err) {
		return
	}

	baseImageLoopback, err := safeloopback.NewLoopback(tempRawBaseImage)
	if !assert.NoError(t, err) {
		return
	}
	defer baseImageLoopback.Close()

	baseImagePartitions, err := diskutils.GetDiskPartitions(baseImageLoopback.DevicePath())
	if !assert.NoError(t, err, "get base image partitions") {
		return
	}

	err = baseImageLoopback.CleanClose()
	if !assert.NoError(t, err) {
		return
	}

	os.Remove(tempRawBaseImage)

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

	newImagePartitions, err := diskutils.GetDiskPartitions(imageConnection.Loopback().DevicePath())
	if !assert.NoError(t, err, "get customized image partitions") {
		return
	}

	// Ensure the partition UUIDs have been changed.
	if assert.Equal(t, len(baseImagePartitions), len(newImagePartitions)) {
		for i := range baseImagePartitions {
			baseImagePartition := baseImagePartitions[i]
			newImagePartition := newImagePartitions[i]

			if baseImagePartition.Type != "part" {
				continue
			}

			assert.Equalf(t, baseImagePartition.FileSystemType, newImagePartition.FileSystemType, "[%d] filesystem type didn't change", i)
			assert.NotEqualf(t, baseImagePartition.PartUuid, newImagePartition.PartUuid, "[%d] partition UUID did change", i)
			assert.NotEqual(t, baseImagePartition.Uuid, newImagePartition.Uuid, "[%d] filesystem UUID did change", i)
		}
	}

	// Check that the fstab entries are correct.
	verifyFstabEntries(t, imageConnection, coreEfiMountPoints, newImagePartitions)
	verifyBootloaderConfig(t, imageConnection, "",
		newImagePartitions[coreEfiMountPoints[0].PartitionNum].Uuid,
		newImagePartitions[coreEfiMountPoints[0].PartitionNum].PartUuid)
}

func verifyFstabEntries(t *testing.T, imageConnection *ImageConnection, mountPoints []mountPoint,
	partitions []diskutils.PartitionInfo,
) {
	fstabPath := filepath.Join(imageConnection.Chroot().RootDir(), "/etc/fstab")
	fstabEntries, err := diskutils.ReadFstabFile(fstabPath)
	if !assert.NoError(t, err, "read /etc/fstab") {
		return
	}

	filteredFstabEntries := filterOutSpecialPartitions(fstabEntries)

	if !assert.Equalf(t, len(mountPoints), len(filteredFstabEntries), "/etc/fstab entries count: %v", filteredFstabEntries) {
		return
	}

	for i := range mountPoints {
		mountPoint := mountPoints[i]
		fstabEntry := filteredFstabEntries[i]
		partition := partitions[mountPoint.PartitionNum]

		assert.Equalf(t, mountPoint.FileSystemType, fstabEntry.FsType, "fstab [%d]: file system type", i)
		assert.Equalf(t, mountPoint.Path, fstabEntry.Target, "fstab [%d]: target path", i)

		expectedSource := fmt.Sprintf("PARTUUID=%s", partition.PartUuid)
		assert.Equalf(t, expectedSource, fstabEntry.Source, "fstab [%d]: source", i)
	}
}

func verifyBootloaderConfig(t *testing.T, imageConnection *ImageConnection, extraCommandLineArgs string,
	bootUuid string, rootfsPartUuid string,
) {
	verifyEspGrubCfg(t, imageConnection, bootUuid)
	verifyBootGrubCfg(t, imageConnection, extraCommandLineArgs, bootUuid, rootfsPartUuid)
}

func verifyEspGrubCfg(t *testing.T, imageConnection *ImageConnection, bootUuid string) {
	grubCfgFilePath := filepath.Join(imageConnection.Chroot().RootDir(), "/boot/efi/boot/grub2/grub.cfg")
	grubCfgContents, err := file.Read(grubCfgFilePath)
	if !assert.NoError(t, err, "read ESP grub.cfg file") {
		return
	}

	assert.Regexp(t, fmt.Sprintf("(?m)^search -n -u %s -s$", regexp.QuoteMeta(bootUuid)), grubCfgContents)
}

func verifyBootGrubCfg(t *testing.T, imageConnection *ImageConnection, extraCommandLineArgs string, bootUuid string,
	rootfsPartUuid string,
) {
	grubCfgFilePath := filepath.Join(imageConnection.Chroot().RootDir(), "/boot/grub2/grub.cfg")
	grubCfgContents, err := file.Read(grubCfgFilePath)
	if !assert.NoError(t, err, "read boot grub.cfg file") {
		return
	}

	assert.Regexp(t, fmt.Sprintf("(?m)^search -n -u %s -s$", regexp.QuoteMeta(bootUuid)), grubCfgContents)
	assert.Regexp(t, fmt.Sprintf("(?m)^set rootdevice=PARTUUID=%s$", regexp.QuoteMeta(rootfsPartUuid)), grubCfgContents)

	if extraCommandLineArgs != "" {
		assert.Regexp(t, fmt.Sprintf("linux.* %s ", regexp.QuoteMeta(extraCommandLineArgs)), grubCfgContents)
	}
}
