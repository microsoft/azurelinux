// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestKernelExtraArgumentsIsValid(t *testing.T) {
	/*
		The following test cases are based on the 'quoting' section in grub
		documentation: https://www.gnu.org/software/grub/manual/grub/grub.html#Quoting

		Here is a copy for convenience along with section numbers to be associated
		with test cases:

		There are three quoting mechanisms: the escape character, single quotes, and
		double quotes.

		(1)
		A non-quoted backslash (\) is the escape character. It preserves the literal
		value of the next character that follows, with the exception of newline.

		(2)
		Enclosing characters in single quotes preserves the literal value of each
		character within the quotes.

		(3)
		A single quote may not occur between single
		quotes, even when preceded by a backslash.

		(4)
		Enclosing characters in double quotes preserves the literal value of all
		characters within the quotes, with the exception of ‘$’ and ‘\’.

		(5)
		The ‘$’ character retains its special meaning within double quotes.

		(6)
		The backslash retains its special meaning only when followed by one of the
		following characters: ‘$’, ‘"’, ‘\’, or newline. A backslash-newline pair is
		treated as a line continuation (that is, it is removed from the input stream
		and effectively ignored.

		(7)
		A double quote may be quoted within double quotes by preceding it with a
		backslash.
	*/

	missingClosingDoubleQuotes := "invalid double-quoted string: missing closing double-quotes"
	missingClosingSingleQuote := "invalid single-quoted string: missing closing single-quote"

	configsToTest := []struct {
		config      KernelExtraArguments
		expectedErr *string
	}{
		// Simple cases (no quoting)
		{KernelExtraArguments{""}, nil},
		{KernelExtraArguments{"a"}, nil},
		{KernelExtraArguments{"a=b"}, nil},
		{KernelExtraArguments{"a=b", "x=y"}, nil},

		// Enclosed in double quotes
		{KernelExtraArguments{"\"a=b\""}, nil},

		// Enclosed in single quotes
		{KernelExtraArguments{"'a=b'"}, nil},

		// Single quote embedded within double quotes and vice versa
		{KernelExtraArguments{"\"a='b\" 'x=\"y'"}, nil},

		// Single-quoted string embedded within a double-quoted value
		{KernelExtraArguments{"\"'a=b'", "x=y\""}, nil},

		// Double-quoted string embedded within a double-quoted value
		{KernelExtraArguments{"\"a=b", "\\\"x=y\\\"\""}, nil},

		// \n embedded within a double-quoted value
		{KernelExtraArguments{"\"a=b", "x=y\\n\""}, nil},

		// \ embedded within a double-quoted value
		{KernelExtraArguments{"\"a=b", "x=y\\\\\""}, nil},

		// Unmatched open double-quote - beginning of string
		{KernelExtraArguments{"\"a=b", "x=y"}, &missingClosingDoubleQuotes},

		// Unmatched open double-quote - middle of string
		{KernelExtraArguments{"a=b", "\"x=y"}, &missingClosingDoubleQuotes},

		// Unmatched open double-quote - end of string
		{KernelExtraArguments{"a=b", "x=y\""}, &missingClosingDoubleQuotes},

		// Unmatched open single-quote - beginning of string
		{KernelExtraArguments{"'a=b", "x=y"}, &missingClosingSingleQuote},

		// Unmatched open single-quote - middle of string
		{KernelExtraArguments{"a=b", "'x=y"}, &missingClosingSingleQuote},

		// Unmatched open single-quote - end of string
		{KernelExtraArguments{"a=b", "x='y"}, &missingClosingSingleQuote},

		// Attempt to use \ to escape single quotes
		{KernelExtraArguments{"'a=\\'b'"}, &missingClosingSingleQuote},
	}

	for _, test := range configsToTest {
		err := test.config.IsValid()
		if test.expectedErr == nil {
			assert.NoError(t, err)
		} else {
			assert.Error(t, err)
			assert.ErrorContains(t, err, *test.expectedErr)
		}
	}
}
