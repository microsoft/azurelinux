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

	"golang.org/x/sys/unix"
	"microsoft.com/pkggen/internal/logger"
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

// PermanentlyStopAllProcesses will send the provided signal to all processes spawned by this package,
// and all of those process's children.
// Invoking this will also block future process creation, causing the Execute methods to return an error.
func PermanentlyStopAllProcesses(signal unix.Signal) {
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
		processCommand := strings.Join(cmd.Args, " ")
		logger.Log.Infof("Stopping (%s)", processCommand)

		// Issue the provided signal to the negative Pid, this signifies it should be
		// sent to the process's process group.
		err := unix.Kill(-cmd.Process.Pid, signal)
		if err != nil {
			logger.Log.Errorf("Unable to stop (%s): %v", processCommand, err)
			continue
		}

		// Wait for the process to fully exit
		cmd.Wait()
	}
}

// Execute runs the provided command.
func Execute(program string, args ...string) (stdout, stderr string, err error) {
	var (
		outBuf bytes.Buffer
		errBuf bytes.Buffer
	)

	cmd := exec.Command(program, args...)
	cmd.Stdout = &outBuf
	cmd.Stderr = &errBuf

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

	return ExecuteLiveWithCallback(onStdout, onStderr, program, args...)
}

// ExecuteLiveWithCallback runs a command in the shell and invokes the provided callbacks it in real-time on stdout and stderr.
func ExecuteLiveWithCallback(onStdout, onStderr func(...interface{}), program string, args ...string) (err error) {
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

	go logger.StreamOutput(stdoutPipe, onStdout, wg)
	go logger.StreamOutput(stderrPipe, onStderr, wg)

	wg.Wait()

	return cmd.Wait()
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
