// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/ptrutils"
	"github.com/stretchr/testify/assert"
)

func TestDiskIsValid(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            3 * diskutils.MiB,
		Partitions: []Partition{
			{
				Id:    "a",
				Start: 1 * diskutils.MiB,
			},
		},
	}

	err := disk.IsValid()
	assert.NoError(t, err)
}

func TestDiskIsValidWithEnd(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            3 * diskutils.MiB,
		Partitions: []Partition{
			{
				Id:    "a",
				Start: 1 * diskutils.MiB,
				End:   ptrutils.PtrTo(DiskSize(2 * diskutils.MiB)),
			},
		},
	}

	err := disk.IsValid()
	assert.NoError(t, err)
}

func TestDiskIsValidWithSize(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            3 * diskutils.MiB,
		Partitions: []Partition{
			{
				Id:    "a",
				Start: 1 * diskutils.MiB,
				Size: PartitionSize{
					Type: PartitionSizeTypeExplicit,
					Size: 1 * diskutils.MiB,
				},
			},
		},
	}

	err := disk.IsValid()
	assert.NoError(t, err)
}

func TestDiskIsValidStartAt0(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            3 * diskutils.MiB,
		Partitions: []Partition{
			{
				Id:    "a",
				Start: 0,
			},
		},
	}

	err := disk.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid partition (a) start")
	assert.ErrorContains(t, err, "first 1 MiB of disk is reserved for the GPT header")
}

func TestDiskIsValidInvalidTableType(t *testing.T) {
	disk := &Disk{
		PartitionTableType: "a",
		MaxSize:            3 * diskutils.MiB,
		Partitions: []Partition{
			{
				Id:    "a",
				Start: 1 * diskutils.MiB,
			},
		},
	}

	err := disk.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid partitionTableType value (a)")
}

func TestDiskIsValidInvalidPartition(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            2 * diskutils.MiB,
		Partitions: []Partition{
			{
				Id:    "a",
				Start: 2 * diskutils.MiB,
				End:   ptrutils.PtrTo(DiskSize(0)),
			},
		},
	}

	err := disk.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid partition at index 0")
	assert.ErrorContains(t, err, "partition's (a) size can't be 0 or negative")
}

func TestDiskIsValidTwoExpanding(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            4 * diskutils.MiB,
		Partitions: []Partition{
			{
				Id:    "a",
				Start: 1 * diskutils.MiB,
			},
			{
				Id:    "b",
				Start: 2 * diskutils.MiB,
			},
		},
	}

	err := disk.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "partition (a) is not last partition but size is set to \"grow\"")
}

func TestDiskIsValidTwoExpandingGrow(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            4 * diskutils.MiB,
		Partitions: []Partition{
			{
				Id:    "a",
				Start: 1 * diskutils.MiB,
			},
			{
				Id:    "b",
				Start: 2 * diskutils.MiB,
				Size: PartitionSize{
					Type: PartitionSizeTypeGrow,
				},
			},
		},
	}

	err := disk.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "partition (a) is not last partition but size is set to \"grow\"")
}

func TestDiskIsValidOverlaps(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            4 * diskutils.MiB,
		Partitions: []Partition{
			{
				Id:    "a",
				Start: 1 * diskutils.MiB,
				End:   ptrutils.PtrTo(DiskSize(3 * diskutils.MiB)),
			},
			{
				Id:    "b",
				Start: 2 * diskutils.MiB,
				End:   ptrutils.PtrTo(DiskSize(4 * diskutils.MiB)),
			},
		},
	}

	err := disk.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "partition's (a) range [1 MiB, 3 MiB) overlaps partition's (b) range [2 MiB, 4 MiB)")
}

func TestDiskIsValidOverlapsExpanding(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            4 * diskutils.MiB,
		Partitions: []Partition{
			{
				Id:    "a",
				Start: 1 * diskutils.MiB,
				End:   ptrutils.PtrTo(DiskSize(3 * diskutils.MiB)),
			},
			{
				Id:    "b",
				Start: 2 * diskutils.MiB,
			},
		},
	}

	err := disk.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "partition's (a) range [1 MiB, 3 MiB) overlaps partition's (b) range [2 MiB, )")
}

func TestDiskIsValidTooSmall(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            4 * diskutils.MiB,
		Partitions: []Partition{
			{
				Id:    "a",
				Start: 1 * diskutils.MiB,
				End:   ptrutils.PtrTo(DiskSize(2 * diskutils.MiB)),
			},
			{
				Id:    "b",
				Start: 3 * diskutils.MiB,
				End:   ptrutils.PtrTo(DiskSize(4 * diskutils.MiB)),
			},
		},
	}

	err := disk.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "disk's partitions need 5 MiB but maxSize is only 4 MiB")
	assert.ErrorContains(t, err, "GPT footer size is 1 MiB")
}

func TestDiskIsValidTooSmallExpanding(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            3 * diskutils.MiB,
		Partitions: []Partition{
			{
				Id:    "a",
				Start: 1 * diskutils.MiB,
				End:   ptrutils.PtrTo(DiskSize(3 * diskutils.MiB)),
			},
			{
				Id:    "b",
				Start: 3 * diskutils.MiB,
			},
		},
	}

	err := disk.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "disk's partitions need 5 MiB but maxSize is only 3 MiB")
	assert.ErrorContains(t, err, "GPT footer size is 1 MiB")
}

func TestDiskIsValidZeroSize(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            0,
		Partitions:         []Partition{},
	}

	err := disk.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "a disk's maxSize value (0) must be a positive non-zero number")
}
