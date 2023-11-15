// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A tool for generating snapshots of built RPMs from local specs.

package main

import (
	"os"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/specarchchecker"

	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app = kingpin.New("specarchchecker", "Checks if the architecture of a .spec file is valid.")

	specsDirPath       = exe.InputStringFlag(app, "Path to specs directory.")
	outputFilteredList = exe.OutputFlag(app, "Path to the filtered list.")

	pkgsToBuild   = app.Flag("packages", "Space separated list of top-level packages that should be built. Omit this argument to build all packages.").String()
	pkgsToRebuild = app.Flag("rebuild-packages", "Space separated list of base package names packages that should be rebuilt.").String()

	buildDirPath = app.Flag("build-dir", "Directory to store temporary files.").Required().String()
	distTag      = app.Flag("dist-tag", "The distribution tag.").Required().String()
	workerTar    = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz.").Required().ExistingFile()

	testOnly = app.Flag("test-only", "Whether or not to run the filter out specs which don't run tests.").Bool()

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)
	logColor = exe.LogColorFlag(app)
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel, *logColor)

	packagesToBuild := exe.ParseListArgument(*pkgsToBuild)
	packagesToRebuild := exe.ParseListArgument(*pkgsToRebuild)

	specNames := append(packagesToBuild, packagesToRebuild...)
	if len(specNames) == 0 {
		logger.Log.Fatalf("No specs were provided to filter.")
	}

	archChecker, err := specarchchecker.New(*buildDirPath, *workerTar, *specsDirPath)
	if err != nil {
		logger.Log.Fatalf("Failed to initialize spec arch checker. Error:\n%s", err)
	}
	defer func() {
		cleanupErr := archChecker.CleanUp()
		if cleanupErr != nil {
			logger.Log.Fatalf("Failed to cleanup spec arch checker. Error:\n%s", cleanupErr)
		}
	}()

	logger.Log.Infof("Filtering spec list in (%s).", *specsDirPath)
	logger.Log.Debugf("Distribution tag: %s.", *distTag)
	logger.Log.Debugf("Input list: %v.", specNames)
	filteredSpecNames, err := archChecker.FilterSpecsByArch(specNames, *distTag, *testOnly)
	if err != nil {
		logger.Log.Fatalf("Failed to filter specs folder (%s) Error:\n%s", *specsDirPath, err)
	}

	// Print the list of specs that were filtered out space separated into the output file
	outputString := strings.Join(filteredSpecNames, " ")
	err = file.Write(outputString, *outputFilteredList)
	if err != nil {
		logger.Log.Fatalf("Failed to write output file (%s) Error:\n%s", *outputFilteredList, err)
	}
}
