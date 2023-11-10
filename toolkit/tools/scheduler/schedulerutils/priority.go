// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"fmt"
	"path/filepath"
	"sync"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/rpm"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
	"gonum.org/v1/gonum/graph"
	"gonum.org/v1/gonum/graph/traverse"
)

// The scheduler currently supports three different priority levels for nodes: low, medium, and high. These are used to
// prioritize which jobs the workers will pick up first. The priority levels are used to optimize the build process by
// prioritizing the packages that will bring the most benefit to the build process. The priority levels are as follows:
//   - Low: These are packages that are not expected to be needed for the build process. These packages will be built
//     after the medium and high priority packages only if the build is stuck.
//   - Medium: These are packages that are set by PACKAGE_BUILD_LIST, CONFIG_FILE, etc., and all of their dependencies.
//     This is the "normal" priority level for packages.
//   - High: High priority is used for packages that may cause changes in the build goals. The earlier they are processed
//     the more likely the build will be optimized. This is currently used for packages that satisfy implicit provides
//     that are expected to be needed for the build process.
const (
	LowNodePriority    int = 0
	MediumNodePriority int = 1
	HighNodePriority   int = 2
	MinPriority            = LowNodePriority
	MaxPriority            = HighNodePriority
)

type NodePriorityMap struct {
	priorities map[*pkggraph.PkgNode]int
}

// BuildNodeResolutionPriorityMap will build a map of node priorities for the given graph. The graph is expected to
// contain a goal node named "PackagesToBuild" that lists the packages that should be built. A map of nodes will list
// all nodes that do not have default (0) priority. Any node not in the map will be assumed to have the implicit default
// priority of 0.
func BuildNodeResolutionPriorityMap(pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex) (nodePriorityMap *NodePriorityMap, err error) {
	timestamp.StartEvent("generate priority map", nil)
	defer timestamp.StopEvent(nil)

	graphMutex.RLock()
	defer graphMutex.RUnlock()

	// Any node not found in the prioirty set will have an implicit default priority of 0. This should be the nodes in the graph
	// that we do not expect to need.
	nodePriorityMap = &NodePriorityMap{
		priorities: make(map[*pkggraph.PkgNode]int),
	}

	// Create a fake optimized subgraph, this should be the bulk of the packages we expect to need.
	// Set these to medium.
	logger.Log.Debugf("Setting priority for requested build nodes")
	buildGoalNode := pkgGraph.FindGoalNode(buildGoalNodeName)
	if buildGoalNode == nil {
		err = fmt.Errorf("could not find goal node %s", buildGoalNodeName)
		return
	}
	subgraph, err := pkgGraph.CreateSubGraph(buildGoalNode)
	if err != nil {
		logger.Log.Warnf("Failed to create subgraph error: %s", err)
		return
	}
	for _, node := range subgraph.AllNodes() {
		nodePriorityMap.IncreaseNodePriority(node, MediumNodePriority)
	}

	// Finally, we want to prioritize resolving any implicit nodes in the subgraph. Implicit nodes are what blocks the
	// scheduler from optimizing and getting a true copy of the above sub-grpah. This is done by finding a real
	// package that should satisfy the implicit node and prioritizing that package and all of its dependencies above all
	// else.
	// This process is best-effort and does not guarantee that all implicit nodes will be satisfied, or that the
	// predicted package will be the one that actually provides the implicit provide. If the prediction is incorrect
	// the scheduler can still rely on the low-priority nodes to eventually provide the correct result.
	logger.Log.Debugf("Setting priority for implicit provider nodes")
	implicitNodes := subgraph.AllImplicitNodes()
	satisfyingNodes := []*pkggraph.PkgNode{}
	for _, implicitNode := range implicitNodes {
		satisfyingNodesForImplicitNode, findErr := findMatchesForImplicit(implicitNode, pkgGraph)
		if findErr != nil {
			err = fmt.Errorf("failed to find match for implicit node (%s):\n%w", implicitNode.FriendlyName(), findErr)
			return
		}
		if len(satisfyingNodesForImplicitNode) > 0 {
			logger.Log.Debugf("For implicit (%s), we found (%v) that likely provides it.", implicitNode.FriendlyName(), satisfyingNodesForImplicitNode)
			satisfyingNodes = append(satisfyingNodes, satisfyingNodesForImplicitNode...)
		}
	}

	// For each real node we found, we want to prioritize it and all of its dependencies at high.
	for _, realBuildNode := range satisfyingNodes {
		nodePriorityMap.SetSubgraphPriority(pkgGraph, realBuildNode, HighNodePriority)
	}

	return
}

// IsElevatedPriority returns true if the given node is a medium or high priority node.
func (s NodePriorityMap) IsElevatedPriority(node *pkggraph.PkgNode) bool {
	pri := s.priorities[node]
	return pri > LowNodePriority
}

// IncreaseNodePriority will increase the priority of the given node to the given priority. If the node already has a
// higher priority, the priority will not be changed.
func (s NodePriorityMap) IncreaseNodePriority(node *pkggraph.PkgNode, priority int) {
	// Limit range of priority to MinPriority and MaxPriority
	if priority < MinPriority {
		priority = MinPriority
	} else if priority > MaxPriority {
		priority = MaxPriority
	}

	if s.priorities[node] < priority {
		logger.Log.Tracef("Setting %s to priority %d", node.FriendlyName(), priority)
		s.priorities[node] = priority
	} else {
		logger.Log.Tracef("Leaving %s at existing priority %d", node.FriendlyName(), s.priorities[node])
	}
}

func (s NodePriorityMap) GetPriority(node *pkggraph.PkgNode) (priority int) {
	return s.priorities[node]
}

// SetSubgraphPriority will increase the priority of the given node and all of its dependencies to the given priority.
func (s NodePriorityMap) SetSubgraphPriority(pkgGraph *pkggraph.PkgGraph, node *pkggraph.PkgNode, priority int) {
	search := traverse.BreadthFirst{}

	// Walk the graph from the node and prioritize all its dependencies
	search.Walk(pkgGraph, node, func(n graph.Node, d int) (stopSearch bool) {
		pkgNode := n.(*pkggraph.PkgNode)
		logger.Log.Warnf("Setting %s to priority %d", pkgNode.FriendlyName(), priority)
		s.IncreaseNodePriority(pkgNode, priority)
		return
	})
}

// findMatchesForImplicit will try and find real packages that satisfies the implicit node. This is done through four methods:
// 1. Find the best package node for the implicit node
// 2. Try to find a local build node that is backed by the exact same RPM as the implicit node
// 3. Try 1. again with the version information stripped
// 4. Finally try 2. again, also with  the version information from the .rpm path removed
func findMatchesForImplicit(implicitNode *pkggraph.PkgNode, pkgGraph *pkggraph.PkgGraph) (matches []*pkggraph.PkgNode, err error) {
	const (
		stripVersion = true
		matchVersion = false
	)

	matches, err = findBuildNodesByGraph(implicitNode, pkgGraph, matchVersion)
	if err != nil {
		err = fmt.Errorf("failed to find best package node for implicit node (%s):\n%w", implicitNode.FriendlyName(), err)
		return
	}
	if len(matches) > 0 {
		return
	}

	matches = findBuildNodesByPath(implicitNode.RpmPath, pkgGraph, matchVersion)
	if len(matches) > 0 {
		return
	}

	matches, err = findBuildNodesByGraph(implicitNode, pkgGraph, stripVersion)
	if err != nil {
		err = fmt.Errorf("failed to find best package node for implicit node (%s):\n%w", implicitNode.FriendlyName(), err)
		return
	}
	if len(matches) > 0 {
		return
	}

	// Exact match via RPM path
	matches = findBuildNodesByPath(implicitNode.RpmPath, pkgGraph, stripVersion)
	if len(matches) > 0 {
		return
	}

	return
}

// findBuildNodesByGraph will try to find a build node that satisfies the implicit node by looking at the best package node. We don't want to search
// for run nodes since those may pull in additional runtime dependencies we may not care about. Once the graph is optimized we will have an exhaustive
// list of nodes and we can build any actual runtime dependencies we need at that point.
func findBuildNodesByGraph(implicitNode *pkggraph.PkgNode, pkgGraph *pkggraph.PkgGraph, stripVersion bool) (buildNodes []*pkggraph.PkgNode, err error) {
	version := *implicitNode.VersionedPkg
	if stripVersion {
		version = pkgjson.PackageVer{
			Name: implicitNode.VersionedPkg.Name,
		}
	}
	lookup, err := pkgGraph.FindBestPkgNode(&version)
	if err != nil {
		err = fmt.Errorf("failed to find best package node for implicit node (%s):\n%w", implicitNode.FriendlyName(), err)
		return
	}
	if lookup != nil && lookup.BuildNode != nil {
		buildNodes = []*pkggraph.PkgNode{lookup.BuildNode}
	}
	return
}

// findBuildNodesByPath will try to find a build node that satisfies the implicit node by looking at the RPM path. This is a best-effort
// approach that will try to find a build node that has the same RPM path as the implicit node.
func findBuildNodesByPath(rpmPath string, pkgGraph *pkggraph.PkgGraph, stripVersion bool) (buildNodes []*pkggraph.PkgNode) {
	buildNodes = make([]*pkggraph.PkgNode, 0)
	implicitRPMBaseName := filepath.Base(rpmPath)

	var err error
	if stripVersion {
		implicitRPMBaseName, err = rpm.ExtractNameFromRPMPath(implicitRPMBaseName)
		if err != nil {
			logger.Log.Warnf("Failed to extract name from RPM path: %s", err)
			return nil
		}
	}

	for _, node := range pkgGraph.AllBuildNodes() {
		graphNodeRPMBaseName := filepath.Base(node.RpmPath)
		if stripVersion {
			graphNodeRPMBaseName, err = rpm.ExtractNameFromRPMPath(graphNodeRPMBaseName)
			if err != nil {
				continue
			}
		}
		if implicitRPMBaseName == graphNodeRPMBaseName {
			buildNodes = append(buildNodes, node)
			break
		}
	}
	return
}
