// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestVerityIsValidInvalidPartLabel(t *testing.T) {
	validVerity := Verity{
		DataPartition: VerityPartition{
			IdType: "PartUuid",
			Id:     "0f2884c0-8fe0-4a19-87bf-286b7fe9d6f2",
		},
		HashPartition: VerityPartition{
			IdType: "PartLabel",
			Id:     "",
		},
	}

	err := validVerity.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid Id: empty string")
}

func TestVerityIsValidInvalidPartUuid(t *testing.T) {
	invalidVerity := Verity{
		DataPartition: VerityPartition{
			IdType: "PartUuid",
			Id:     "incorrect-uuid-format",
		},
		HashPartition: VerityPartition{
			IdType: "PartLabel",
			Id:     "hash_partition",
		},
	}

	err := invalidVerity.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid Id format")
}
