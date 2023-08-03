package retry

import (
	"fmt"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

// Delay vs. retry count for mult = 1.0, delay = .1 seconds
var expectedValuesMillis1 = []int{0, 100, 200, 300, 400, 500}

// Delay vs. retry count for exp = 2.0, delay = 0.1 seconds
var expectedValuesMillis2 = []int{0, 100, 400, 900, 1600, 2500}

func TestCalcDelay1(t *testing.T) {
	mult := 1.0
	sleep := time.Millisecond * 100
	for i, expected := range expectedValuesMillis1 {
		expected := time.Duration(expected) * time.Millisecond
		actual := calcDelay(i, sleep, mult)
		assert.Equal(t, expected, actual)
	}
}

func TestCalcDelay2(t *testing.T) {
	mult := 2.0
	sleep := time.Millisecond * 100
	for i, expected := range expectedValuesMillis2 {
		expected := time.Duration(expected) * time.Millisecond
		actual := calcDelay(i, sleep, mult)
		assert.Equal(t, expected, actual)
	}
}

func TestTotalRunTimeWithFailures1(t *testing.T) {
	startTime := time.Now()
	err := RunWithExpBackoff(func() error {
		return fmt.Errorf("test error")
	}, 3, time.Millisecond*100, 1.0)
	endTime := time.Now()
	assert.NotNil(t, err)
	// Delays should be 0 seconds, <attempt>, .1 second, <attempt>, .2 seconds, <attempt>
	// for a total of .3 seconds.
	minDelay := time.Millisecond * 300
	maxDelay := time.Millisecond * 500
	assert.GreaterOrEqual(t, endTime.Sub(startTime), minDelay)
	assert.LessOrEqual(t, endTime.Sub(startTime), maxDelay)
}

func TestTotalRunTimeWithFailures2(t *testing.T) {
	startTime := time.Now()
	err := RunWithExpBackoff(func() error {
		return fmt.Errorf("test error")
	}, 3, time.Millisecond*100, 2.0)
	endTime := time.Now()
	assert.NotNil(t, err)
	// Delays should be 0 seconds, <attempt>, .1 second, <attempt>, .4 seconds, <attempt>
	// for a total of .5 seconds.
	minDelay := time.Millisecond * 500
	maxDelay := time.Millisecond * 700
	assert.GreaterOrEqual(t, endTime.Sub(startTime), minDelay)
	assert.LessOrEqual(t, endTime.Sub(startTime), maxDelay)
}

func TestTotalRunTimeWithSuccess(t *testing.T) {
	startTime := time.Now()
	err := RunWithExpBackoff(func() error {
		return nil
	}, 3, time.Second, 1.0)
	endTime := time.Now()
	assert.Nil(t, err)
	// Delays should be 0 seconds, <attempt>
	// for a total of 0 seconds.
	maxDelay := time.Millisecond * 100
	assert.LessOrEqual(t, endTime.Sub(startTime), maxDelay)
}

func TestZeroMult(t *testing.T) {
	val := calcDelay(2, time.Second, 0.0)
	assert.LessOrEqual(t, val, time.Second*2)
}
