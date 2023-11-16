// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"sync"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/sliceutils"
	"github.com/sirupsen/logrus"
	"gonum.org/v1/gonum/graph"
	"gonum.org/v1/gonum/graph/path"
	"gonum.org/v1/gonum/graph/traverse"
)

// CanSubGraph returns true if a node can be subgraphed without any unresolved dynamic dependencies.
// Used to optimize graph solving.
func CanSubGraph(pkgGraph *pkggraph.PkgGraph, node *pkggraph.PkgNode, useCachedImplicit bool) bool {
	search := traverse.BreadthFirst{}

	foundUnsolvableNode := false

	// Walk entire graph and print list of any/all unsolvable nodes
	search.Walk(pkgGraph, node, func(n graph.Node, d int) (stopSearch bool) {
		pkgNode := n.(*pkggraph.PkgNode)

		// Non-implicit nodes are solvable
		if !pkgNode.Implicit {
			return
		}

		// Cached implicit nodes are solvable so long as useCachedImplicit is set
		if useCachedImplicit && pkgNode.State == pkggraph.StateCached {
			return
		}

		// Resolved and non-cached nodes are solvable
		if pkgNode.State != pkggraph.StateUnresolved && pkgNode.State != pkggraph.StateCached {
			return
		}

		// This node is not yet solvable
		logger.Log.Warnf("Could not subgraph due to node: %v", pkgNode)

		// If we are in trace mode, print the path from the root node to the unsolvable node
		if logger.Log.IsLevelEnabled(logrus.TraceLevel) {
			paths := path.YenKShortestPaths(pkgGraph, 1, node, pkgNode)
			if len(paths) == 0 {
				logger.Log.Warnf("Could not find path between %v and %v with YenKShortestPaths()", node, pkgNode)
			} else {
				logger.Log.Tracef("Path between %v and %v:", node, pkgNode)
				for _, n := range paths[0] {
					logger.Log.Tracef("  %v", n.(*pkggraph.PkgNode))
				}
			}
		}

		foundUnsolvableNode = true
		return
	})

	return foundUnsolvableNode == false
}

// LeafNodes returns a slice of all leaf nodes in the graph.
func LeafNodes(pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex, goalNode *pkggraph.PkgNode, buildState *GraphBuildState, useCachedImplicit bool) (leafNodes []*pkggraph.PkgNode) {
	graphMutex.RLock()
	defer graphMutex.RUnlock()

	search := traverse.BreadthFirst{}

	search.Walk(pkgGraph, goalNode, func(n graph.Node, d int) (stopSearch bool) {
		pkgNode := n.(*pkggraph.PkgNode)

		// Skip nodes that have already been processed
		if buildState.IsNodeProcessed(pkgNode) {
			return
		}

		if pkgNode.State == pkggraph.StateUnresolved {
			return
		}

		dependencies := pkgGraph.From(n.ID())

		if dependencies.Len() != 0 {
			return
		}

		// Implicit nodes will only be considered valid leaf nodes as a last resort (aka when useCachedImplicit is set).
		// Ideally we will wait for the actual provider of the implicit node to be built and convert the implicit node to
		// a normal node via InjectMissingImplicitProvides().
		if !useCachedImplicit && pkgNode.Implicit && pkgNode.State == pkggraph.StateCached {
			logger.Log.Debugf("Skipping cached implicit provide leaf node: %v", pkgNode)
			return
		}

		logger.Log.Debugf("Found leaf node: %v", pkgNode)
		leafNodes = append(leafNodes, pkgNode)

		return
	})

	logger.Log.Debugf("Discovered %d leaf nodes", len(leafNodes))

	return
}

// FindUnblockedNodesFromResult takes a package build result and returns a list of nodes that are now unblocked for building.
func FindUnblockedNodesFromResult(res *BuildResult, pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex, buildState *GraphBuildState) (unblockedNodes []*pkggraph.PkgNode) {
	if res.Err != nil {
		return
	}

	graphMutex.RLock()
	defer graphMutex.RUnlock()

	// Since all the ancillary nodes are marked as available already, there may be duplicate nodes returned by the below loop.
	// e.g. If a meta node requires two build nodes for the same SPEC, then that meta node will be reported twice.
	// Filter the nodes to ensure no duplicates.
	unblockedNodesMap := make(map[*pkggraph.PkgNode]bool)
	for _, node := range res.AncillaryNodes {
		findUnblockedNodesFromNode(pkgGraph, buildState, node, unblockedNodesMap)
	}

	return sliceutils.MapToSliceBool(unblockedNodesMap)
}

// findUnblockedNodesFromNode takes a built node and returns a list of nodes that are now unblocked by it.
func findUnblockedNodesFromNode(pkgGraph *pkggraph.PkgGraph, buildState *GraphBuildState, builtNode *pkggraph.PkgNode, unblockedNodes map[*pkggraph.PkgNode]bool) {
	dependents := pkgGraph.To(builtNode.ID())

	for dependents.Next() {
		dependent := dependents.Node().(*pkggraph.PkgNode)

		if isNodeUnblocked(pkgGraph, buildState, dependent) {
			unblockedNodes[dependent] = true
		}
	}
}

// isNodeUnblocked returns true if all nodes required to build `node` are UpToDate and do not need to be built.
func isNodeUnblocked(pkgGraph *pkggraph.PkgGraph, buildState *GraphBuildState, node *pkggraph.PkgNode) bool {
	dependencies := pkgGraph.From(node.ID())
	for dependencies.Next() {
		dependency := dependencies.Node().(*pkggraph.PkgNode)

		if !buildState.IsNodeAvailable(dependency) {
			return false
		}
	}

	return true
}
