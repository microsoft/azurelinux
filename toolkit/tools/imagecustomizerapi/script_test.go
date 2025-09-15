// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestScriptIsValid(t *testing.T) {
	script := Script{
		Path: "a.sh",
	}
	err := script.IsValid()
	assert.NoError(t, err)
}

func TestScriptIsValidBothPathAndContent(t *testing.T) {
	script := Script{
		Path:    "a.sh",
		Content: "echo hello",
	}
	err := script.IsValid()
	assert.ErrorContains(t, err, "path and content may not both have a value")
}
