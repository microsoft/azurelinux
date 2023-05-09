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

func TestPackageVersSetToSliceShouldCreateEmptySliceFromNil(t *testing.T) {
	outputSlice := PackageVersSetToSlice(nil)

	assert.NotNil(t, outputSlice)
	assert.Empty(t, outputSlice)
}

func TestPackageVersSetToSliceShouldCreateEmptySliceFromEmptySet(t *testing.T) {
	outputSlice := PackageVersSetToSlice(map[*pkgjson.PackageVer]bool{})

	assert.NotNil(t, outputSlice)
	assert.Empty(t, outputSlice)
}

func TestPackageVersSetToSliceShouldReturnValuesForAllTrueElementsInSet(t *testing.T) {
	existingPackageVer := &pkgjson.PackageVer{Name: "A"}
	missingPackageVer := &pkgjson.PackageVer{Name: "X"}
	inputSet := map[*pkgjson.PackageVer]bool{
		existingPackageVer: true,
		missingPackageVer:  false,
	}
	outputSlice := PackageVersSetToSlice(inputSet)

	assert.NotNil(t, outputSlice)
	assert.Len(t, outputSlice, 2)
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

func TestStringsSetToSliceShouldCreateEmptySliceFromNil(t *testing.T) {
	outputSlice := StringsSetToSlice(nil)

	assert.NotNil(t, outputSlice)
	assert.Empty(t, outputSlice)
}

func TestStringsSetToSliceShouldCreateEmptySliceFromEmptySet(t *testing.T) {
	outputSlice := StringsSetToSlice(map[string]bool{})

	assert.NotNil(t, outputSlice)
	assert.Empty(t, outputSlice)
}

func TestStringsSetToSliceShouldReturnValuesForAllTrueElementsInSet(t *testing.T) {
	inputSet := map[string]bool{
		"A": true,
		"B": true,
		"X": false,
		"Y": false,
	}
	outputSlice := StringsSetToSlice(inputSet)

	assert.NotNil(t, outputSlice)
	assert.Len(t, outputSlice, 2)
	assert.Contains(t, outputSlice, "A")
	assert.Contains(t, outputSlice, "B")
	assert.NotContains(t, outputSlice, "X")
	assert.NotContains(t, outputSlice, "Y")
}
