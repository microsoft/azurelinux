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

func TestShouldSucceedParsingValidDiskEmptyTarget_Disk(t *testing.T) {
	var checkedDisk Disk

	diskWithNoTarget := validDisk
	diskWithNoTarget.TargetDisk = TargetDisk{}

	assert.NoError(t, diskWithNoTarget.IsValid())
	err := remarshalJSON(diskWithNoTarget, &checkedDisk)
	assert.NoError(t, err)
	assert.Equal(t, diskWithNoTarget, checkedDisk)
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

func TestShouldFailPartitionsOverlapping_Disk(t *testing.T) {
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

func TestShouldFailMaxSizeInsufficient_Disk(t *testing.T) {
	var checkedDisk Disk
	invalidDisk := validDisk

	invalidDisk.MaxSize = uint64(512)
	invalidDisk.TargetDisk.Type = ""
	invalidDisk.TargetDisk.Value = ""
	err := invalidDisk.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [Disk]: the MaxSize of 512 is not large enough to accomodate defined partitions ending at 1024.", err.Error())

	// remarshal runs IsValid() on [SystemConfig] prior to running it on [Config], so we get a different error message here.
	err = remarshalJSON(invalidDisk, &checkedDisk)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Disk]: invalid [Disk]: the MaxSize of 512 is not large enough to accomodate defined partitions ending at 1024.", err.Error())
}

func TestShouldFailNoSizeSet_Disk(t *testing.T) {
	var checkedDisk Disk
	invalidDisk := validDisk

	invalidDisk.MaxSize = 0
	invalidDisk.TargetDisk.Type = ""
	invalidDisk.TargetDisk.Value = ""
	err := invalidDisk.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [Disk]: a configuration without a defined target disk must have a non-zero MaxSize", err.Error())

	// remarshal runs IsValid() on [SystemConfig] prior to running it on [Config], so we get a different error message here.
	err = remarshalJSON(invalidDisk, &checkedDisk)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Disk]: invalid [Disk]: a configuration without a defined target disk must have a non-zero MaxSize", err.Error())
}

func TestShouldFailInvalidTargetDisk_Disk(t *testing.T) {
	var checkedDisk Disk
	invalidDisk := validDisk

	invalidDisk.MaxSize = uint64(512)
	invalidDisk.TargetDisk.Type = "path"
	invalidDisk.TargetDisk.Value = ""
	err := invalidDisk.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [TargetDisk]: Value must be specified for TargetDiskType of 'path'", err.Error())

	err = remarshalJSON(invalidDisk, &checkedDisk)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Disk]: failed to parse [TargetDisk]: invalid [TargetDisk]: Value must be specified for TargetDiskType of 'path'", err.Error())
}

func TestShouldFailMissingPartitionTableType_Disk(t *testing.T) {
	var checkedDisk Disk
	invalidDisk := validDisk

	invalidDisk.PartitionTableType = ""
	err := invalidDisk.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [PartitionTableType]: '', must be set to one of 'gpt' or 'mbr' when defining a real disk with partitions", err.Error())

	err = remarshalJSON(invalidDisk, &checkedDisk)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Disk]: invalid [PartitionTableType]: '', must be set to one of 'gpt' or 'mbr' when defining a real disk with partitions", err.Error())
}

func TestShouldPassNoPartitionTableTypeWithNoParts_Disk(t *testing.T) {
	var checkedDisk Disk
	diskNoParts := validDisk

	diskNoParts.PartitionTableType = ""
	diskNoParts.Partitions = []Partition{}
	err := diskNoParts.IsValid()
	assert.NoError(t, err)

	err = remarshalJSON(diskNoParts, &checkedDisk)
	assert.NoError(t, err)
}

func TestShouldFailRAIDMultiplePartitions(t *testing.T) {
	var checkedDisk Disk
	diskMultiPartRaid := validDisk

	// Add a new raid disk config
	diskMultiPartRaid = Disk{ID: "MyRaidDisk"}
	diskMultiPartRaid.Partitions = []Partition{
		{
			ID: "MyRaidPart",
		},
		{
			ID: "MyRaidPart2",
		},
	}
	diskMultiPartRaid.TargetDisk = TargetDisk{
		Type: "raid",
		RaidConfig: RaidConfig{
			RaidID:           "MyRaidDisk",
			Level:            1,
			ComponentPartIDs: []string{"MyRaidPart", "MyRaidPart2"},
		},
	}

	err := diskMultiPartRaid.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [Disk]: a [Disk] 'MyRaidDisk' with a [TargetDisk] of type 'raid' must define exactly one [Partition]", err.Error())

	err = remarshalJSON(diskMultiPartRaid, &checkedDisk)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Disk]: invalid [Disk]: a [Disk] 'MyRaidDisk' with a [TargetDisk] of type 'raid' must define exactly one [Partition]", err.Error())
}

func TestShouldFailBootLoaderRaidNotLegacy_Disk(t *testing.T) {
	var checkedDisk Disk
	diskRaidBootLoader := validDisk

	// Add a new raid disk config
	diskRaidBootLoader = Disk{ID: "MyRaidBootDisk"}
	diskRaidBootLoader.Partitions = []Partition{
		{
			ID:    "MyRaidBootPart",
			Flags: []PartitionFlag{PartitionFlagBiosGrub},
		},
	}
	diskRaidBootLoader.TargetDisk = TargetDisk{
		Type: "raid",
		RaidConfig: RaidConfig{
			RaidID:           "MyRaidBootDisk",
			Level:            1,
			ComponentPartIDs: []string{"MyRaidBootPart"},
		},
	}

	err := diskRaidBootLoader.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [Disk]: RAID disk 'MyRaidBootDisk' cannot have a [Partition] with a BootLoaderFlag set to true when the RAID config has LegacyMetadata set to false", err.Error())

	err = remarshalJSON(diskRaidBootLoader, &checkedDisk)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Disk]: invalid [Disk]: RAID disk 'MyRaidBootDisk' cannot have a [Partition] with a BootLoaderFlag set to true when the RAID config has LegacyMetadata set to false", err.Error())
}

func TestShouldFailBootLoaderRaidNotLevel1_Disk(t *testing.T) {
	var checkedDisk Disk
	diskRaidBootLoader := validDisk

	// Add a new raid disk config
	diskRaidBootLoader = Disk{ID: "MyRaidBootDisk"}
	diskRaidBootLoader.Partitions = []Partition{
		{
			ID:    "MyRaidBootPart",
			Flags: []PartitionFlag{PartitionFlagBiosGrub},
		},
	}
	diskRaidBootLoader.TargetDisk = TargetDisk{
		Type: "raid",
		RaidConfig: RaidConfig{
			RaidID:           "MyRaidBootDisk",
			Level:            5,
			ComponentPartIDs: []string{"MyRaidBootPart"},
			LegacyMetadata:   true,
		},
	}

	err := diskRaidBootLoader.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [Disk]: RAID disk 'MyRaidBootDisk' cannot have a [Partition] with a BootLoaderFlag set to true without setting the RAID config has Level to '1'", err.Error())

	err = remarshalJSON(diskRaidBootLoader, &checkedDisk)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Disk]: invalid [Disk]: RAID disk 'MyRaidBootDisk' cannot have a [Partition] with a BootLoaderFlag set to true without setting the RAID config has Level to '1'", err.Error())
}
