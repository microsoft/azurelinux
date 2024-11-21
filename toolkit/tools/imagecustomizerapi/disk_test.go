// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/ptrutils"
	"github.com/stretchr/testify/assert"
)

func TestDiskIsValid(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            2,
		Partitions: []Partition{
			{
				ID:             "a",
				FileSystemType: "ext4",
				Start:          1,
			},
		},
	}

	err := disk.IsValid()
	assert.NoError(t, err)
}

func TestDiskIsValidWithEnd(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            2,
		Partitions: []Partition{
			{
				ID:             "a",
				FileSystemType: "ext4",
				Start:          1,
				End:            ptrutils.PtrTo(uint64(2)),
			},
		},
	}

	err := disk.IsValid()
	assert.NoError(t, err)
}

func TestDiskIsValidWithSize(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            2,
		Partitions: []Partition{
			{
				ID:             "a",
				FileSystemType: "ext4",
				Start:          1,
				Size:           ptrutils.PtrTo(uint64(1)),
			},
		},
	}

	err := disk.IsValid()
	assert.NoError(t, err)
}

func TestDiskIsValidStartAt0(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            2,
		Partitions: []Partition{
			{
				ID:             "a",
				FileSystemType: "ext4",
				Start:          0,
			},
		},
	}

	err := disk.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "block 0")
	assert.ErrorContains(t, err, "MBR header")
}

func TestDiskIsValidInvalidTableType(t *testing.T) {
	disk := &Disk{
		PartitionTableType: "a",
		MaxSize:            2,
		Partitions: []Partition{
			{
				ID:             "a",
				FileSystemType: "ext4",
				Start:          1,
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
		MaxSize:            2,
		Partitions: []Partition{
			{
				ID:             "a",
				FileSystemType: "ext4",
				Start:          2,
				End:            ptrutils.PtrTo(uint64(0)),
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
		MaxSize:            4,
		Partitions: []Partition{
			{
				ID:             "a",
				FileSystemType: "ext4",
				Start:          1,
			},
			{
				ID:             "b",
				FileSystemType: "ext4",
				Start:          2,
			},
		},
	}

	err := disk.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "is not last partition")
}

func TestDiskIsValidOverlaps(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            4,
		Partitions: []Partition{
			{
				ID:             "a",
				FileSystemType: "ext4",
				Start:          1,
				End:            ptrutils.PtrTo(uint64(3)),
			},
			{
				ID:             "b",
				FileSystemType: "ext4",
				Start:          2,
				End:            ptrutils.PtrTo(uint64(4)),
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
		MaxSize:            4,
		Partitions: []Partition{
			{
				ID:             "a",
				FileSystemType: "ext4",
				Start:          1,
				End:            ptrutils.PtrTo(uint64(3)),
			},
			{
				ID:             "b",
				FileSystemType: "ext4",
				Start:          2,
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
		MaxSize:            3,
		Partitions: []Partition{
			{
				ID:             "a",
				FileSystemType: "ext4",
				Start:          1,
				End:            ptrutils.PtrTo(uint64(2)),
			},
			{
				ID:             "b",
				FileSystemType: "ext4",
				Start:          3,
				End:            ptrutils.PtrTo(uint64(4)),
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
		MaxSize:            3,
		Partitions: []Partition{
			{
				ID:             "a",
				FileSystemType: "ext4",
				Start:          1,
				End:            ptrutils.PtrTo(uint64(3)),
			},
			{
				ID:             "b",
				FileSystemType: "ext4",
				Start:          3,
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

func TestDiskIsValidMissingEspFlag(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            3,
		Partitions: []Partition{
			{
				ID:             "a",
				FileSystemType: "fat32",
				Start:          1,
				Flags: []PartitionFlag{
					"boot",
				},
			},
		},
	}

	err := disk.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "esp")
	assert.ErrorContains(t, err, "boot")
	assert.ErrorContains(t, err, "flag")
}

func TestDiskIsValidMissingBootFlag(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            3,
		Partitions: []Partition{
			{
				ID:             "a",
				FileSystemType: "fat32",
				Start:          1,
				Flags: []PartitionFlag{
					"esp",
				},
			},
		},
	}

	err := disk.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "esp")
	assert.ErrorContains(t, err, "boot")
	assert.ErrorContains(t, err, "flag")
}

func TestDiskIsValidDuplicatePartitionId(t *testing.T) {
	disk := &Disk{
		PartitionTableType: PartitionTableTypeGpt,
		MaxSize:            2,
		Partitions: []Partition{
			{
				ID:             "a",
				FileSystemType: "ext4",
				Start:          1,
				End:            ptrutils.PtrTo(uint64(2)),
			},
			{
				ID:             "a",
				FileSystemType: "ext4",
				Start:          2,
			},
		},
	}

	err := disk.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "duplicate partition id")
}
