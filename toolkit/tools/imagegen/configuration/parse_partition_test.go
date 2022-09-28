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

	validLegacyBootPartitionCommand = "part biosboot --fstype=biosboot --size=8 --ondisk=/dev/sda"
	validUEFIBootPartitionCommand   = "part /boot/efi --fstype=efi --size=8 --ondisk=/dev/sda"
	validEFIPartitionCommand        = "part /boot --fstype=ext4 --size=512 --ondisk=/dev/sda"
	validPartitionCommand2          = "part / --fstype=ext4 --size=800 --ondisk=/dev/sda"

	validTestParserDisk_LegacyPartition = Disk{
		PartitionTableType: "mbr",
		TargetDisk: TargetDisk{
			Type:  "path",
			Value: "/dev/sda",
		},
		Partitions: []Partition{
			{
				ID: "Partition1",
				Flags: []PartitionFlag{
					"boot",
				},
				Start:  1,
				End:    9,
				FsType: "fat32",
			},
		},
	}

	validTestParserDisk_UEFIPartition = Disk{
		PartitionTableType: "gpt",
		TargetDisk: TargetDisk{
			Type:  "path",
			Value: "/dev/sda",
		},
		Partitions: []Partition{
			{
				ID: "Partition1",
				Flags: []PartitionFlag{
					"esp",
					"boot",
				},
				Start:  1,
				End:    9,
				FsType: "fat32",
			},
		},
	}

	validTestParserDisk_LegacyPartitions = Disk{
		PartitionTableType: "mbr",
		TargetDisk: TargetDisk{
			Type:  "path",
			Value: "/dev/sda",
		},
		Partitions: []Partition{
			{
				ID: "Partition1",
				Flags: []PartitionFlag{
					"boot",
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

	validTestParserDisk_UEFIPartitions = Disk{
		PartitionTableType: "gpt",
		TargetDisk: TargetDisk{
			Type:  "path",
			Value: "/dev/sda",
		},
		Partitions: []Partition{
			{
				ID: "Partition1",
				Flags: []PartitionFlag{
					"esp",
					"boot",
				},
				Start:  1,
				End:    9,
				FsType: "fat32",
			},
			{
				ID:     "Partition2",
				Start:  9,
				End:    521,
				FsType: "ext4",
			},
			{
				ID:     "Partition3",
				Start:  521,
				End:    1321,
				FsType: "ext4",
			},
		},
	}

	validTestParserPartitionSettings_LegacyPartitions = []PartitionSetting{
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

	validTestParserPartitionSettings_UEFIPartitions = []PartitionSetting{
		{
			ID:              "Partition1",
			MountPoint:      "/boot/efi",
			MountOptions:    "umask=0077,nodev",
			MountIdentifier: GetDefaultMountIdentifier(),
		},
		{
			ID:              "Partition2",
			MountPoint:      "/boot",
			MountIdentifier: GetDefaultMountIdentifier(),
		},
		{
			ID:              "Partition3",
			MountPoint:      "/",
			MountIdentifier: GetDefaultMountIdentifier(),
		},
	}
)

func TestShouldFailParsingInvalidOnDiskPartitionCommand(t *testing.T) {
	err := initializePrerequisitesForParser()
	assert.NoError(t, err)

	err = parsePartitionFlags(invalidOnDiskPartitionCommand, 1)
	assert.Error(t, err)
	assert.Equal(t, onDiskInputErrorMsg, err.Error())
}

func TestShouldFailParsingInvalidFstypePartitionCommand(t *testing.T) {
	err := initializePrerequisitesForParser()
	assert.NoError(t, err)

	err = parsePartitionFlags(invalidFstypePartitionCommand, 1)
	assert.Error(t, err)
	assert.Equal(t, fsTypeInputErrorMsg, err.Error())
}

func TestShouldFailParsingInvalidSizePartitionCommand(t *testing.T) {
	err := initializePrerequisitesForParser()
	assert.NoError(t, err)

	err = parsePartitionFlags(invalidSizePartitionCommand, 1)
	assert.Error(t, err)
	assert.Equal(t, "strconv.ParseUint: parsing \"abcd\": invalid syntax", err.Error())
}

func TestShouldSucceedParsingOneValidPartitionCommand(t *testing.T) {
	err := initializePrerequisitesForParser()
	assert.NoError(t, err)

	systemBootType := SystemBootType()

	if systemBootType == "efi" {
		err = parsePartitionFlags(validUEFIBootPartitionCommand, 1)
		assert.NoError(t, err)

		assert.Equal(t, validTestParserDisk_UEFIPartition, disks[0])
		assert.Equal(t, 1, len(disks))

		assert.Equal(t, validTestParserPartitionSettings_UEFIPartitions[0], partitionSettings[0])
		assert.Equal(t, 1, len(partitionSettings))
	}

	if systemBootType == "legacy" {
		err = parsePartitionFlags(validLegacyBootPartitionCommand, 1)
		assert.NoError(t, err)

		assert.Equal(t, validTestParserDisk_LegacyPartition, disks[0])
		assert.Equal(t, 1, len(disks))

		assert.Equal(t, validTestParserPartitionSettings_LegacyPartitions[0], partitionSettings[0])
		assert.Equal(t, 1, len(partitionSettings))
	}
}

func TestShouldSucceedParsingMultipleValidPartitionCommands(t *testing.T) {
	err := initializePrerequisitesForParser()
	assert.NoError(t, err)

	systemBootType := SystemBootType()

	if systemBootType == "efi" {
		err = parsePartitionFlags(validUEFIBootPartitionCommand, 1)
		assert.NoError(t, err)
		err = parsePartitionFlags(validEFIPartitionCommand, 2)
		assert.NoError(t, err)
		err = parsePartitionFlags(validPartitionCommand2, 3)
		assert.NoError(t, err)

		assert.Equal(t, validTestParserDisk_UEFIPartitions, disks[0])

		assert.Equal(t, validTestParserPartitionSettings_UEFIPartitions[0], partitionSettings[0])
		assert.Equal(t, validTestParserPartitionSettings_UEFIPartitions[1], partitionSettings[1])
		assert.Equal(t, validTestParserPartitionSettings_UEFIPartitions[2], partitionSettings[2])

		assert.Equal(t, 3, len(partitionSettings))
	}

	if systemBootType == "legacy" {
		err = parsePartitionFlags(validLegacyBootPartitionCommand, 1)
		assert.NoError(t, err)
		err = parsePartitionFlags(validPartitionCommand2, 2)
		assert.NoError(t, err)

		assert.Equal(t, validTestParserDisk_LegacyPartitions, disks[0])

		assert.Equal(t, validTestParserPartitionSettings_LegacyPartitions[0], partitionSettings[0])
		assert.Equal(t, validTestParserPartitionSettings_LegacyPartitions[1], partitionSettings[1])

		assert.Equal(t, 2, len(partitionSettings))
	}

	assert.Equal(t, 1, len(disks))
}
