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

	configsToTest := map[KernelExtraArguments]*string{
		// very simple cases (no quoting)
		"":        nil,
		"a":       nil,
		"a=b":     nil,
		"a=b x=y": nil,
		// enlosed in double quotes (4)
		"\"a=b\"": nil,
		// enclosed in single quotes (2)
		"'a=b'": nil,
		// single quote embedded within double quotes and vice versa (2)
		"\"a='b\" 'x=\"y'": nil,
		// single-quoted string embedded within a double quoted value (4)
		"\"'a=b' x=y\"": nil,
		// double-quoted string embedded within a double quoted value (4)(6)(7)
		"\"a=b \\\"x=y\\\"\"": nil,
		// \n embedded within a double quoted value (4)(6)
		"\"a=b x=y\\n\"": nil,
		// \ embedded within a double quoted value (4)(6)
		"\"a=b x=y\\\\\"": nil,
		// unmatched open double-quote - beginning of string (4)
		"\"a=b x=y": &missingClosingDoubleQuotes,
		// unmatched open double-quote - middle of string (4)
		"a=b \"x=y": &missingClosingDoubleQuotes,
		// unmatched open double-quote - end of string (4)
		"a=b x=y\"": &missingClosingDoubleQuotes,
		// unmatched open single-quote - beginning of string (2)
		"'a=b x=y": &missingClosingSingleQuote,
		// unmatched open single-quote - middle of string (2)
		"a=b 'x=y": &missingClosingSingleQuote,
		// unmatched open single-quote - end of string (2)
		"a=b x='y": &missingClosingSingleQuote,
		// attempt to use \ to escape single quotes (3)
		"'a=\\'b'": &missingClosingSingleQuote,
	}

	// testsOk := true
	for config, expectedErr := range configsToTest {
		err := config.IsValid()
		if expectedErr == nil {
			assert.NoError(t, err)
		} else {
			assert.Error(t, err)
			assert.ErrorContains(t, err, *expectedErr)
		}
	}
}
