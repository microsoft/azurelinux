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

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/sirupsen/logrus"

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
	return NewExecBuilder(program, args...).
		LogLevel(logrus.TraceLevel, logrus.DebugLevel).
		ExecuteCaptureOuput()
}

// ExecuteWithStdin - Run the command and use Stdin to pass input during execution
func ExecuteWithStdin(input, program string, args ...string) (stdout, stderr string, err error) {
	return NewExecBuilder(program, args...).
		LogLevel(logrus.TraceLevel, logrus.DebugLevel).
		Stdin(input).
		ExecuteCaptureOuput()
}

// ExecuteLive runs a command in the shell and logs it in real-time
func ExecuteLive(squashErrors bool, program string, args ...string) (err error) {
	b := NewExecBuilder(program, args...).
		LogLevel(logrus.DebugLevel, logrus.DebugLevel)

	if !squashErrors {
		b = b.StderrLogLevel(logrus.WarnLevel)
	}

	return b.Execute()
}

// ExecuteLiveWithErr runs a command in the shell and logs it in real-time.
// In addition, if there is an error, the last x lines of stderr will be attached to the err object.
func ExecuteLiveWithErr(stderrLines int, program string, args ...string) (err error) {
	return NewExecBuilder(program, args...).
		LogLevel(logrus.DebugLevel, logrus.DebugLevel).
		ErrorStderrLines(stderrLines).
		Execute()
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

	if cmd.Env == nil && len(currentEnv) > 0 {
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
