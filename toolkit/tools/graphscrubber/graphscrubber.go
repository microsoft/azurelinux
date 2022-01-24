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
	allGoalNodeName   = "ALL"
)

var (
	app    = kingpin.New("graphscrubber", "Update the graph for the build requested")
	inputGraphFile  = exe.InputFlag(app, "Input graph file having full build graph")
	outputGraphFile = exe.OutputFlag(app, "Output file to export the scrubbed graph to")
	imageConfig = app.Flag("image-config-file", "Optional image config file to extract a package list from.").String()
	baseDirPath = app.Flag("base-dir", "Base directory for relative file paths from the config. Defaults to config's directory.").ExistingDir()
	hydratedBuild        = app.Flag("hydrated-build", "Build individual packages with dependencies Hydrated").Bool()
	ignoredPackages = app.Flag("ignored-packages", "Space separated list of specs ignoring rebuilds if their dependencies have been updated. Will still build if all of the spec's RPMs have not been built.").String()
	pkgsToBuild   = app.Flag("packages", "Space separated list of top-level packages that should be built. Omit this argument to build all packages.").String()
	pkgsToRebuild = app.Flag("rebuild-packages", "Space separated list of base package names packages that should be rebuilt.").String()

	logFile          = exe.LogFileFlag(app)
	logLevel         = exe.LogLevelFlag(app)
)

func isNodeInList(pkgGraph *pkggraph.PkgGraph, node *pkggraph.PkgNode, packagesToBuild []*pkgjson.PackageVer) (bool){
    for _, pkgVer := range packagesToBuild {

        lookupNode, err := pkgGraph.FindExactPkgNodeFromPkg(pkgVer)
        if err != nil {
            continue
        }

        if lookupNode != nil {
            switch node.Type {
            case pkggraph.TypeBuild:
                if node.ID() == lookupNode.BuildNode.ID() {
                    logger.Log.Infof("Lookup match - Build: %s", node.FriendlyName())
                    return true
                }
            case pkggraph.TypeRun:
                if node.ID() == lookupNode.RunNode.ID() {
                    logger.Log.Infof("Lookup match - Run: %s", node.FriendlyName())
                    return true
                }
            }
        }
    }

    return false
}

func replaceRunNodesWithPrebuiltNodes(pkgGraph *pkggraph.PkgGraph, skipPkgs []*pkgjson.PackageVer) (err error) {
	for _, node := range pkgGraph.AllNodes() {

		if node.Type != pkggraph.TypeRun {
			continue
		}

        isNodeInList(pkgGraph, node, skipPkgs)

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

	    		//logger.Log.Infof("Adding a 'PreBuilt' node '%s' with id %d. For '%s'", preBuiltNode.FriendlyName(), preBuiltNode.ID(), parentNode.FriendlyName())
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
        logger.Log.Warnf("Found goalNode: %s. Removing it.", goalNodeName)
        pkgGraph.RemoveNode(goalNode.ID())
    } else {
        logger.Log.Warnf("Can't find goalNode: %s", goalNodeName)
    }
    return
}

func subGraphPkgsToBuild(pkgGraph *pkggraph.PkgGraph, packageVersToBuild []*pkgjson.PackageVer) (optimizedGraph *pkggraph.PkgGraph, err error) {
    optimizedGraph = pkgGraph

    pkgToBuildGoalNode := pkgGraph.FindGoalNode(allGoalNodeName)
    if schedulerutils.CanSubGraph(pkgGraph, pkgToBuildGoalNode, true) {
        optimizedGraph, err = pkgGraph.CreateSubGraph(pkgToBuildGoalNode)
		if err != nil {
			logger.Log.Warnf("Failed to create subgraph error: %s", err)
			return
		}
    } else {
        logger.Log.Warnf("OOPS: Its not possible to subgraph")
        return
    }

    return
}

func isNodeInListt(pkgGraph *pkggraph.PkgGraph, node *pkggraph.PkgNode, packagesToBuild []*pkgjson.PackageVer) (bool){
    for _, pkgVer := range packagesToBuild {

        lookupNode, err := pkgGraph.FindExactPkgNodeFromPkg(pkgVer)
        if err != nil {
            continue
        }

        if lookupNode != nil {
            switch node.Type {
            case pkggraph.TypeBuild:
                if node.ID() == lookupNode.BuildNode.ID() {
                    logger.Log.Infof("Lookup match - Build: %s", node.FriendlyName())
                    return true
                }
            case pkggraph.TypeRun:
                if node.ID() == lookupNode.RunNode.ID() {
                    logger.Log.Infof("Lookup match - Run: %s", node.FriendlyName())
                    return true
                }
            }
        }
    }

    return false
}

func resetToBuildNodes(pkgGraph *pkggraph.PkgGraph, packagesToBuild []*pkgjson.PackageVer) {
    goalNode := pkgGraph.FindGoalNode(allGoalNodeName)

    firstLevelRunNodes := pkgGraph.From(goalNode.ID())
    for firstLevelRunNodes.Next() {
        runNode := firstLevelRunNodes.Node().(*pkggraph.PkgNode)
        runNode.Type = pkggraph.TypeRun
		runNode.State = pkggraph.StateMeta
    }
    return
}

func skipNodesNotInPkgsToBuild(pkgGraph *pkggraph.PkgGraph, packagesToBuild []*pkgjson.PackageVer) {
    for _, node := range pkgGraph.AllNodes() {
        if node.Type == pkggraph.TypeBuild {
            node.State = pkggraph.StateUpToDate
        }
    }

    for _, node := range pkgGraph.AllNodes() {

        if node.Type != pkggraph.TypeBuild {
            continue
        }

        isNodeTobeRebuild := isNodeInListt(pkgGraph, node, packagesToBuild)
        if isNodeTobeRebuild {
            logger.Log.Infof("Adding package from building: '%s'", node.FriendlyName())
            node.State = pkggraph.StateBuild
        }
    }
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
        logger.Log.Warnf("Not scrubbing the graph")
	    if err != nil {
		    logger.Log.Panicf("Failed to write cache graph to file, %s. Error: %s", *outputGraphFile, err)
	    }
        return
    }

	//ignoredPackages := exe.ParseListArgument(*ignoredPackages)

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

    logger.Log.Warnf("Nodes before subgraphing: %d", len(scrubbedGraph.AllNodes()))

    optimizedGraph, err := subGraphPkgsToBuild(scrubbedGraph, pkgVersToBuild)
    if err != nil {
		logger.Log.Panicf("Error while creating sub graph. Error: %s", err)
        return
    }
    scrubbedGraph = optimizedGraph

    logger.Log.Warnf("Nodes after subgraphing: %d", len(scrubbedGraph.AllNodes()))

    resetToBuildNodes(scrubbedGraph, pkgVersToBuild)

    //TODO: Ideally there shouldn't any build nodes to be skipped
    skipNodesNotInPkgsToBuild(scrubbedGraph, pkgVersToBuild)
    if err != nil {
	    logger.Log.Panicf("Failed while skipping build nodes. Error: %s", err)
    }

    err = pkggraph.WriteDOTGraphFile(scrubbedGraph, *outputGraphFile)
	if err != nil {
	    logger.Log.Panicf("Failed to write cache graph to file, %s. Error: %s", *outputGraphFile, err)
	}
    return
}
