// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package rpm

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"microsoft.com/pkggen/internal/logger"
)

const specsDir = "testdata"

var defines = map[string]string{
	"dist":       ".cmX",
	"with_check": "1",
}

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	os.Exit(m.Run())
}

func TestShouldSucceedForSupportedArchitectures(t *testing.T) {
	specFilePath := filepath.Join(specsDir, "supported_unsupported_architectures.spec")

	matches, err := SpecExclusiveArchIsCompatible(specFilePath, specsDir, defines)
	assert.NoError(t, err)
	assert.True(t, matches)
}

func TestShouldSucceedForNoExclusiveArch(t *testing.T) {
	specFilePath := filepath.Join(specsDir, "no_exclusive_architecture.spec")

	matches, err := SpecExclusiveArchIsCompatible(specFilePath, specsDir, defines)
	assert.NoError(t, err)
	assert.True(t, matches)
}

func TestShouldFailForUnsupportedArchitectures(t *testing.T) {
	specFilePath := filepath.Join(specsDir, "unsupported_architectures.spec")

	matches, err := SpecExclusiveArchIsCompatible(specFilePath, specsDir, defines)
	assert.NoError(t, err)
	assert.False(t, matches)
}
