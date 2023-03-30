// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A tool for generating snapshots of built RPMs from local specs.

package main

import (
	"os"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/logger"
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
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	snapshotGenerator := rpmssnapshot.New(*buildDirPath, *workerTar)

	err := snapshotGenerator.GenerateSnapshot(*specsDirPath, *outputSnapshotPath, *distTag)
	if err != nil {
		logger.Log.Errorf("Failed to generate snapshot from specs folder (%s) into (%s). Error: %v", *specsDirPath, *outputSnapshotPath, err)
	}
}
