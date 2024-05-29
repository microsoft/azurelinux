// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package retry

import (
	"context"
	"fmt"
	"math"
	"time"
)

const (
	// With 8 attempts (7 retries) and a backoff factor of 2 seconds the total time spent retrying will be approximately:
	// 0 + 1 + 2 + 4 + 8 + 16 + 32 + 64 = 127 seconds (2 min, 7 sec)
	DefaultDownloadBackoffBase   = 2.0
	DefaultDownloadRetryAttempts = 8
	DefaultDownloadRetryDuration = time.Second
)

var ErrNilContext = fmt.Errorf("nil context")

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

// backoffSleep sleeps for the given duration, unless the context is cancelled. The context
// may be nil in which case the background context will be used and the sleep will always complete.
func backoffSleep(ctx context.Context, delay time.Duration) (cancelled bool, err error) {
	if ctx == nil {
		return false, ErrNilContext
	}

	// Check if we were cancelled before we sleep to avoid a race condition with
	// delay=0 and an immediate cancel.
	select {
	case <-ctx.Done():
		cancelled = true
		return
	default:
	}

	select {
	case <-time.After(delay):
	case <-ctx.Done():
		cancelled = true
	}
	return
}

// runWithBackoffInternal runs function up to 'attempts' times, waiting delayCalc(failCount) before each i-th attempt.
// delayCalc(0) is expected to return 0.
// The function will return early if the cancel channel is closed.
func runWithBackoffInternal(ctx context.Context, function func() error, delayCalc func(failCount int) time.Duration, attempts int) (wasCancelled bool, err error) {
	for failures := 0; failures < attempts; failures++ {
		delayTime := delayCalc(failures)
		var sleepErr error
		wasCancelled, sleepErr = backoffSleep(ctx, delayTime)
		if sleepErr != nil {
			return false, sleepErr
		}
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
	_, err = RunWithLinearBackoff(context.Background(), function, attempts, sleep)
	return
}

// RunWithLinearBackoff runs function up to 'attempts' times, waiting i * sleep duration before each i-th attempt. An
// optional context can be provided to cancel the retry loop immediately.
func RunWithLinearBackoff(ctx context.Context, function func() error, attempts int, sleep time.Duration) (wasCancelled bool, err error) {
	return runWithBackoffInternal(ctx, function, func(failCount int) time.Duration {
		return calculateLinearDelay(failCount, sleep)
	}, attempts)
}

// RunWithDefaultDownloadBackoff runs function up to 'DefaultDownloadRetryAttempts' times, waiting 'DefaultDownloadBackoffBase^(i-1)' seconds before
// each i-th attempt. An optional context can be provided to cancel the retry loop immediately.
//
// The function is meant as a default for network download operations.
func RunWithDefaultDownloadBackoff(ctx context.Context, function func() error) (wasCancelled bool, err error) {
	return RunWithExpBackoff(ctx, function, DefaultDownloadRetryAttempts, DefaultDownloadRetryDuration, DefaultDownloadBackoffBase)
}

// RunWithExpBackoff runs function up to 'attempts' times, waiting 'backoffExponentBase^(i-1) * sleep' duration before
// each i-th attempt. An optional context can be provided to cancel the retry loop immediately.
func RunWithExpBackoff(ctx context.Context, function func() error, attempts int, sleep time.Duration, backoffExponentBase float64) (wasCancelled bool, err error) {
	return runWithBackoffInternal(ctx, function, func(failCount int) time.Duration {
		return calculateExpDelay(failCount, sleep, backoffExponentBase)
	}, attempts)
}
