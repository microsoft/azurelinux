// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package logger

import (
	"fmt"
	"io"
	"runtime"
	"strings"
	"sync"

	"github.com/fatih/color"
	"github.com/sirupsen/logrus"
)

// writerHook is a hook to handle writing to a writer at a custom log level
type writerHook struct {
	lock      sync.Mutex
	level     logrus.Level
	writer    io.Writer
	formatter logrus.Formatter
	useColors bool
}

// newWriterHook returns new writerHook
func newWriterHook(writer io.Writer, level logrus.Level, useColors bool, toolName string) *writerHook {
	formatter := &logrus.TextFormatter{
		ForceColors: useColors,
		CallerPrettyfier: func(frame *runtime.Frame) (function string, file string) {
			return
		},
	}

	if toolName != "" {
		formatter.CallerPrettyfier = func(frame *runtime.Frame) (function string, file string) {
			toolNameField := fmt.Sprintf("[%s]", toolName)
			if useColors {
				toolNameField = fmt.Sprintf(color.BlackString("[%s]"), toolName)
			}

			return "", toolNameField
		}
	}

	return &writerHook{
		level:     level,
		writer:    writer,
		formatter: formatter,
		useColors: useColors,
	}
}

// Fire writes the log entry to the writer
func (h *writerHook) Fire(entry *logrus.Entry) (err error) {
	// Filter out entries that are at a higher level (more verbose) than the current filter
	if entry.Level > h.level {
		return
	}

	if !h.useColors {
		entry.Message = strings.ReplaceAll(entry.Message, "\x1b[31m", "")
		entry.Message = strings.ReplaceAll(entry.Message, "\x1b[34m", "")
		entry.Message = strings.ReplaceAll(entry.Message, "\x1b[0m", "")
		entry.Message = strings.ReplaceAll(entry.Message, "\x1b[32m", "")
	}

	h.lock.Lock()
	defer h.lock.Unlock()

	msg, err := h.formatter.Format(entry)
	if err != nil {
		return
	}

	_, err = fmt.Fprint(h.writer, string(msg))
	return
}

// SetLevel sets the lowest log level
func (h *writerHook) SetLevel(level logrus.Level) {
	h.level = level
}

// Levels returns configured log levels
func (h *writerHook) Levels() []logrus.Level {
	return logrus.AllLevels
}

// ReplaceWriter replaces the writer and returns the old one
func (h *writerHook) ReplaceWriter(newWriter io.Writer) (oldWriter io.Writer) {
	h.lock.Lock()
	defer h.lock.Unlock()

	oldWriter = h.writer
	h.writer = newWriter

	return
}

// ReplaceFormatter replaces the formatter used by the hook and returns the old formatter
func (h *writerHook) ReplaceFormatter(newFormatter logrus.Formatter) (oldFormatter logrus.Formatter) {
	h.lock.Lock()
	defer h.lock.Unlock()

	oldFormatter = h.formatter
	h.formatter = newFormatter

	return
}

// CurrentLevel returns the current log level for the hook
func (h *writerHook) CurrentLevel() logrus.Level {
	return h.level
}
