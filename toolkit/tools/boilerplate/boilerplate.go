// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A boilerplate for Mariner go tools

package main

import (
	"os"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/boilerplate/hello"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"

	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app = kingpin.New("boilerplate", "A sample golang tool for Mariner.")

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)

	timestampFile = app.Flag("timestamp-file", "File that stores timestamps for this program.").Required().String()
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))

	logger.InitBestEffort(*logFile, *logLevel)
	timestamp.InitCSV(*timestampFile)

	logger.Log.Info(hello.World())
	timestamp.Stamp.RecordToCSV("execution", "print 'Hello, World!'")
}
