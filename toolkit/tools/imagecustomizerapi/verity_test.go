// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestVerityIsValid(t *testing.T) {
	validVerity := Verity{
		DataPartition: VerityPartition{
			IdType: "PartUuid",
			Id:     "0f2884c0-8fe0-4a19-87bf-286b7fe9d6f2",
		},
		HashPartition: VerityPartition{
			IdType: "IdTypePartLabel",
			Id:     "hash_partition",
		},
	}

	err := validVerity.IsValid()
	assert.NoError(t, err)
}

func TestVerityIsInvalid(t *testing.T) {
	invalidVerity := Verity{
		DataPartition: VerityPartition{
			IdType: "PartUuid",
			Id:     "incorrect-uuid-format",
		},
		HashPartition: VerityPartition{
			IdType: "IdTypePartLabel",
			Id:     "",
		},
	}

	err := invalidVerity.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid Id")
}
