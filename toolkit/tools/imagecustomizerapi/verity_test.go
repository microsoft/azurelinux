// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestVerityIsValidInvalidDataPartition(t *testing.T) {
	invalidVerity := Verity{
		DataPartition: IdentifiedPartition{
			IdType: "PartUuid",
			Id:     "incorrect-uuid-format",
		},
		HashPartition: IdentifiedPartition{
			IdType: "PartLabel",
			Id:     "hash_partition",
		},
	}

	err := invalidVerity.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid DataPartition")
}

func TestVerityIsValidInvalidHashPartition(t *testing.T) {
	invalidVerity := Verity{
		DataPartition: IdentifiedPartition{
			IdType: "PartUuid",
			Id:     "123e4567-e89b-4d3a-a456-426614174000",
		},
		HashPartition: IdentifiedPartition{
			IdType: "PartLabel",
			Id:     "",
		},
	}

	err := invalidVerity.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid HashPartition")
}
