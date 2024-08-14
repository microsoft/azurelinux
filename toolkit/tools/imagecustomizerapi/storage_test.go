// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/ptrutils"
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

func TestStorageIsValidMissingFileSystemEntry(t *testing.T) {
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
	}

	err := storage.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid disk at index 0")
	assert.ErrorContains(t, err, "partition (esp) at index 0 must have a corresponding filesystem entry")
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

func TestStorageIsValidDuplicatePartitionId(t *testing.T) {
	storage := Storage{
		BootType: BootTypeEfi,
		Disks: []Disk{
			{
				PartitionTableType: PartitionTableTypeGpt,
				MaxSize:            3 * diskutils.MiB,
				Partitions: []Partition{
					{
						Id:    "a",
						Start: 1 * diskutils.MiB,
						End:   ptrutils.PtrTo(DiskSize(2 * diskutils.MiB)),
					},
					{
						Id:    "a",
						Start: 2 * diskutils.MiB,
					},
				},
			},
		},
		FileSystems: []FileSystem{
			{
				DeviceId: "a",
				Type:     "ext4",
			},
		},
	}

	err := storage.IsValid()
	assert.ErrorContains(t, err, "duplicate partition id")
}

func TestStorageIsValidNoLabel(t *testing.T) {
	storage := Storage{
		BootType: BootTypeEfi,
		Disks: []Disk{
			{
				PartitionTableType: PartitionTableTypeGpt,
				MaxSize:            3 * diskutils.MiB,
				Partitions: []Partition{
					{
						Id:    "a",
						Start: 1 * diskutils.MiB,
						End:   ptrutils.PtrTo(DiskSize(2 * diskutils.MiB)),
						Type:  PartitionTypeESP,
					},
				},
			},
		},
		FileSystems: []FileSystem{
			{
				DeviceId: "a",
				Type:     FileSystemTypeFat32,
				MountPoint: &MountPoint{
					IdType: MountIdentifierTypePartLabel,
					Path:   "/",
				},
			},
		},
	}

	err := storage.IsValid()
	assert.ErrorContains(t, err, "invalid fileSystem at index 0")
	assert.ErrorContains(t, err, "idType is set to (part-label) but partition (a) has no label set")
}

func TestStorageIsValidUniqueLabel(t *testing.T) {
	storage := Storage{
		BootType: BootTypeEfi,
		Disks: []Disk{
			{
				PartitionTableType: PartitionTableTypeGpt,
				MaxSize:            3 * diskutils.MiB,
				Partitions: []Partition{
					{
						Id:    "a",
						Start: 1 * diskutils.MiB,
						End:   ptrutils.PtrTo(DiskSize(2 * diskutils.MiB)),
						Type:  PartitionTypeESP,
						Label: "a",
					},
					{
						Id:    "b",
						Start: 2 * diskutils.MiB,
						Label: "b",
					},
				},
			},
		},
		FileSystems: []FileSystem{
			{
				DeviceId: "a",
				Type:     FileSystemTypeFat32,
				MountPoint: &MountPoint{
					IdType: MountIdentifierTypePartLabel,
					Path:   "/",
				},
			},
			{
				DeviceId: "b",
				Type:     FileSystemTypeFat32,
				MountPoint: &MountPoint{
					IdType: MountIdentifierTypePartLabel,
					Path:   "/b",
				},
			},
		},
	}

	err := storage.IsValid()
	assert.NoError(t, err)
}

func TestStorageIsValidDuplicateLabel(t *testing.T) {
	storage := Storage{
		BootType: BootTypeEfi,
		Disks: []Disk{
			{
				PartitionTableType: PartitionTableTypeGpt,
				MaxSize:            3 * diskutils.MiB,
				Partitions: []Partition{
					{
						Id:    "a",
						Start: 1 * diskutils.MiB,
						End:   ptrutils.PtrTo(DiskSize(2 * diskutils.MiB)),
						Type:  PartitionTypeESP,
						Label: "a",
					},
					{
						Id:    "b",
						Start: 2 * diskutils.MiB,
						Label: "a",
					},
				},
			},
		},
		FileSystems: []FileSystem{
			{
				DeviceId: "a",
				Type:     FileSystemTypeFat32,
				MountPoint: &MountPoint{
					IdType: MountIdentifierTypePartLabel,
					Path:   "/",
				},
			},
			{
				DeviceId: "b",
				Type:     FileSystemTypeFat32,
				MountPoint: &MountPoint{
					IdType: MountIdentifierTypePartLabel,
					Path:   "/b",
				},
			},
		},
	}

	err := storage.IsValid()
	assert.ErrorContains(t, err, "invalid fileSystem at index 0")
	assert.ErrorContains(t, err, "more than one partition has a label of (a)")
}
