// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// specreader is a tool to parse spec files into a JSON structure

package main

import (
	"os"
	"path/filepath"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/exe"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	packagelist "github.com/microsoft/azurelinux/toolkit/tools/internal/packlist"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/timestamp"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/profile"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/specreaderutils"
	"github.com/microsoft/azurelinux/toolkit/tools/scheduler/schedulerutils"

	"gopkg.in/alecthomas/kingpin.v2"
)

const (
	defaultWorkerCount = "100"
)

var (
	app                     = kingpin.New("specreader", "A tool to parse spec dependencies into JSON")
	specsDir                = exe.InputDirFlag(app, "Directory to scan for SPECS")
	specList                = app.Flag("spec-list", "List of SPECs to parse. If empty will parse all SPECs.").Default("").String()
	output                  = exe.OutputFlag(app, "Output file to export the JSON")
	workers                 = app.Flag("workers", "Number of concurrent goroutines to parse with").Default(defaultWorkerCount).Int()
	buildDir                = app.Flag("build-dir", "Directory to store temporary files while parsing.").String()
	srpmsDir                = app.Flag("srpm-dir", "Directory containing SRPMs.").Required().ExistingDir()
	rpmsDir                 = app.Flag("rpm-dir", "Directory containing built RPMs.").Required().ExistingDir()
	toolchainManifest       = app.Flag("toolchain-manifest", "Path to a list of RPMs which are created by the toolchain. Will mark RPMs from this list as prebuilt.").ExistingFile()
	existingToolchainRpmDir = app.Flag("toolchain-rpms-dir", "Directory that contains already built toolchain RPMs. Should contain top level directories for architecture.").Required().ExistingDir()
	distTag                 = app.Flag("dist-tag", "The distribution tag the SPEC will be built with.").Required().String()
	workerTar               = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz.  If this argument is empty, specs will be parsed in the host environment.").ExistingFile()
	targetArch              = app.Flag("target-arch", "The architecture of the machine the RPM binaries run on").String()
	runCheck                = app.Flag("run-check", "Whether or not to run the spec file's check section during package build.").Bool()
	logFlags                = exe.SetupLogFlags(app)
	profFlags               = exe.SetupProfileFlags(app)
	timestampFile           = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(logFlags)

	prof, err := profile.StartProfiling(profFlags)
	if err != nil {
		logger.Log.Warnf("Could not start profiling: %s", err)
	}
	defer prof.StopProfiler()

	timestamp.BeginTiming("specreader", *timestampFile)
	defer timestamp.CompleteTiming()

	if *workers <= 0 {
		logger.Log.Panicf("Value in --workers must be greater than zero. Found %d", *workers)
	}

	toolchainRPMs, err := schedulerutils.ReadReservedFilesList(*toolchainManifest)
	logger.PanicOnError(err, "Unable to read toolchain manifest file '%s': %s", *toolchainManifest, err)

	// A parse list may be provided, if so only parse this subset.
	// If none is provided, parse all specs.
	specListSet, err := packagelist.ParsePackageList(*specList)
	logger.PanicOnError(err)

	// Convert specsDir to an absolute path
	specsAbsDir, err := filepath.Abs(*specsDir)
	logger.PanicOnError(err, "Unable to get absolute path for specs directory '%s': %s", *specsDir, err)

	err = specreaderutils.ParseSPECsWrapper(*buildDir, specsAbsDir, *rpmsDir, *srpmsDir, *existingToolchainRpmDir, *distTag, *output, *workerTar, *targetArch, specListSet, toolchainRPMs, *workers, *runCheck)
	logger.PanicOnError(err)
}
