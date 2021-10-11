// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package rpm

import (
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
)

const sourceDir = "testdata"

var defines = map[string]string{
	"_sourcedir": "SPECS/dpdk",
	"dist":       ".cmX",
	"with_check": "1",
}

func TestShouldSucceedForSupportedArchitectures(t *testing.T) {
	specFilePath := filepath.Join(sourceDir, "supported_unsupported_architectures.spec")

	matches, err := SpecArchitectureMatchesBuild(specFilePath, sourceDir, defines)
	assert.NoError(t, err)
	assert.True(t, matches)
}

func TestShouldFailForUnsupportedArchitectures(t *testing.T) {
	specFilePath := filepath.Join(sourceDir, "unsupported_architectures.spec")

	matches, err := SpecArchitectureMatchesBuild(specFilePath, sourceDir, defines)
	assert.NoError(t, err)
	assert.False(t, matches)
}
