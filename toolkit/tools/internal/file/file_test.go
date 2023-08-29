// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package file

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	retVal := m.Run()
	os.Exit(retVal)
}

func testFileName(t *testing.T) string {
	return filepath.Join(t.TempDir(), t.Name())
}

func TestRemoveFileIfExistsValid(t *testing.T) {
	// Create a file to remove
	err := Write("test", testFileName(t))
	assert.NoError(t, err)

	err = RemoveFileIfExists(testFileName(t))
	assert.NoError(t, err)
}

func TestRemoveFileDoesNotExist(t *testing.T) {
	err := RemoveFileIfExists(testFileName(t))
	assert.NoError(t, err)
}
