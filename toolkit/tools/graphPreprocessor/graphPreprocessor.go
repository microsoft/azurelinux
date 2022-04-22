// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"os"

	"gopkg.in/alecthomas/kingpin.v2"
	"microsoft.com/pkggen/internal/exe"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkggraph"
)

var (
	app             = kingpin.New("graphPreprocessor", "Update the graph for the build requested")
	inputGraphFile  = exe.InputFlag(app, "Input graph file having full build graph")
	outputGraphFile = exe.OutputFlag(app, "Output file to export the scrubbed graph to")
	hydratedBuild   = app.Flag("hydrated-build", "Build individual packages with dependencies Hydrated").Bool()

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)
)

func replaceRunNodesWithPrebuiltNodes(pkgGraph *pkggraph.PkgGraph) (err error) {
	for _, node := range pkgGraph.AllNodes() {

		if node.Type != pkggraph.TypeRun {
			continue
		}

		isPrebuilt, _, missing := pkggraph.IsSRPMPrebuilt(node.SrpmPath, pkgGraph, nil)

		if isPrebuilt == false {
			logger.Log.Tracef("Can't mark %s as prebuilt, missing: %v", node.SrpmPath, missing)
			continue
		}

		preBuiltNode := pkgGraph.CloneNode(node)
		preBuiltNode.State = pkggraph.StateUpToDate
		preBuiltNode.Type = pkggraph.TypePreBuilt

		parentNodes := pkgGraph.To(node.ID())
		for parentNodes.Next() {
			parentNode := parentNodes.Node().(*pkggraph.PkgNode)

			if parentNode.Type != pkggraph.TypeGoal {
				pkgGraph.RemoveEdge(parentNode.ID(), node.ID())

				logger.Log.Debugf("Adding a 'PreBuilt' node '%s' with id %d. For '%s'", preBuiltNode.FriendlyName(), preBuiltNode.ID(), parentNode.FriendlyName())
				err = pkgGraph.AddEdge(parentNode, preBuiltNode)

				if err != nil {
					logger.Log.Errorf("Adding edge failed for %v -> %v", parentNode, preBuiltNode)
					return
				}
			}
		}
	}

	return
}

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	scrubbedGraph := pkggraph.NewPkgGraph()

	err := pkggraph.ReadDOTGraphFile(scrubbedGraph, *inputGraphFile)
	if err != nil {
		logger.Log.Panicf("Failed to read graph to file, %s. Error: %s", *inputGraphFile, err)
	}

	if *hydratedBuild {
		logger.Log.Debugf("Nodes before replacing prebuilt nodes: %d", len(scrubbedGraph.AllNodes()))
		err = replaceRunNodesWithPrebuiltNodes(scrubbedGraph)
		logger.Log.Debugf("Nodes after replacing prebuilt nodes: %d", len(scrubbedGraph.AllNodes()))
		if err != nil {
			logger.Log.Panicf("Failed to replace run nodes with preBuilt nodes. Error: %s", err)
		}
	}

	err = pkggraph.WriteDOTGraphFile(scrubbedGraph, *outputGraphFile)
	if err != nil {
		logger.Log.Panicf("Failed to write cache graph to file, %s. Error: %s", *outputGraphFile, err)
	}
	return
}
