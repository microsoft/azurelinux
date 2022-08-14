// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// specreader is a tool to parse spec files into a JSON structure

package main

import (
	"os"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/specreader"

	"gopkg.in/alecthomas/kingpin.v2"
)

const (
	defaultWorkerCount = "10"
)

var (
	app       = kingpin.New("specreader", "A tool to parse spec dependencies into JSON")
	specsDir  = exe.InputDirFlag(app, "Directory to scan for SPECS")
	output    = exe.OutputFlag(app, "Output file to export the JSON")
	workers   = app.Flag("workers", "Number of concurrent goroutines to parse with").Default(defaultWorkerCount).Int()
	buildDir  = app.Flag("build-dir", "Directory to store temporary files while parsing.").String()
	srpmsDir  = app.Flag("srpm-dir", "Directory containing SRPMs.").Required().ExistingDir()
	rpmsDir   = app.Flag("rpm-dir", "Directory containing built RPMs.").Required().ExistingDir()
	distTag   = app.Flag("dist-tag", "The distribution tag the SPEC will be built with.").Required().String()
	workerTar = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz.  If this argument is empty, specs will be parsed in the host environment.").ExistingFile()
	runCheck  = app.Flag("run-check", "Whether or not to run the spec file's check section during package build.").Bool()
	logFile   = exe.LogFileFlag(app)
	logLevel  = exe.LogLevelFlag(app)
)

func populateSpecReaderConfig() *specreader.Config {
	return &specreader.Config{
		SpecsDir:  *specsDir,
		Output:    *output,
		Workers:   *workers,
		BuildDir:  *buildDir,
		SrpmsDir:  *srpmsDir,
		RpmsDir:   *rpmsDir,
		DistTag:   *distTag,
		WorkerTar: *workerTar,
		RunCheck:  *runCheck,
	}
}

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	if *workers <= 0 {
		logger.Log.Panicf("Value in --workers must be greater than zero. Found %d", *workers)
	}
	cfg := populateSpecReaderConfig()

	err := cfg.ParseSPECsWrapper()
	logger.PanicOnError(err)
}
