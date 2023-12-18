// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package shell

import (
	"bytes"
	"fmt"
	"os"
	"os/exec"
	"strings"
	"sync"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"

	"golang.org/x/sys/unix"
)

// ShellProgram is the default shell program used by the tooling.
const ShellProgram = "/bin/bash"

var (
	activeCommands = make(map[*exec.Cmd]bool)
	// Guards activeCommands
	activeCommandsMutex  sync.Mutex
	allowProcessCreation = true

	currentEnv = os.Environ()
)

// SetEnvironment sets the default environment variables to be used for all processes launched from this package.
func SetEnvironment(env []string) {
	currentEnv = env
}

// CurrentEnvironment returns the current environment variables that are being used for all processes launched from this package.
func CurrentEnvironment() []string {
	return currentEnv
}

// PermanentlyStopAllChildProcesses will send the provided signal to all processes spawned by this package,
// and all of those process's children.
// Invoking this will also block future process creation, causing the Execute methods to return an error.
func PermanentlyStopAllChildProcesses(signal unix.Signal) {
	// Acquire the global activeCommandsMutex to ensure no
	// new commands are executed during this teardown routine
	logger.Log.Info("Waiting for outstanding processes to be created")

	activeCommandsMutex.Lock()
	defer activeCommandsMutex.Unlock()

	// Disallow future processes from being created
	allowProcessCreation = false

	// For every running process, issue the provided signal to its process group,
	// resulting in both the process and all of its children being stopped.
	for cmd := range activeCommands {
		logger.Log.Infof("Stopping (%s)", cmd.Path)

		// Issue the provided signal to the negative Pid, this signifies it should be
		// sent to the process's process group.
		err := unix.Kill(-cmd.Process.Pid, signal)
		if err != nil {
			logger.Log.Errorf("Unable to stop (%s): %v", strings.Join(cmd.Args, " "), err)
			continue
		}

		// Wait for the process to fully exit
		cmd.Wait()
	}
}

// Execute runs the provided command.
func Execute(program string, args ...string) (stdout, stderr string, err error) {
	return ExecuteInDirectory("", program, args...)
}

// Execute runs the provided command in a specific working directory.
func ExecuteInDirectory(workingDirectory, program string, args ...string) (stdout, stderr string, err error) {
	var (
		outBuf bytes.Buffer
		errBuf bytes.Buffer
	)

	cmd := exec.Command(program, args...)
	cmd.Stdout = &outBuf
	cmd.Stderr = &errBuf

	if workingDirectory != "" {
		cmd.Dir = workingDirectory
	}

	err = trackAndStartProcess(cmd)
	if err != nil {
		return
	}

	defer untrackProcess(cmd)

	err = cmd.Wait()
	return outBuf.String(), errBuf.String(), err
}

// ExecuteWithStdin - Run the command and use Stdin to pass input during execution
func ExecuteWithStdin(input, program string, args ...string) (stdout, stderr string, err error) {
	var (
		outBuf bytes.Buffer
		errBuf bytes.Buffer
	)

	cmd := exec.Command(program, args...)
	cmd.Stdout = &outBuf
	cmd.Stderr = &errBuf
	cmd.Stdin = strings.NewReader(input)

	err = trackAndStartProcess(cmd)
	if err != nil {
		return
	}

	defer untrackProcess(cmd)

	err = cmd.Wait()
	return outBuf.String(), errBuf.String(), err
}

// ExecuteLive runs a command in the shell and logs it in real-time
func ExecuteLive(squashErrors bool, program string, args ...string) (err error) {
	var (
		onStdout func(...interface{})
		onStderr func(...interface{})
	)

	onStdout = logger.Log.Debug
	if squashErrors {
		onStderr = logger.Log.Debug
	} else {
		onStderr = logger.Log.Warn
	}

	return ExecuteLiveWithCallback(onStdout, onStderr, false, program, args...)
}

// ExecuteLiveWithErr runs a command in the shell and logs it in real-time.
// In addition, if there is an error, the last x lines of stderr will be attached to the err object.
func ExecuteLiveWithErr(stderrLines int, program string, args ...string) (err error) {
	return ExecuteLiveWithErrAndCallbacks(stderrLines, logger.Log.Debug, logger.Log.Debug, program, args...)
}

// ExecuteLiveWithErr runs a command in the shell and logs it in real-time.
// In addition, if there is an error, the last x lines of stderr will be attached to the err object.
func ExecuteLiveWithErrAndCallbacks(stderrLines int, onStdout, onStderr func(...interface{}), program string,
	args ...string,
) (err error) {
	stderrChan := make(chan string, stderrLines)

	err = ExecuteLiveWithCallbackAndChannels(onStdout, onStderr, nil, stderrChan, program, args...)
	close(stderrChan)
	if err != nil {
		errLines := ""
		for errLine := range stderrChan {
			if errLines != "" {
				errLines += "\n"
			}
			errLines += errLine
		}

		if errLines != "" {
			err = fmt.Errorf("%s\n%w", errLines, err)
		}
		return
	}
	return nil
}

// ExecuteLiveWithCallback runs a command in the shell and invokes the provided callbacks in real-time on each line of stdout and stderr.
// If printOutputOnError is true, the full output of the command will be printed after completion if the command returns an error. In the event
// the buffer becomes full the oldest buffered output is discarded.
func ExecuteLiveWithCallback(onStdout, onStderr func(...interface{}), printOutputOnError bool, program string, args ...string) (err error) {
	var outputChan chan string
	const outputChanBufferSize = 1500

	if printOutputOnError {
		outputChan = make(chan string, outputChanBufferSize)
	}

	err = ExecuteLiveWithCallbackAndChannels(onStdout, onStderr, outputChan, outputChan, program, args...)
	if err != nil {
		return
	}

	// Optionally dump the output in the event of an error
	if outputChan != nil {
		close(outputChan)
	}
	if err != nil && printOutputOnError {
		logger.Log.Errorf("Call to %s returned error, last %d lines of output:", program, outputChanBufferSize)
		for line := range outputChan {
			logger.Log.Warn(line)
		}
	}

	return
}

func ExecuteLiveWithCallbackAndChannels(onStdout, onStderr func(...interface{}),
	stdoutChannel, stderrChannel chan string,
	program string, args ...string,
) (err error) {
	cmd := exec.Command(program, args...)

	stdoutPipe, err := cmd.StdoutPipe()
	if err != nil {
		logger.Log.Error("ExecuteLive failed to start StdoutPipe ", err)
		return
	}
	defer stdoutPipe.Close()

	stderrPipe, err := cmd.StderrPipe()
	if err != nil {
		logger.Log.Error("ExecuteLive failed to start StderrPipe ", err)
		return
	}
	defer stderrPipe.Close()

	err = trackAndStartProcess(cmd)
	if err != nil {
		return
	}

	defer untrackProcess(cmd)

	wg := new(sync.WaitGroup)
	wg.Add(2)

	go logger.StreamOutput(stdoutPipe, onStdout, wg, stdoutChannel)
	go logger.StreamOutput(stderrPipe, onStderr, wg, stderrChannel)

	wg.Wait()
	err = cmd.Wait()

	return
}

// ExecuteAndLogToFile runs a command in the shell and redirects stdout to the given file
func ExecuteAndLogToFile(filepath string, command string, args ...string) {
	var (
		errBuf bytes.Buffer
	)
	cmd := exec.Command(command, args...)
	outfile, err := os.Create(filepath)
	if err != nil {
		logger.Log.Errorf("Unable to create file '%s'. Error: %s", filepath, err)
		return
	}
	defer outfile.Close()
	cmd.Stdout = outfile
	cmd.Stderr = &errBuf
	err = cmd.Start()
	if err != nil {
		logger.Log.Errorf("Unable to start command '%s %s'. Error: '%s'", command, strings.Join(args, " "), err)
		return
	}
	err = cmd.Wait()
	if err != nil {
		logger.Log.Errorf("Command '%s' failed with: '%s'. Error: '%s'", command, errBuf.String(), err)
		return
	}
	return
}

// MustExecuteLive executes the shell command.
// Panics on failure.
func MustExecuteLive(command string, args ...string) {
	const squashErrors = false

	err := ExecuteLive(squashErrors, command, args...)
	if err != nil {
		logger.Log.Panicf("Command '%s' failed with error: %v", command, err)
	}
}

func trackAndStartProcess(cmd *exec.Cmd) (err error) {
	logger.Log.Debugf("Executing: %v", cmd.Args)

	if len(currentEnv) > 0 {
		cmd.Env = currentEnv
	}

	activeCommandsMutex.Lock()
	defer activeCommandsMutex.Unlock()

	if !allowProcessCreation {
		return fmt.Errorf("process creation is not allowed")
	}

	// Make the process, and any children it spawns, belong to a new process group
	cmd.SysProcAttr = &unix.SysProcAttr{Setpgid: true}

	err = cmd.Start()
	if err != nil {
		return
	}

	activeCommands[cmd] = true

	return
}

func untrackProcess(cmd *exec.Cmd) {
	activeCommandsMutex.Lock()
	defer activeCommandsMutex.Unlock()

	delete(activeCommands, cmd)
}
