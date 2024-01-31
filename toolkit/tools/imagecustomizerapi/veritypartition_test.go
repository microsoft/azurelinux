// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestVerityPartitionIsValid_PartUuid_Valid(t *testing.T) {
	validPartition := VerityPartition{
		IdType: IdTypePartUuid,
		Id:     "0f2884c0-8fe0-4a19-87bf-286b7fe9d6f2",
	}

	err := validPartition.IsValid()
	assert.NoError(t, err)
}

func TestVerityPartitionIsValid_EmptyId_Invalid(t *testing.T) {
	emptyIdPartition := VerityPartition{
		IdType: IdTypePartUuid,
		Id:     "",
	}

	err := emptyIdPartition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid Id")
}

func TestVerityPartitionIsValid_IncorrectUuidFormat_Invalid(t *testing.T) {
	incorrectUuidPartition := VerityPartition{
		IdType: IdTypePartUuid,
		Id:     "incorrect-uuid-format",
	}

	err := incorrectUuidPartition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid Id format")
}
