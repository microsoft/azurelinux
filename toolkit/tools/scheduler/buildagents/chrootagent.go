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
// - basePackageName is the base package name (i.e. 'kernel').
// - inputFile is the SRPM to build.
// - logName is the file name to save the package build log to.
// - outArch is the target architecture to build for.
// - runCheck is true if the package should run the "%check" section during the build
// - dependencies is a list of dependencies that need to be installed before building.
func (c *ChrootAgent) BuildPackage(basePackageName, inputFile, logName, outArch string, runCheck bool, dependencies []string) (builtFiles []string, logFile string, err error) {
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

	args := serializeChrootBuildAgentConfig(c.config, basePackageName, inputFile, logFile, outArch, runCheck, dependencies)
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

// serializeChrootBuildAgentConfig serializes a BuildAgentConfig into arguments usable by pkgworker for the sake of building the package.
func serializeChrootBuildAgentConfig(config *BuildAgentConfig, basePackageName, inputFile, logFile, outArch string, runCheck bool, dependencies []string) (serializedArgs []string) {
	serializedArgs = []string{
		fmt.Sprintf("--input=%s", inputFile),
		fmt.Sprintf("--work-dir=%s", config.WorkDir),
		fmt.Sprintf("--worker-tar=%s", config.WorkerTar),
		fmt.Sprintf("--repo-file=%s", config.RepoFile),
		fmt.Sprintf("--rpm-dir=%s", config.RpmDir),
		fmt.Sprintf("--toolchain-rpms-dir=%s", config.ToolchainDir),
		fmt.Sprintf("--srpm-dir=%s", config.SrpmDir),
		fmt.Sprintf("--cache-dir=%s", config.CacheDir),
		fmt.Sprintf("--base-package-name=%s", basePackageName),
		fmt.Sprintf("--dist-tag=%s", config.DistTag),
		fmt.Sprintf("--distro-release-version=%s", config.DistroReleaseVersion),
		fmt.Sprintf("--distro-build-number=%s", config.DistroBuildNumber),
		fmt.Sprintf("--log-file=%s", logFile),
		fmt.Sprintf("--log-level=%s", config.LogLevel),
		fmt.Sprintf("--out-arch=%s", outArch),
		fmt.Sprintf("--max-cpu=%s", config.MaxCpu),
		fmt.Sprintf("--timeout=%s", config.Timeout.String()),
	}

	if config.RpmmacrosFile != "" {
		serializedArgs = append(serializedArgs, fmt.Sprintf("--rpmmacros-file=%s", config.RpmmacrosFile))
	}

	if config.NoCleanup {
		serializedArgs = append(serializedArgs, "--no-cleanup")
	}

	if runCheck {
		serializedArgs = append(serializedArgs, "--run-check")
	}

	if config.UseCcache {
		serializedArgs = append(serializedArgs, "--use-ccache")
		serializedArgs = append(serializedArgs, fmt.Sprintf("--ccache-root-dir=%s", config.CCacheDir))
		serializedArgs = append(serializedArgs, fmt.Sprintf("--ccache-config=%s", config.CCacheConfig))
	}

	for _, dependency := range dependencies {
		serializedArgs = append(serializedArgs, fmt.Sprintf("--install-package=%s", dependency))
	}

	return
}
