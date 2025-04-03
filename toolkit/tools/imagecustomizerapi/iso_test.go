// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestIsoIsValid(t *testing.T) {
	iso := Iso{
		KernelCommandLine: KernelCommandLine{
			ExtraCommandLine: "'",
		},
	}

	err := iso.IsValid()
	assert.ErrorContains(t, err, "invalid kernelCommandLine")
}
