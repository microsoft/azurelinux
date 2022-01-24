// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"os"

	"gopkg.in/alecthomas/kingpin.v2"
	"microsoft.com/pkggen/internal/exe"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkggraph"
	"microsoft.com/pkggen/internal/pkgjson"
	"microsoft.com/pkggen/scheduler/schedulerutils"
)

const (
	allGoalNodeName = "ALL"
)

var (
	app             = kingpin.New("graphscrubber", "Update the graph for the build requested")
	inputGraphFile  = exe.InputFlag(app, "Input graph file having full build graph")
	outputGraphFile = exe.OutputFlag(app, "Output file to export the scrubbed graph to")
	imageConfig     = app.Flag("image-config-file", "Optional image config file to extract a package list from.").String()
	baseDirPath     = app.Flag("base-dir", "Base directory for relative file paths from the config. Defaults to config's directory.").ExistingDir()
	hydratedBuild   = app.Flag("hydrated-build", "Build individual packages with dependencies Hydrated").Bool()
	ignoredPackages = app.Flag("ignored-packages", "Space separated list of specs ignoring rebuilds if their dependencies have been updated. Will still build if all of the spec's RPMs have not been built.").String()
	pkgsToBuild     = app.Flag("packages", "Space separated list of top-level packages that should be built. Omit this argument to build all packages.").String()
	pkgsToRebuild   = app.Flag("rebuild-packages", "Space separated list of base package names packages that should be rebuilt.").String()

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)
)

func replaceRunNodesWithPrebuiltNodes(pkgGraph *pkggraph.PkgGraph, skipPkgs []*pkgjson.PackageVer) (err error) {
	for _, node := range pkgGraph.AllNodes() {

		if node.Type != pkggraph.TypeRun {
			continue
		}

		isPrebuilt, _ := pkggraph.IsSRPMPrebuilt(node.SrpmPath, pkgGraph, nil)

		if isPrebuilt == false {
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
				}
			}
		}
	}

	return
}

func removeExistingGoalNode(pkgGraph *pkggraph.PkgGraph, goalNodeName string) {
	goalNode := pkgGraph.FindGoalNode(goalNodeName)
	if goalNode != nil {
		logger.Log.Infof("Found goalNode: %s. Removing it.", goalNodeName)
		pkgGraph.RemoveNode(goalNode.ID())
	} else {
		logger.Log.Warnf("Can't find goalNode: %s. Skipping Removal", goalNodeName)
	}
	return
}

func subGraphPkgsToBuild(pkgGraph *pkggraph.PkgGraph, packageVersToBuild []*pkgjson.PackageVer) (optimizedGraph *pkggraph.PkgGraph, err error) {
	optimizedGraph = pkgGraph

	pkgToBuildGoalNode := pkgGraph.FindGoalNode(allGoalNodeName)
	if schedulerutils.CanSubGraph(pkgGraph, pkgToBuildGoalNode, true) {
		optimizedGraph, err = pkgGraph.CreateSubGraph(pkgToBuildGoalNode)
		if err != nil {
			logger.Log.Panicf("Failed to create subgraph error: %s", err)
			return
		}
	} else {
		logger.Log.Warnf("Not possible to subgraph")
		return
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

	if !*hydratedBuild {
		err = pkggraph.WriteDOTGraphFile(scrubbedGraph, *outputGraphFile)
		if err != nil {
			logger.Log.Panicf("Failed to write cache graph to file, %s. Error: %s", *outputGraphFile, err)
		}
		return
	}

	// Generate the list of packages that need to be built.
	// If none are requested then all packages will be built.
	packagesNamesToBuild := exe.ParseListArgument(*pkgsToBuild)
	packagesNamesToRebuild := exe.ParseListArgument(*pkgsToRebuild)

	pkgVersToBuild, err := schedulerutils.CalculatePackagesToBuild(packagesNamesToBuild, packagesNamesToRebuild, *imageConfig, *baseDirPath)
	if err != nil {
		logger.Log.Panicf("Error while calculating to build. Error: %s", err)
	}

	removeExistingGoalNode(scrubbedGraph, allGoalNodeName)
	_, err = scrubbedGraph.AddGoalNode(allGoalNodeName, pkgVersToBuild, true)
	if err != nil {
		logger.Log.Panicf("Unable to set Goal node for packages to build. error: %s", err)
	}

	err = replaceRunNodesWithPrebuiltNodes(scrubbedGraph, pkgVersToBuild)
	if err != nil {
		logger.Log.Panicf("Failed to replace run nodes with preBuilt nodes. Error: %s", err)
	}

	logger.Log.Infof("Nodes before subgraphing: %d", len(scrubbedGraph.AllNodes()))

	optimizedGraph, err := subGraphPkgsToBuild(scrubbedGraph, pkgVersToBuild)
	if err != nil {
		logger.Log.Panicf("Error while creating sub graph. Error: %s", err)
		return
	}
	scrubbedGraph = optimizedGraph

	logger.Log.Infof("Nodes after subgraphing: %d", len(scrubbedGraph.AllNodes()))

	err = pkggraph.WriteDOTGraphFile(scrubbedGraph, *outputGraphFile)
	if err != nil {
		logger.Log.Panicf("Failed to write cache graph to file, %s. Error: %s", *outputGraphFile, err)
	}
	return
}
