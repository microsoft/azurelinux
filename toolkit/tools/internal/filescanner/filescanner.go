// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package filescanner

import (
	"unicode/utf8"
)

// Iterator for scanning through a file a character (i.e. UTF-8 rune) at a time, while keeping track of the location
// (line and column) of each character.
type FileScanner struct {
	content   string
	col       int
	line      int
	index     int
	runeValue rune
	runeWidth int
}

type SourceLoc struct {
	Col   int
	Line  int
	Index int
}

func NewFileScanner(content string) *FileScanner {
	s := FileScanner{
		content: content,
		col:     1,
		line:    1,
		index:   0,
	}
	s.updateRune()
	return &s
}

func (s *FileScanner) Content() string {
	return s.content
}

func (s *FileScanner) Peek() (rune, bool) {
	return s.runeValue, s.Eof()
}

func (s *FileScanner) Next() bool {
	if s.runeValue == '\n' {
		s.line += 1
		s.col = 1
	} else {
		s.col += 1
	}

	s.index += s.runeWidth
	s.updateRune()

	return s.Eof()
}

func (s *FileScanner) Eof() bool {
	return s.index >= len(s.content)
}

func (s *FileScanner) Col() int {
	return s.col
}

func (s *FileScanner) Line() int {
	return s.line
}

func (s *FileScanner) Loc() SourceLoc {
	return SourceLoc{
		Col:   s.col,
		Line:  s.line,
		Index: s.index,
	}
}

func (s *FileScanner) updateRune() {
	s.runeValue, s.runeWidth = utf8.DecodeRuneInString(s.content[s.index:])
}
