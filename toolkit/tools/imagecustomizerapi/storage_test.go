// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/ptrutils"
	"github.com/stretchr/testify/assert"
)

func TestStorageIsValidCoreEfi(t *testing.T) {
	value := Storage{
		Disks: []Disk{{
			PartitionTableType: "gpt",
			MaxSize:            ptrutils.PtrTo(DiskSize(4 * diskutils.GiB)),
			Partitions: []Partition{
				{
					Id:    "esp",
					Start: ptrutils.PtrTo(DiskSize(1 * diskutils.MiB)),
					End:   ptrutils.PtrTo(DiskSize(9 * diskutils.MiB)),
					Type:  PartitionTypeESP,
				},
				{
					Id:    "rootfs",
					Start: ptrutils.PtrTo(DiskSize(9 * diskutils.MiB)),
				},
			},
		}},
		BootType: "efi",
		FileSystems: []FileSystem{
			{
				DeviceId: "esp",
				Type:     "vfat",
				MountPoint: &MountPoint{
					Path: "/boot/efi",
				},
			},
			{
				DeviceId: "rootfs",
				Type:     "ext4",
				MountPoint: &MountPoint{
					Path: "/",
				},
			},
		},
	}

	err := value.IsValid()
	assert.NoError(t, err)
}

func TestStorageIsValidDuplicatePartitionID(t *testing.T) {
	value := Storage{
		Disks: []Disk{{
			PartitionTableType: "gpt",
			MaxSize:            ptrutils.PtrTo(DiskSize(2 * diskutils.GiB)),
			Partitions: []Partition{
				{
					Id:    "esp",
					Start: ptrutils.PtrTo(DiskSize(1 * diskutils.MiB)),
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
			MaxSize:            ptrutils.PtrTo(DiskSize(2 * diskutils.GiB)),
			Partitions: []Partition{
				{
					Id:    "a",
					Start: ptrutils.PtrTo(DiskSize(1 * diskutils.MiB)),
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

func TestStorageIsValidMountPointWithoutFileSystem(t *testing.T) {
	storage := Storage{
		Disks: []Disk{{
			PartitionTableType: PartitionTableTypeGpt,
			MaxSize:            ptrutils.PtrTo(DiskSize(2 * diskutils.GiB)),
			Partitions: []Partition{
				{
					Id:    "a",
					Start: ptrutils.PtrTo(DiskSize(1 * diskutils.MiB)),
					End:   nil,
				},
			},
		}},
		BootType: BootTypeEfi,
		FileSystems: []FileSystem{
			{
				DeviceId: "a",
				MountPoint: &MountPoint{
					Path: "/",
				},
			},
		},
	}

	err := storage.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "filesystem with 'mountPoint' must have a 'type'")
}

func TestStorageIsValidMissingFileSystemEntry(t *testing.T) {
	storage := Storage{
		Disks: []Disk{{
			PartitionTableType: PartitionTableTypeGpt,
			MaxSize:            ptrutils.PtrTo(DiskSize(2 * diskutils.GiB)),
			Partitions: []Partition{
				{
					Id:    "esp",
					Start: ptrutils.PtrTo(DiskSize(1 * diskutils.MiB)),
					End:   nil,
					Type:  PartitionTypeESP,
				},
			},
		}},
		BootType: BootTypeEfi,
	}

	err := storage.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "ESP partition (esp) must have 'fat32' or 'vfat' filesystem type")
}

func TestStorageIsValidBadEspFsType(t *testing.T) {
	storage := Storage{
		Disks: []Disk{{
			PartitionTableType: PartitionTableTypeGpt,
			MaxSize:            ptrutils.PtrTo(DiskSize(2 * diskutils.GiB)),
			Partitions: []Partition{
				{
					Id:    "esp",
					Start: ptrutils.PtrTo(DiskSize(1 * diskutils.MiB)),
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
	assert.ErrorContains(t, err, "ESP partition (esp) must have 'fat32' or 'vfat' filesystem type")
}

func TestStorageIsValidBadBiosBootFsType(t *testing.T) {
	storage := Storage{
		Disks: []Disk{{
			PartitionTableType: PartitionTableTypeGpt,
			MaxSize:            ptrutils.PtrTo(DiskSize(2 * diskutils.GiB)),
			Partitions: []Partition{
				{
					Id:    "bios",
					Start: ptrutils.PtrTo(DiskSize(1 * diskutils.MiB)),
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
	assert.ErrorContains(t, err, "BIOS boot partition (bios) must not have a filesystem 'type'")
}

func TestStorageIsValidBiosWithMountPoint(t *testing.T) {
	storage := Storage{
		Disks: []Disk{{
			PartitionTableType: PartitionTableTypeGpt,
			MaxSize:            ptrutils.PtrTo(DiskSize(2 * diskutils.GiB)),
			Partitions: []Partition{
				{
					Id:    "bios",
					Start: ptrutils.PtrTo(DiskSize(1 * diskutils.MiB)),
					End:   nil,
					Type:  PartitionTypeBiosGrub,
				},
			},
		}},
		BootType: BootTypeEfi,
		FileSystems: []FileSystem{
			{
				DeviceId: "bios",
				MountPoint: &MountPoint{
					Path: "/boot/bios",
				},
			},
		},
	}

	err := storage.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "BIOS boot partition (bios) must not have a 'mountPoint'")
}

func TestStorageIsValidBadBiosBootStart(t *testing.T) {
	storage := Storage{
		Disks: []Disk{{
			PartitionTableType: PartitionTableTypeGpt,
			MaxSize:            ptrutils.PtrTo(DiskSize(2 * diskutils.GiB)),
			Partitions: []Partition{
				{
					Id:    "bios",
					Start: ptrutils.PtrTo(DiskSize(2 * diskutils.MiB)),
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
			MaxSize:            ptrutils.PtrTo(DiskSize(2 * diskutils.GiB)),
			Partitions: []Partition{
				{
					Id:    "esp",
					Start: ptrutils.PtrTo(DiskSize(1 * diskutils.MiB)),
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
				MaxSize:            ptrutils.PtrTo(DiskSize(4 * diskutils.MiB)),
				Partitions: []Partition{
					{
						Id:    "a",
						Start: ptrutils.PtrTo(DiskSize(1 * diskutils.MiB)),
						End:   ptrutils.PtrTo(DiskSize(2 * diskutils.MiB)),
					},
					{
						Id:    "a",
						Start: ptrutils.PtrTo(DiskSize(2 * diskutils.MiB)),
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
				MaxSize:            ptrutils.PtrTo(DiskSize(3 * diskutils.MiB)),
				Partitions: []Partition{
					{
						Id:    "a",
						Start: ptrutils.PtrTo(DiskSize(1 * diskutils.MiB)),
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
				MaxSize:            ptrutils.PtrTo(DiskSize(4 * diskutils.MiB)),
				Partitions: []Partition{
					{
						Id:    "a",
						Start: ptrutils.PtrTo(DiskSize(1 * diskutils.MiB)),
						End:   ptrutils.PtrTo(DiskSize(2 * diskutils.MiB)),
						Type:  PartitionTypeESP,
						Label: "a",
					},
					{
						Id:    "b",
						Start: ptrutils.PtrTo(DiskSize(2 * diskutils.MiB)),
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
				MaxSize:            ptrutils.PtrTo(DiskSize(4 * diskutils.MiB)),
				Partitions: []Partition{
					{
						Id:    "a",
						Start: ptrutils.PtrTo(DiskSize(1 * diskutils.MiB)),
						End:   ptrutils.PtrTo(DiskSize(2 * diskutils.MiB)),
						Type:  PartitionTypeESP,
						Label: "a",
					},
					{
						Id:    "b",
						Start: ptrutils.PtrTo(DiskSize(2 * diskutils.MiB)),
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

func TestStorageIsValidBothDisksAndResetUuid(t *testing.T) {
	value := Storage{
		Disks: []Disk{{
			PartitionTableType: "gpt",
			MaxSize:            ptrutils.PtrTo(DiskSize(4 * diskutils.GiB)),
			Partitions: []Partition{
				{
					Id:    "esp",
					Start: ptrutils.PtrTo(DiskSize(1 * diskutils.MiB)),
					End:   ptrutils.PtrTo(DiskSize(9 * diskutils.MiB)),
					Type:  PartitionTypeESP,
				},
				{
					Id:    "rootfs",
					Start: ptrutils.PtrTo(DiskSize(9 * diskutils.MiB)),
				},
			},
		}},
		BootType: "efi",
		FileSystems: []FileSystem{
			{
				DeviceId: "esp",
				Type:     "vfat",
				MountPoint: &MountPoint{
					Path: "/boot/efi",
				},
			},
			{
				DeviceId: "rootfs",
				Type:     "ext4",
				MountPoint: &MountPoint{
					Path: "/",
				},
			},
		},
		ResetPartitionsUuidsType: ResetPartitionsUuidsTypeAll,
	}

	err := value.IsValid()
	assert.ErrorContains(t, err, "cannot specify both 'resetPartitionsUuidsType' and 'disks'")
}

func TestStorageIsValidFileSystemsWithoutDisks(t *testing.T) {
	value := Storage{
		FileSystems: []FileSystem{
			{
				DeviceId: "esp",
				Type:     "vfat",
				MountPoint: &MountPoint{
					Path: "/boot/efi",
				},
			},
			{
				DeviceId: "rootfs",
				Type:     "ext4",
				MountPoint: &MountPoint{
					Path: "/",
				},
			},
		},
		ResetPartitionsUuidsType: ResetPartitionsUuidsTypeAll,
	}

	err := value.IsValid()
	assert.ErrorContains(t, err, "cannot specify 'filesystems' without specifying 'disks'")
}
