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
	assert.ErrorContains(t, err, "invalid lowerDir ()")
	assert.ErrorContains(t, err, "path cannot be empty")
}

func TestOverlayInvalidInvalidWorkDir(t *testing.T) {
	overlay := Overlay{
		LowerDir: "/lower",
		UpperDir: "/upper",
		WorkDir:  " ",
	}

	err := overlay.IsValid()
	assert.ErrorContains(t, err, "invalid workDir ( )")
	assert.ErrorContains(t, err, "path ( ) contains spaces and is invalid")
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

func TestOverlayInvalidWorkDirSubsUpperDir(t *testing.T) {
	overlay := Overlay{
		LowerDir: "/lower",
		UpperDir: "/invalid",
		WorkDir:  "/invalid/same",
	}

	err := overlay.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "upperDir (/invalid) should not be a subdirectory of workDir (/invalid/same)")
}

func TestOverlayInvalidUpperDirSubsWorkDir(t *testing.T) {
	overlay := Overlay{
		LowerDir: "/lower",
		UpperDir: "/invalid/same",
		WorkDir:  "/invalid",
	}

	err := overlay.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "workDir (/invalid) should not be a subdirectory of upperDir (/invalid/same)")
}

func TestOverlayInvalidPartition(t *testing.T) {
	overlay := Overlay{
		LowerDir:  "/lower",
		UpperDir:  "/upper",
		WorkDir:   "/work",
		Partition: &IdentifiedPartition{},
	}

	err := overlay.IsValid()
	assert.ErrorContains(t, err, "invalid partition")
}
