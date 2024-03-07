// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package buildagents

import (
	"fmt"
	"time"
)

// BuildAgentConfig represents configuration options a BuildAgent would need to successfully build a given package.
type BuildAgentConfig struct {
	Program string

	WorkDir      string
	WorkerTar    string
	RepoFile     string
	RpmDir       string
	ToolchainDir string
	SrpmDir      string
	CacheDir     string
	CCacheDir    string
	CCacheConfig string

	DistTag              string
	DistroReleaseVersion string
	DistroBuildNumber    string
	RpmmacrosFile        string

	NoCleanup bool
	UseCcache bool
	MaxCpu    string
	Timeout   time.Duration

	LogDir   string
	LogLevel string
}

// BuildAgent provides an interface for a build agent that takes in an input package and builds it.
type BuildAgent interface {
	// Initialize initializes the build agent with the given configuration.
	Initialize(config *BuildAgentConfig) error

	// BuildPackage builds a given file and returns the output files or error.
	// - basePackageName is the base package name derived from the spec file (i.e. 'kernel').
	// - inputFile is the SRPM to build.
	// - logName is the file name to save the package build log to.
	// - outArch is the target architecture to build for.
	// - runCheck is true if the package should run the "%check" section during the build
	// - dependencies is a list of dependencies that need to be installed before building.
	BuildPackage(basePackageName, inputFile, logName, outArch string, runCheck bool, dependencies []string) ([]string, string, error)

	// Config returns a copy of the agent's configuration.
	Config() BuildAgentConfig

	// Close closes the build agent, releasing any resources.
	Close() error
}

// BuildAgentFactory returns an instance of the build agent that corresponds to the buildAgent string.
func BuildAgentFactory(buildAgent string) (agent BuildAgent, err error) {
	switch buildAgent {
	case TestAgentFlag:
		agent = NewTestAgent()
	case ChrootAgentFlag:
		agent = NewChrootAgent()
	default:
		err = fmt.Errorf("unknown build agent type (%s)", buildAgent)
	}

	return
}
