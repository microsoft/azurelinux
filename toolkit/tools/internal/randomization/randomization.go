// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package randomization

import (
	"crypto/rand"
	"fmt"
	"math/big"
	"strings"
)

const (
	// LegalCharactersAlphaNum is the set of legal characters for generating random alphanumeric strings
	LegalCharactersAlphaNum = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	// LegalCharactersHex is the set of legal characters for generating random hexadecimal strings
	LegalCharactersHex = "0123456789abcdef"
)

// RandomString generates a random string consisting of "length" runes
// randomly selected from the provided legalCharacters.  crypto.rand is more secure
// than math.rand and does not need to be seeded.
func RandomString(length int, legalCharacters string) (output string, err error) {
	builder := strings.Builder{}
	legalRunes := []rune(legalCharacters)
	// Max index is length of the valid runes. rand.Int() returns values in the range [0, max),
	// i.e. exclusive. So for "abcd", we want max = 4, so rand.Int() can return indices {0,1,2,3}
	maxIdx := big.NewInt((int64)(len(legalRunes)))

	if maxIdx.Int64() <= 0 {
		err = fmt.Errorf("legalCharacters may not be empty string")
		return
	}

	for i := 0; i < length; i++ {
		// Randomly select one of the characters in legalRunes to add to the string
		var randIdx *big.Int
		randIdx, err = rand.Int(rand.Reader, maxIdx)
		if err != nil {
			return
		}
		randomRune := legalRunes[randIdx.Int64()]
		builder.WriteString(string(randomRune))
	}

	output = builder.String()
	return
}
