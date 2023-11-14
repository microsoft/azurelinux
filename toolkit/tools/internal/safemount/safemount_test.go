// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package safemount

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/buildpipeline"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safeloopback"
	"github.com/moby/sys/mountinfo"
	"github.com/stretchr/testify/assert"
)

func TestResourceBusy(t *testing.T) {
	if testing.Short() {
		t.Skip("Short mode enabled")
	}

	if !buildpipeline.IsRegularBuild() {
		t.Skip("loopback block device not available")
	}

	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses loopback devices")
	}

	buildDir := filepath.Join(tmpDir, "TestResourceBusy")
	err := os.MkdirAll(buildDir, 0o770)
	if !assert.NoError(t, err, "failed to test temp directory (%s)", buildDir) {
		return
	}

	diskConfig := configuration.Disk{
		PartitionTableType: configuration.PartitionTableTypeGpt,
		MaxSize:            4096,
		Partitions: []configuration.Partition{
			{
				ID:     "a",
				Start:  1,
				End:    0,
				FsType: "ext4",
			},
		},
	}

	// Create raw disk image file.
	rawDisk, err := diskutils.CreateEmptyDisk(buildDir, "disk.raw", diskConfig.MaxSize)
	assert.NoError(t, err, "failed to create empty disk file (%s)", buildDir)

	// Connect raw disk image file.
	loopback, err := safeloopback.NewLoopback(rawDisk)
	if !assert.NoError(t, err, "failed to mount raw disk as a loopback device (%s)", rawDisk) {
		return
	}
	defer loopback.Close()

	// Set up partitions.
	_, _, _, _, err = diskutils.CreatePartitions(loopback.DevicePath(), diskConfig,
		configuration.RootEncryption{}, configuration.ReadOnlyVerityRoot{})
	if !assert.NoError(t, err, "failed to create partitions on disk", loopback.DevicePath()) {
		return
	}

	// Mount the partition.
	partitionDevPath := loopback.DevicePath() + "p1"
	partitionMountPath := filepath.Join(buildDir, "mount")

	mount, err := NewMount(partitionDevPath, partitionMountPath, "ext4", 0, "", true)
	if !assert.NoError(t, err, "failed to mount partition", partitionDevPath, partitionMountPath) {
		return
	}
	defer mount.Close()

	// Check that the mount exists.
	exists, err := file.PathExists(partitionMountPath)
	if !assert.NoError(t, err, "failed to check if mount directory exists") {
		return
	}
	if !assert.Equal(t, true, exists, "mount directory doesn't exist") {
		return
	}

	isMounted, err := mountinfo.Mounted(partitionMountPath)
	if !assert.NoError(t, err, "failed to check if directory is not a mount point") {
		return
	}
	if !assert.Equal(t, true, isMounted, "directory is not a mount point") {
		return
	}

	// Open a file.
	fileOnPartitionPath := filepath.Join(partitionMountPath, "test")

	fileOnPartition, err := os.OpenFile(fileOnPartitionPath, os.O_RDWR|os.O_CREATE, 0)
	if !assert.NoErrorf(t, err, "failed to open file", fileOnPartitionPath) {
		return
	}
	defer fileOnPartition.Close()

	// Try to close the mount.
	err = mount.CleanClose()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "busy")

	// Close the file.
	fileOnPartition.Close()

	// Try to close the mount again.
	err = mount.CleanClose()
	assert.NoError(t, err, "failed to close the mount")

	// Make sure directory is deleted.
	exists, err = file.PathExists(partitionMountPath)
	if !assert.NoError(t, err, "failed to check if mount still directory exists") {
		return
	}
	assert.Equal(t, false, exists, "mount directory still exists")
}
