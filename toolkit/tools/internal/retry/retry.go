// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package retry

import (
	"math"
	"time"
)

// calculateDelay calculates the delay for the given failure count, sleep duration, and backoff exponent base.
// If the base is positive, it will calculate an exponential backoff.
func calculateExpDelay(failCount int, sleep time.Duration, backoffExponentBase float64) time.Duration {
	if failCount <= 0 {
		return 0
	}
	// Calculate an exponential backoff. We calculate and sleep BEFORE we try to run the function, so we need to
	// subtract 1 from the failCount to get the correct exponent.

	// The formula is: sleep * (backoffExpBase ^ (failCount-1))
	// For example, if sleep = 1 second, backoffExp = 2.0, failCount = 3
	// then the delay will be 1 * (2 ^ 2) = 4 seconds.
	// (0 sec on the first call, 1 sec on the second call, 2 sec on the third call, etc.)
	expRetry := math.Pow(backoffExponentBase, float64(failCount-1))
	return time.Duration(expRetry * float64(sleep))
}

func calculateLinearDelay(failCount int, sleep time.Duration) time.Duration {
	if failCount <= 0 {
		return 0
	}
	return sleep * time.Duration(failCount)
}

// runWithBackoffInternal runs function up to 'attempts' times, waiting delayCalc(failCount) before each i-th attempt.
// delayCalc(0) is expected to return 0.
func runWithBackoffInternal(function func() error, delayCalc func(failCount int) time.Duration, attempts int) (err error) {
	for failures := 0; failures < attempts; failures++ {
		delayTime := delayCalc(failures)
		time.Sleep(delayTime)
		if err = function(); err == nil {
			break
		}
	}
	return err
}

// Run runs function up to 'attempts' times, waiting i * sleep duration before each i-th attempt.
func Run(function func() error, attempts int, sleep time.Duration) (err error) {
	return runWithBackoffInternal(function, func(failCount int) time.Duration {
		return calculateLinearDelay(failCount, sleep)
	}, attempts)
}

// RunWithExpBackoff runs function up to 'attempts' times, waiting 'backoffExponentBase^(i-1) * sleep' duration before each i-th attempt.
func RunWithExpBackoff(function func() error, attempts int, sleep time.Duration, backoffExponentBase float64) (err error) {
	return runWithBackoffInternal(function, func(failCount int) time.Duration {
		return calculateExpDelay(failCount, sleep, backoffExponentBase)
	}, attempts)
}
