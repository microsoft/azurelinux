// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package sliceutils

import (
	"os"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	os.Exit(m.Run())
}

func TestPackageVersMapToSliceBoolShouldCreateEmptySliceFromNil(t *testing.T) {
	outputSlice := MapToSliceBool[*pkgjson.PackageVer](nil)

	assert.NotNil(t, outputSlice)
	assert.Empty(t, outputSlice)
}

func TestPackageVersMapToSliceBoolShouldCreateEmptySliceFromEmptyMap(t *testing.T) {
	outputSlice := MapToSliceBool(map[*pkgjson.PackageVer]bool{})

	assert.NotNil(t, outputSlice)
	assert.Empty(t, outputSlice)
}

func TestPackageVersMapToSliceBoolShouldReturnValuesForAllTrueElementsInMap(t *testing.T) {
	existingPackageVer := &pkgjson.PackageVer{Name: "A"}
	missingPackageVer := &pkgjson.PackageVer{Name: "X"}
	inputMap := map[*pkgjson.PackageVer]bool{
		existingPackageVer: true,
		missingPackageVer:  false,
	}
	outputSlice := MapToSliceBool(inputMap)

	assert.NotNil(t, outputSlice)
	assert.Len(t, outputSlice, 1)
	assert.Contains(t, outputSlice, existingPackageVer)
	assert.NotContains(t, outputSlice, missingPackageVer)
}

func TestPackageVersShouldMatch(t *testing.T) {
	packageVer1 := &pkgjson.PackageVer{Name: "A"}
	packageVer2 := &pkgjson.PackageVer{Name: "A"}

	assert.True(t, PackageVerMatch(packageVer1, packageVer2))
}

func TestPackageVersShouldNotMatch(t *testing.T) {
	packageVer1 := &pkgjson.PackageVer{Name: "A"}
	packageVer2 := &pkgjson.PackageVer{Name: "B"}

	assert.False(t, PackageVerMatch(packageVer1, packageVer2))
}

func TestPackageVerShouldNotMatchNil(t *testing.T) {
	packageVer1 := &pkgjson.PackageVer{Name: "A"}

	assert.False(t, PackageVerMatch(packageVer1, nil))
}

func TestStringShouldMatch(t *testing.T) {
	assert.True(t, StringMatch("A", "A"))
}

func TestStringShouldNotMatch(t *testing.T) {
	assert.False(t, StringMatch("A", "B"))
}

func TestStringShouldNotMatchForNilFirst(t *testing.T) {
	assert.False(t, StringMatch(nil, "A"))
}

func TestStringShouldNotMatchNilSecond(t *testing.T) {
	assert.False(t, StringMatch("A", nil))
}

func TestStringShouldMatchForNilInBoth(t *testing.T) {
	assert.True(t, StringMatch(nil, nil))
}

func TestStringsMapToSliceBoolShouldCreateEmptySliceFromNil(t *testing.T) {
	outputSlice := MapToSliceBool[string](nil)

	assert.NotNil(t, outputSlice)
	assert.Empty(t, outputSlice)
}

func TestStringsMapToSliceBoolShouldCreateEmptySliceFromEmptyMap(t *testing.T) {
	outputSlice := MapToSliceBool(map[string]bool{})

	assert.NotNil(t, outputSlice)
	assert.Empty(t, outputSlice)
}

func TestMapToSliceBoolShouldReturnValuesForAllTrueElementsInMap(t *testing.T) {
	inputMap := map[string]bool{
		"A": true,
		"B": true,
		"X": false,
		"Y": false,
	}
	outputSlice := MapToSliceBool(inputMap)

	assert.NotNil(t, outputSlice)
	assert.Len(t, outputSlice, 2)
	assert.Contains(t, outputSlice, "A")
	assert.Contains(t, outputSlice, "B")
	assert.NotContains(t, outputSlice, "X")
	assert.NotContains(t, outputSlice, "Y")
}

func TestSliceToMapBoolShouldCreateEmptyMapFromNil(t *testing.T) {
	outputMap := SliceToMapBool[string](nil)

	assert.NotNil(t, outputMap)
	assert.Empty(t, outputMap)
}

func TestSliceToMapBoolShouldCreateEmptyMapFromEmptySlice(t *testing.T) {
	outputMap := SliceToMapBool([]string{})

	assert.NotNil(t, outputMap)
	assert.Empty(t, outputMap)
}

func TestSliceToMapBoolShouldReturnValuesForAllElementsInSlice(t *testing.T) {
	inputSlice := []string{"A", "B", "C"}
	outputMap := SliceToMapBool(inputSlice)

	assert.NotNil(t, outputMap)
	assert.Len(t, outputMap, 3)
	assert.Contains(t, outputMap, "A")
	assert.Contains(t, outputMap, "B")
	assert.Contains(t, outputMap, "C")
	assert.NotContains(t, outputMap, "X")
}

func TestShouldRemoveDuplicates(t *testing.T) {
	inputSlice := []string{"A", "B", "C", "A", "B", "C"}
	outputSlice := RemoveDuplicatesFromSlice(inputSlice)

	assert.NotNil(t, outputSlice)
	assert.Len(t, outputSlice, 3)
	assert.Contains(t, outputSlice, "A")
	assert.Contains(t, outputSlice, "B")
	assert.Contains(t, outputSlice, "C")
	assert.NotContains(t, outputSlice, "X")
}
