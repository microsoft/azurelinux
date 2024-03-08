// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package randomization

import (
	"math"
	"math/big"
	"os"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"gonum.org/v1/gonum/stat/distuv"
)

const (
	normalString                    = "abcde12345"
	multiByteString                 = "世界您好IsHelloWorld"
	emojiString                     = "1🤷‍♂️2@3( •_•)>⌐■~■ab~52(⌐■_■)67👩‍💻"
	maxAllowableFailureRate float64 = 1e-100 // Max allowable probability of failure
)

func TestMain(m *testing.M) {
	testResult := 0

	testResult = m.Run()

	os.Exit(testResult)
}

// Check if we are running enough trials to satisfy our probability threshold
// This is an approximation based on a binomial distribution. It slightly over-estimates the failure rates of the test
// which is acceptable here (~3% error).
func checkSufficientTrials(lenInputString, lenOutputString int) (isSufficientTrials bool, probabilityOfTrialFailing *big.Float) {
	// What is the probability we always roll less than (expected # of char) / 2?
	// ie 100/10 = 10, 10/2 = 5, make sure every character shows up at least 5 times
	minimumNumberOfOccurrences := (lenOutputString / lenInputString) / 2

	// Sum the probabilities of rolling 0,1,2,3,...(minimumNumberOfOccurrences-1) of any given character
	// i.e. the cumulative distribution function (CDF) of a binomial distribution
	distribution := distuv.Binomial{N: (float64)(lenOutputString), P: (1.0 / (float64)(lenInputString))}
	probabilityOfSingleCharFailure := big.NewFloat(distribution.CDF((float64)(minimumNumberOfOccurrences - 1)))

	// This probability is for one character, we could fail ANY of the characters...
	// i.e. Probability of rolling a 6 less than 3 times out of 10 rolls.
	// Need the probability of rolling any result less than 3 times out of 10 rolls.
	probabilityOfTrialFailing = big.NewFloat(1.0)
	probabilityOfTrialFailing.Mul(probabilityOfSingleCharFailure, big.NewFloat((float64)(lenInputString)))

	isSufficientTrials = probabilityOfTrialFailing.Cmp(big.NewFloat(maxAllowableFailureRate)) < 0
	return
}

// Generate a random string and validate that on the strings contain
// roughly the expected number of each character. Also make sure there are no
// unexpected characters included in the string. With a long enough string the chance of
// the test failing is vanishingly small (recommend at least 100000).
func runTrials(inputString string, length int, t *testing.T) {
	// Heuristic to check we are getting a "roughly" random distribution:
	// Generate random strings, check if each character is used at least an (average / 2) number of times at some point during the trials
	// ie 100/10 = 10, 10/2 = 5, make sure every character shows up at least 5 times at least once during the repeated trials

	enoughTrials, probOfFailure := checkSufficientTrials(len([]rune(inputString)), length)
	if !enoughTrials {
		assert.FailNowf(t, "Insufficient string length", "Require more than (%d) characters to reach required threshold (Probability of failure is: %v, we want: %v)", length, probOfFailure.String(), maxAllowableFailureRate)
	}

	randomString, err := RandomString(length, inputString)
	assert.NoError(t, err)
	// We need to count runes, not bytes, since there are multi-byte characters possible
	assert.Equal(t, length, len([]rune(randomString)))

	expectedCount := (length / len(inputString)) / 2
	for _, c := range inputString {
		count := strings.Count(randomString, string(c))
		assert.Truef(t, count > expectedCount, "Char (%c) from (%s) did not show up expected number of times in random string (found (%d), expected (%d))", c, randomString, count, expectedCount)
	}

	// Make sure we only have runes from the input string in our output
	for i, c := range randomString {
		if !strings.Contains(inputString, string(c)) {
			assert.FailNowf(t, "Illegal character in return", "Random string (%s) contained an unexpected character (%c) at index (%d) not found in set (%s)", randomString, c, i, inputString)
		}
	}
}

func TestRandomNoNormalStringError(t *testing.T) {
	var (
		inputString = normalString
		length      = 100000
	)
	runTrials(inputString, length, t)
}

func TestRandomNoMultiByteStringError(t *testing.T) {
	var (
		inputString = multiByteString
		length      = 100000
	)
	runTrials(inputString, length, t)
}

func TestRandomNoEmojiStringError(t *testing.T) {
	var (
		inputString = emojiString
		length      = 100000
	)
	runTrials(inputString, length, t)
}

func TestRandomEmptyInputString(t *testing.T) {
	var (
		inputString = ""
		length      = 100
	)
	randomString, err := RandomString(length, inputString)
	assert.Equal(t, "", randomString)
	assert.Error(t, err)
	assert.Equal(t, "legalCharacters may not be empty string", err.Error())
}

func TestRandomZeroLength(t *testing.T) {
	var (
		inputString = "abcde12345"
		length      = 0
	)
	randomString, err := RandomString(length, inputString)
	assert.Equal(t, "", randomString)
	assert.NoError(t, err)
}

// Make sure we aren't getting unseeded random values (i.e. math.random would give us the
// same strings since we don't seed it)
func TestNoDuplicates(t *testing.T) {
	var (
		inputString = "abcde12345"
	)

	probOfChar := 1.0 / (float64)(len([]rune(inputString)))

	// Figure out how long our string needs to be to get our desired probability of no collisions (~100)
	length := (int)(math.Ceil(math.Log(maxAllowableFailureRate) / math.Log(probOfChar)))
	s1, err1 := RandomString(length, inputString)
	s2, err2 := RandomString(length, inputString)
	assert.NoError(t, err1)
	assert.NoError(t, err2)
	assert.NotEqual(t, s1, s2)
}
