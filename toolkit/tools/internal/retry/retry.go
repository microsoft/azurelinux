// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package retry

import (
	"math"
	"time"
)

const (
	// With 5 attempts (4 retries) and a backoff factor of 2 seconds the total time spent retrying will be approximately:
	// 1 + 4 + 8 + 16 = 31 seconds.
	DefaultDownloadBackoffBase   = 2.0
	DefaultDownloadRetryAttempts = 5
	DefaultDownloadRetryDuration = time.Second
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

// backoffSleep sleeps for the given duration, unless the cancel channel is triggered or closed first. The cancel channel
// may be nil in which case the sleep will always complete.
func backoffSleep(delay time.Duration, cancel <-chan struct{}) (cancelled bool) {
	// Check if we were cancelled before we sleep to avoid a race condition with
	// delay=0 and an immediate cancel.
	select {
	case <-cancel:
		cancelled = true
		return
	default:
	}

	select {
	case <-time.After(delay):
	case <-cancel:
		cancelled = true
	}
	return
}

// runWithBackoffInternal runs function up to 'attempts' times, waiting delayCalc(failCount) before each i-th attempt.
// delayCalc(0) is expected to return 0.
// The function will return early if the cancel channel is closed.
func runWithBackoffInternal(function func() error, delayCalc func(failCount int) time.Duration, attempts int, cancel <-chan struct{}) (wasCancelled bool, err error) {
	for failures := 0; failures < attempts; failures++ {
		delayTime := delayCalc(failures)
		wasCancelled = backoffSleep(delayTime, cancel)
		if wasCancelled {
			break
		}
		if err = function(); err == nil {
			break
		}
	}
	return wasCancelled, err
}

// Run runs function up to 'attempts' times, waiting i * sleep duration before each i-th attempt.
func Run(function func() error, attempts int, sleep time.Duration) (err error) {
	_, err = RunWithLinearBackoff(function, attempts, sleep, nil)
	return
}

// RunWithLinearBackoff runs function up to 'attempts' times, waiting i * sleep duration before each i-th attempt. An
// optional cancel channel can be provided to cancel the retry loop immediately by closing the channel.
func RunWithLinearBackoff(function func() error, attempts int, sleep time.Duration, cancel <-chan struct{}) (wasCancelled bool, err error) {
	return runWithBackoffInternal(function, func(failCount int) time.Duration {
		return calculateLinearDelay(failCount, sleep)
	}, attempts, cancel)
}

// RunWithDefaultDownloadBackoff runs function up to 'DefaultDownloadRetryAttempts' times, waiting 'DefaultDownloadBackoffBase^(i-1)' seconds before
// each i-th attempt. An optional cancel channel can be provided to cancel the retry loop immediately by closing the channel.
//
// The function is meant as a default for network download operations.
func RunWithDefaultDownloadBackoff(function func() error, cancel <-chan struct{}) (wasCancelled bool, err error) {
	return RunWithExpBackoff(function, DefaultDownloadRetryAttempts, DefaultDownloadRetryDuration, DefaultDownloadBackoffBase, cancel)
}

// RunWithExpBackoff runs function up to 'attempts' times, waiting 'backoffExponentBase^(i-1) * sleep' duration before
// each i-th attempt. An optional cancel channel can be provided to cancel the retry loop immediately by closing the channel.
func RunWithExpBackoff(function func() error, attempts int, sleep time.Duration, backoffExponentBase float64, cancel <-chan struct{}) (wasCancelled bool, err error) {
	return runWithBackoffInternal(function, func(failCount int) time.Duration {
		return calculateExpDelay(failCount, sleep, backoffExponentBase)
	}, attempts, cancel)
}
