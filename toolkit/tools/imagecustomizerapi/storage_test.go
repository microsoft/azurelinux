// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/stretchr/testify/assert"
)

func TestStorageIsValidDuplicatePartitionID(t *testing.T) {
	value := Storage{
		Disks: []Disk{{
			PartitionTableType: "gpt",
			MaxSize:            2 * diskutils.GiB,
			Partitions: []Partition{
				{
					Id:    "esp",
					Start: 1 * diskutils.MiB,
					Type:  PartitionTypeESP,
				},
			},
		}},
		BootType: "efi",
		FileSystems: []FileSystem{
			{
				DeviceId: "esp",
				Type:     "fat32",
				MountPoint: &MountPoint{
					Path: "/boot/efi",
				},
			},
			{
				DeviceId: "esp",
				Type:     "fat32",
				MountPoint: &MountPoint{
					Path: "/",
				},
			},
		},
	}

	err := value.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "duplicate fileSystem deviceId used")
}

func TestStorageIsValidUnsupportedFileSystem(t *testing.T) {
	storage := Storage{
		Disks: []Disk{{
			PartitionTableType: PartitionTableTypeGpt,
			MaxSize:            2 * diskutils.GiB,
			Partitions: []Partition{
				{
					Id:    "a",
					Start: 1 * diskutils.MiB,
					End:   nil,
				},
			},
		}},
		BootType: BootTypeEfi,
		FileSystems: []FileSystem{
			{
				DeviceId: "a",
				Type:     "ntfs",
			},
		},
	}

	err := storage.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid fileSystemType value (ntfs)")
}

func TestStorageIsValidBadEspFsType(t *testing.T) {
	storage := Storage{
		Disks: []Disk{{
			PartitionTableType: PartitionTableTypeGpt,
			MaxSize:            2 * diskutils.GiB,
			Partitions: []Partition{
				{
					Id:    "esp",
					Start: 1 * diskutils.MiB,
					End:   nil,
					Type:  PartitionTypeESP,
				},
			},
		}},
		BootType: BootTypeEfi,
		FileSystems: []FileSystem{
			{
				DeviceId: "esp",
				Type:     "ext4",
			},
		},
	}

	err := storage.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "ESP partition must have 'fat32' filesystem type")
}

func TestStorageIsValidBadBiosBootFsType(t *testing.T) {
	storage := Storage{
		Disks: []Disk{{
			PartitionTableType: PartitionTableTypeGpt,
			MaxSize:            2 * diskutils.GiB,
			Partitions: []Partition{
				{
					Id:    "bios",
					Start: 1 * diskutils.MiB,
					End:   nil,
					Type:  PartitionTypeBiosGrub,
				},
			},
		}},
		BootType: BootTypeEfi,
		FileSystems: []FileSystem{
			{
				DeviceId: "bios",
				Type:     "ext4",
			},
		},
	}

	err := storage.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "BIOS boot partition must have 'fat32' filesystem type")
}

func TestStorageIsValidBadBiosBootStart(t *testing.T) {
	storage := Storage{
		Disks: []Disk{{
			PartitionTableType: PartitionTableTypeGpt,
			MaxSize:            2 * diskutils.GiB,
			Partitions: []Partition{
				{
					Id:    "bios",
					Start: 2 * diskutils.MiB,
					End:   nil,
					Type:  PartitionTypeBiosGrub,
				},
			},
		}},
		BootType: BootTypeLegacy,
		FileSystems: []FileSystem{
			{
				DeviceId: "bios",
				Type:     "fat32",
			},
		},
	}

	err := storage.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "BIOS boot partition must start at 1 MiB")
}

func TestStorageIsValidBadDeviceId(t *testing.T) {
	value := Storage{
		Disks: []Disk{{
			PartitionTableType: "gpt",
			MaxSize:            2 * diskutils.GiB,
			Partitions: []Partition{
				{
					Id:    "esp",
					Start: 1 * diskutils.MiB,
					Type:  PartitionTypeESP,
				},
			},
		}},
		BootType: "efi",
		FileSystems: []FileSystem{
			{
				DeviceId: "esp",
				Type:     "fat32",
				MountPoint: &MountPoint{
					Path: "/boot/efi",
				},
			},
			{
				DeviceId: "a",
				Type:     "fat32",
			},
		},
	}

	err := value.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "no partition with matching ID (a)")
}
