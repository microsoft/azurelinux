// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package grub

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/grub/filescanner"
)

// The type of a token.
type TokenType int

const (
	// The { symbol.
	LBRACE TokenType = iota
	// The } symbol.
	RBRACE
	// The | symbol.
	BAR
	// The & symbol.
	AND
	// The ; symbol.
	SEMICOLON
	// The < symbol.
	LT
	// The > symbol.
	GT
	// A newline.
	NEWLINE
	// A word.
	// Words are a catch-all for all other types of (valid) strings within a grub.cfg file.
	WORD
)

// The type of a subword.
type SubWordType int

const (
	// A string value that doesn't contain any character escaping, single quotes, or double quotes.
	// A word token with only a single sub-word of type KEYWORD_STRING is eligible to be a keyword.
	// For example, `if` is a keyword but `"if"` is not a keyword, even though both have the same string value.
	KEYWORD_STRING SubWordType = iota
	// A string value that may contain character escaping, single quotes, and/or double quotes.
	STRING
	// A variable expansion without double quotes (e.g. $a).
	// These types of variable expansions can technically produce new words, when the value contains space characters.
	// But there is no way to determine this without running the grub.cfg "script".
	VAR_EXPANSION
	// A variable expansion within double quotes (e.g. "$a").
	// These type of variable expansions cannot produce new words.
	QUOTED_VAR_EXPANSION
)

// The location of a token within the original grub.cfg file.
type SourceLoc struct {
	Start filescanner.SourceLoc
	End   filescanner.SourceLoc
}

// A single syntactical element within the grub.cfg file.
type Token struct {
	// Loc is the source location of the token.
	Loc SourceLoc
	// Type is the type of the token.
	Type TokenType
	// RawContent is the token as it appears in the grub file.
	RawContent string
	// When Type is WORD, contains the sub-words of the word.
	SubWords []SubWord
}

// Tokens that have the WORD type, are split up into smaller subwords.
type SubWord struct {
	// Loc is the source location of the token.
	Loc SourceLoc
	// Type is the type of the token.
	Type SubWordType
	// RawContent is the token as it appears in the grub file.
	RawContent string
	// Value
	Value string
}

func TokenTypeString(tokenType TokenType) string {
	switch tokenType {
	case LBRACE:
		return "LBRACE"
	case RBRACE:
		return "RBRACE"
	case BAR:
		return "BAR"
	case AND:
		return "AND"
	case SEMICOLON:
		return "SEMICOLON"
	case LT:
		return "LT"
	case GT:
		return "GT"
	case NEWLINE:
		return "NEWLINE"
	case WORD:
		return "WORD"
	default:
		return fmt.Sprintf("UNKNOWN(%d)", tokenType)
	}
}

func SubWordTypeString(subWordType SubWordType) string {
	switch subWordType {
	case KEYWORD_STRING:
		return "KEYWORD_STRING"
	case STRING:
		return "STRING"
	case VAR_EXPANSION:
		return "VAR_EXPANSION"
	case QUOTED_VAR_EXPANSION:
		return "QUOTED_VAR_EXPANSION"
	default:
		return fmt.Sprintf("UNKNOWN(%d)", subWordType)
	}
}
