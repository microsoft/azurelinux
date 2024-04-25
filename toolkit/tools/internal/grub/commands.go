// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package grub

type Command struct {
	Name string
	Args []Token
}

// Split the tokens into lines, using (unescaped) newlines and semicolons as separator tokens.
// Note: Technically this is incorrect, since some constructs (e.g. "then") supporting having the subsequent command on
// the same line. But to avoid needing to write a full parser, this code instead assumes that the grub config files are
// at least somewhat sensibly formatted.
func SplitTokensIntoLines(tokens []Token) [][]Token {
	lines := [][]Token(nil)
	line := []Token(nil)

	for _, token := range tokens {
		switch token.Type {
		case NEWLINE, SEMICOLON:
			if len(line) > 0 {
				lines = append(lines, line)
			}
			line = nil

		default:
			line = append(line, token)
		}
	}

	if len(line) > 0 {
		lines = append(lines, line)
	}

	return lines
}

// Checks if a token is keyword.
func IsTokenKeyword(token Token, keyword string) bool {
	return token.Type == WORD &&
		len(token.SubWords) == 1 &&
		token.SubWords[0].Type == KEYWORD_STRING &&
		token.SubWords[0].Value == keyword
}

func FindCommandAll(lines [][]Token, command string) [][]Token {
	commandLines := [][]Token(nil)

	for _, line := range lines {
		if len(line) >= 1 && IsTokenKeyword(line[0], command) {
			commandLines = append(commandLines, line)
		}
	}

	return commandLines
}
