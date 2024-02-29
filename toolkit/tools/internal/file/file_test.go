// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package file

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	retVal := m.Run()
	os.Exit(retVal)
}

// testFileName returns a file name in a temporary directory. This path will
// be different for EVERY call to this function.
func testFileName(t *testing.T) string {
	return filepath.Join(t.TempDir(), t.Name())
}

func TestRemoveFileIfExistsValid(t *testing.T) {
	fileName := testFileName(t)
	// Create a file to remove
	err := Write("test", fileName)
	assert.NoError(t, err)

	err = RemoveFileIfExists(fileName)
	assert.NoError(t, err)

	exists, err := PathExists(fileName)
	assert.NoError(t, err)
	assert.False(t, exists)
}

func TestRemoveFileDoesNotExist(t *testing.T) {
	fileName := testFileName(t)
	err := RemoveFileIfExists(fileName)
	assert.NoError(t, err)
}
