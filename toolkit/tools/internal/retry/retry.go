// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package retry

import (
	"math"
	"time"
)

func calcDelay(retryCount int, sleep time.Duration, backoffExp float64) time.Duration {
	// Calculate an exponential backoff.
	// The formula is: sleep * (backoffExp ^ retryCount)
	// For example, if sleep = 1 second, backoffExp = 2.0, retryCount = 3
	// then the delay will be 1 * (2 ^ 3) = 8 seconds.
	expRetry := math.Pow(float64(retryCount), backoffExp)
	return time.Duration(expRetry * float64(sleep))
}

// Run runs function up to attempts times, waiting i * sleep duration before each i-th attempt.
func Run(function func() error, attempts int, sleep time.Duration) (err error) {
	return RunWithExpBackoff(function, attempts, sleep, 1.0)
}

// Run runs function up to attempts times, waiting i * backoffMult * sleep duration before each i-th attempt.
func RunWithExpBackoff(function func() error, attempts int, sleep time.Duration, backoffExp float64) (err error) {
	for i := 0; i < attempts; i++ {
		// Calculate an exponential backoff.
		time.Sleep(calcDelay(i, sleep, backoffExp))
		if err = function(); err == nil {
			break
		}
	}
	return err
}
