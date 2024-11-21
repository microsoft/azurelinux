// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestIdentifiedPartitionIsValidValidPartUuidFormat(t *testing.T) {
	correctUuidPartition := IdentifiedPartition{
		IdType: "PartUuid",
		Id:     "123e4567-e89b-4d3a-a456-426614174000",
	}

	err := correctUuidPartition.IsValid()
	assert.NoError(t, err)
}

func TestIdentifiedPartitionIsValidValidPartLabel(t *testing.T) {
	validPartition := IdentifiedPartition{
		IdType: "PartLabel",
		Id:     "ValidLabelName",
	}

	err := validPartition.IsValid()
	assert.NoError(t, err)
}

func TestIdentifiedPartitionIsValidInvalidPartLabel(t *testing.T) {
	invalidPartition := IdentifiedPartition{
		IdType: "PartLabel",
		Id:     "",
	}

	err := invalidPartition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid Id: empty string")
}

func TestIdentifiedPartitionIsValidInvalidEmptyPartUuid(t *testing.T) {
	emptyIdPartition := IdentifiedPartition{
		IdType: "PartUuid",
		Id:     "",
	}

	err := emptyIdPartition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid Id: empty string")
}

func TestIdentifiedPartitionIsValidInvalidPartUuidFormat(t *testing.T) {
	incorrectUuidPartition := IdentifiedPartition{
		IdType: "PartUuid",
		Id:     "incorrect-uuid-format",
	}

	err := incorrectUuidPartition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid Id format")
}
