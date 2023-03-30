// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package retry

import (
	"time"
)

// Run runs function up to attempts times, waiting i * sleep duration before each i-th attempt.
func Run(function func() error, attempts int, sleep time.Duration) (err error) {
	for i := 0; i < attempts; i++ {
		time.Sleep(time.Duration(i) * sleep)
		if err = function(); err == nil {
			break
		}
	}
	return err
}
