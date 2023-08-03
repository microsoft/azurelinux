// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package retry

import (
	"time"
)

// Run runs function up to attempts times, waiting i * sleep duration before each i-th attempt.
func Run(function func() error, attempts int, sleep time.Duration) (err error) {
	return RunWithExpBackoff(function, attempts, sleep, 1.0)
}

// Run runs function up to attempts times, waiting i * backoffMult * sleep duration before each i-th attempt.
func RunWithExpBackoff(function func() error, attempts int, sleep time.Duration, backoffMult float32) (err error) {
	for i := 0; i < attempts; i++ {
		//time.Sleep(time.Duration(i*backoffMult) * sleep)

		// Calculate an exponential backoff.
		backOffMillis := int64(float32(i) * backoffMult * float32(sleep/time.Millisecond))
		time.Sleep(time.Duration(backOffMillis) * time.Millisecond)
		if err = function(); err == nil {
			break
		}
	}
	return err
}
