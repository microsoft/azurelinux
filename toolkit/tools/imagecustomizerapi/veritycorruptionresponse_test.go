// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestVerityCorruptionResponseIsValid(t *testing.T) {
	err := VerityCorruptionResponseIgnore.IsValid()
	assert.NoError(t, err)
}

func TestVerityCorruptionResponseIsValidBadValue(t *testing.T) {
	err := VerityCorruptionResponse("bad").IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid VerityCorruptionResponse value")
}
