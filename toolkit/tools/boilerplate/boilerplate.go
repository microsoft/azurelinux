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

	logFlags = exe.SetupLogFlags(app)
	timestampFile = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))

	logger.InitBestEffort(logFlags)

	timestamp.BeginTiming("boilerplate", *timestampFile)
	defer timestamp.CompleteTiming()

	logger.Log.Info(hello.World())
}
