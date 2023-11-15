// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A tool for generating snapshots of built RPMs from local specs.

package main

import (
	"os"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/rpmssnapshot"

	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app = kingpin.New("rpmsspnapshot", "A tool to generate a snapshot of all RPMs expected to be built from given specs folder.")

	specsDirPath       = exe.InputStringFlag(app, "Path to specs directory.")
	outputSnapshotPath = exe.OutputFlag(app, "Path to the generated snapshot.")

	buildDirPath = app.Flag("build-dir", "Directory to store temporary files.").Required().String()
	distTag      = app.Flag("dist-tag", "The distribution tag.").Required().String()
	workerTar    = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz.").Required().ExistingFile()

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)
	logColor = exe.LogColorFlag(app)
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel, *logColor)

	snapshotGenerator, err := rpmssnapshot.New(*buildDirPath, *workerTar, *specsDirPath)
	if err != nil {
		logger.Log.Fatalf("Failed to initialize RPM snapshot generator. Error: %v", err)
	}
	defer func() {
		cleanupErr := snapshotGenerator.CleanUp()
		if cleanupErr != nil {
			logger.Log.Fatalf("Failed to cleanup snapshot generator. Error: %s", cleanupErr)
		}
	}()

	logger.Log.Infof("Generating RPMs snapshot from specs inside (%s).", *specsDirPath)
	logger.Log.Debugf("Distribution tag: %s.", *distTag)
	err = snapshotGenerator.GenerateSnapshot(*outputSnapshotPath, *distTag)
	if err != nil {
		logger.Log.Errorf("Failed to generate snapshot from specs folder (%s) into (%s). Error: %v", *specsDirPath, *outputSnapshotPath, err)
	}
}
