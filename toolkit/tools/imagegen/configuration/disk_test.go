// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

//TestMain found in configuration_test.go.

var (
	validDisk = Disk{
		PartitionTableType: "gpt",
		MaxSize:            uint64(1024),
		TargetDisk: TargetDisk{
			Type:  "path",
			Value: "/dev/sda",
		},
		Artifacts: []Artifact{
			{
				Name:        "CompressedVHD",
				Type:        "vhd",
				Compression: "gz",
			},
			{
				Name: "UncompressedVHD",
				Type: "vhd",
			},
		},
		RawBinaries: []RawBinary{
			{
				BinPath:   "binaries/1.bin",
				BlockSize: uint64(1024),
				Seek:      uint64(1),
			},
			{
				BinPath:   "binaries/2.bin",
				BlockSize: uint64(1024),
				Seek:      uint64(2),
			},
		},
		Partitions: []Partition{
			{
				ID: "MyBoot",
				Flags: []string{
					"esp",
					"boot",
				},
				Start:  uint64(3),
				End:    uint64(9),
				FsType: "fat32",
			},
			{
				ID:     "MyRootfs",
				Start:  uint64(9),
				End:    uint64(1024),
				FsType: "ext4",
			},
		},
	}
)

func TestShouldSucceedParsingValidDisk_Disk(t *testing.T) {
	var checkedDisk Disk

	assert.NoError(t, validDisk.IsValid())
	err := remarshalJSON(validDisk, &checkedDisk)
	assert.NoError(t, err)
	assert.Equal(t, validDisk, checkedDisk)
}

func TestShouldFailParsingInvalidDisk_Disk(t *testing.T) {
	var checkedDisk Disk
	invalidDisk := validDisk
	invalidDisk.PartitionTableType = invalidPartitionTableType

	err := invalidDisk.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [PartitionTableType]: invalid value for PartitionTableType (not_a_partition_type)", err.Error())

	err = remarshalJSON(invalidDisk, &checkedDisk)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Disk]: failed to parse [PartitionTableType]: invalid value for PartitionTableType (not_a_partition_type)", err.Error())
}
