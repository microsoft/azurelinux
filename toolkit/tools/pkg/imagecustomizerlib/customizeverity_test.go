// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"path/filepath"
	"regexp"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/stretchr/testify/assert"
	"golang.org/x/sys/unix"
)

func TestCustomizeImageVerity(t *testing.T) {
	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	testTempDir := filepath.Join(tmpDir, "TestCustomizeImageVerity")
	buildDir := filepath.Join(testTempDir, "build")
	outImageFilePath := filepath.Join(testTempDir, "image.raw")
	configFile := filepath.Join(testDir, "verity-config.yaml")

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

	imageConnection, err := connectToImage(buildDir, outImageFilePath, mountPoints)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Verify verity kernel args.
	grubCfgPath := filepath.Join(imageConnection.chroot.RootDir(), "/boot/grub2/grub.cfg")
	grubCfgContents, err := file.Read(grubCfgPath)
	if !assert.NoError(t, err) {
		return
	}

	assert.Regexp(t, "linux.* rd.systemd.verity=1 ", grubCfgContents)
	assert.Regexp(t, "linux.* systemd.verity_root_data=PARTLABEL=root ", grubCfgContents)
	assert.Regexp(t, "linux.* systemd.verity_root_hash=PARTLABEL=root-hash ", grubCfgContents)
	assert.Regexp(t, "linux.* systemd.verity_root_options=panic-on-corruption ", grubCfgContents)

	// Read root hash from grub.cfg file.
	roothashRegexp, err := regexp.Compile("linux.* roothash=([a-fA-F0-9]*) ")
	if !assert.NoError(t, err) {
		return
	}

	roothashMatches := roothashRegexp.FindStringSubmatch(grubCfgContents)
	if !assert.Equal(t, 2, len(roothashMatches)) {
		return
	}

	roothash := roothashMatches[1]

	// Verify verity hashes.
	err = shell.ExecuteLive(false, "veritysetup", "verify", partitionDevPath(imageConnection, 3),
		partitionDevPath(imageConnection, 4), roothash)
	assert.NoError(t, err)
}
