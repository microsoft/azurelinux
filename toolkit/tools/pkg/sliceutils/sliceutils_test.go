// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package sliceutils

import (
	"os"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/logger"
	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	os.Exit(m.Run())
}

func TestShouldCreateEmptySliceFromNil(t *testing.T) {
	outputSlice := StringsSetToSlice(nil)

	assert.NotNil(t, outputSlice)
	assert.Empty(t, outputSlice)
}

func TestShouldCreateEmptySliceFromEmptySet(t *testing.T) {
	outputSlice := StringsSetToSlice(map[string]bool{})

	assert.NotNil(t, outputSlice)
	assert.Empty(t, outputSlice)
}

func TestShouldReturnValuesForAllTrueElementsInSet(t *testing.T) {
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
