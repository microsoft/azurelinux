// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

var (
	invalidOnDiskPartitionCommand = "part / --fstype=ext4 --size=800 --ondisk="
	invalidFstypePartitionCommand = "part / --fstype=     --size=800 --ondisk=/dev/sda"
	invalidSizePartitionCommand   = "part / --fstype=ext4 --size=abcd --ondisk=/dev/sda"

	validPartitionCommand1 = "part biosboot --fstype=biosboot --size=8 --ondisk=/dev/sda"
	validPartitionCommand2 = "part / --fstype=ext4 --size=800 --ondisk=/dev/sda"

	validTestParserDisk_OnePartition = Disk{
		PartitionTableType: "gpt",
		TargetDisk: TargetDisk{
			Type:  "path",
			Value: "/dev/sda",
		},
		Partitions: []Partition{
			{
				ID:     "Partition1",
				Flags: []PartitionFlag{
					"bios_grub",
				},
				Start:  1,
				End:    9,
				FsType: "fat32",
			},
		},
	}

	validTestParserDisk_TwoPartitions = Disk{
		PartitionTableType: "gpt",
		TargetDisk: TargetDisk{
			Type:  "path",
			Value: "/dev/sda",
		},
		Partitions: []Partition{
			{
				ID: "Partition1",
				Flags: []PartitionFlag{
					"bios_grub",
				},
				Start:  1,
				End:    9,
				FsType: "fat32",
			},
			{
				ID:     "Partition2",
				Start:  9,
				End:    809,
				FsType: "ext4",
			},
		},
	}

	validTestParserPartitionSettings = []PartitionSetting{
		{
			ID:              "Partition1",
			MountPoint:      "",
			MountIdentifier: GetDefaultMountIdentifier(),
		},
		{
			ID:              "Partition2",
			MountPoint:      "/",
			MountIdentifier: GetDefaultMountIdentifier(),
		},
	}
)

func TestShouldFailParsingInvalidOnDiskPartitionCommand(t *testing.T) {
	initializePrerequisitesForParser()

	err := parsePartitionFlags(invalidOnDiskPartitionCommand, 1)
	assert.Error(t, err)
	assert.Equal(t, onDiskInputErrorMsg, err.Error())
}

func TestShouldFailParsingInvalidFstypePartitionCommand(t *testing.T) {
	initializePrerequisitesForParser()

	err := parsePartitionFlags(invalidFstypePartitionCommand, 1)
	assert.Error(t, err)
	assert.Equal(t, fsTypeInputErrorMsg, err.Error())
}

func TestShouldFailParsingInvalidSizePartitionCommand(t *testing.T) {
	initializePrerequisitesForParser()

	err := parsePartitionFlags(invalidSizePartitionCommand, 1)
	assert.Error(t, err)
	assert.Equal(t, "strconv.ParseUint: parsing \"abcd\": invalid syntax", err.Error())
}

func TestShouldSucceedParsingOneValidPartitionCommand(t *testing.T) {
	initializePrerequisitesForParser()

	err := parsePartitionFlags(validPartitionCommand1, 1)
	assert.NoError(t, err)

	assert.Equal(t, validTestParserDisk_OnePartition, disks[0])
	assert.Equal(t, 1, len(disks))

	assert.Equal(t, validTestParserPartitionSettings[0], partitionSettings[0])
	assert.Equal(t, 1, len(partitionSettings))
}

func TestShouldSucceedParsingTwoValidPartitionCommands(t *testing.T) {
	initializePrerequisitesForParser()

	err := parsePartitionFlags(validPartitionCommand1, 1)
	assert.NoError(t, err)
	err = parsePartitionFlags(validPartitionCommand2, 2)
	assert.NoError(t, err)

	assert.Equal(t, validTestParserDisk_TwoPartitions, disks[0])
	assert.Equal(t, 1, len(disks))

	assert.Equal(t, validTestParserPartitionSettings[0], partitionSettings[0])
	assert.Equal(t, validTestParserPartitionSettings[1], partitionSettings[1])
	assert.Equal(t, 2, len(partitionSettings))
}
