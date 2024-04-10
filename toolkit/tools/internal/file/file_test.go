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
func TestRemoveDirectoryContents(t *testing.T) {
	// Create a temporary directory
	tempDir := t.TempDir()

	// Create some files and directories inside the temporary directory
	file1 := filepath.Join(tempDir, "file1.txt")
	file2 := filepath.Join(tempDir, "file2.txt")
	dir1 := filepath.Join(tempDir, "dir1")
	dir2 := filepath.Join(tempDir, "dir2")
	file3 := filepath.Join(dir1, "file3.txt")

	// Create the files and directories
	err := os.Mkdir(dir1, 0755)
	assert.NoError(t, err)
	err = os.Mkdir(dir2, 0755)
	assert.NoError(t, err)
	err = os.WriteFile(file1, []byte("test"), 0644)
	assert.NoError(t, err)
	err = os.WriteFile(file2, []byte("test"), 0644)
	assert.NoError(t, err)
	err = os.WriteFile(file3, []byte("test"), 0644)
	assert.NoError(t, err)

	// Call the function to remove the contents of the directory
	err = RemoveDirectoryContents(tempDir)
	assert.NoError(t, err)

	// Check if the files and directories have been removed
	exists, err := PathExists(file1)
	assert.NoError(t, err)
	assert.False(t, exists)

	exists, err = PathExists(file2)
	assert.NoError(t, err)
	assert.False(t, exists)

	exists, err = PathExists(dir1)
	assert.NoError(t, err)
	assert.False(t, exists)

	exists, err = PathExists(dir2)
	assert.NoError(t, err)
	assert.False(t, exists)

	exists, err = PathExists(file3)
	assert.NoError(t, err)
	assert.False(t, exists)

	// Ensure the directory itself is not removed
	exists, err = PathExists(tempDir)
	assert.NoError(t, err)
	assert.True(t, exists)
}

func TestRemoveDirectoryContentsEmpty(t *testing.T) {
	// Create a temporary directory
	tempDir := t.TempDir()

	// Call the function to remove the contents of the directory
	err := RemoveDirectoryContents(tempDir)
	assert.NoError(t, err)

	// Ensure the directory itself is not removed
	exists, err := PathExists(tempDir)
	assert.NoError(t, err)
	assert.True(t, exists)
}

func TestRemoveDirectoryContentsNonExistent(t *testing.T) {
	// Create a temporary directory
	tempDir := t.TempDir()

	// Remove the temporary directory
	err := os.RemoveAll(tempDir)
	assert.NoError(t, err)

	// Call the function to remove the contents of the directory
	err = RemoveDirectoryContents(tempDir)
	assert.Error(t, err)
}
