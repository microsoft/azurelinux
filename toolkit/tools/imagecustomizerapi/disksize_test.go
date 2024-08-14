// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/stretchr/testify/assert"
)

func TestDiskSizeNum(t *testing.T) {
	var diskSize DiskSize
	err := UnmarshalYaml([]byte("1048576"), &diskSize)
	assert.ErrorContains(t, err, "must have a unit suffix (K, M, G, or T)")
}

func TestDiskSizeNumTooLarge(t *testing.T) {
	var diskSize DiskSize
	err := UnmarshalYaml([]byte("18446744073709551616M"), &diskSize)
	assert.ErrorContains(t, err, "value out of range")
}

func TestDiskSizeKiB(t *testing.T) {
	var diskSize DiskSize
	err := UnmarshalYaml([]byte("1024K"), &diskSize)
	assert.NoError(t, err)
	assert.Equal(t, DiskSize(1024)*diskutils.KiB, diskSize)
}

func TestDiskSizeMiB(t *testing.T) {
	var diskSize DiskSize
	err := UnmarshalYaml([]byte("1M"), &diskSize)
	assert.NoError(t, err)
	assert.Equal(t, DiskSize(1)*diskutils.MiB, diskSize)
}

func TestDiskSizeGiB(t *testing.T) {
	var diskSize DiskSize
	err := UnmarshalYaml([]byte("2G"), &diskSize)
	assert.NoError(t, err)
	assert.Equal(t, DiskSize(2)*diskutils.GiB, diskSize)
}

func TestDiskSizeTiB(t *testing.T) {
	var diskSize DiskSize
	err := UnmarshalYaml([]byte("3T"), &diskSize)
	assert.NoError(t, err)
	assert.Equal(t, DiskSize(3)*diskutils.TiB, diskSize)
}

func TestDiskSizeAlpha(t *testing.T) {
	var diskSize DiskSize
	err := UnmarshalYaml([]byte("T"), &diskSize)
	assert.ErrorContains(t, err, "incorrect format")
}

func TestDiskSizeList(t *testing.T) {
	var diskSize DiskSize
	err := UnmarshalYaml([]byte("- 12"), &diskSize)
	assert.ErrorContains(t, err, "failed to parse disk size")
}

func TestDiskSizeNotMultipleOf1Mib(t *testing.T) {
	var diskSize DiskSize
	err := UnmarshalYaml([]byte("512K"), &diskSize)
	assert.ErrorContains(t, err, "must be a multiple of 1 MiB")
}

func TestDiskSizeBadFormat(t *testing.T) {
	var diskSize DiskSize
	err := UnmarshalYaml([]byte("2M2"), &diskSize)
	assert.ErrorContains(t, err, "has incorrect format")
}

func TestDiskSizeHumanReadableTiB(t *testing.T) {
	assert.Equal(t, DiskSize(diskutils.TiB).HumanReadable(), "1 TiB")
}

func TestDiskSizeHumanReadableGiB(t *testing.T) {
	assert.Equal(t, DiskSize(diskutils.GiB).HumanReadable(), "1 GiB")
}

func TestDiskSizeHumanReadableMiB(t *testing.T) {
	assert.Equal(t, DiskSize(diskutils.MiB).HumanReadable(), "1 MiB")
}

func TestDiskSizeHumanReadableKiB(t *testing.T) {
	assert.Equal(t, DiskSize(diskutils.KiB).HumanReadable(), "1 KiB")
}

func TestDiskSizeHumanReadableBytes(t *testing.T) {
	assert.Equal(t, DiskSize(1).HumanReadable(), "1 bytes")
}
