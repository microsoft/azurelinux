// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestVerityPartitionIsValidValidPartUuidFormat(t *testing.T) {
	correctUuidPartition := VerityPartition{
		IdType: "PartUuid",
		Id:     "123e4567-e89b-12d3-a456-426614174000",
	}

	err := correctUuidPartition.IsValid()
	assert.NoError(t, err)
}

func TestVerityPartitionIsValidValidPartLabel(t *testing.T) {
	validPartition := VerityPartition{
		IdType: "PartLabel",
		Id:     "ValidLabelName",
	}

	err := validPartition.IsValid()
	assert.NoError(t, err)
}

func TestVerityPartitionIsValidInvalidPartLabel(t *testing.T) {
	invalidPartition := VerityPartition{
		IdType: "PartLabel",
		Id:     "",
	}

	err := invalidPartition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid Id: empty string")
}

func TestVerityPartitionIsValidInvalidEmptyPartUuid(t *testing.T) {
	emptyIdPartition := VerityPartition{
		IdType: "PartUuid",
		Id:     "",
	}

	err := emptyIdPartition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid Id: empty string")
}

func TestVerityPartitionIsValidInvalidPartUuidFormat(t *testing.T) {
	incorrectUuidPartition := VerityPartition{
		IdType: "PartUuid",
		Id:     "incorrect-uuid-format",
	}

	err := incorrectUuidPartition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid Id format")
}
