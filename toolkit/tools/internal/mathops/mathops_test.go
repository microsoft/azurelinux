// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package mathops

import (
	"math"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestAddIntsShouldAddSmallPositiveNumbers(t *testing.T) {
	result, err := AddInts(5, 10)
	assert.NoError(t, err)
	assert.Equal(t, 15, result)
}

func TestAddIntsShouldAddSmallNegativeNumbers(t *testing.T) {
	result, err := AddInts(-5, -10)
	assert.NoError(t, err)
	assert.Equal(t, -15, result)
}

func TestAddIntsShouldAddZeroToMaxInt(t *testing.T) {
	result, err := AddInts(math.MaxInt, 0)
	assert.NoError(t, err)
	assert.Equal(t, math.MaxInt, result)
}

func TestAddIntsShouldSubtractZeroFromMinInt(t *testing.T) {
	result, err := AddInts(math.MinInt, 0)
	assert.NoError(t, err)
	assert.Equal(t, math.MinInt, result)
}

func TestAddIntsShouldAddMinIntToMaxInt(t *testing.T) {
	result, err := AddInts(math.MinInt, math.MaxInt)
	assert.NoError(t, err)
	assert.Equal(t, -1, result)
}

func TestAddIntsShouldOverflow(t *testing.T) {
	result, err := AddInts(math.MaxInt, 1)
	assert.Error(t, err)
	assert.Equal(t, 0, result)
	assert.Equal(t, ErrOverflow, err)
}

func TestAddIntsShouldUnderflow(t *testing.T) {
	result, err := AddInts(math.MinInt, -1)
	assert.Error(t, err)
	assert.Equal(t, 0, result)
	assert.Equal(t, ErrUnderflow, err)
}
