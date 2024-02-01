// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

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
