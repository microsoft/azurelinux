// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestIdentifiedPartitionIsValidValidPartUuidFormat(t *testing.T) {
	correctUuidPartition := IdentifiedPartition{
		IdType: "part-uuid",
		Id:     "123e4567-e89b-4d3a-a456-426614174000",
	}

	err := correctUuidPartition.IsValid()
	assert.NoError(t, err)
}

func TestIdentifiedPartitionIsValidValidPartLabel(t *testing.T) {
	validPartition := IdentifiedPartition{
		IdType: "part-label",
		Id:     "ValidLabelName",
	}

	err := validPartition.IsValid()
	assert.NoError(t, err)
}

func TestIdentifiedPartitionIsValidEmptyPartLabel(t *testing.T) {
	invalidPartition := IdentifiedPartition{
		IdType: "part-label",
		Id:     "",
	}

	err := invalidPartition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid id: empty string")
}

func TestIdentifiedPartitionIsValidInvalidEmptyPartUuid(t *testing.T) {
	emptyIdPartition := IdentifiedPartition{
		IdType: "part-uuid",
		Id:     "",
	}

	err := emptyIdPartition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid id: empty string")
}

func TestIdentifiedPartitionIsValidInvalidPartUuidFormat(t *testing.T) {
	incorrectUuidPartition := IdentifiedPartition{
		IdType: "part-uuid",
		Id:     "incorrect-uuid-format",
	}

	err := incorrectUuidPartition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid id format")
}

func TestIdentifiedPartitionIsValidInvalidIdType(t *testing.T) {
	incorrectUuidPartition := IdentifiedPartition{
		IdType: "cat",
		Id:     "incorrect-uuid-format",
	}

	err := incorrectUuidPartition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid idType")
	assert.ErrorContains(t, err, "invalid idType value (cat)")
}

func TestIdentifiedPartitionIsValidInvalidPartLabel(t *testing.T) {
	incorrectUuidPartition := IdentifiedPartition{
		IdType: IdTypePartLabel,
		Id:     "i ❤️ cats",
	}

	err := incorrectUuidPartition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid id format for part-label")
	assert.ErrorContains(t, err, "partition name (i ❤️ cats) contains a non-ASCII character (❤)")
}
