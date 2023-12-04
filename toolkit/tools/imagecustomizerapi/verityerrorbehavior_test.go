// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestVerityErrorBehaviorIsValid(t *testing.T) {
	err := VerityErrorBehaviorIgnore.IsValid()
	assert.NoError(t, err)
}

func TestVerityErrorBehaviorIsValidBadValue(t *testing.T) {
	err := VerityErrorBehavior("bad").IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid VerityErrorBehavior value")
}
