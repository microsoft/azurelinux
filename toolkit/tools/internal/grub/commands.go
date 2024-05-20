// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package grub

type Line struct {
	Tokens   []Token
	EndToken *Token
}

// Split the tokens into lines, using (unescaped) newlines and semicolons as separator tokens.
// Note: Technically this is incorrect, since some constructs (e.g. "then") supporting having the subsequent command on
// the same line. But to avoid needing to write a full parser, this code instead assumes that the grub config files are
// at least somewhat sensibly formatted.
func SplitTokensIntoLines(tokens []Token) []Line {
	lines := []Line(nil)
	lineTokens := []Token(nil)

	for i := range tokens {
		token := tokens[i]

		switch token.Type {
		case NEWLINE, SEMICOLON:
			if len(lineTokens) > 0 {
				line := Line{
					Tokens:   lineTokens,
					EndToken: &token,
				}
				lines = append(lines, line)
			}
			lineTokens = nil

		default:
			lineTokens = append(lineTokens, token)
		}
	}

	if len(lineTokens) > 0 {
		line := Line{
			Tokens:   lineTokens,
			EndToken: nil,
		}
		lines = append(lines, line)
	}

	return lines
}

// IsTokenKeyword checks if a token is keyword.
func IsTokenKeyword(token Token, keyword string) bool {
	return token.Type == WORD &&
		len(token.SubWords) == 1 &&
		token.SubWords[0].Type == KEYWORD_STRING &&
		token.SubWords[0].Value == keyword
}

// FindCommandAll looks for all the lines that contain a command with the provided name.
func FindCommandAll(lines []Line, command string) []Line {
	commandLines := []Line(nil)

	for _, line := range lines {
		if len(line.Tokens) >= 1 && IsTokenKeyword(line.Tokens[0], command) {
			commandLines = append(commandLines, line)
		}
	}

	return commandLines
}
