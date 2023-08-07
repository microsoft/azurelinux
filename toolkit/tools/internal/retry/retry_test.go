package retry

import (
	"fmt"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

var defaultTestTime = time.Millisecond * 100

// Tests won't run with perfect timing, so we need to allow for some fudge factor when we check maximum duration.
var timingFudgeFactor = time.Millisecond * 100

func TestZeroBase(t *testing.T) {
	// Two failures, 0.0 multiplier, should be 0 second delay
	base := 0.0
	fails := 2
	val := calculateExpDelay(fails, defaultTestTime, base)
	assert.Equal(t, time.Duration(0), val)
}

func TestZeroI(t *testing.T) {
	// Zero failures, 1.0 base, should be 0 second delay
	fails := 0
	base := 1.0
	val := calculateExpDelay(fails, defaultTestTime, base)
	assert.Equal(t, time.Second*0, val)

	// Three failures, 1.0 base, should still be 0 second delay
	fails = 3
	base = 0.0
	val = calculateExpDelay(fails, defaultTestTime, base)
	assert.Equal(t, time.Second*0, val)
}

func TestNegativeI(t *testing.T) {
	// Negative failures, 1.0 base, should be 0 second delay
	fails := -1
	base := 1.0
	val := calculateExpDelay(fails, defaultTestTime, base)
	assert.Equal(t, time.Second*0, val)

	// Negative failures, should be 0 second delay
	fails = -1
	base = 1.0
	val = calculateLinearDelay(fails, defaultTestTime)
	assert.Equal(t, time.Second*0, val)
}

func TestCalcDelayBaseLinear(t *testing.T) {
	// Delay vs. retry count for base = -1.0, delay = .1 seconds (ie legacy "linear" backoff)
	var expectedValuesMillis1 = []int{0, 100, 200, 300, 400, 500}

	for failures, expected := range expectedValuesMillis1 {
		expected := time.Duration(expected) * time.Millisecond
		actual := calculateLinearDelay(failures, defaultTestTime)
		assert.Equal(t, expected, actual)
	}
}

func TestCalcDelayBase2(t *testing.T) {
	// Delay vs. retry count for base = 2.0, delay = 0.1 seconds
	var expectedValuesMillis2 = []int{0, 100, 200, 400, 800, 1600}

	base := 2.0
	for failures, expected := range expectedValuesMillis2 {
		expected := time.Duration(expected) * time.Millisecond
		actual := calculateExpDelay(failures, defaultTestTime, base)
		assert.Equal(t, expected, actual)
	}
}

func TestTotalRunTimeWithFailuresLinear(t *testing.T) {
	attempts := 3
	startTime := time.Now()
	err := Run(func() error {
		return fmt.Errorf("test error")
	}, attempts, defaultTestTime)
	endTime := time.Now()
	assert.NotNil(t, err)
	// Delays should be 0 seconds, <attempt>, .1 second, <attempt>, .2 seconds, <attempt>
	// for a total of .3 seconds.
	idealTime := time.Millisecond * 300
	minDelay := idealTime
	maxDelay := idealTime + timingFudgeFactor
	assert.GreaterOrEqual(t, endTime.Sub(startTime), minDelay)
	assert.LessOrEqual(t, endTime.Sub(startTime), maxDelay)

	// Ensure the default Run() method works the same way
	startTime = time.Now()
	err = Run(func() error {
		return fmt.Errorf("test error")
	}, attempts, defaultTestTime)
	endTime = time.Now()
	assert.NotNil(t, err)
	assert.GreaterOrEqual(t, endTime.Sub(startTime), minDelay)
	assert.LessOrEqual(t, endTime.Sub(startTime), maxDelay)
}

func TestTotalRunTimeWithFailuresBase2(t *testing.T) {
	tries := 3
	base := 2.0
	startTime := time.Now()
	err := RunWithExpBackoff(func() error {
		return fmt.Errorf("test error")
	}, tries, defaultTestTime, base)
	endTime := time.Now()
	assert.NotNil(t, err)
	// Delays should be 0 seconds, <attempt>, .1 second, <attempt>, .2 seconds, <attempt>
	// for a total of .3 seconds.
	idealTime := time.Millisecond * 300
	minDelay := idealTime
	maxDelay := idealTime + timingFudgeFactor
	assert.GreaterOrEqual(t, endTime.Sub(startTime), minDelay)
	assert.LessOrEqual(t, endTime.Sub(startTime), maxDelay)
}

func TestTotalRunTimeWithSuccess(t *testing.T) {
	tries := 3
	base := 2.0
	startTime := time.Now()
	err := RunWithExpBackoff(func() error {
		return nil
	}, tries, time.Second, base)
	endTime := time.Now()
	assert.Nil(t, err)
	// Delays should be 0 seconds, <attempt>
	// for a total of 0 seconds.
	maxDelay := timingFudgeFactor
	assert.LessOrEqual(t, endTime.Sub(startTime), maxDelay)
}

// func TestFoo(t *testing.T) {
// 	const (
// 		downloadRetryAttempts  = 5
// 		failureBackoffExponent = 2.0
// 		downloadRetryDuration  = time.Second
// 	)
// 	totalDuration := time.Duration(0)
// 	for i := 1; i <= downloadRetryAttempts; i++ {
// 		totalDuration += calculateDelay(i, downloadRetryDuration, failureBackoffExponent)
// 	}
// 	assert.Equal(t, time.Duration(1023)*time.Millisecond, totalDuration)
// }
