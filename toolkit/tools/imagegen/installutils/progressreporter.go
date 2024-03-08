// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package installutils

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

var doEmitProgress bool

// EnableEmittingProgress enables progress updates on stdout, such as percent complete and the current action.
func EnableEmittingProgress() {
	doEmitProgress = true
}

// ReportPercentComplete emits the current percent complete on stdout, only if EnableEmittingProgress was invoked with true.
func ReportPercentComplete(progress int) {
	emitUpdate("progress", progress)
}

// ReportActionf emits the formatted current action being performed on stdout, only if EnableEmittingProgress was invoked with true.
// It also prints the output to the log at debug level regardless of EnableEmittingProgress
func ReportActionf(format string, args ...interface{}) {
	ReportAction(fmt.Sprintf(format, args...))
}

// ReportAction emits the current action being performed on stdout, only if EnableEmittingProgress was invoked with true.
// It also prints the output to the log at debug level regardless of EnableEmittingProgress.
func ReportAction(status string) {
	emitUpdate("action", status)
	logger.Log.Debugf("ReportAction: (%s)", status)
}

func emitUpdate(key string, value interface{}) {
	if !doEmitProgress {
		return
	}

	fmt.Printf("%s:%v\n", key, value)
}
