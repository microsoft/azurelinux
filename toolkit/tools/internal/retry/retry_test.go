package retry

import (
	"context"
	"fmt"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

const (
	defaultTestTime = time.Millisecond * 100

	// Tests won't run with perfect timing, so we need to allow for some fudge factor when we check maximum duration.
	timingFudgeFactor = time.Millisecond * 100
)

func TestZeroBase(t *testing.T) {
	// Two failures, 0.0 multiplier, should be 0 second delay
	base := 0.0
	fails := 2
	val := calculateExpDelay(fails, defaultTestTime, base)
	assert.Equal(t, time.Duration(0), val)
}

func TestZeroFailuresTime(t *testing.T) {
	// Zero failures, 1.0 base, should be 0 second delay
	fails := 0
	base := 1.0
	val := calculateExpDelay(fails, defaultTestTime, base)
	assert.Equal(t, time.Second*0, val)
}

func TestZeroBaseTime(t *testing.T) {
	// Three failures, 0.0 base, should be 0 second delay
	fails := 3
	base := 0.0
	val := calculateExpDelay(fails, defaultTestTime, base)
	assert.Equal(t, time.Second*0, val)
}

func TestNegativeFailuresCountExp(t *testing.T) {
	// Negative failures, 1.0 base, should be 0 second delay
	fails := -1
	base := 1.0
	val := calculateExpDelay(fails, defaultTestTime, base)
	assert.Equal(t, time.Second*0, val)
}

func TestNegativeFailuresCountLinear(t *testing.T) {
	// Negative failures, should be 0 second delay
	fails := -1
	val := calculateLinearDelay(fails, defaultTestTime)
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

func TestCalcDelayExpBase2(t *testing.T) {
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
	cancelled, err := RunWithLinearBackoff(context.Background(), func() error {
		return fmt.Errorf("test error")
	}, attempts, defaultTestTime)
	endTime := time.Now()
	assert.NotNil(t, err)
	assert.False(t, cancelled)
	// Delays should be 0 seconds, <attempt>, .1 second, <attempt>, .2 seconds, <attempt>
	// for a total of .3 seconds.
	idealTime := time.Millisecond * 300
	minDelay := idealTime
	maxDelay := idealTime + timingFudgeFactor
	assert.GreaterOrEqual(t, endTime.Sub(startTime), minDelay)
	assert.LessOrEqual(t, endTime.Sub(startTime), maxDelay)
}

func TestTotalRunTimeWithFailuresDefaultRun(t *testing.T) {
	attempts := 3
	// Ensure the default Run() method works the same way
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
}

func TestTotalRunTimeWithFailuresBase2(t *testing.T) {
	tries := 3
	base := 2.0
	startTime := time.Now()
	cancelled, err := RunWithExpBackoff(context.Background(), func() error {
		return fmt.Errorf("test error")
	}, tries, defaultTestTime, base)
	endTime := time.Now()
	assert.NotNil(t, err)
	assert.False(t, cancelled)
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
	cancelled, err := RunWithExpBackoff(context.Background(), func() error {
		return nil
	}, tries, time.Second, base)
	endTime := time.Now()
	assert.Nil(t, err)
	assert.False(t, cancelled)
	// Delays should be 0 seconds, <attempt>
	// for a total of 0 seconds.
	maxDelay := timingFudgeFactor
	assert.LessOrEqual(t, endTime.Sub(startTime), maxDelay)
}

func TestCancelsEarlyWithSignalImmediately(t *testing.T) {
	tries := 3
	base := 2.0
	ctx, cancelFunc := context.WithCancel(context.Background())
	startTime := time.Now()

	// Send a signal immediately
	cancelFunc()

	cancelled, err := RunWithExpBackoff(ctx, func() error {
		return fmt.Errorf("test error")
	}, tries, defaultTestTime, base)

	endTime := time.Now()
	// Error should be nil since we never ran the function before cancelling.
	assert.Nil(t, err)
	assert.True(t, cancelled)
	// Delays should be 0 seconds, <attempt>
	// for a total of 0 seconds.
	maxDelay := timingFudgeFactor
	assert.LessOrEqual(t, endTime.Sub(startTime), maxDelay)
}

func TestCancelsEarlyWithSignalAfterDelay(t *testing.T) {
	tries := 3
	base := 2.0
	cancelTime := defaultTestTime * 2
	ctx, cancelFunc := context.WithCancel(context.Background())
	startTime := time.Now()

	// Send a signal after the first delay (wait for the first failure before cancelling)
	go func() {
		time.Sleep(cancelTime)
		cancelFunc()
	}()

	cancelled, err := RunWithExpBackoff(ctx, func() error {
		return fmt.Errorf("test error")
	}, tries, defaultTestTime, base)

	endTime := time.Now()
	// Error should still be set since we ran the function at least once.
	assert.NotNil(t, err)
	assert.True(t, cancelled)

	// Delay should be 0.2 seconds before the signal is received
	idealTime := cancelTime
	minDelay := idealTime
	maxDelay := idealTime + timingFudgeFactor
	assert.GreaterOrEqual(t, endTime.Sub(startTime), minDelay)
	assert.LessOrEqual(t, endTime.Sub(startTime), maxDelay)
}

func TestNonCancelGivesCorrectError(t *testing.T) {
	tries := 1
	base := 2.0
	cancelled, err := RunWithExpBackoff(context.Background(), func() error {
		return fmt.Errorf("test error")
	}, tries, defaultTestTime, base)

	assert.NotNil(t, err)
	assert.Equal(t, "test error", err.Error())
	assert.False(t, cancelled)
}

func TestFailsOnNilCtx(t *testing.T) {
	//lint:ignore SA1012 We intentionally want to test the error case of a nil context
	_, err := RunWithLinearBackoff(nil, func() error {
		return nil
	}, 1, time.Second)
	assert.NotNil(t, err)
	assert.Equal(t, ErrNilContext, err)

	//lint:ignore SA1012 We intentionally want to test the error case of a nil context
	_, err = RunWithDefaultDownloadBackoff(nil, func() error {
		return nil
	})
	assert.NotNil(t, err)
	assert.Equal(t, ErrNilContext, err)

	//lint:ignore SA1012 We intentionally want to test the error case of a nil context
	_, err = RunWithExpBackoff(nil, func() error {
		return nil
	}, 1, time.Second, 2.0)
	assert.NotNil(t, err)
	assert.Equal(t, ErrNilContext, err)
}
