// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package writerhook

import (
	"fmt"
	"io"
	"sync"

	"github.com/sirupsen/logrus"
)

// WriterHook is a hook to handle writing to a writer at a custom log level
type WriterHook struct {
	lock      sync.Mutex
	level     logrus.Level
	writer    io.Writer
	formatter logrus.Formatter
}

// NewWriterHook returns new WriterHook
func NewWriterHook(writer io.Writer, level logrus.Level, useColors bool) *WriterHook {
	formatter := &logrus.TextFormatter{
		ForceColors: useColors,
	}

	return &WriterHook{
		level:     level,
		writer:    writer,
		formatter: formatter,
	}
}

// Fire writes the log entry to the writer
func (h *WriterHook) Fire(entry *logrus.Entry) (err error) {
	// Filter out entries that are at a higher level (more verbose) than the current filter
	if entry.Level > h.level {
		return
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
func (h *WriterHook) SetLevel(level logrus.Level) {
	h.level = level
}

// Levels returns configured log levels
func (h *WriterHook) Levels() []logrus.Level {
	return logrus.AllLevels
}

// ReplaceWriter replaces the writer and returns the old one
func (h *WriterHook) ReplaceWriter(newWriter io.Writer) (oldWriter io.Writer) {
	h.lock.Lock()
	defer h.lock.Unlock()

	oldWriter = h.writer
	h.writer = newWriter

	return
}

// ReplaceFormatter replaces the formatter used by the hook and returns the old formatter
func (h *WriterHook) ReplaceFormatter(newFormatter logrus.Formatter) (oldFormatter logrus.Formatter) {
	h.lock.Lock()
	defer h.lock.Unlock()

	oldFormatter = h.formatter
	h.formatter = newFormatter

	return
}

// CurrentLevel returns the current log level for the hook
func (h *WriterHook) CurrentLevel() logrus.Level {
	return h.level
}
