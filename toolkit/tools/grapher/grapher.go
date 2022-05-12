// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"os"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/graph/grapher"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/logger"

	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app    = kingpin.New("grapher", "Dependency graph generation tool")
	input  = exe.InputFlag(app, "Input json listing all local SRPMs")
	output = exe.OutputFlag(app, "Output file to export the graph to")

	logFile          = exe.LogFileFlag(app)
	logLevel         = exe.LogLevelFlag(app)
	strictGoals      = app.Flag("strict-goals", "Don't allow missing goal packages").Bool()
	strictUnresolved = app.Flag("strict-unresolved", "Don't allow missing unresolved packages").Bool()
)

func populateGrapherConfig() *grapher.Config {
	return &grapher.Config{
		Input:            *input,
		Output:           *output,
		StrictGoals:      *strictGoals,
		StrictUnresolved: *strictUnresolved,
	}
}

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	cfg := populateGrapherConfig()
	depGraph, err := cfg.GenerateDependencyGraph()
	if err != nil {
		logger.Log.Panic(err)
	}

	err = pkggraph.WriteDOTGraphFile(depGraph, *output)
	if err != nil {
		logger.Log.Panic(err)
	}

	logger.Log.Info("Finished generating graph.")
}
