// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parses a grub config file into tokens.
// This handles proper interpretation of metacharacters, newlines, variable expansions, character escapes, single quoted
// strings, and double quoted strings. While this is not a full parser into an AST (abstract syntax tree), it is better
// than parsing the grub config files using regexes.

package grub

import (
	"fmt"
	"os"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/grub/filescanner"
)

func TokenizeGrubConfigFile(name string) ([]Token, error) {
	configContent, err := os.ReadFile(name)
	if err != nil {
		return nil, fmt.Errorf("failed to read grub config file:\n%w", err)
	}

	return TokenizeGrubConfig(string(configContent))
}

func TokenizeGrubConfig(configContent string) ([]Token, error) {
	scanner := filescanner.NewFileScanner(configContent)
	tokenizer := grubConfigTokenizer{
		scanner: scanner,
	}

	err := tokenizer.tokenize()
	if err != nil {
		return tokenizer.tokens, fmt.Errorf("failed to parse (tokenize) grub config file:\n%w", err)
	}

	return tokenizer.tokens, nil
}

type grubConfigTokenizer struct {
	scanner  *filescanner.FileScanner
	tokens   []Token
	subWords []SubWord
}

func (t *grubConfigTokenizer) tokenize() error {
	for {
		c, eof := t.scanner.Peek()
		if eof {
			break
		}

		switch c {
		// Metacharacters
		case '{', '}', '|', '&', ';', '<', '>', '\n':
			locStart := t.scanner.Loc()
			// Consume metacharacter
			t.scanner.Next()

			var tokenType TokenType
			switch c {
			case '{':
				tokenType = LBRACE
			case '}':
				tokenType = RBRACE
			case '|':
				tokenType = BAR
			case '&':
				tokenType = AND
			case ';':
				tokenType = SEMICOLON
			case '<':
				tokenType = LT
			case '>':
				tokenType = GT
			case '\n':
				tokenType = NEWLINE
			}

			token := t.newToken(locStart, t.scanner.Loc(), tokenType)
			t.tokens = append(t.tokens, token)

		// Space
		case ' ', '\t':
			err := t.parseSpace()
			if err != nil {
				return err
			}

		default:
			err := t.parseWord()
			if err != nil {
				return err
			}
		}

	}

	return nil
}

func (t *grubConfigTokenizer) parseWord() error {
	locStart := t.scanner.Loc()

	c, eof := t.scanner.Peek()
	if eof {
		return nil
	}

	// Check if the word starts with '#'.
	// Note: A '#' in the middle of a word doesn't start a comment.
	if c == '#' {
		err := t.parseComment()
		if err != nil {
			return err
		}

		return nil
	}

	var err error
	t.subWords = nil
	notFirst := false
loop:
	for {
		c, eof := t.scanner.Peek()
		if eof {
			break
		}

		switch c {
		// Metacharacters and spaces
		case '{', '}', '|', '&', ';', '<', '>', '\n', ' ', '\t':
			break loop

		// Double-quoted string
		case '"':
			err = t.parseDoubleQuotedString()
			if err != nil {
				break loop
			}

		// Single-quoted string
		case '\'':
			err = t.parseSingleQuotedString()
			if err != nil {
				break loop
			}

		// Variable expansion
		case '$':
			err = t.parseVariableExpansion(VAR_EXPANSION)
			if err != nil {
				break loop
			}

		// Unquoted string
		default:
			err = t.parseUnquotedString(notFirst)
			if err != nil {
				break loop
			}
		}

		notFirst = true
	}

	token := t.newToken(locStart, t.scanner.Loc(), WORD)
	token.SubWords = t.subWords
	t.subWords = nil
	t.tokens = append(t.tokens, token)
	return err
}

func (t *grubConfigTokenizer) parseSpace() error {
loop:
	for {
		c, eof := t.scanner.Peek()
		if eof {
			break loop
		}

		switch c {
		case ' ', '\t':
			t.scanner.Next()

		default:
			break loop
		}
	}

	return nil
}

func (t *grubConfigTokenizer) parseComment() error {
	// Consume the '#' char.
	t.scanner.Next()

loop:
	for {
		c, eof := t.scanner.Peek()
		if eof {
			break loop
		}

		switch c {
		case '\n':
			break loop

		default:
			t.scanner.Next()
		}
	}

	return nil
}

func (t *grubConfigTokenizer) parseUnquotedString(notFirst bool) error {
	locStart := t.scanner.Loc()

	sb := strings.Builder{}
loop:
	for {
		c, eof := t.scanner.Peek()
		if eof {
			break loop
		}

		switch c {
		case '{', '}', '|', '&', ';', '<', '>', ' ', '\t', '\n', '"', '\'', '$':
			break loop

		// Escape character
		case '\\':
			if !notFirst {
				notFirst = true

				// Add token for what was seen so far.
				locEnd := t.scanner.Loc()
				if locEnd.Index != locStart.Index {
					subWord := t.newSubWord(locStart, locEnd, KEYWORD_STRING, sb.String())
					t.subWords = append(t.subWords, subWord)
				}

				// Reset token
				locStart = t.scanner.Loc()
				sb = strings.Builder{}
			}

			// Consume \ char.
			t.scanner.Next()

			c, eof := t.scanner.Peek()
			if eof {
				// If the \ is the last character in the file, then the \ is preserved.
				sb.WriteRune('\\')
				break loop
			}

			switch c {
			case '\n':
				// Drop escaped newline character.

			default:
				// Write escaped character.
				sb.WriteRune(c)
			}

			t.scanner.Next()

		// Normal character
		default:
			sb.WriteRune(c)
			t.scanner.Next()
		}
	}

	tokenType := KEYWORD_STRING
	if notFirst {
		tokenType = STRING
	}

	subWord := t.newSubWord(locStart, t.scanner.Loc(), tokenType, sb.String())
	t.subWords = append(t.subWords, subWord)
	return nil
}

// Parse double-quoted string.
func (t *grubConfigTokenizer) parseDoubleQuotedString() error {
	locStart := t.scanner.Loc()

	// Consume " char.
	t.scanner.Next()

	sb := strings.Builder{}
loop:
	for {
		c, eof := t.scanner.Peek()
		if eof {
			return fmt.Errorf("unexpected end-of-file during double-quoted string (%d:%d)", t.scanner.Line(),
				t.scanner.Col())
		}

		switch c {
		// End of string
		case '"':
			// Consume " char.
			t.scanner.Next()
			break loop

		// Escape character
		case '\\':
			// Consume \ character.
			t.scanner.Next()

			c, eof := t.scanner.Peek()
			if eof {
				return fmt.Errorf("unexpected end-of-file after '\\' character (%d:%d)", t.scanner.Line(),
					t.scanner.Col())
			}

			switch c {
			// Within double-quoted strings, only some characters are valid escape sequences.
			case '$', '"', '\\':
				sb.WriteRune(c)

			case '\n':
				// Drop the escaped newline.

			default:
				// Invalid escape sequences preserve the '\' character.
				sb.WriteRune('\\')
				sb.WriteRune(c)
			}

			t.scanner.Next()

		// Variable expansion
		case '$':
			// Close out the current string token.
			locEnd := t.scanner.Loc()
			if locEnd.Index != locStart.Index {
				subWord := t.newSubWord(locStart, locEnd, STRING, sb.String())
				t.subWords = append(t.subWords, subWord)
			}

			// Parse the variable expansion.
			err := t.parseVariableExpansion(QUOTED_VAR_EXPANSION)
			if err != nil {
				return err
			}

			// Restart parsing the double-quoted string.
			locStart = t.scanner.Loc()
			sb = strings.Builder{}

		// Normal character
		default:
			sb.WriteRune(c)
			t.scanner.Next()
		}
	}

	subWord := t.newSubWord(locStart, t.scanner.Loc(), STRING, sb.String())
	t.subWords = append(t.subWords, subWord)
	return nil
}

// Parses single quoted string.
// Single quoted strings don't accept any character escapes and end at the first ' character.
func (t *grubConfigTokenizer) parseSingleQuotedString() error {
	locStart := t.scanner.Loc()

	// Consume ' char.
	t.scanner.Next()

	sb := strings.Builder{}
loop:
	for {
		c, eof := t.scanner.Peek()
		if eof {
			return fmt.Errorf("unexpected end-of-file during single-quoted string (%d:%d)", t.scanner.Line(),
				t.scanner.Col())
		}

		switch c {
		// End of string
		case '\'':
			// Consume ' char.
			t.scanner.Next()
			break loop

		// Normal character
		default:
			sb.WriteRune(c)
			t.scanner.Next()
		}
	}

	subWord := t.newSubWord(locStart, t.scanner.Loc(), STRING, sb.String())
	t.subWords = append(t.subWords, subWord)
	return nil
}

// Parses variable expansions.
// e.g. $a, ${a}
func (t *grubConfigTokenizer) parseVariableExpansion(subWordType SubWordType) error {
	locStart := t.scanner.Loc()

	// Consume $ char.
	t.scanner.Next()

	// Check if name is surrounded by braces.
	c, eof := t.scanner.Peek()
	usesBraces := false
	if !eof && c == '{' {
		usesBraces = true
		// Consume { char
		t.scanner.Next()
	}

	sb := strings.Builder{}
loop:
	for {
		c, eof := t.scanner.Peek()
		if eof {
			break loop
		}

		switch {
		// Name characters.
		case (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') || c == '_':
			sb.WriteRune(c)
			t.scanner.Next()

		default:
			break loop
		}
	}

	varName := sb.String()
	if usesBraces {
		c, eof := t.scanner.Peek()
		if eof {
			return fmt.Errorf("unexpected end-of-file while parsing variable expansion (%d:%d)", t.scanner.Line(),
				t.scanner.Col())
		}

		switch c {
		case '}':
			// Consume } char
			t.scanner.Next()

		default:
			return fmt.Errorf("missing } in variable expansion (%d:%d)", t.scanner.Line(), t.scanner.Col())
		}

		if varName == "" {
			return fmt.Errorf("variable expansion missing name (%d:%d)", locStart.Line, locStart.Col)
		}
	} else if varName == "" {
		// Name is invalid. So, $ is interpreted as a normal character.
		subWord := t.newSubWord(locStart, t.scanner.Loc(), STRING, "$")
		t.subWords = append(t.subWords, subWord)
		return nil
	}

	subWord := t.newSubWord(locStart, t.scanner.Loc(), subWordType, varName)
	t.subWords = append(t.subWords, subWord)
	return nil
}

func (t *grubConfigTokenizer) newToken(locStart, locEnd filescanner.SourceLoc, tokenType TokenType) Token {
	rawContentStart := locStart.Index
	rawContentEnd := locEnd.Index
	rawContent := t.scanner.Content()[rawContentStart:rawContentEnd]

	token := Token{
		Loc: SourceLoc{
			Start: locStart,
			End:   locEnd,
		},
		Type:       tokenType,
		RawContent: rawContent,
	}
	return token
}

func (t *grubConfigTokenizer) newSubWord(locStart, locEnd filescanner.SourceLoc, subWordType SubWordType, value string,
) SubWord {
	rawContentStart := locStart.Index
	rawContentEnd := locEnd.Index
	rawContent := t.scanner.Content()[rawContentStart:rawContentEnd]

	token := SubWord{
		Loc: SourceLoc{
			Start: locStart,
			End:   locEnd,
		},
		Type:       subWordType,
		RawContent: rawContent,
		Value:      value,
	}
	return token
}
