// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestStorageIsValidDuplicatePartitionID(t *testing.T) {
	value := Storage{
		Disks: []Disk{{
			PartitionTableType: "gpt",
			MaxSize:            2,
			Partitions: []Partition{
				{
					Id:             "esp",
					FileSystemType: "fat32",
					Start:          1,
					Flags: []PartitionFlag{
						"esp",
						"boot",
					},
				},
			},
		}},
		BootType: "efi",
		FileSystems: []FileSystem{
			{
				DeviceId: "esp",
				MountPoint: &MountPoint{
					Path: "/boot/efi",
				},
			},
			{
				DeviceId: "esp",
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
