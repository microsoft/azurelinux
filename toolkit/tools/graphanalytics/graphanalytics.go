// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"os"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/exe"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/graphanalytics"

	"gopkg.in/alecthomas/kingpin.v2"
)

const (
	defaultMaxResults = "10"
)

var (
	app            = kingpin.New("graphanalytics", "A tool to print analytics of a given dependency graph.")
	inputGraphFile = exe.InputFlag(app, "Path to the DOT graph file to analyze.")
	maxResults     = app.Flag("max-results", "The number of results to print per category. Set 0 to print unlimited.").Default(defaultMaxResults).Int()
	logFlags       = exe.SetupLogFlags(app)
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))

	logger.InitBestEffort(logFlags)

	err := graphanalytics.AnalyzeGraph(*inputGraphFile, *maxResults)
	if err != nil {
		logger.Log.Fatalf("Unable to analyze dependency graph, error: %s", err)
	}
}
