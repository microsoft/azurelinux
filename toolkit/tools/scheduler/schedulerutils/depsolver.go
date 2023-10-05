// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"sync"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
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
	unsolvedNodes := make([]*pkggraph.PkgNode, 0)

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
		logger.Log.Debugf("Could not subgraph due to node: %v", pkgNode)
		unsolvedNodes = append(unsolvedNodes, pkgNode)

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

	if len(unsolvedNodes) > 0 {
		logger.Log.Warnf("Found %d unsolved implicit nodes, cannot optimize subgraph yet...", len(unsolvedNodes))
		if len(unsolvedNodes) <= 3 {
			logger.Log.Infof("\tUnsolvable nodes: %v", unsolvedNodes)
		}
	}

	return foundUnsolvableNode == false
}

// LeafNodes returns a slice of all leaf nodes in the graph.
func LeafNodes(pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex, goalNode *pkggraph.PkgNode, buildState *GraphBuildState, useCachedImplicit, allowLowPriorityNodes bool) (leafNodes, lowPriorityLeafNodes []*pkggraph.PkgNode) {
	graphMutex.RLock()
	defer graphMutex.RUnlock()

	search := traverse.BreadthFirst{}

	search.Walk(pkgGraph, goalNode, func(n graph.Node, d int) (stopSearch bool) {
		pkgNode := n.(*pkggraph.PkgNode)
		isLowPriority := false

		isBadNode := n.ID() == 1
		if isBadNode {
			logger.Log.Warnf("Found bad node: %v", pkgNode)
		}

		// Skip nodes that have already been processed
		if buildState.IsNodeProcessed(pkgNode) {
			if isBadNode {
				logger.Log.Warn("    PROCESSED")
			}
			return
		}

		// Only let low priority nodes through if allowLowPriorityNodes is set
		if !(allowLowPriorityNodes || buildState.IsNodeElevatedPriority(pkgNode)) {
			if isBadNode {
				logger.Log.Warn("    LOW PRIORITY")
			}
			//isLowPriority = true
		}

		if pkgNode.State == pkggraph.StateUnresolved {
			if isBadNode {
				logger.Log.Warn("    UNRESOLVED")
			}
			return
		}

		dependencies := pkgGraph.From(n.ID())

		if dependencies.Len() != 0 {
			if isBadNode {
				logger.Log.Warn("    DEPENDENCIES")
			}
			return
		}

		// Implicit nodes will only be considered valid leaf nodes as a last resort (aka when useCachedImplicit is set).
		// Ideally we will wait for the actual provider of the implicit node to be built and convert the implicit node to
		// a normal node via InjectMissingImplicitProvides().
		if !useCachedImplicit && pkgNode.Implicit && pkgNode.State == pkggraph.StateCached {
			logger.Log.Debugf("Skipping cached implicit provide leaf node: %v", pkgNode)
			return
		}

		logger.Log.Infof("Found leaf node: %v", pkgNode)
		if isLowPriority {
			lowPriorityLeafNodes = append(lowPriorityLeafNodes, pkgNode)
		} else {
			leafNodes = append(leafNodes, pkgNode)
		}

		return
	})

	logger.Log.Infof("Discovered %d leaf nodes", len(leafNodes))

	return
}

// FindUnblockedNodesFromResult takes a package build result and returns a list of nodes that are now unblocked for building.
func FindUnblockedNodesFromResult(res *BuildResult, pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex, buildState *GraphBuildState, allowLowPriorityNodes bool) (unblockedNodes []*pkggraph.PkgNode, unblockedLowPriorityNodes []*pkggraph.PkgNode) {
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

	for node := range unblockedNodesMap {
		if buildState.IsNodeElevatedPriority(node) || allowLowPriorityNodes {
			unblockedNodes = append(unblockedNodes, node)
		} else {
			// If the scheduler isn't queueing low prioirity nodes then stash them away for later
			unblockedLowPriorityNodes = append(unblockedLowPriorityNodes, node)
		}
	}
	return
}

// findUnblockedNodesFromNode takes a built node and returns a list of nodes that are now unblocked by it.
func findUnblockedNodesFromNode(pkgGraph *pkggraph.PkgGraph, buildState *GraphBuildState, builtNode *pkggraph.PkgNode, unblockedNodes map[*pkggraph.PkgNode]bool) {
	dependents := pkgGraph.To(builtNode.ID())

	for dependents.Next() {
		logger.Log.Debugf("Checking if %v is unblocked by %v", dependents.Node(), builtNode)
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
