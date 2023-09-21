// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"log"
	"os"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/imagecustomizerlib"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/profile"
	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app = kingpin.New("imagecustomizer", "Customizes a pre-built CBL-Mariner image")

	buildDir          = app.Flag("build-dir", "Directory to run build out of.").Required().String()
	imageFile         = app.Flag("image-file", "Path of the base CBL-Mariner image which the customization will be applied to.").Required().String()
	outputImageFile   = app.Flag("output-image-file", "Path to write the customized image to.").Required().String()
	outputImageFormat = app.Flag("output-image-format", "Format of output image. Supported: vhd, vhdx, qcow2, raw.").Required().Enum("vhd", "vhdx", "qcow2", "raw")
	configFile        = app.Flag("config-file", "Path of the image customization config file.").Required().String()
	logFile           = exe.LogFileFlag(app)
	logLevel          = exe.LogLevelFlag(app)
	profFlags         = exe.SetupProfileFlags(app)
	timestampFile     = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()
)

func main() {
	var err error

	kingpin.MustParse(app.Parse(os.Args[1:]))

	logger.InitBestEffort(*logFile, *logLevel)

	prof, err := profile.StartProfiling(profFlags)
	if err != nil {
		logger.Log.Warnf("Could not start profiling: %s", err)
	}
	defer prof.StopProfiler()

	timestamp.BeginTiming("imagecustomizer", *timestampFile)
	defer timestamp.CompleteTiming()

	err = customizeImage()
	if err != nil {
		log.Fatalf("image customization failed: %v", err)
	}
}

func customizeImage() error {
	var err error

	err = imagecustomizerlib.CustomizeImageWithConfigFile(*buildDir, *configFile, *imageFile,
		*outputImageFile, *outputImageFormat)
	if err != nil {
		return err
	}

	return nil
}
