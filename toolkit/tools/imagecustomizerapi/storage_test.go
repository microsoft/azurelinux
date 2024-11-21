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
	assert.ErrorContains(t, err, "invalid filesystem item at index 1")
	assert.ErrorContains(t, err, "invalid 'deviceId'")
	assert.ErrorContains(t, err, "device (esp) is used by multiple things")
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
	assert.ErrorContains(t, err, "invalid filesystem item at index 1")
	assert.ErrorContains(t, err, "invalid 'deviceId'")
	assert.ErrorContains(t, err, "device (a) not found")
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
	assert.ErrorContains(t, err, "invalid disk at index 0")
	assert.ErrorContains(t, err, "invalid partition at index 1")
	assert.ErrorContains(t, err, "duplicate id (a)")
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
	assert.ErrorContains(t, err, "invalid filesystem item at index 0")
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
	assert.ErrorContains(t, err, "invalid filesystem item at index 0")
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

func TestStorageIsValidDuplicateMountPoint(t *testing.T) {
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
					Path: "/",
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
	assert.ErrorContains(t, err, "invalid filesystem item at index 1:\n"+
		"duplicate 'mountPoint.path' (/)")
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

func TestStorageIsValidVerityRoot(t *testing.T) {
	value := Storage{
		Disks: []Disk{{
			PartitionTableType: "gpt",
			Partitions: []Partition{
				{
					Id: "esp",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 8 * diskutils.MiB,
					},
					Type: PartitionTypeESP,
				},
				{
					Id: "root",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 1 * diskutils.GiB,
					},
				},
				{
					Id: "roothash",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 100 * diskutils.MiB,
					},
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
				DeviceId: "rootverity",
				Type:     "ext4",
				MountPoint: &MountPoint{
					Path: "/",
				},
			},
		},
		Verity: []Verity{
			{
				Id:           "rootverity",
				Name:         "root",
				DataDeviceId: "root",
				HashDeviceId: "roothash",
			},
		},
	}

	err := value.IsValid()
	assert.NoError(t, err)
}

func TestStorageIsValidVerityUsr(t *testing.T) {
	value := Storage{
		Disks: []Disk{{
			PartitionTableType: "gpt",
			Partitions: []Partition{
				{
					Id: "esp",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 8 * diskutils.MiB,
					},
					Type: PartitionTypeESP,
				},
				{
					Id: "root",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 1 * diskutils.GiB,
					},
				},
				{
					Id: "usr",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 1 * diskutils.GiB,
					},
				},
				{
					Id: "usrhash",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 100 * diskutils.MiB,
					},
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
				DeviceId: "root",
				Type:     "ext4",
				MountPoint: &MountPoint{
					Path: "/",
				},
			},
			{
				DeviceId: "usrverity",
				Type:     "ext4",
				MountPoint: &MountPoint{
					Path: "/usr",
				},
			},
		},
		Verity: []Verity{
			{
				Id:           "usrverity",
				Name:         "usr",
				DataDeviceId: "usr",
				HashDeviceId: "usrhash",
			},
		},
	}

	err := value.IsValid()
	assert.ErrorContains(t, err, "defining non-root verity devices is not currently supported")
	assert.ErrorContains(t, err, "filesystems[].mountPoint.path' of verity device (usrverity) must be set to '/'")
}

func TestStorageIsValidVerityInvalidName(t *testing.T) {
	value := Storage{
		Disks: []Disk{{
			PartitionTableType: "gpt",
			Partitions: []Partition{
				{
					Id: "esp",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 8 * diskutils.MiB,
					},
					Type: PartitionTypeESP,
				},
				{
					Id: "root",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 1 * diskutils.GiB,
					},
				},
				{
					Id: "roothash",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 100 * diskutils.MiB,
					},
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
				DeviceId: "root",
				Type:     "ext4",
				MountPoint: &MountPoint{
					Path: "/",
				},
			},
		},
		Verity: []Verity{
			{
				Id:           "rootverity",
				Name:         "root",
				HashDeviceId: "roothash",
			},
		},
	}

	err := value.IsValid()
	assert.ErrorContains(t, err, "invalid verity item at index 0")
	assert.ErrorContains(t, err, "'dataDeviceId' may not be empty")
}

func TestStorageIsValidVerityDuplicateId(t *testing.T) {
	value := Storage{
		Disks: []Disk{{
			PartitionTableType: "gpt",
			Partitions: []Partition{
				{
					Id: "esp",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 8 * diskutils.MiB,
					},
					Type: PartitionTypeESP,
				},
				{
					Id: "root",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 1 * diskutils.GiB,
					},
				},
				{
					Id: "roothash",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 100 * diskutils.MiB,
					},
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
				DeviceId: "root",
				Type:     "ext4",
				MountPoint: &MountPoint{
					Path: "/",
				},
			},
		},
		Verity: []Verity{
			{
				Id:           "root",
				Name:         "root",
				DataDeviceId: "root",
				HashDeviceId: "roothash",
			},
		},
	}

	err := value.IsValid()
	assert.ErrorContains(t, err, "invalid verity item at index 0")
	assert.ErrorContains(t, err, "duplicate id (root)")
}

func TestStorageIsValidVerityBadDataId(t *testing.T) {
	value := Storage{
		Disks: []Disk{{
			PartitionTableType: "gpt",
			Partitions: []Partition{
				{
					Id: "esp",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 8 * diskutils.MiB,
					},
					Type: PartitionTypeESP,
				},
				{
					Id: "root",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 1 * diskutils.GiB,
					},
				},
				{
					Id: "roothash",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 100 * diskutils.MiB,
					},
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
				DeviceId: "root",
				Type:     "ext4",
				MountPoint: &MountPoint{
					Path: "/",
				},
			},
		},
		Verity: []Verity{
			{
				Id:           "rootverity",
				Name:         "root",
				DataDeviceId: "usr",
				HashDeviceId: "roothash",
			},
		},
	}

	err := value.IsValid()
	assert.ErrorContains(t, err, "invalid verity item at index 0")
	assert.ErrorContains(t, err, "invalid 'dataDeviceId':\ndevice (usr) not found")
}

func TestStorageIsValidVerityBadHashId(t *testing.T) {
	value := Storage{
		Disks: []Disk{{
			PartitionTableType: "gpt",
			Partitions: []Partition{
				{
					Id: "esp",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 8 * diskutils.MiB,
					},
					Type: PartitionTypeESP,
				},
				{
					Id: "root",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 1 * diskutils.GiB,
					},
				},
				{
					Id: "roothash",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 100 * diskutils.MiB,
					},
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
				DeviceId: "root",
				Type:     "ext4",
				MountPoint: &MountPoint{
					Path: "/",
				},
			},
		},
		Verity: []Verity{
			{
				Id:           "rootverity",
				Name:         "root",
				DataDeviceId: "root",
				HashDeviceId: "usrhash",
			},
		},
	}

	err := value.IsValid()
	assert.ErrorContains(t, err, "invalid verity item at index 0")
	assert.ErrorContains(t, err, "invalid 'hashDeviceId':\ndevice (usrhash) not found")
}

func TestStorageIsValidVerityWrongDeviceName(t *testing.T) {
	value := Storage{
		Disks: []Disk{{
			PartitionTableType: "gpt",
			Partitions: []Partition{
				{
					Id: "esp",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 8 * diskutils.MiB,
					},
					Type: PartitionTypeESP,
				},
				{
					Id: "root",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 1 * diskutils.GiB,
					},
				},
				{
					Id: "roothash",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 100 * diskutils.MiB,
					},
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
				DeviceId: "rootverity",
				Type:     "ext4",
				MountPoint: &MountPoint{
					Path: "/",
				},
			},
		},
		Verity: []Verity{
			{
				Id:           "rootverity",
				Name:         "usr",
				DataDeviceId: "root",
				HashDeviceId: "roothash",
			},
		},
	}

	err := value.IsValid()
	assert.ErrorContains(t, err, "verity 'name' (usr) must be \"root\" for filesystem (/) partition (root)")
}

func TestStorageIsValidVerityHashFileSystem(t *testing.T) {
	value := Storage{
		Disks: []Disk{{
			PartitionTableType: "gpt",
			Partitions: []Partition{
				{
					Id: "esp",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 8 * diskutils.MiB,
					},
					Type: PartitionTypeESP,
				},
				{
					Id: "root",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 1 * diskutils.GiB,
					},
				},
				{
					Id: "roothash",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 100 * diskutils.MiB,
					},
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
				DeviceId: "rootverity",
				Type:     "ext4",
				MountPoint: &MountPoint{
					Path: "/",
				},
			},
			{
				DeviceId: "roothash",
				Type:     "ext4",
			},
		},
		Verity: []Verity{
			{
				Id:           "rootverity",
				Name:         "root",
				DataDeviceId: "root",
				HashDeviceId: "roothash",
			},
		},
	}

	err := value.IsValid()
	assert.ErrorContains(t, err, "invalid filesystem item at index 2")
	assert.ErrorContains(t, err, "invalid 'deviceId'")
	assert.ErrorContains(t, err, "device (roothash) is used by multiple things")
}

func TestStorageIsValidVerityFileSystemHasIdType(t *testing.T) {
	value := Storage{
		Disks: []Disk{{
			PartitionTableType: "gpt",
			Partitions: []Partition{
				{
					Id: "esp",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 8 * diskutils.MiB,
					},
					Type: PartitionTypeESP,
				},
				{
					Id: "root",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 1 * diskutils.GiB,
					},
				},
				{
					Id: "roothash",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 100 * diskutils.MiB,
					},
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
				DeviceId: "rootverity",
				Type:     "ext4",
				MountPoint: &MountPoint{
					Path:   "/",
					IdType: MountIdentifierTypeUuid,
				},
			},
		},
		Verity: []Verity{
			{
				Id:           "rootverity",
				Name:         "root",
				DataDeviceId: "root",
				HashDeviceId: "roothash",
			},
		},
	}

	err := value.IsValid()
	assert.ErrorContains(t, err, "filesystem for verity device (rootverity) may not specify 'mountPoint.idType'")
}

func TestStorageIsValidVerityFileSystemMissing(t *testing.T) {
	value := Storage{
		Disks: []Disk{{
			PartitionTableType: "gpt",
			Partitions: []Partition{
				{
					Id: "esp",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 8 * diskutils.MiB,
					},
					Type: PartitionTypeESP,
				},
				{
					Id: "root",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 1 * diskutils.GiB,
					},
				},
				{
					Id: "roothash",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 100 * diskutils.MiB,
					},
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
		},
		Verity: []Verity{
			{
				Id:           "rootverity",
				Name:         "root",
				DataDeviceId: "root",
				HashDeviceId: "roothash",
			},
		},
	}

	err := value.IsValid()
	assert.ErrorContains(t, err, "defining non-root verity devices is not currently supported:\n"+
		"filesystems[].mountPoint.path' of verity device (rootverity) must be set to '/'")
}

func TestStorageIsValidVerityTwoVerity(t *testing.T) {
	value := Storage{
		Disks: []Disk{{
			PartitionTableType: "gpt",
			Partitions: []Partition{
				{
					Id: "esp",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 8 * diskutils.MiB,
					},
					Type: PartitionTypeESP,
				},
				{
					Id: "root",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 1 * diskutils.GiB,
					},
				},
				{
					Id: "roothash",
					Size: PartitionSize{
						Type: PartitionSizeTypeExplicit,
						Size: 100 * diskutils.MiB,
					},
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
				DeviceId: "rootverity",
				Type:     "ext4",
				MountPoint: &MountPoint{
					Path: "/",
				},
			},
		},
		Verity: []Verity{
			{
				Id:           "rootverity",
				Name:         "root",
				DataDeviceId: "root",
				HashDeviceId: "roothash",
			},
			{
				Id:           "rootverity2",
				Name:         "root",
				DataDeviceId: "root",
				HashDeviceId: "roothash",
			},
		},
	}

	err := value.IsValid()
	assert.ErrorContains(t, err, "invalid verity item at index 1")
	assert.ErrorContains(t, err, "invalid 'dataDeviceId'")
	assert.ErrorContains(t, err, "device (root) is used by multiple things")
}
