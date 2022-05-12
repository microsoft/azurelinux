// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"os"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/graph/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/graph/preprocessor"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/logger"

	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app             = kingpin.New("graphPreprocessor", "Update the graph for the build requested")
	inputGraphFile  = exe.InputFlag(app, "Input graph file having full build graph")
	outputGraphFile = exe.OutputFlag(app, "Output file to export the scrubbed graph to")
	hydratedBuild   = app.Flag("hydrated-build", "Build individual packages with dependencies Hydrated").Bool()

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)
)

func populatePreprocessorConfig() *preprocessor.Config {
	return &preprocessor.Config{
		InputGraphFile:  *inputGraphFile,
		OutputGraphFile: *outputGraphFile,
		HydratedBuild:   *hydratedBuild,
	}

}

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	cfg := populatePreprocessorConfig()
	scrubbedGraph, err := cfg.ReadAndPreprocessGraph()
	if err != nil {
		logger.Log.Panic(err)
	}
	err = pkggraph.WriteDOTGraphFile(scrubbedGraph, cfg.OutputGraphFile)
	if err != nil {
		logger.Log.Panicf("Failed to write cache graph to file, %s. Error: %s", cfg.OutputGraphFile, err)
	}
	return
}
