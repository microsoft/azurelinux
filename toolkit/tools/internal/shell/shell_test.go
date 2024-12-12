package shell

import (
	"bufio"
	"os"
	"os/exec"
	"path"
	"syscall"
	"testing"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	os.Exit(m.Run())
}

func resetState() {
	activeCommandsMutex.Lock()
	defer activeCommandsMutex.Unlock()
	allowProcessCreation = true
	for cmd := range activeCommands {
		cmd.Process.Kill()
	}
	activeCommands = make(map[*exec.Cmd]bool)
}

// file package has a cyclic dependency on shell package, re-implement ReadLines here
func readLinesHelper(t *testing.T, path string) (lines []string) {
	t.Helper()
	handle, err := os.Open(path)
	if err != nil {
		t.Fatalf("Failed to open file %s, error: %s", path, err)
	}
	defer handle.Close()

	scanner := bufio.NewScanner(handle)

	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		t.Fatalf("Failed to read file %s, error: %s", path, err)
	}

	return lines
}

func TestPermanentlyStopAllChildProcesses(t *testing.T) {
	tests := []struct {
		name   string
		signal syscall.Signal
		script string
	}{
		{
			name:   "SIGTERM",
			signal: syscall.SIGTERM,
			script: path.Join(".", "testdata", "will_exit.sh"),
		},
		{
			name:   "SIGKILL",
			signal: syscall.SIGKILL,
			script: path.Join(".", "testdata", "will_exit.sh"),
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			t.Cleanup(resetState)
			logger.Log.Warnf("Running test %s", tt.name)
			// bash command that echos counting numbers to a temp file
			tempFile := path.Join(t.TempDir(), "tempFile")
			bashArgs := []string{t.Name(), tempFile}
			cmd := exec.Command(tt.script, bashArgs...)

			var trackError error = nil
			go func() {
				trackError = trackAndStartProcess(cmd)
			}()

			// Sleep for 2.2 seconds to allow the child process to start and write to the temp file
			// It should write the name of the test and then the numbers 1,2,3 before being killed
			time.Sleep(2200 * time.Millisecond)

			// Call the function to stop all child processes
			results := PermanentlyStopAllChildProcesses(tt.signal, nil)

			// Get the exit code from  cmd
			err := results[cmd]
			logger.Log.Infof("Exit code: %v", err)
			// Check if the child process was stopped by sending a signal
			if err, ok := err.(*exec.ExitError); ok {
				if status, ok := err.Sys().(syscall.WaitStatus); ok {
					if !status.Signaled() || status.Signal() != tt.signal {
						t.Errorf("Expected child process to be stopped with %s, but got signal: %v", tt.name, status.Signal())
					}
				}
			}

			// Check if the allowProcessCreation flag is set to false
			if allowProcessCreation {
				t.Error("Expected allowProcessCreation to be false, but it is true")
			}

			// Check if the trackAndStartProcess function returned an error
			assert.NoError(t, trackError)

			// Check if we wrote to the temp file as expected
			expectedOutput := []string{t.Name(), "START", "MIDDLE"}
			actualOutput := readLinesHelper(t, tempFile)
			assert.Equal(t, expectedOutput, actualOutput)
		})
	}
}

func TestTimeoutAfterIgnoreSignal(t *testing.T) {
	t.Cleanup(resetState)
	// bash command that echos counting numbers to a temp file
	script := path.Join(".", "testdata", "trap.sh")
	tempFile := path.Join(t.TempDir(), "tempFile")
	bashArgs := []string{t.Name(), tempFile}
	cmd := exec.Command(script, bashArgs...)

	var trackError error = nil
	go func() {
		trackError = trackAndStartProcess(cmd)
	}()

	// Timeout after 2.2 seconds.
	delay := 200 * time.Millisecond
	timeout := 2000 * time.Millisecond
	// Give a bit of extra time for the child process to start and write to the file
	time.Sleep(delay)
	// Call the function to stop all child processes. Set timout to
	results := PermanentlyStopAllChildProcesses(syscall.SIGTERM, &timeout)

	// Get the exit code from  cmd
	err := results[cmd]
	logger.Log.Infof("Exit code: %v", err)

	// We should see the timeout error wrapped here
	assert.ErrorIs(t, err, ErrProcessTerminateTimeout)

	// Check if the allowProcessCreation flag is set to false
	if allowProcessCreation {
		t.Error("Expected allowProcessCreation to be false, but it is true")
	}

	// Check if the trackAndStartProcess function returned an error
	assert.NoError(t, trackError)

	// Check if we wrote to the temp file as expected
	expectedOutput := []string{t.Name(), "START", "MIDDLE"}
	actualOutput := readLinesHelper(t, tempFile)
	assert.Equal(t, expectedOutput, actualOutput)
}
