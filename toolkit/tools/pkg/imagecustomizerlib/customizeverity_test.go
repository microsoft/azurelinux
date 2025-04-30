// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"path/filepath"
	"regexp"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safeloopback"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safemount"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/stretchr/testify/assert"
	"golang.org/x/sys/unix"
)

func TestCustomizeImageVerity(t *testing.T) {
	for _, version := range supportedAzureLinuxVersions {
		t.Run(string(version), func(t *testing.T) {
			testCustomizeImageVerityHelper(t, "TestCustomizeImageVerity"+string(version), baseImageTypeCoreEfi,
				version)
		})
	}
}

func testCustomizeImageVerityHelper(t *testing.T, testName string, imageType baseImageType,
	imageVersion baseImageVersion,
) {
	baseImage := checkSkipForCustomizeImage(t, imageType, imageVersion)

	testTempDir := filepath.Join(tmpDir, testName)
	buildDir := filepath.Join(testTempDir, "build")
	outImageFilePath := filepath.Join(testTempDir, "image.raw")
	configFile := filepath.Join(testDir, "verity-config.yaml")

	// Customize image.
	err := CustomizeImageWithConfigFile(buildDir, configFile, baseImage, nil, outImageFilePath, "raw", "",
		"" /*outputPXEArtifactsDir*/, true /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	// Connect to customized image.
	mountPoints := []mountPoint{
		{
			PartitionNum:   3,
			Path:           "/",
			FileSystemType: "ext4",
			Flags:          unix.MS_RDONLY,
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
			PartitionNum:   5,
			Path:           "/var",
			FileSystemType: "ext4",
		},
	}

	imageConnection, err := connectToImage(buildDir, outImageFilePath, false /*includeDefaultMounts*/, mountPoints)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	partitions, err := getDiskPartitionsMap(imageConnection.Loopback().DevicePath())
	assert.NoError(t, err, "get disk partitions")

	// Verify that verity is configured correctly.
	bootPath := filepath.Join(imageConnection.chroot.RootDir(), "/boot")
	rootDevice := partitionDevPath(imageConnection, 3)
	hashDevice := partitionDevPath(imageConnection, 4)
	verifyVerity(t, bootPath, rootDevice, hashDevice, "PARTUUID="+partitions[3].PartUuid,
		"PARTUUID="+partitions[4].PartUuid)
}

func TestCustomizeImageVerityShrinkExtract(t *testing.T) {
	for _, version := range supportedAzureLinuxVersions {
		t.Run(string(version), func(t *testing.T) {
			testCustomizeImageVerityShrinkExtractHelper(t, "TestCustomizeImageVerityShrinkExtract"+string(version),
				baseImageTypeCoreEfi, version)
		})
	}
}

func testCustomizeImageVerityShrinkExtractHelper(t *testing.T, testName string, imageType baseImageType,
	imageVersion baseImageVersion,
) {
	baseImage := checkSkipForCustomizeImage(t, imageType, imageVersion)

	testTempDir := filepath.Join(tmpDir, testName)
	buildDir := filepath.Join(testTempDir, "build")
	outImageFilePath := filepath.Join(testTempDir, "image.raw")
	configFile := filepath.Join(testDir, "verity-partition-labels.yaml")

	var config imagecustomizerapi.Config
	err := imagecustomizerapi.UnmarshalYamlFile(configFile, &config)
	if !assert.NoError(t, err) {
		return
	}

	bootPartitionNum := 2
	rootPartitionNum := 3
	hashPartitionNum := 4

	// Change the hash partition's filesystem type to ext4.
	// This tests the logic that skips the hash partition when looking for partitions to shrink.
	config.Storage.FileSystems[hashPartitionNum-1].Type = "ext4"

	// Customize image, shrink partitions, and split the partitions into individual files.
	err = CustomizeImage(buildDir, testDir, &config, baseImage, nil, outImageFilePath, "", "raw",
		"" /*outputPXEArtifactsDir*/, true /*useBaseImageRpmRepos*/, true /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	// Attach partition files.
	bootPartitionPath := filepath.Join(testTempDir, fmt.Sprintf("image_%d.raw", bootPartitionNum))
	rootPartitionPath := filepath.Join(testTempDir, fmt.Sprintf("image_%d.raw", rootPartitionNum))
	hashPartitionPath := filepath.Join(testTempDir, fmt.Sprintf("image_%d.raw", hashPartitionNum))

	bootDevice, err := safeloopback.NewLoopback(bootPartitionPath)
	if !assert.NoError(t, err) {
		return
	}
	defer bootDevice.Close()

	rootDevice, err := safeloopback.NewLoopback(rootPartitionPath)
	if !assert.NoError(t, err) {
		return
	}
	defer rootDevice.Close()

	hashDevice, err := safeloopback.NewLoopback(hashPartitionPath)
	if !assert.NoError(t, err) {
		return
	}
	defer hashDevice.Close()

	bootMountPath := filepath.Join(buildDir, "bootpartition")
	bootMount, err := safemount.NewMount(bootDevice.DevicePath(), bootMountPath, "ext4", 0, "", true)
	if !assert.NoError(t, err) {
		return
	}
	defer bootMount.Close()

	// Verify that verity is configured correctly.
	verifyVerity(t, bootMountPath, rootDevice.DevicePath(), hashDevice.DevicePath(), "PARTLABEL=root",
		"PARTLABEL=roothash")
}

func verifyVerity(t *testing.T, bootPath string, rootDevice string, hashDevice string, rootId string, hashId string) {
	// Verify verity kernel args.
	grubCfgPath := filepath.Join(bootPath, "/grub2/grub.cfg")
	grubCfgContents, err := file.Read(grubCfgPath)
	if !assert.NoError(t, err) {
		return
	}

	assert.Regexp(t, `(?m)linux.* rd.systemd.verity=1 `, grubCfgContents)
	assert.Regexp(t, fmt.Sprintf(`(?m)linux.* systemd.verity_root_data=%s `, rootId), grubCfgContents)
	assert.Regexp(t, fmt.Sprintf(`(?m)linux.* systemd.verity_root_hash=%s `, hashId), grubCfgContents)
	assert.Regexp(t, `(?m)linux.* systemd.verity_root_options=panic-on-corruption `, grubCfgContents)

	// Read root hash from grub.cfg file.
	roothashRegexp, err := regexp.Compile(`(?m)linux.* roothash=([a-fA-F0-9]*) `)
	if !assert.NoError(t, err) {
		return
	}

	roothashMatches := roothashRegexp.FindStringSubmatch(grubCfgContents)
	if !assert.Equal(t, 2, len(roothashMatches)) {
		return
	}

	roothash := roothashMatches[1]

	// Verify verity hashes.
	err = shell.ExecuteLive(false, "veritysetup", "verify", rootDevice, hashDevice, roothash)
	assert.NoError(t, err)
}
