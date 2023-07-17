// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package buildagents

import (
	"fmt"
	"path/filepath"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

// ChrootAgentFlag is the build-agent option for ChrootAgent.
const ChrootAgentFlag = "chroot-agent"

// ChrootAgent implements the BuildAgent interface to build SRPMs using a local chroot.
type ChrootAgent struct {
	config *BuildAgentConfig
}

// NewChrootAgent returns a new ChrootAgent.
func NewChrootAgent() *ChrootAgent {
	return &ChrootAgent{}
}

// Initialize initializes the chroot agent with the given configuration.
func (c *ChrootAgent) Initialize(config *BuildAgentConfig) (err error) {
	c.config = config
	return
}

// BuildPackage builds a given file and returns the output files or error.
// - inputFile is the SRPM to build.
// - logName is the file name to save the package build log to.
// - outArch is the target architecture to build for.
// - dependencies is a list of dependencies that need to be installed before building.
func (c *ChrootAgent) BuildPackage(inputFile, logName, outArch string, dependencies []string) (builtFiles []string, logFile string, err error) {
	// On success, pkgworker will print a comma-seperated list of all RPMs built to stdout.
	// This will be the last stdout line written.
	const delimiter = ","

	logFile = filepath.Join(c.config.LogDir, logName)

	var lastStdoutLine string
	onStdout := func(args ...interface{}) {
		if len(args) == 0 {
			return
		}

		lastStdoutLine = strings.TrimSpace(args[0].(string))
		logger.Log.Trace(lastStdoutLine)
	}

	args := serializeChrootBuildConfig(c.config, inputFile, logFile, outArch, dependencies)
	err = shell.ExecuteLiveWithCallback(onStdout, logger.Log.Trace, true, c.config.Program, args...)

	if err == nil && lastStdoutLine != "" {
		builtFiles = strings.Split(lastStdoutLine, delimiter)
	}

	return
}

// Config returns a copy of the agent's configuration.
func (c *ChrootAgent) Config() (config BuildAgentConfig) {
	return *c.config
}

// Close closes the ChrootAgent, releasing any resources.
func (c *ChrootAgent) Close() (err error) {
	return
}

// TestPackage runs the '%check' section for the given input and returns a path to the test log.
// - inputFile is the SRPM to test.
// - logName is the file name to save the package test log to.
// - dependencies is a list of dependencies that need to be installed before testing.
func (c *ChrootAgent) TestPackage(inputFile, logName string, dependencies []string) (logFile string, err error) {
	logFile = filepath.Join(c.config.LogDir, logName)

	args := serializeChrootTestConfig(c.config, inputFile, logFile, dependencies)

	_, stderr, err := shell.Execute(c.config.Program, args...)
	if err != nil {
		err = fmt.Errorf("failed to run pkgworker.\nError:\n%w\nStderr:\n%s", err, stderr)
	}

	return
}

// serializeChrootBuildConfig serializes a BuildAgentConfig into arguments usable by pkgworker for the sake of building the package.
func serializeChrootBuildConfig(config *BuildAgentConfig, inputFile, logFile, outArch string, dependencies []string) (serializedArgs []string) {
	serializedArgs = []string{
		fmt.Sprintf("--input=%s", inputFile),
		fmt.Sprintf("--work-dir=%s", config.WorkDir),
		fmt.Sprintf("--worker-tar=%s", config.WorkerTar),
		fmt.Sprintf("--repo-file=%s", config.RepoFile),
		fmt.Sprintf("--rpm-dir=%s", config.RpmDir),
		fmt.Sprintf("--toolchain-rpms-dir=%s", config.ToolchainDir),
		fmt.Sprintf("--srpm-dir=%s", config.SrpmDir),
		fmt.Sprintf("--cache-dir=%s", config.CacheDir),
		fmt.Sprintf("--ccache-dir=%s", config.CCacheDir),
		fmt.Sprintf("--dist-tag=%s", config.DistTag),
		fmt.Sprintf("--distro-release-version=%s", config.DistroReleaseVersion),
		fmt.Sprintf("--distro-build-number=%s", config.DistroBuildNumber),
		fmt.Sprintf("--log-file=%s", logFile),
		fmt.Sprintf("--log-level=%s", config.LogLevel),
		fmt.Sprintf("--out-arch=%s", outArch),
		fmt.Sprintf("--max-cpu=%s", config.MaxCpu),
	}

	if config.RpmmacrosFile != "" {
		serializedArgs = append(serializedArgs, fmt.Sprintf("--rpmmacros-file=%s", config.RpmmacrosFile))
	}

	if config.NoCleanup {
		serializedArgs = append(serializedArgs, "--no-cleanup")
	}

	if config.RunCheck {
		serializedArgs = append(serializedArgs, "--run-check")
	}

	if config.UseCcache {
		serializedArgs = append(serializedArgs, "--use-ccache")
	}

	for _, dependency := range dependencies {
		serializedArgs = append(serializedArgs, fmt.Sprintf("--install-package=%s", dependency))
	}

	return
}

// serializeChrootTestConfig serializes a BuildAgentConfig into arguments usable by pkgworker for the sake of testing the package.
func serializeChrootTestConfig(config *BuildAgentConfig, inputFile, logFile string, dependencies []string) (serializedArgs []string) {
	serializedArgs = []string{
		fmt.Sprintf("--input=%s", inputFile),
		fmt.Sprintf("--work-dir=%s", config.WorkDir),
		fmt.Sprintf("--worker-tar=%s", config.WorkerTar),
		fmt.Sprintf("--repo-file=%s", config.RepoFile),
		fmt.Sprintf("--rpm-dir=%s", config.RpmDir),
		fmt.Sprintf("--toolchain-rpms-dir=%s", config.ToolchainDir),
		fmt.Sprintf("--srpm-dir=%s", config.SrpmDir),
		fmt.Sprintf("--cache-dir=%s", config.CacheDir),
		fmt.Sprintf("--ccache-dir=%s", config.CCacheDir),
		fmt.Sprintf("--dist-tag=%s", config.DistTag),
		fmt.Sprintf("--distro-release-version=%s", config.DistroReleaseVersion),
		fmt.Sprintf("--distro-build-number=%s", config.DistroBuildNumber),
		fmt.Sprintf("--log-file=%s", logFile),
		fmt.Sprintf("--log-level=%s", config.LogLevel),
		fmt.Sprintf("--max-cpu=%s", config.MaxCpu),
		fmt.Sprintf("--run-check"),
	}

	if config.RpmmacrosFile != "" {
		serializedArgs = append(serializedArgs, fmt.Sprintf("--rpmmacros-file=%s", config.RpmmacrosFile))
	}

	if config.NoCleanup {
		serializedArgs = append(serializedArgs, "--no-cleanup")
	}

	if config.UseCcache {
		serializedArgs = append(serializedArgs, "--use-ccache")
	}

	for _, dependency := range dependencies {
		serializedArgs = append(serializedArgs, fmt.Sprintf("--install-package=%s", dependency))
	}

	return
}
