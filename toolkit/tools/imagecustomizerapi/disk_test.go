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
		MaxSize:            2 * diskutils.MiB,
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
		MaxSize:            2 * diskutils.MiB,
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
		MaxSize:            2 * diskutils.MiB,
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
		MaxSize:            2 * diskutils.MiB,
		Partitions: []Partition{
			{
				Id:    "a",
				Start: 0,
			},
		},
	}

	err := disk.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "first 1 MiB must be reserved for the MBR header")
}

func TestDiskIsValidInvalidTableType(t *testing.T) {
	disk := &Disk{
		PartitionTableType: "a",
		MaxSize:            2 * diskutils.MiB,
		Partitions: []Partition{
			{
				Id:    "a",
				Start: 1 * diskutils.MiB,
			},
		},
	}

	err := disk.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "partitionTableType")
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
	assert.ErrorContains(t, err, "invalid partition")
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
	assert.ErrorContains(t, err, "is not last partition but size is set to \"grow\"")
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
	assert.ErrorContains(t, err, "is not last partition but size is set to \"grow\"")
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
	assert.ErrorContains(t, err, "overlaps")
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
	assert.ErrorContains(t, err, "overlaps")
}

func TestDiskIsValidTooSmall(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            3 * diskutils.MiB,
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
	assert.ErrorContains(t, err, "maxSize")
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
	assert.ErrorContains(t, err, "maxSize")
}

func TestDiskIsValidZeroSize(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            0,
		Partitions:         []Partition{},
	}

	err := disk.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "maxSize")
}
