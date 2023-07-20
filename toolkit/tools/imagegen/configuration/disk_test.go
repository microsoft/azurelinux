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
				Flags: []PartitionFlag{
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

func TestShouldFailParsingDiskWithBadPartition_Disk(t *testing.T) {
	var checkedDisk Disk
	invalidDisk := validDisk
	invalidDisk.Partitions = append([]Partition{}, validPartition)
	// Currently the only way a Partion can be invalid is by having an invalid flag
	invalidDisk.Partitions[0].Flags = []PartitionFlag{invalidPartitionFlag}

	err := invalidDisk.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for Flag (not_a_partition_flag)", err.Error())

	err = remarshalJSON(invalidDisk, &checkedDisk)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Disk]: failed to parse [Partition]: failed to parse [Flag]: invalid value for Flag (not_a_partition_flag)", err.Error())
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

func TestShouldFailPartitionsOverlapping(t *testing.T) {
	var checkedDisk Disk
	invalidDisk := validDisk

	invalidDisk.Partitions = []Partition{
		{
			ID:     "MySecondRootfs",
			Start:  uint64(512),
			End:    uint64(1024),
			FsType: "ext4",
		}, {
			ID:     "MyRootfs",
			Start:  uint64(0),
			End:    uint64(9),
			FsType: "ext4",
		}, {
			ID:     "MyThirdRootfs",
			Start:  uint64(9),
			End:    uint64(514),
			FsType: "ext4",
		},
	}

	err := invalidDisk.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [Disk]: a [Partition] with an end location 514 overlaps with a [Partition] with a start location 512", err.Error())

	// remarshal runs IsValid() on [SystemConfig] prior to running it on [Config], so we get a different error message here.
	err = remarshalJSON(invalidDisk, &checkedDisk)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Disk]: invalid [Disk]: a [Partition] with an end location 514 overlaps with a [Partition] with a start location 512", err.Error())
}

func TestShouldFailMaxSizeInsufficient(t *testing.T) {
	var checkedDisk Disk
	invalidDisk := validDisk

	invalidDisk.MaxSize = uint64(512)
	invalidDisk.TargetDisk.Type = ""
	err := invalidDisk.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [Disk]: the MaxSize of 512 is not large enough to accomodate defined partitions ending at 1024", err.Error())

	// remarshal runs IsValid() on [SystemConfig] prior to running it on [Config], so we get a different error message here.
	err = remarshalJSON(invalidDisk, &checkedDisk)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Disk]: invalid [Disk]: the MaxSize of 512 is not large enough to accomodate defined partitions ending at 1024", err.Error())
}
