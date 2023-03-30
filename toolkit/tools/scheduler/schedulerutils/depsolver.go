// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"sync"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/pkggraph"
	"gonum.org/v1/gonum/graph"
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
	var unfilteredUnblockedNodes []*pkggraph.PkgNode
	unblockedNodesMap := make(map[*pkggraph.PkgNode]bool)
	for _, node := range res.AncillaryNodes {
		unfilteredUnblockedNodes = append(unfilteredUnblockedNodes, findUnblockedNodesFromNode(pkgGraph, buildState, node)...)
	}

	for _, node := range unfilteredUnblockedNodes {
		_, found := unblockedNodesMap[node]
		if !found {
			unblockedNodesMap[node] = true
			unblockedNodes = append(unblockedNodes, node)
		}
	}

	return
}

// findUnblockedNodesFromNode takes a built node and returns a list of nodes that are now unblocked by it.
func findUnblockedNodesFromNode(pkgGraph *pkggraph.PkgGraph, buildState *GraphBuildState, builtNode *pkggraph.PkgNode) (unblockedNodes []*pkggraph.PkgNode) {
	dependents := pkgGraph.To(builtNode.ID())

	for dependents.Next() {
		dependent := dependents.Node().(*pkggraph.PkgNode)

		if isNodeUnblocked(pkgGraph, buildState, dependent) {
			unblockedNodes = append(unblockedNodes, dependent)
		}
	}

	return
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
