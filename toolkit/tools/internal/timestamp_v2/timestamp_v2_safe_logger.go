// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.
package timestamp_v2

import (
	"fmt"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
)

// The timestamping code may be called from environments where logging is not configured

// This code should be callable from anywhere, regardless of if a logger is configured
func failsafeLoggerErrorf(format string, args ...interface{}) {
	if logger.Log != nil {
		logger.Log.Errorf(format, args...)
	} else {
		fmt.Printf(format, args...)
	}
}

// This code should be callable from anywhere, regardless of if a logger is configured
func failsafeLoggerWarnf(format string, args ...interface{}) {
	if logger.Log != nil {
		logger.Log.Warnf(format, args...)
	} else {
		fmt.Printf(format, args...)
	}
}

// This code should be callable from anywhere, regardless of if a logger is configured
func failsafeLoggerTracef(format string, args ...interface{}) {
	if logger.Log != nil {
		logger.Log.Tracef(format, args...)
	}
}
