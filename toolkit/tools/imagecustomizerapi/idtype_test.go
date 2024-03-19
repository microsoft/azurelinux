// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestIdTypeIsValid(t *testing.T) {
	err := IdTypePartLabel.IsValid()
	assert.NoError(t, err)
}

func TestIdTypeIsValidBadValue(t *testing.T) {
	err := IdType("bad").IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid idType value")
}
