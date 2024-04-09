// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/ptrutils"
	"github.com/stretchr/testify/assert"
)

func TestPartitionIsValidExpanding(t *testing.T) {
	partition := Partition{
		Id:    "a",
		Start: 0,
	}

	err := partition.IsValid()
	assert.NoError(t, err)
}

func TestPartitionIsValidFixedSize(t *testing.T) {
	partition := Partition{
		Id:    "a",
		Start: 0,
		End:   ptrutils.PtrTo(DiskSize(1 * diskutils.MiB)),
	}

	err := partition.IsValid()
	assert.NoError(t, err)
}

func TestPartitionIsValidZeroSize(t *testing.T) {
	partition := Partition{
		Id:    "a",
		Start: 0,
		End:   ptrutils.PtrTo(DiskSize(0)),
	}

	err := partition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "partition")
	assert.ErrorContains(t, err, "size")
}

func TestPartitionIsValidZeroSizeV2(t *testing.T) {
	partition := Partition{
		Id:    "a",
		Start: 0,
		Size:  ptrutils.PtrTo(DiskSize(0)),
	}

	err := partition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "partition")
	assert.ErrorContains(t, err, "size")
}

func TestPartitionIsValidNegativeSize(t *testing.T) {
	partition := Partition{
		Id:    "a",
		Start: 2 * diskutils.MiB,
		End:   ptrutils.PtrTo(DiskSize(1 * diskutils.MiB)),
	}

	err := partition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "partition")
	assert.ErrorContains(t, err, "size")
}

func TestPartitionIsValidBothEndAndSize(t *testing.T) {
	partition := Partition{
		Id:    "a",
		Start: 2 * diskutils.MiB,
		End:   ptrutils.PtrTo(DiskSize(3 * diskutils.MiB)),
		Size:  ptrutils.PtrTo(DiskSize(1 * diskutils.MiB)),
	}

	err := partition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "end")
	assert.ErrorContains(t, err, "size")
}

func TestPartitionIsValidGoodName(t *testing.T) {
	partition := Partition{
		Id:    "a",
		Start: 0,
		End:   nil,
		Label: "a",
	}

	err := partition.IsValid()
	assert.NoError(t, err)
}

func TestPartitionIsValidNameTooLong(t *testing.T) {
	partition := Partition{
		Id:    "a",
		Start: 0,
		End:   nil,
		Label: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
	}

	err := partition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "name")
	assert.ErrorContains(t, err, "too long")
}

func TestPartitionIsValidNameNonASCII(t *testing.T) {
	partition := Partition{
		Id:    "a",
		Start: 0,
		End:   nil,
		Label: "❤️",
	}

	err := partition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "name")
	assert.ErrorContains(t, err, "ASCII")
}

func TestPartitionIsValidGoodType(t *testing.T) {
	partition := Partition{
		Id:    "a",
		Start: 0,
		End:   nil,
		Type:  PartitionTypeESP,
	}

	err := partition.IsValid()
	assert.NoError(t, err)
}

func TestPartitionIsValidBadType(t *testing.T) {
	partition := Partition{
		Id:    "a",
		Start: 0,
		End:   nil,
		Type:  PartitionType("a"),
	}

	err := partition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "unknown partition type")
}
