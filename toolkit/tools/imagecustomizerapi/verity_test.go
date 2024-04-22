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
			IdType: "part-uuid",
			Id:     "incorrect-uuid-format",
		},
		HashPartition: IdentifiedPartition{
			IdType: "part-label",
			Id:     "hash_partition",
		},
	}

	err := invalidVerity.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid dataPartition")
}

func TestVerityIsValidInvalidHashPartition(t *testing.T) {
	invalidVerity := Verity{
		DataPartition: IdentifiedPartition{
			IdType: "part-uuid",
			Id:     "123e4567-e89b-4d3a-a456-426614174000",
		},
		HashPartition: IdentifiedPartition{
			IdType: "part-label",
			Id:     "",
		},
	}

	err := invalidVerity.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid hashPartition")
}

func TestVerityIsValid(t *testing.T) {
	panicOption := CorruptionOption("panic")

	validVerity := Verity{
		DataPartition: IdentifiedPartition{
			IdType: "part-uuid",
			Id:     "123e4567-e89b-4d3a-a456-426614174000",
		},
		HashPartition: IdentifiedPartition{
			IdType: "part-label",
			Id:     "hash_partition",
		},
		CorruptionOption: &panicOption,
	}

	err := validVerity.IsValid()
	assert.NoError(t, err)
}

func TestVerityIsValidInvalidCorruptionOption(t *testing.T) {
	badOption := CorruptionOption("bad")

	invalidVerity := Verity{
		DataPartition: IdentifiedPartition{
			IdType: "part-uuid",
			Id:     "123e4567-e89b-4d3a-a456-426614174000",
		},
		HashPartition: IdentifiedPartition{
			IdType: "part-label",
			Id:     "hash_partition",
		},
		CorruptionOption: &badOption,
	}

	err := invalidVerity.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid CorruptionOption value")
}
