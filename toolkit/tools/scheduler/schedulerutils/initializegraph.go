// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"fmt"

	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkggraph"
	"microsoft.com/pkggen/internal/pkgjson"
)

const (
	allGoalNodeName   = "ALL"
	buildGoalNodeName = "PackagesToBuild"
)

// InitializeGraph initializes and prepares a graph dot file for building.
// - It will load and return the graph.
// - It will subgraph the graph to only contain the desired packages if possible.
func InitializeGraph(inputFile string, packagesToBuild []*pkgjson.PackageVer) (isOptimized bool, pkgGraph *pkggraph.PkgGraph, goalNode *pkggraph.PkgNode, err error) {
	const (
		canUseCachedImplicit = false
		strictGoalNode       = true
	)

	pkgGraph = pkggraph.NewPkgGraph()
	err = pkggraph.ReadDOTGraphFile(pkgGraph, inputFile)
	if err != nil {
		return
	}

	_, err = pkgGraph.AddGoalNode(buildGoalNodeName, packagesToBuild, strictGoalNode)
	if err != nil {
		return
	}

	optimizedGraph, goalNode, optimizeErr := OptimizeGraph(pkgGraph, canUseCachedImplicit)
	if optimizeErr == nil {
		logger.Log.Infof("Successfully created solvable subgraph")
		isOptimized = true
		pkgGraph = optimizedGraph
	} else {
		logger.Log.Warn("Could not create solvable subgraph, forcing full package build")
		goalNode = pkgGraph.FindGoalNode(allGoalNodeName)
		if goalNode == nil {
			err = fmt.Errorf("could not find goal node %s", allGoalNodeName)
			return
		}
	}

	return
}

// OptimizeGraph will attempt to create a solvable subgraph that satisfies the build goal node.
func OptimizeGraph(pkgGraph *pkggraph.PkgGraph, canUseCachedImplicit bool) (optimizedGraph *pkggraph.PkgGraph, goalNode *pkggraph.PkgNode, err error) {
	buildGoalNode := pkgGraph.FindGoalNode(buildGoalNodeName)
	if buildGoalNode == nil {
		err = fmt.Errorf("could not find goal node %s", buildGoalNodeName)
		logger.Log.Warnf("%s", err)
		return
	}

	if CanSubGraph(pkgGraph, buildGoalNode, canUseCachedImplicit) {
		optimizedGraph, err = pkgGraph.CreateSubGraph(buildGoalNode)
		if err != nil {
			logger.Log.Warnf("Failed to create subgraph error: %s", err)
			return
		}

		// Create a solvable ALL goal node
		goalNode, err = optimizedGraph.AddGoalNode(allGoalNodeName, nil, true)
		if err != nil {
			logger.Log.Warnf("Failed to add goal node (%s), error: %s", allGoalNodeName, err)
			return
		}
	} else {
		err = fmt.Errorf("could not create solvable subgraph")
	}

	return
}
