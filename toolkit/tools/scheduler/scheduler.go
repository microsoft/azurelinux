// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"os"

	"gopkg.in/alecthomas/kingpin.v2"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/scheduler"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/scheduler/buildagents"
)

const (
	// default worker count to 0 to automatically scale with the number of logical CPUs.
	defaultWorkerCount   = "0"
	defaultBuildAttempts = "1"
)

var (
	app = kingpin.New("scheduler", "A tool to schedule package builds from a dependency graph.")

	inputGraphFile  = exe.InputFlag(app, "Path to the DOT graph file to build.")
	outputGraphFile = exe.OutputFlag(app, "Path to save the built DOT graph file.")

	outputCSVFile = app.Flag("output-build-state-csv-file", "Path to save the CSV file.").Required().String()
	workDir       = app.Flag("work-dir", "The directory to create the build folder").Required().String()
	workerTar     = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz").Required().ExistingFile()
	repoFile      = app.Flag("repo-file", "Full path to local.repo").Required().ExistingFile()
	rpmDir        = app.Flag("rpm-dir", "The directory to use as the local repo and to submit RPM packages to").Required().ExistingDir()
	srpmDir       = app.Flag("srpm-dir", "The output directory for source RPM packages").Required().String()
	cacheDir      = app.Flag("cache-dir", "The cache directory containing downloaded dependency RPMS from Mariner Base").Required().ExistingDir()
	buildLogsDir  = app.Flag("build-logs-dir", "Directory to store package build logs").Required().ExistingDir()

	imageConfig = app.Flag("image-config-file", "Optional image config file to extract a package list from.").String()
	baseDirPath = app.Flag("base-dir", "Base directory for relative file paths from the config. Defaults to config's directory.").ExistingDir()

	distTag              = app.Flag("dist-tag", "The distribution tag SRPMs will be built with.").Required().String()
	distroReleaseVersion = app.Flag("distro-release-version", "The distro release version that the SRPM will be built with.").Required().String()
	distroBuildNumber    = app.Flag("distro-build-number", "The distro build number that the SRPM will be built with.").Required().String()
	rpmmacrosFile        = app.Flag("rpmmacros-file", "Optional file path to an rpmmacros file for rpmbuild to use.").ExistingFile()
	buildAttempts        = app.Flag("build-attempts", "Sets the number of times to try building a package.").Default(defaultBuildAttempts).Int()
	runCheck             = app.Flag("run-check", "Run the check during package builds.").Bool()
	noCleanup            = app.Flag("no-cleanup", "Whether or not to delete the chroot folder after the build is done").Bool()
	noCache              = app.Flag("no-cache", "Disables using prebuilt cached packages.").Bool()
	stopOnFailure        = app.Flag("stop-on-failure", "Stop on failed build").Bool()
	reservedFileListFile = app.Flag("reserved-file-list-file", "Path to a list of files which should not be generated during a build").ExistingFile()
	deltaBuild           = app.Flag("delta-build", "Enable delta build using remote cached packages.").Bool()

	validBuildAgentFlags = []string{buildagents.TestAgentFlag, buildagents.ChrootAgentFlag}
	buildAgent           = app.Flag("build-agent", "Type of build agent to build packages with.").PlaceHolder(exe.PlaceHolderize(validBuildAgentFlags)).Required().Enum(validBuildAgentFlags...)
	buildAgentProgram    = app.Flag("build-agent-program", "Path to the build agent that will be invoked to build packages.").String()
	workers              = app.Flag("workers", "Number of concurrent build agents to spawn. If set to 0, will automatically set to the logical CPU count.").Default(defaultWorkerCount).Int()

	ignoredPackages = app.Flag("ignored-packages", "Space separated list of specs ignoring rebuilds if their dependencies have been updated. Will still build if all of the spec's RPMs have not been built.").String()

	pkgsToBuild   = app.Flag("packages", "Space separated list of top-level packages that should be built. Omit this argument to build all packages.").String()
	pkgsToRebuild = app.Flag("rebuild-packages", "Space separated list of base package names packages that should be rebuilt.").String()

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)
)

func populateSchedulerConfig() *scheduler.Config {
	return &scheduler.Config{
		InputGraphFile:       *inputGraphFile,
		OutputGraphFile:      *outputGraphFile,
		OutputCSVFile:        *outputCSVFile,
		WorkDir:              *workDir,
		WorkerTar:            *workerTar,
		RepoFile:             *repoFile,
		RpmDir:               *rpmDir,
		SrpmDir:              *srpmDir,
		CacheDir:             *cacheDir,
		BuildLogsDir:         *buildLogsDir,
		ImageConfig:          *imageConfig,
		BaseDirPath:          *baseDirPath,
		DistTag:              *distTag,
		DistroReleaseVersion: *distroReleaseVersion,
		DistroBuildNumber:    *distroBuildNumber,
		RpmmacrosFile:        *rpmmacrosFile,
		BuildAttempts:        *buildAttempts,
		RunCheck:             *runCheck,
		NoCleanup:            *noCleanup,
		NoCache:              *noCache,
		StopOnFailure:        *stopOnFailure,
		ReservedFileListFile: *reservedFileListFile,
		DeltaBuild:           *deltaBuild,
		ValidBuildAgentFlags: validBuildAgentFlags,
		BuildAgent:           *buildAgent,
		BuildAgentProgram:    *buildAgentProgram,
		Workers:              *workers,
		IgnoredPackages:      *ignoredPackages,
		PkgsToBuild:          *pkgsToBuild,
		PkgsToRebuild:        *pkgsToRebuild,
		LogFile:              *logFile,
		LogLevel:             *logLevel,
	}

}

func main() {
	app.Version(exe.ToolkitVersion)

	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	cfg := populateSchedulerConfig()
	err := cfg.ScheduleBuild()
	if err != nil {
		logger.Log.Fatalf("Unable to build package graph.\nFor details see the build summary section above.\nError: %s", err)
	}
}
