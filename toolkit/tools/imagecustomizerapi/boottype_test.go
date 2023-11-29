// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestBootTypeIsValid(t *testing.T) {
	err := BootTypeEfi.IsValid()
	assert.NoError(t, err)
}

func TestBootTypeIsValidBadValue(t *testing.T) {
	err := BootType("bad").IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid BootType value")
}
