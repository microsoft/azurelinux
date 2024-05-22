// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Shared logger

package logger

import (
	"fmt"
	"io"
	"log"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"unicode/utf8"

	"github.com/sirupsen/logrus"
)

var (
	// Log contains the shared Logger
	Log *logrus.Logger

	stderrHook *writerHook
	fileHook   *writerHook

	// Valid log levels
	levelsArray = []string{"panic", "fatal", "error", "warn", "info", "debug", "trace"}

	// Valid log colors
	colorsArray = []string{"always", "auto", "never"}
)

const (
	// LevelsPlaceholder are all valid log levels separated by '|' character.
	LevelsPlaceholder = "(panic|fatal|error|warn|info|debug|trace)"

	// LevelsFlag is the suggested name of the flag for loglevel
	LevelsFlag = "log-level"

	// LevelsHelp is the suggested help message for the loglevel flag
	LevelsHelp = "The minimum log level."

	// FileFlag is the suggested name for logfile flag
	FileFlag = "log-file"

	// FileFlagHelp is the suggested help message for the logfile flag
	FileFlagHelp = "Path to the image's log file."

	// ColorsPlaceholder are all valid log colors separated by '|' character.
	ColorsPlaceholder = "(always|auto|never)"

	// ColorFlag is the suggested name for logcolor flag
	ColorFlag = "log-color"

	// ColorFlagHelp is the suggested help message for the logcolor flag
	ColorFlagHelp = "Color setting for log terminal output."

	defaultLogFileLevel   = logrus.DebugLevel
	defaultStderrLogLevel = logrus.InfoLevel
	parentCallerLevel     = 1
	colorModeAuto         = "auto"
	colorModeAlways       = "always"
	colorModeNever        = "never"
)

type LogFlags struct {
	LogColor *string
	LogFile  *string
	LogLevel *string
}

// initLogFile initializes the common logger with a file
func initLogFile(filePath string, color string) (err error) {
	useColors := false
	if color == colorModeAlways {
		useColors = true
	}
	const (
		noToolName = ""
	)

	err = os.MkdirAll(filepath.Dir(filePath), os.ModePerm)
	if err != nil {
		return
	}

	file, err := os.Create(filePath)
	if err != nil {
		return
	}

	fileHook = newWriterHook(file, defaultLogFileLevel, useColors, noToolName)
	Log.Hooks.Add(fileHook)
	Log.SetLevel(defaultLogFileLevel)

	return
}

// InitStderrLog initializes the logger to print to stderr
func InitStderrLog() {
	_, callerFilePath, _, ok := runtime.Caller(parentCallerLevel)
	if !ok {
		log.Panic("Failed to get caller info.")
	}

	initStderrLogInternal(callerFilePath, colorModeAuto)
}

// SetFileLogLevel sets the lowest log level for file output
func SetFileLogLevel(level string) (err error) {
	return setHookLogLevel(fileHook, level)
}

// SetStderrLogLevel sets the lowest log level for stderr output
func SetStderrLogLevel(level string) (err error) {
	return setHookLogLevel(stderrHook, level)
}

// InitBestEffort runs InitStderrLog always, and InitLogFile if path is not empty
func InitBestEffort(lf *LogFlags) {
	level := *lf.LogLevel
	color := *lf.LogColor
	path := *lf.LogFile

	if level == "" {
		level = defaultStderrLogLevel.String()
	}

	_, callerFilePath, _, ok := runtime.Caller(parentCallerLevel)
	if !ok {
		log.Panic("Failed to get caller info.")
	}

	initStderrLogInternal(callerFilePath, color)

	if path != "" {
		PanicOnError(initLogFile(path, color), "Failed while setting log file (%s).", path)
	}

	PanicOnError(SetStderrLogLevel(level), "Failed while setting log level.")
}

// Levels returns list of strings representing valid log levels.
func Levels() []string {
	return levelsArray
}

// Colors returns list of strings representing valid log colors.
func Colors() []string {
	return colorsArray
}

// PanicOnError logs the error and any message strings and then panics
func PanicOnError(err interface{}, args ...interface{}) {
	if err != nil {
		if len(args) > 0 {
			Log.Errorf(args[0].(string), args[1:]...)
		}

		Log.Panicln(err)
	}
}

// WarningOnError logs a warning error and any message strings
func WarningOnError(err interface{}, args ...interface{}) {
	if err != nil {
		if len(args) > 0 {
			Log.Warningf(args[0].(string), args[1:]...)
		}
	}
}

// ReplaceStderrWriter replaces the stderr writer and returns the old one
func ReplaceStderrWriter(newOut io.Writer) (oldOut io.Writer) {
	return stderrHook.ReplaceWriter(newOut)
}

// ReplaceStderrFormatter replaces the stderr formatter and returns the old formatter
func ReplaceStderrFormatter(newFormatter logrus.Formatter) (oldFormatter logrus.Formatter) {
	return stderrHook.ReplaceFormatter(newFormatter)
}

func initStderrLogInternal(callerFilePath string, color string) {
	useColors := true
	if color == colorModeNever {
		useColors = false
	}

	Log = logrus.New()
	Log.ReportCaller = true

	toolName := strings.TrimSuffix(filepath.Base(callerFilePath), ".go")

	// By default send all log messages through stderrHook
	stderrHook = newWriterHook(os.Stderr, defaultStderrLogLevel, useColors, toolName)
	Log.AddHook(stderrHook)
	Log.SetLevel(defaultStderrLogLevel)
	Log.SetOutput(io.Discard)
}

func setHookLogLevel(hook *writerHook, level string) (err error) {
	logLevel, err := logrus.ParseLevel(level)
	if err != nil {
		return
	}

	// Update the base logger level if its not at least equal to the hook level
	// Otherwise the hook will not receive any entries
	if logLevel > hook.CurrentLevel() {
		Log.SetLevel(logLevel)
	}

	hook.SetLevel(logLevel)
	return
}

// PrintMessageBox prints a message box to the log with the specified log level.
func PrintMessageBox(level logrus.Level, message []string) {
	for _, line := range FormatMessageBox(message) {
		Log.Log(level, line)
	}
}

// FormatMessageBox formats a message into a box with a border. The box is automatically sized to fit the longest line.
// Each line will be centered in the box.
func FormatMessageBox(message []string) []string {
	maxLineLength := 0
	for _, line := range message {
		len := utf8.RuneCountInString(line)
		if len > maxLineLength {
			maxLineLength = len
		}
	}
	lines := []string{messageBoxTopString(maxLineLength)}
	for _, line := range message {
		lines = append(lines, messageBoxMiddleString(line, maxLineLength))
	}
	lines = append(lines, messageBoxBottomString(maxLineLength))
	return lines
}

func messageBoxTopString(width int) string {
	return fmt.Sprintf("╔═%s═╗", strings.Repeat("═", width))
}

func messageBoxMiddleString(s string, width int) string {
	return fmt.Sprintf("║ %s ║", messageBoxPadString(s, width))
}

func messageBoxBottomString(width int) string {
	return fmt.Sprintf("╚═%s═╝", strings.Repeat("═", width))
}

func messageBoxPadString(s string, width int) string {
	lineLen := utf8.RuneCountInString(s)
	if lineLen >= width {
		return s
	}
	padding := width - lineLen
	paddingL := padding / 2
	paddingR := padding - paddingL
	return fmt.Sprintf("%s%s%s", strings.Repeat(" ", paddingL), s, strings.Repeat(" ", paddingR))
}
