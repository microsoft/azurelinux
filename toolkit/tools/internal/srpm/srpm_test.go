// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package srpm

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	os.Exit(m.Run())
}

func TestShouldReturnArrayOfSpecs(t *testing.T) {
	inputSet := []string{
		"test-a",
	}
	var emptyInputSet []string
	specDir := "./testout"
	fileA := "test-a.spec"
	fileB := "test-b.spec"
	filepathA := filepath.Join(specDir, fileA)
	filepathB := filepath.Join(specDir, fileB)

	os.Mkdir(specDir, 0777)
	defer os.Remove(specDir)

	fileAPtr, err := os.Create(filepathA)
	assert.NoError(t, err)
	defer os.Remove(filepathA)
	defer fileAPtr.Close()

	fileBPtr, err := os.Create(filepathB)
	assert.NoError(t, err)
	defer os.Remove(filepathB)
	defer fileBPtr.Close()

	outputSlice, err := FindSPECFiles("./", inputSet)

	assert.NoError(t, err)
	assert.NotNil(t, outputSlice)
	assert.Len(t, outputSlice, 1)
	assert.Contains(t, outputSlice, filepathA)

	outputSlice, err = FindSPECFiles("./", emptyInputSet)
	assert.NoError(t, err)
	assert.NotNil(t, outputSlice)
	assert.Contains(t, outputSlice, filepathA)
	assert.Contains(t, outputSlice, filepathB)

}

func TestShouldFailMissingSpec(t *testing.T) {
	badInputSet := []string{
		"test-a",
	}
	specDir := "./"
	outputSlice, err := FindSPECFiles(specDir, badInputSet)
	assert.Error(t, err)
	assert.Equal(t, "unexpected number of matches (0) for spec file (test-a)", err.Error())
	assert.Nil(t, outputSlice)
}

func TestShouldParseFileForSpecs(t *testing.T) {
	d1 := []byte("test-a\ntest-b\ntest-a")
	specDir := "./testout"
	fileA := "packlist.txt"
	filepathA := filepath.Join(specDir, fileA)

	os.Mkdir(specDir, 0777)
	defer os.Remove(specDir)

	fileAPtr, err := os.Create(filepathA)
	assert.NoError(t, err)
	err = os.WriteFile(filepathA, d1, 0644)
	assert.NoError(t, err)
	defer os.Remove(filepathA)
	defer fileAPtr.Close()

	outputSlice, err := ParsePackListFile(filepathA)

	assert.NoError(t, err)
	assert.NotNil(t, outputSlice)
	assert.Len(t, outputSlice, 2)
	assert.Contains(t, outputSlice, "test-a")
	assert.Contains(t, outputSlice, "test-b")

}

func TestShouldFailEmptyPackList(t *testing.T) {
	d1 := []byte("")
	specDir := "./testout"
	fileA := "packlist.txt"
	filepathA := filepath.Join(specDir, fileA)

	os.Mkdir(specDir, 0777)
	defer os.Remove(specDir)

	fileAPtr, err := os.Create(filepathA)
	assert.NoError(t, err)
	err = os.WriteFile(filepathA, d1, 0644)
	assert.NoError(t, err)
	defer os.Remove(filepathA)
	defer fileAPtr.Close()

	outputSlice, err := ParsePackListFile(filepathA)

	assert.Error(t, err)
	assert.Equal(t, "cannot have empty pack list (testout/packlist.txt)", err.Error())
	assert.Nil(t, outputSlice)
}
