// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestServicesIsValid(t *testing.T) {
	services := Services{
		Enable: []string{
			"nbd",
		},
	}

	err := services.IsValid()
	assert.NoError(t, err)
}

func TestServicesIsValidInvalidName(t *testing.T) {
	services := Services{
		Disable: []string{
			"",
		},
	}

	err := services.IsValid()
	assert.ErrorContains(t, err, "invalid service disable at index (0)")
	assert.ErrorContains(t, err, "name of service may not be empty")
}
