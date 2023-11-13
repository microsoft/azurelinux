// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/ptrutils"
	"github.com/stretchr/testify/assert"
)

func TestPartitionIsValidExpanding(t *testing.T) {
	partition := Partition{
		ID:     "a",
		FsType: "ext4",
		Start:  0,
		End:    nil,
	}

	err := partition.IsValid()
	assert.NoError(t, err)
}

func TestPartitionIsValidFixedSize(t *testing.T) {
	partition := Partition{
		ID:     "a",
		FsType: "ext4",
		Start:  0,
		End:    ptrutils.PtrTo(uint64(1)),
	}

	err := partition.IsValid()
	assert.NoError(t, err)
}

func TestPartitionIsValidZeroSize(t *testing.T) {
	partition := Partition{
		ID:     "a",
		FsType: "ext4",
		Start:  0,
		End:    ptrutils.PtrTo(uint64(0)),
	}

	err := partition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "partition")
	assert.ErrorContains(t, err, "size")
}

func TestPartitionIsValidNegativeSize(t *testing.T) {
	partition := Partition{
		ID:     "a",
		FsType: "ext4",
		Start:  2,
		End:    ptrutils.PtrTo(uint64(1)),
	}

	err := partition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "partition")
	assert.ErrorContains(t, err, "size")
}

func TestPartitionIsValidGoodName(t *testing.T) {
	partition := Partition{
		ID:     "a",
		FsType: "ext4",
		Start:  0,
		End:    nil,
		Name:   "a",
	}

	err := partition.IsValid()
	assert.NoError(t, err)
}

func TestPartitionIsValidNameTooLong(t *testing.T) {
	partition := Partition{
		ID:     "a",
		FsType: "ext4",
		Start:  0,
		End:    nil,
		Name:   "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
	}

	err := partition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "name")
	assert.ErrorContains(t, err, "too long")
}

func TestPartitionIsValidNameNonASCII(t *testing.T) {
	partition := Partition{
		ID:     "a",
		FsType: "ext4",
		Start:  0,
		End:    nil,
		Name:   "❤️",
	}

	err := partition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "name")
	assert.ErrorContains(t, err, "ASCII")
}

func TestPartitionIsValidGoodFlag(t *testing.T) {
	partition := Partition{
		ID:     "a",
		FsType: "fat32",
		Start:  0,
		End:    nil,
		Flags:  []PartitionFlag{"esp"},
	}

	err := partition.IsValid()
	assert.NoError(t, err)
}

func TestPartitionIsValidBadFlag(t *testing.T) {
	partition := Partition{
		ID:     "a",
		FsType: "ext4",
		Start:  0,
		End:    nil,
		Flags:  []PartitionFlag{"a"},
	}

	err := partition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "PartitionFlag")
}

func TestPartitionIsValidUnsupportedFileSystem(t *testing.T) {
	partition := Partition{
		ID:     "a",
		FsType: "ntfs",
		Start:  0,
		End:    nil,
		Flags:  []PartitionFlag{"a"},
	}

	err := partition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "FileSystemType")
}

func TestPartitionIsValidBadEspFsType(t *testing.T) {
	partition := Partition{
		ID:     "a",
		FsType: "ext4",
		Start:  0,
		End:    nil,
		Flags:  []PartitionFlag{"esp"},
	}

	err := partition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "ESP")
	assert.ErrorContains(t, err, "fat32")
}

func TestPartitionIsValidBadBiosBootFsType(t *testing.T) {
	partition := Partition{
		ID:     "a",
		FsType: "ext4",
		Start:  1,
		End:    nil,
		Flags:  []PartitionFlag{"bios_grub"},
	}

	err := partition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "BIOS boot")
	assert.ErrorContains(t, err, "fat32")
}

func TestPartitionIsValidBadBiosBootStart(t *testing.T) {
	partition := Partition{
		ID:     "a",
		FsType: "ext4",
		Start:  2,
		End:    nil,
		Flags:  []PartitionFlag{"bios_grub"},
	}

	err := partition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "BIOS boot")
	assert.ErrorContains(t, err, "start")
}
