// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"fmt"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
)

const (
	allGoalNodeName   = "ALL"
	buildGoalNodeName = "PackagesToBuild"
)

// InitializeGraph initializes and prepares a graph dot file for building.
//   - It will load and return the graph.
//   - It will subgraph the graph to only contain the desired packages if possible.
//   - If canUseCachedImplicit is true, it will use cached nodes to resolve implicit dependencies instead of waiting for
//     them to be built in the graph (This can allow the graph to be optimized immediately instead of waiting for the
//     implicit nodes to be resolved by an unknown package later in the build).
func InitializeGraph(inputFile string, packagesToBuild []*pkgjson.PackageVer, canUseCachedImplicit bool) (isOptimized bool, pkgGraph *pkggraph.PkgGraph, goalNode *pkggraph.PkgNode, err error) {
	const (
		strictGoalNode = true
	)
	timestamp.StartEvent("graph initialization", nil)
	defer timestamp.StopEvent(nil)

	pkgGraph, err = pkggraph.ReadDOTGraphFile(inputFile)
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
