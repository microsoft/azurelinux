// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package versioncompare

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

const (
	emojiHighString    = "1🤷‍♂️2@3( •_•)>⌐■~■ab~52(⌐■_■)67👩‍💻"
	emojiHighStringAlt = "1👌2🤣3🤢ab~52*^&%$67(•_•)"
	emojiLowString     = "1🤷‍♂️2@3( •_•)>⌐■~■ab~42(⌐■_■)67👩‍💻"
	emojiMidString     = "1👌2🤣3🤢ab~52*^&%$6"
)

func TestCompareShouldProcessHigherEpochVersion(t *testing.T) {
	highVer := New("2:1.2.1")
	lowVer := New("4.2.2.1")
	assert.Equal(t, 1, highVer.Compare(lowVer))
}

func TestCompareShouldProcessLowerEpochVersion(t *testing.T) {
	highVer := New("2:1.2.1")
	lowVer := New("4.2.2.1")
	assert.Equal(t, 1, highVer.Compare(lowVer))
}

func TestCompareShouldProcessSameEpochVersion(t *testing.T) {
	highVer := New("1.2.3")
	lowVer := New("0:1.2.3")
	assert.Equal(t, 0, lowVer.Compare(highVer))
	assert.Equal(t, 0, highVer.Compare(lowVer))
}

func TestCompareShouldProcessHigherVersion(t *testing.T) {
	highVer := New("1.2.3")
	lowVer := New("1.2.2")
	assert.Equal(t, 1, highVer.Compare(lowVer))
}

func TestCompareShouldProcessLowerVersion(t *testing.T) {
	highVer := New("1.2.3")
	lowVer := New("1.2.2")
	assert.Equal(t, -1, lowVer.Compare(highVer))
}

func TestCompareShouldProcessSameVersion(t *testing.T) {
	highVer := New("1.2.3")
	lowVer := New("1.2.3")
	assert.Equal(t, 0, lowVer.Compare(highVer))
	assert.Equal(t, 0, highVer.Compare(lowVer))
}

func TestCompareShouldProcessHigherVersionWhenHigherLonger(t *testing.T) {
	highVer := New("1.2.3")
	lowVer := New("1.2")
	assert.Equal(t, 1, highVer.Compare(lowVer))
}

func TestCompareShouldProcessLowerVersionWhenHigherLonger(t *testing.T) {
	highVer := New("1.2.3")
	lowVer := New("1.2")
	assert.Equal(t, -1, lowVer.Compare(highVer))
}

func TestCompareShouldProcessHigherVersionWhenLowerLonger(t *testing.T) {
	highVer := New("1.4")
	lowVer := New("1.3.0")
	assert.Equal(t, 1, highVer.Compare(lowVer))
}

func TestCompareShouldProcessLowerVersionWhenLowerLonger(t *testing.T) {
	highVer := New("1.3")
	lowVer := New("1.2.3")
	assert.Equal(t, -1, lowVer.Compare(highVer))
}

func TestCompareShouldProcessHigherVersionWhenHigherLongerAndInstantlyGreater(t *testing.T) {
	highVer := New("1.4.0")
	lowVer := New("1.3")
	assert.Equal(t, 1, highVer.Compare(lowVer))
}

func TestCompareShouldProcessSameVersionWithGarbage(t *testing.T) {
	ver := New(emojiHighString)
	otherVer := New(emojiHighStringAlt)
	assert.Equal(t, 0, ver.Compare(otherVer))
	assert.Equal(t, 0, otherVer.Compare(ver))
}

func TestCompareShouldProcessLowerVersionWithGarbage(t *testing.T) {
	highVer := New(emojiHighString)
	lowVer := New(emojiMidString)
	assert.Equal(t, -1, lowVer.Compare(highVer))
}

func TestCompareShouldProcessHigherVersionWithGarbage(t *testing.T) {
	highVer := New(emojiMidString)
	lowVer := New(emojiLowString)
	assert.Equal(t, 1, highVer.Compare(lowVer))
}

func TestCompareShouldProcessHigherVersionWithGarbageAndDifferentLength(t *testing.T) {
	highVer := New(emojiHighString)
	lowVer := New(emojiMidString)
	assert.Equal(t, 1, highVer.Compare(lowVer))
}

func TestCompareShouldTreatEmptyVersionAsTheLowestValue(t *testing.T) {
	highVer := New("1.")
	lowVer := New("")
	assert.Equal(t, 1, highVer.Compare(lowVer))
	assert.Equal(t, -1, lowVer.Compare(highVer))
}

func TestCompareShouldTreatGarbageAsEmptyVersion(t *testing.T) {
	highVer := New("1.")
	lowVer := New(".#&$ . . .(@%) | 👩‍💻")
	assert.Equal(t, 1, highVer.Compare(lowVer))
	assert.Equal(t, -1, lowVer.Compare(highVer))
}

func TestCompareShouldCompareVersionToItself(t *testing.T) {
	ver := New("1.2.3")
	assert.Equal(t, 0, ver.Compare(ver))
}

func TestCompareShouldNotEquateEmptyWithString(t *testing.T) {
	str := New("1.2.3")
	empty := New("")
	assert.Equal(t, 1, str.Compare(empty))
}

func TestShouldIgnoreRelease(t *testing.T) {
	verAndRev := New("1.2.3-3")
	ver := New("1.2.3")
	assert.Equal(t, 0, verAndRev.Compare(ver))
	assert.Equal(t, 0, ver.Compare(verAndRev))
}

func TestCompareShouldEqualWithRevision(t *testing.T) {
	ver := New("1.2.3-1.2.3")
	assert.Equal(t, 0, ver.Compare(ver))
}

func TestShouldIgnoreReleaseWithGreaterLessThan(t *testing.T) {
	low := New("1.2.3-3")
	high := New("4.5.6")
	assert.Equal(t, -1, low.Compare(high))
	assert.Equal(t, 1, high.Compare(low))
}

func TestShouldCompareRelease(t *testing.T) {
	high := New("1.2.3-3")
	low := New("1.2.3-2")
	assert.Equal(t, -1, low.Compare(high))
	assert.Equal(t, 1, high.Compare(low))
}

func TestNoVersionWithRelease(t *testing.T) {
	high := New("-3")
	low := New("-2")
	assert.Equal(t, -1, low.Compare(high))
	assert.Equal(t, 1, high.Compare(low))
}

func TestMultiplePartRelease(t *testing.T) {
	high := New("1.2.3-2.2")
	low := New("1.2.3-2")
	assert.Equal(t, -1, low.Compare(high))
	assert.Equal(t, 1, high.Compare(low))
}

func TestMaxVersion(t *testing.T) {
	high := NewMax()
	low := New("1")
	assert.Equal(t, -1, low.Compare(high))
	assert.Equal(t, 1, high.Compare(low))
	assert.Equal(t, 0, high.Compare(high))
}

func TestMinVersion(t *testing.T) {
	high := New("1")
	low := NewMin()
	assert.Equal(t, -1, low.Compare(high))
	assert.Equal(t, 1, high.Compare(low))
	assert.Equal(t, 0, low.Compare(low))
}

func TestMaxAndMin(t *testing.T) {
	high := NewMax()
	low := NewMin()
	assert.Equal(t, -1, low.Compare(high))
	assert.Equal(t, 1, high.Compare(low))
}

func TestConditional(t *testing.T) {
	high := New("2")
	low := New("1")
	tests := []struct {
		string
		bool
	}{{"<", true}, {"<=", true}, {"=", false}, {">", false}, {">=", false}}
	for _, test := range tests {
		res, err := low.CompareWithConditional(test.string, high)
		assert.NoError(t, err)
		assert.Equal(t, test.bool, res)

	}
}

func TestInvalidConditional(t *testing.T) {
	high := New("2")
	low := New("1")
	_, err := low.CompareWithConditional("?", high)
	assert.Error(t, err)
}
