// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package retry

import (
	"math"
	"time"
)

// calculateDelay calculates the delay for the given failure count, sleep duration, and backoff exponent base.
// If the base is negative, it will calculate a linear backoff.
// If the base is positive, it will calculate an exponential backoff.
func calculateDelay(failCount int, sleep time.Duration, backoffExponentBase float64) time.Duration {
	if failCount == 0 {
		return 0
	}
	// Treat negative values of base as linear backoff.
	if backoffExponentBase < 0 {
		return sleep * time.Duration(failCount)
	}
	// Calculate an exponential backoff.
	// The formula is: sleep * (backoffExpBase ^ failCount)
	// For example, if sleep = 1 second, backoffExp = 2.0, failCount = 3
	// then the delay will be 1 * (2 ^ 3) = 8 seconds.
	expRetry := math.Pow(backoffExponentBase, float64(failCount-1))
	return time.Duration(expRetry * float64(sleep))
}

// Run runs function up to attempts times, waiting i * sleep duration before each i-th attempt.
func Run(function func() error, attempts int, sleep time.Duration) (err error) {
	return RunWithExpBackoff(function, attempts, sleep, -1)
}

// RunWithExpBackoff runs function up to 'attempts' times, waiting 'backoffExponentBase^i * sleep' duration before each i-th attempt.
func RunWithExpBackoff(function func() error, attempts int, sleep time.Duration, backoffExponentBase float64) (err error) {
	for failures := 0; failures < attempts; failures++ {
		// Calculate an exponential backoff. For i=0 we will calculate 0 delay and immediately call the function.
		time.Sleep(calculateDelay(failures, sleep, backoffExponentBase))
		if err = function(); err == nil {
			break
		}
	}
	return err
}
