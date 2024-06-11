// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestScriptsIsValid(t *testing.T) {
	scripts := Scripts{
		PostCustomization: []Script{
			{
				Path: "a.sh",
			},
		},
		FinalizeCustomization: []Script{
			{
				Content: "echo hello",
			},
		},
	}
	err := scripts.IsValid()
	assert.NoError(t, err)
}

func TestScriptsInvalidPostCustomization(t *testing.T) {
	scripts := Scripts{
		PostCustomization: []Script{
			{},
		},
	}
	err := scripts.IsValid()
	assert.ErrorContains(t, err, "invalid postCustomization script at index 0")
	assert.ErrorContains(t, err, "either path or content must have a value")
}

func TestScriptsInvalidFinalizeCustomization(t *testing.T) {
	scripts := Scripts{
		FinalizeCustomization: []Script{
			{
				Path:    "a.sh",
				Content: "echo hello",
			},
		},
	}
	err := scripts.IsValid()
	assert.ErrorContains(t, err, "invalid finalizeCustomization script at index 0")
	assert.ErrorContains(t, err, "path and content may not both have a value")
}
