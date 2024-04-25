// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package grub

import (
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

const (
	// The directory that contains token tests.
	tokenTestsDir = "tokentests"
	// The directory that contains the output of the tests.
	// This is useful for comparing actual and expected results.
	tokenActualDir = "tokentests/actual"
)

func TestTokenizeGrubConfig(t *testing.T) {
	os.Mkdir(tokenActualDir, os.ModePerm)

	testFiles, err := os.ReadDir(tokenTestsDir)
	if !assert.NoError(t, err) {
		return
	}

	// Iterate through the list of files with the '.test' extension.
	for _, testFile := range testFiles {
		if filepath.Ext(testFile.Name()) != ".test" {
			continue
		}

		testName := strings.TrimSuffix(testFile.Name(), ".test")

		// Tokenize the test file.
		tokens, err := TokenizeGrubConfigFile(filepath.Join(tokenTestsDir, testFile.Name()))

		// Produce a string representation of the result.
		actual := tokenGrubConfigResultString(tokens, err)

		// Write out the actual result to file.
		err = os.WriteFile(filepath.Join(tokenActualDir, testName+".result"), []byte(actual), os.ModePerm)
		assert.NoErrorf(t, err, "[%s] Write actual file", testName)

		// Compare the actual and expected results.
		expected, err := os.ReadFile(filepath.Join(tokenTestsDir, testName+".result"))
		if assert.NoErrorf(t, err, "[%s] Read expected file", testName) {
			assert.Equal(t, string(expected), actual)
		}
	}
}

// Produce a string representation of the results of a TokenizeGrubConfigFile() call.
// This allows the representation to be a lot more compact than the equivalent Go representation.
func tokenGrubConfigResultString(tokens []Token, err error) string {
	sb := strings.Builder{}

	sb.WriteString(fmt.Sprintf("Error:\n%v\n\n", err))
	sb.WriteString("Tokens:\n")

	for _, token := range tokens {
		sb.WriteString(fmt.Sprintf("%s[%d:%d-%d:%d][%d-%d]\n", TokenTypeString(token.Type),
			token.Loc.Start.Line, token.Loc.Start.Col, token.Loc.End.Line, token.Loc.End.Col,
			token.Loc.Start.Index, token.Loc.End.Index))

		for _, subWord := range token.SubWords {
			sb.WriteString(fmt.Sprintf("  %s[%d:%d-%d:%d][%d-%d](%s)\n", SubWordTypeString(subWord.Type),
				subWord.Loc.Start.Line, subWord.Loc.Start.Col, subWord.Loc.End.Line, subWord.Loc.End.Col,
				subWord.Loc.Start.Index, subWord.Loc.End.Index, strconv.Quote(subWord.Value)))
		}
	}

	return sb.String()
}
