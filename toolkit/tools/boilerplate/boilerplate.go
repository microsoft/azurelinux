// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A boilerplate for Mariner go tools

package main

import (
	"os"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/boilerplate/hello"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/logger"

	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app = kingpin.New("boilerplate", "A sample golang tool for Mariner.")

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))

	logger.InitBestEffort(*logFile, *logLevel)

	logger.Log.Info(hello.World())
}
