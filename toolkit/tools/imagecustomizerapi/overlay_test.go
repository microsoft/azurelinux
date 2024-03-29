// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestOverlayValidConfiguration(t *testing.T) {
	overlay := Overlay{
		LowerDir: "/lower",
		UpperDir: "/upper",
		WorkDir:  "/work",
		Partition: &IdentifiedPartition{
			IdType: "part-uuid",
			Id:     "123e4567-e89b-4d3a-a456-426614174000",
		},
	}

	err := overlay.IsValid()
	assert.NoError(t, err)
}

func TestOverlayInvalidEmptyLowerDir(t *testing.T) {
	overlay := Overlay{
		LowerDir: "",
		UpperDir: "/upper",
		WorkDir:  "/work",
	}

	err := overlay.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "path cannot be empty")
}

func TestOverlayInvalidSameUpperAndWorkDir(t *testing.T) {
	overlay := Overlay{
		LowerDir: "/lower",
		UpperDir: "/invalid/same",
		WorkDir:  "/invalid/same",
	}

	err := overlay.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "upperDir and workDir must be distinct")
}
