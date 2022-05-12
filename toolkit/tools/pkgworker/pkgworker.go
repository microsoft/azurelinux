// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A worker for building packages locally

package main

import (
	"fmt"
	"os"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/pkgworker"

	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app                  = kingpin.New("pkgworker", "A worker for building packages locally")
	srpmFile             = exe.InputFlag(app, "Full path to the SRPM to build")
	workDir              = app.Flag("work-dir", "The directory to create the build folder").Required().String()
	workerTar            = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz").Required().ExistingFile()
	repoFile             = app.Flag("repo-file", "Full path to local.repo").Required().ExistingFile()
	rpmsDirPath          = app.Flag("rpm-dir", "The directory to use as the local repo and to submit RPM packages to").Required().ExistingDir()
	srpmsDirPath         = app.Flag("srpm-dir", "The output directory for source RPM packages").Required().String()
	cacheDir             = app.Flag("cache-dir", "The cache directory containing downloaded dependency RPMS from CBL-Mariner Base").Required().ExistingDir()
	noCleanup            = app.Flag("no-cleanup", "Whether or not to delete the chroot folder after the build is done").Bool()
	distTag              = app.Flag("dist-tag", "The distribution tag the SPEC will be built with.").Required().String()
	distroReleaseVersion = app.Flag("distro-release-version", "The distro release version that the SRPM will be built with").Required().String()
	distroBuildNumber    = app.Flag("distro-build-number", "The distro build number that the SRPM will be built with").Required().String()
	rpmmacrosFile        = app.Flag("rpmmacros-file", "Optional file path to an rpmmacros file for rpmbuild to use").ExistingFile()
	runCheck             = app.Flag("run-check", "Run the check during package build").Bool()
	packagesToInstall    = app.Flag("install-package", "Filepaths to RPM packages that should be installed before building.").Strings()

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)
)

func populatePkgworkerConfig() *pkgworker.Config {
	return &pkgworker.Config{
		SrpmFile:             *srpmFile,
		WorkDir:              *workDir,
		WorkerTar:            *workerTar,
		RepoFile:             *repoFile,
		RpmsDirPath:          *rpmsDirPath,
		SrpmsDirPath:         *srpmsDirPath,
		CacheDir:             *cacheDir,
		NoCleanup:            *noCleanup,
		DistTag:              *distTag,
		DistroReleaseVersion: *distroReleaseVersion,
		DistroBuildNumber:    *distroBuildNumber,
		RpmmacrosFile:        *rpmmacrosFile,
		RunCheck:             *runCheck,
		PackagesToInstall:    *packagesToInstall,
	}

}

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	cfg := populatePkgworkerConfig()
	builtRPMs, err := cfg.BuildSRPMInChrootAndCopyToOut()
	logger.PanicOnError(err, "Failed to build SRPM '%s'. For details see log file: %s .", *srpmFile, *logFile)

	// On success write a comma-seperated list of RPMs built to stdout that can be parsed by the invoker.
	// Any output from logger will be on stderr so stdout will only contain this output.
	fmt.Printf(strings.Join(builtRPMs, ","))
}
