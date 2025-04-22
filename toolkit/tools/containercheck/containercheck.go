// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Returns true (exit code 0) if the current build is a container build, false (exit code 1) otherwise

package main

import (
	"os"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/buildpipeline"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/exe"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"

	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app      = kingpin.New("containercheck", "Returns true (0) if the current build is a container build, false (1) otherwise")
	logFlags = exe.SetupLogFlags(app)
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(logFlags)

	if buildpipeline.IsRegularBuild() {
		os.Exit(1)
	} else {
		os.Exit(0)
	}
}
