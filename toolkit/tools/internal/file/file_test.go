// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package file

import (
	"fmt"
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

func TestCopyDir(t *testing.T) {
	workingDir, err := os.Getwd()
	if err != nil {
		logger.Log.Panicf("Failed to get working directory, error: %s", err)
	}
	testDir := filepath.Join(workingDir, "testdata")

	// Defining and creating src directory
	src := testDir + "/source"
	err = os.MkdirAll(src, os.ModePerm)
	assert.NoError(t, err)

	// Adding test files into src directory
	err = CreateTestFiles("testfile", src)
	assert.NoError(t, err)

	// Defining dst directory and copying src into dst
	dst := testDir + "/destination"
	err = CopyDir(src, dst)
	assert.NoError(t, err)

	// verifying the directories are equal
	equal, err := AreDirectoriesEqual(src, dst)
	assert.NoError(t, err)
	assert.True(t, equal)

	// Removing all test files and directories
	err = os.RemoveAll(testDir)
	assert.NoError(t, err)
}

func CreateTestFiles(filename string, outputDir string) error {
	// Test data
	testData := []byte{0x01, 0x02, 0x03, 0x04, 0x05}

	// Test file names
	outputFilepath1 := fmt.Sprintf("%s/%s.txt", outputDir, filename+"1")
	outputFilepath2 := fmt.Sprintf("%s/%s.txt", outputDir, filename+"2")
	err := os.MkdirAll(outputDir+"/innerTestDir", os.ModePerm)
	if err != nil {
		return err
	}
	outputFilepath3 := fmt.Sprintf("%s/innerTestDir/%s.txt", outputDir, filename+"3")

	// Write data to files
	err = os.WriteFile(outputFilepath1, testData, os.ModePerm)
	if err != nil {
		return err
	}
	err = os.WriteFile(outputFilepath2, testData, os.ModePerm)
	if err != nil {
		return err
	}
	err = os.WriteFile(outputFilepath3, testData, os.ModePerm)
	if err != nil {
		return err
	}
	logger.Log.Infof("Test files created: %s, %s, %s,", outputFilepath1, outputFilepath2, outputFilepath3)
	return nil
}

// AreDirectoriesEqual checks if two directories are equal based on their files.
func AreDirectoriesEqual(dir1, dir2 string) (bool, error) {
	files1, err := ListFiles(dir1)
	if err != nil {
		return false, err
	}

	files2, err := ListFiles(dir2)
	if err != nil {
		return false, err
	}

	if len(files1) != len(files2) {
		return false, nil
	}

	for i, file1 := range files1 {
		if file1 != files2[i] {
			return false, nil
		}
	}

	return true, nil
}

// ListFiles lists all files in a directory.
func ListFiles(dir string) ([]string, error) {
	var files []string

	err := filepath.Walk(dir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if !info.IsDir() {
			files = append(files, info.Name())
		}
		return nil
	})

	if err != nil {
		return nil, err
	}

	return files, nil
}
