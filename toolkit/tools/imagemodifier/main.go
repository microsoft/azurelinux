// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"log"
	"os"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/imagemodifierlib"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/profile"
	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app = kingpin.New("imagemodifier", "Modifies a pre-built CBL-Mariner image")

	buildDir                 = app.Flag("build-dir", "Directory to run build out of.").Required().String()
	configFile               = app.Flag("config-file", "Path of the image customization config file.").Required().String()
	logFile                  = exe.LogFileFlag(app)
	logLevel                 = exe.LogLevelFlag(app)
	profFlags                = exe.SetupProfileFlags(app)
	timestampFile            = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()
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

	timestamp.BeginTiming("imagemodifier", *timestampFile)
	defer timestamp.CompleteTiming()

	err = modifyImage()
	if err != nil {
		log.Fatalf("image modification failed: %v", err)
	}
}

func modifyImage() error {
	err := imagemodifierlib.ModifyImageWithConfigFile(*buildDir, *configFile)
	if err != nil {
		return err
	}

	return nil
}
