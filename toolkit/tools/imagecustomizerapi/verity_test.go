// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestVerityIsValid(t *testing.T) {
	validVerity := Verity{
		Id:               "root",
		Name:             "root",
		DataDeviceId:     "root",
		HashDeviceId:     "roothash",
		CorruptionOption: CorruptionOption("panic"),
	}

	err := validVerity.IsValid()
	assert.NoError(t, err)
}

func TestVerityIsValidMissingId(t *testing.T) {
	invalidVerity := Verity{
		Name:         "root",
		DataDeviceId: "root",
		HashDeviceId: "roothash",
	}

	err := invalidVerity.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "'id' may not be empty")
}

func TestVerityIsValidInvalidName(t *testing.T) {
	invalidVerity := Verity{
		Id:           "root",
		Name:         "$root",
		DataDeviceId: "root",
		HashDeviceId: "roothash",
	}

	err := invalidVerity.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid 'name' value ($root)")
}

func TestVerityIsValidMissingDataDeviceId(t *testing.T) {
	invalidVerity := Verity{
		Id:           "root",
		Name:         "root",
		HashDeviceId: "roothash",
	}

	err := invalidVerity.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "'dataDeviceId' may not be empty")
}

func TestVerityIsValidMissingHashDeviceId(t *testing.T) {
	invalidVerity := Verity{
		Id:           "root",
		Name:         "root",
		DataDeviceId: "root",
	}

	err := invalidVerity.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "'hashDeviceId' may not be empty")
}

func TestVerityIsValidInvalidCorruptionOption(t *testing.T) {
	invalidVerity := Verity{
		Id:               "root",
		Name:             "root",
		DataDeviceId:     "root",
		HashDeviceId:     "roothash",
		CorruptionOption: CorruptionOption("bad"),
	}

	err := invalidVerity.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid CorruptionOption value")
}
