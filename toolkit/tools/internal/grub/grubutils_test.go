// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package grub

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestQuoteStringNoQuote(t *testing.T) {
	value := "hello"
	result := QuoteString(value)
	assert.Equal(t, value, result)
}

func TestQuoteStringCommentLike(t *testing.T) {
	value := "#hello"
	result := QuoteString(value)
	assert.Equal(t, "\"#hello\"", result)
}

func TestQuoteStringSpecialChar(t *testing.T) {
	value := ";"
	result := QuoteString(value)
	assert.Equal(t, "\";\"", result)
}

func TestQuoteStringNesting(t *testing.T) {
	value := "\\\""
	result := QuoteString(value)
	assert.Equal(t, "\"\\\\\\\"\"", result)
}
