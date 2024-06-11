// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestResetBootLoaderTypeIsValidValid(t *testing.T) {
	err := ResetBootLoaderTypeHard.IsValid()
	assert.NoError(t, err)
}

func TestResetBootLoaderTypeIsValidInvalid(t *testing.T) {
	err := ResetBootLoaderType("aaa").IsValid()
	assert.ErrorContains(t, err, "invalid resetBootLoaderType value (aaa)")
}
