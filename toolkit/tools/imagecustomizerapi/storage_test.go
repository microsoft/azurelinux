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
					ID:             "esp",
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
		PartitionSettings: []PartitionSetting{
			{
				ID:         "esp",
				MountPoint: "/boot/efi",
			},
			{
				ID:         "esp",
				MountPoint: "/",
			},
		},
	}

	err := value.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "duplicate partitionSettings ID")
}
