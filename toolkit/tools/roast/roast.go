// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A raw to other format converter

package main

import (
	"os"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/image/roast"

	"gopkg.in/alecthomas/kingpin.v2"
)

const defaultWorkerCount = "10"

var (
	app = kingpin.New("roast", "A tool to convert raw disk file into another image type")

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)

	inputDir  = exe.InputDirFlag(app, "A directory containing a .RAW image or a rootfs directory")
	outputDir = exe.OutputDirFlag(app, "A destination directory for the output image")

	configFile = app.Flag("config", "Path to the image config file.").Required().ExistingFile()
	tmpDir     = app.Flag("tmp-dir", "Directory to store temporary files while converting.").Required().String()

	releaseVersion = app.Flag("release-version", "Release version to add to the output artifact name").String()

	workers = app.Flag("workers", "Number of concurrent goroutines to convert with.").Default(defaultWorkerCount).Int()

	imageTag = app.Flag("image-tag", "Tag (text) appended to the image name. Empty by default.").String()
)

func populateRoastConfig() *roast.Config {
	return &roast.Config{
		InputDir:       *inputDir,
		OutputDir:      *outputDir,
		ConfigFile:     *configFile,
		TmpDir:         *tmpDir,
		ReleaseVersion: *releaseVersion,
		Workers:        *workers,
		ImageTag:       *imageTag,
	}
}

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	cfg := populateRoastConfig()
	err := cfg.GenerateImageArtifacts()
	if err != nil {
		logger.Log.Panic(err)
	}
}
