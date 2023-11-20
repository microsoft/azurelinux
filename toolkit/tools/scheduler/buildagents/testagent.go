// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package buildagents

import (
	"path/filepath"
	"time"
)

// TestAgentFlag is the build-agent option for TestAgent.
const TestAgentFlag = "test-agent"

// TestAgent implements the BuildAgent interface for testing purposes.
type TestAgent struct {
	config *BuildAgentConfig
}

// NewTestAgent returns a new TestAgent.
func NewTestAgent() *TestAgent {
	return &TestAgent{}
}

// Initialize initializes the test agent with the given configuration.
func (t *TestAgent) Initialize(config *BuildAgentConfig) (err error) {
	t.config = config
	return
}

// BuildPackage simply sleeps and then returns success for TestAgent.
func (t *TestAgent) BuildPackage(basePackageName, inputFile, logName, outArch string, runCheck bool, dependencies []string) (builtFiles []string, logFile string, err error) {
	const sleepDuration = time.Second * 5
	time.Sleep(sleepDuration)

	logFile = filepath.Join(t.config.LogDir, logName)
	return
}

// Config returns a copy of the agent's configuration.
func (t *TestAgent) Config() (config BuildAgentConfig) {
	return *t.config
}

// Close closes the TestAgent, releasing any resources.
func (t *TestAgent) Close() (err error) {
	return
}
