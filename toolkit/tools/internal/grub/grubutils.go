// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package grub

import (
	"strings"
)

func RequiresQuotes(value string) bool {
	// Check a comment-like word or for any metacharacters.
	return strings.HasPrefix(value, "#") ||
		strings.ContainsAny(value, "{}|&;<> \t\n\"'$")
}

// Wraps the value in a double-quoted string, if it contains characters that require escaping.
func QuoteString(value string) string {
	if RequiresQuotes(value) {
		return ForceQuoteString(value)
	}
	return value
}

// Wraps the value in a double-quoted string.
func ForceQuoteString(value string) string {
	// Place value in a double quoted string.
	builder := strings.Builder{}
	builder.WriteRune('"')

	for _, char := range value {
		// Note: The characters that need to be escaped in a double-quoted string are different than the characters that
		// need to be escaped in an unquoted string.
		switch char {
		case '$', '"', '\\':
			// Escape character.
			builder.WriteRune('\\')
			builder.WriteRune(char)

		default:
			builder.WriteRune(char)
		}
	}

	builder.WriteRune('"')
	quotedValue := builder.String()
	return quotedValue
}
