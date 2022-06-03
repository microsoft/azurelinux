// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

var (
	InvalidOnDiskPartitionCommand = "part / --fstype=ext4 --size=800 --ondisk="
	InvalidFstypePartitionCommand = "part / --fstype=     --size=800 --ondisk=/dev/sda"
	InvalidSizePartitionCommand   = "part / --fstype=ext4 --size=abcd --ondisk=/dev/sda"

	ValidPartitionCommand1 = "part / --fstype=ext4 --size=800 --ondisk=/dev/sda"
	ValidPartitionCommand2 = "part biosboot --fstype=biosboot --size=8 --ondisk=/dev/sda"

	validTestParserDisk_OnePartition = Disk{
		PartitionTableType: "mbr",
		TargetDisk: TargetDisk{
			Type:  "path",
			Value: "/dev/sda",
		},
		Partitions: []Partition{
			{
				ID:     "rootfs",
				Start:  1,
				End:    801,
				FsType: "ext4",
			},
		},
	}

	validTestParserDisk_TwoPartitions = Disk{
		PartitionTableType: "mbr",
		TargetDisk: TargetDisk{
			Type:  "path",
			Value: "/dev/sda",
		},
		Partitions: []Partition{
			{
				ID: "boot",
				Flags: []PartitionFlag{
					"bios_grub",
				},
				Start:  1,
				End:    9,
				FsType: "fat32",
			},
			{
				ID:     "rootfs",
				Start:  9,
				End:    809,
				FsType: "ext4",
			},
		},
	}

	validTestParserPartitionSettings = []PartitionSetting{
		{
			ID:              "boot",
			MountPoint:      "",
			MountIdentifier: GetDefaultMountIdentifier(),
		},
		{
			ID:              "rootfs",
			MountPoint:      "/",
			MountIdentifier: GetDefaultMountIdentifier(),
		},
	}
)

func TestShouldFailParsingInvalidOnDiskPartitionCommand(t *testing.T) {
	initializePrerequisitesForParser()

	err := parsePartitionFlags(InvalidOnDiskPartitionCommand)
	assert.Error(t, err)
	assert.Equal(t, onDiskInputErrorMsg, err.Error())
}

func TestShouldFailParsingInvalidFstypePartitionCommand(t *testing.T) {
	initializePrerequisitesForParser()

	err := parsePartitionFlags(InvalidFstypePartitionCommand)
	assert.Error(t, err)
	assert.Equal(t, fsTypeInputErrorMsg, err.Error())
}

func TestShouldFailParsingInvalidSizePartitionCommand(t *testing.T) {
	initializePrerequisitesForParser()

	err := parsePartitionFlags(InvalidSizePartitionCommand)
	assert.Error(t, err)
	assert.Equal(t, "strconv.ParseUint: parsing \"abcd\": invalid syntax", err.Error())
}

func TestShouldSucceedParsingOneValidPartitionCommand(t *testing.T) {
	initializePrerequisitesForParser()

	err := parsePartitionFlags(ValidPartitionCommand1)
	assert.NoError(t, err)

	assert.Equal(t, validTestParserDisk_OnePartition, disks[0])
	assert.Equal(t, 1, len(disks))

	assert.Equal(t, validTestParserPartitionSettings[1], partitionSettings[0])
	assert.Equal(t, 1, len(partitionSettings))
}

func TestShouldSucceedParsingTwoValidPartitionCommands(t *testing.T) {
	initializePrerequisitesForParser()

	err := parsePartitionFlags(ValidPartitionCommand2)
	assert.NoError(t, err)
	err = parsePartitionFlags(ValidPartitionCommand1)
	assert.NoError(t, err)

	assert.Equal(t, validTestParserDisk_TwoPartitions, disks[0])
	assert.Equal(t, 1, len(disks))

	assert.Equal(t, validTestParserPartitionSettings[0], partitionSettings[0])
	assert.Equal(t, validTestParserPartitionSettings[1], partitionSettings[1])
	assert.Equal(t, 2, len(partitionSettings))
}
