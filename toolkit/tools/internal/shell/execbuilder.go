// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package shell

import (
	"bufio"
	"fmt"
	"io"
	"math"
	"os/exec"
	"strings"
	"sync"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/sirupsen/logrus"
)

const (
	// LogDisabledLevel is a fake logrus log level, that is used by ExecBuilder to represent that logging should be
	// disabled.
	LogDisabledLevel logrus.Level = math.MaxUint32

	// DefaultWarnLogLines is a default value that can be used with the WarnLogLines function.
	DefaultWarnLogLines int = 1500
)

type LogCallback func(line string)

type ExecBuilder struct {
	command              string
	args                 []string
	workingDirectory     string
	environmentVariables []string
	stdinString          string
	stdoutLogLevel       logrus.Level
	stderrLogLevel       logrus.Level
	stdoutCallback       LogCallback
	stderrCallback       LogCallback
	errorStderrLines     int
	warnLogLines         int
}

// NewExecBuilder initializes a new execution builder object.
func NewExecBuilder(command string, args ...string) ExecBuilder {
	b := ExecBuilder{
		command:        command,
		args:           args,
		stdoutLogLevel: logrus.DebugLevel,
		stderrLogLevel: logrus.DebugLevel,
	}
	return b
}

// WorkingDirectory sets the working directory for the command to be executed.
func (b ExecBuilder) WorkingDirectory(path string) ExecBuilder {
	b.workingDirectory = path
	return b
}

// EnvironmentVariables sets the complete list of environment variables for the command to be executed.
func (b ExecBuilder) EnvironmentVariables(environmentVariables []string) ExecBuilder {
	b.environmentVariables = environmentVariables
	return b
}

// Stdin sets a string value to be passed to the process via stdin.
func (b ExecBuilder) Stdin(value string) ExecBuilder {
	b.stdinString = value
	return b
}

// Sets the log level for stdout lines.
func (b ExecBuilder) StdoutLogLevel(stdoutLogLevel logrus.Level) ExecBuilder {
	b.stdoutLogLevel = stdoutLogLevel
	return b
}

// Sets the log level for stderr lines.
func (b ExecBuilder) StderrLogLevel(stderrLogLevel logrus.Level) ExecBuilder {
	b.stderrLogLevel = stderrLogLevel
	return b
}

// Sets the log level for stdout and stderr lines.
func (b ExecBuilder) LogLevel(stdoutLogLevel logrus.Level, stderrLogLevel logrus.Level) ExecBuilder {
	b.stdoutLogLevel = stdoutLogLevel
	b.stderrLogLevel = stderrLogLevel
	return b
}

// ErrorStderrLines sets the number of stderr lines to add to the error object, if the execution fails.
func (b ExecBuilder) ErrorStderrLines(lines int) ExecBuilder {
	b.errorStderrLines = lines
	return b
}

// WarnLogLines sets the number of stdout/stderr lines that will be printed as warning logs if the process returns an
// error.
//
// Note: This function exists for the sake of compatability with existing code. It is generally preferable to set the
// stdout and stderr log levels to an appropriate value.
func (b ExecBuilder) WarnLogLines(lines int) ExecBuilder {
	b.warnLogLines = lines
	return b
}

// StdoutCallback sets a callback function that it called for each line of stdout.
func (b ExecBuilder) StdoutCallback(stdoutCallback LogCallback) ExecBuilder {
	b.stdoutCallback = stdoutCallback
	return b
}

// StderrCallback sets a callback function that it called for each line of stderr.
func (b ExecBuilder) StderrCallback(stderrCallback LogCallback) ExecBuilder {
	b.stderrCallback = stderrCallback
	return b
}

// Callbacks sets the callback functions for both stdout and stderr.
func (b ExecBuilder) Callbacks(stdoutCallback LogCallback, stderrCallback LogCallback) ExecBuilder {
	b.stdoutCallback = stdoutCallback
	b.stderrCallback = stderrCallback
	return b
}

func (b ExecBuilder) Execute() error {
	_, _, err := b.executeHelper(false /*captureOutput*/)
	return err
}

func (b ExecBuilder) ExecuteCaptureOuput() (string, string, error) {
	return b.executeHelper(true /*captureOutput*/)
}

func (b ExecBuilder) executeHelper(captureOutput bool) (string, string, error) {
	stdoutLinesChans := []chan string(nil)
	stdErrLinesChans := []chan string(nil)

	var warnLogChan chan string
	if b.warnLogLines > 0 {
		// Setup WarnLogLines.
		warnLogChan = make(chan string, b.warnLogLines)
		stdoutLinesChans = append(stdoutLinesChans, warnLogChan)
		stdErrLinesChans = append(stdErrLinesChans, warnLogChan)
	}

	var errorChan chan string
	if b.errorStderrLines > 0 {
		// Setup ErrorStderrLines.
		errorChan = make(chan string, b.errorStderrLines)
		stdErrLinesChans = append(stdErrLinesChans, errorChan)
	}

	stdoutResultChan := chan string(nil)
	stderrResultChan := chan string(nil)
	if captureOutput {
		// Setup output capture.
		stdoutResultChan = make(chan string, 1)
		stderrResultChan = make(chan string, 1)
	}

	// Setup process.
	cmd := exec.Command(b.command, b.args...)
	cmd.Dir = b.workingDirectory
	cmd.Env = b.environmentVariables

	if b.stdinString != "" {
		cmd.Stdin = strings.NewReader(b.stdinString)
	}

	stdoutPipe, err := cmd.StdoutPipe()
	if err != nil {
		err = fmt.Errorf("failed to open stdout pipe:\n%w", err)
		return "", "", err
	}
	defer stdoutPipe.Close()

	stderrPipe, err := cmd.StderrPipe()
	if err != nil {
		err = fmt.Errorf("failed to open stderr pipe:\n%w", err)
		return "", "", err
	}
	defer stderrPipe.Close()

	// Start process.
	err = trackAndStartProcess(cmd)
	if err != nil {
		err = fmt.Errorf("failed to start process:\n%w", err)
		return "", "", err
	}

	defer untrackProcess(cmd)

	// Read stdout and stderr.
	wg := new(sync.WaitGroup)
	wg.Add(2)
	go execBuilderReadPipe(stdoutPipe, wg, b.stdoutCallback, b.stdoutLogLevel, stdoutLinesChans, stdoutResultChan)
	go execBuilderReadPipe(stderrPipe, wg, b.stderrCallback, b.stderrLogLevel, stdErrLinesChans, stderrResultChan)

	// Wait for process to exit.
	wg.Wait()
	err = cmd.Wait()

	// Cleanup the WarnLogLines and ErrorStderrLines channels.
	// Note: While technically senders are suppose to close channels, it is ok to do it here because of the use of the
	// waitgroup (wg).
	if warnLogChan != nil {
		close(warnLogChan)
	}

	if errorChan != nil {
		close(errorChan)
	}

	stdout := ""
	stderr := ""
	if captureOutput {
		// Get the string values of stdout and stderr.
		stdout = <-stdoutResultChan
		stderr = <-stderrResultChan
	}

	if err != nil {
		if warnLogChan != nil {
			// Report last x lines of process's output (stdout and stderr) as warning logs.
			logger.Log.Errorf("Call to %s returned error, last %d lines of output:", b.command, b.warnLogLines)
			for line := range warnLogChan {
				logger.Log.Warn(line)
			}
		}

		if errorChan != nil {
			// Add last x line from stderr to the error message.
			builder := strings.Builder{}
			for errLine := range errorChan {
				if builder.Len() > 0 {
					builder.WriteString("\n")
				}
				builder.WriteString(errLine)
			}

			errLines := builder.String()
			if errLines != "" {
				err = fmt.Errorf("%s\n%w", errLines, err)
			}
		}
	}

	return stdout, stderr, err
}

func execBuilderReadPipe(pipe io.Reader, wg *sync.WaitGroup, logCallback LogCallback, logLevel logrus.Level,
	linesOutputChans []chan string, outputResultChan chan string,
) {
	defer wg.Done()

	outputBuilder := strings.Builder{}

	reader := bufio.NewReader(pipe)
	for {
		// Read up to the next line.
		bytes, err := reader.ReadBytes('\n')

		// Drop \n or \r\n from line.
		omitBytes := 0
		if len(bytes) >= 1 && bytes[len(bytes)-1] == '\n' {
			omitBytes = 1
			if len(bytes) >= 2 && bytes[len(bytes)-2] == '\r' {
				omitBytes = 2
			}
		}

		line := string(bytes[:len(bytes)-omitBytes])

		if logCallback != nil {
			// Call user callback.
			logCallback(line)
		}

		if logLevel <= logrus.TraceLevel && line != "" {
			// Log the line.
			logger.Log.Log(logLevel, line)
		}

		for _, linesOutputChan := range linesOutputChans {
			channelDropAndPush(line, linesOutputChan)
		}

		if outputResultChan != nil {
			// Collect the entire stream into a single string.
			outputBuilder.Write(bytes)
		}

		if err != nil {
			break
		}
	}

	if outputResultChan != nil {
		// Return the full stream as a string.
		output := outputBuilder.String()
		outputResultChan <- output
		close(outputResultChan)
	}
}

// channelDropAndPush treats a channel as a circular buffer.
func channelDropAndPush(line string, outputChan chan string) {
	const maxRetries = 8

	for i := 0; i < maxRetries; i++ {
		if len(outputChan) == cap(outputChan) {
			// The buffer is full, discard the oldest value.
			select {
			case <-outputChan:
			default:
			}
		}

		select {
		case outputChan <- line:
			// Line was pushed.
			return

		default:
			// The event buffer is full, presumably from another goroutine pushing an entry.
			// So, loop back around and try again.
		}
	}
}
