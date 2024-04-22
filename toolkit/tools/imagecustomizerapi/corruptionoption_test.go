// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCorruptionOptionDefaultIsValid(t *testing.T) {
	err := CorruptionOptionDefault.IsValid()
	assert.NoError(t, err)
}

func TestCorruptionOptionPanicIsValid(t *testing.T) {
	err := CorruptionOptionPanic.IsValid()
	assert.NoError(t, err)
}

func TestCorruptionOptionIsValidBadValue(t *testing.T) {
	err := CorruptionOption("bad").IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid CorruptionOption value")
}
