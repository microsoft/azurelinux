// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"sync"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/sliceutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
)

// ConvertNodesToRequests converts a slice of nodes into a slice of build requests.
// - It will determine if the cache can be used for prebuilt nodes.
// - It will group similar build nodes together into AncillaryNodes.
func ConvertNodesToRequests(pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex, nodesToBuild []*pkggraph.PkgNode, packagesToRebuild []*pkgjson.PackageVer, buildState *GraphBuildState, isCacheAllowed bool) (requests []*BuildRequest) {
	timestamp.StartEvent("generate requests", nil)
	defer timestamp.StopEvent(nil)

	graphMutex.RLock()
	defer graphMutex.RUnlock()

	// Group build nodes together as they will be unblocked all at once for any given SRPM,
	// and building a single build node will result in all of them becoming available.
	buildNodes := make(map[string][]*pkggraph.PkgNode)

	for _, node := range nodesToBuild {
		if node.Type == pkggraph.TypeLocalBuild {
			buildNodes[node.SrpmPath] = append(buildNodes[node.SrpmPath], node)
			continue
		}

		req := &BuildRequest{
			Node:              node,
			PkgGraph:          pkgGraph,
			AncillaryNodes:    []*pkggraph.PkgNode{node},
			IsDelta:           node.State == pkggraph.StateDelta,
			ExpectedFreshness: buildState.GetMaxFreshness(),
		}

		requiredRebuild := isRequiredRebuild(req.Node, packagesToRebuild)
		if !requiredRebuild && isCacheAllowed {
			// We might be able to use the cache, set the freshness based on the node's dependencies.
			req.CanUseCache, req.ExpectedFreshness = canUseCacheForNode(pkgGraph, req.Node, buildState)
		}
		logger.Log.Tracef("Preparing non-build request: requiredRebuild: %v, isCacheAllowed: %v, canUseCache: %v, freshness: %v", requiredRebuild, isCacheAllowed, req.CanUseCache, req.ExpectedFreshness)

		requests = append(requests, req)
	}

	// For each SRPM path, process the list of build nodes associated with it.
	for _, nodes := range buildNodes {
		const defaultNode = 0

		// Check if any of the nodes in buildNodes is a delta node and mark it. We will use this to determine if the
		// build is a delta build that might have pre-built .rpm files available.
		hasADeltaNode := false
		for _, node := range nodes {
			if node.State == pkggraph.StateDelta {
				hasADeltaNode = true
				break
			}
		}

		req := &BuildRequest{
			Node:              nodes[defaultNode],
			PkgGraph:          pkgGraph,
			AncillaryNodes:    nodes,
			IsDelta:           hasADeltaNode,
			ExpectedFreshness: buildState.GetMaxFreshness(),
		}

		requiredRebuild := isRequiredRebuild(req.Node, packagesToRebuild)
		if !requiredRebuild && isCacheAllowed {
			// We might be able to use the cache, set the freshness based on node's dependencies.
			req.CanUseCache, req.ExpectedFreshness = canUseCacheForNode(pkgGraph, req.Node, buildState)
		}
		logger.Log.Tracef("Preparing build request: requiredRebuild: %v, isCacheAllowed: %v, canUseCache: %v, freshness: %v", requiredRebuild, isCacheAllowed, req.CanUseCache, req.ExpectedFreshness)

		requests = append(requests, req)
	}

	return
}

// isRequiredRebuild checks if a node is required to be rebuilt based  on the packagesToRebuild list.
func isRequiredRebuild(node *pkggraph.PkgNode, packagesToRebuild []*pkgjson.PackageVer) (requiredRebuild bool) {
	packageVer := node.VersionedPkg
	requiredRebuild = sliceutils.Contains(packagesToRebuild, packageVer, sliceutils.PackageVerMatch)
	if requiredRebuild {
		logger.Log.Debugf("Marking (%s) for rebuild per user request", packageVer)
	}
	return
}

// canUseCacheForNode checks if the cache can be used for a given node by:
//   - Assume the node is stale to begin (freshness == 0).
//   - Check if all dependencies of the node were cached, and calculate the expected freshness of the node based on the freshest dependency.
//   - If all dependencies are cached (aka stale, freshness == 0) then the node will keep freshness == 0 and may use the cache.
//   - If any dependency was rebuilt then the node can't use the cache and will inherit the freshness of the freshest dependency (possibly -1 for certain edges).
func canUseCacheForNode(pkgGraph *pkggraph.PkgGraph, node *pkggraph.PkgNode, buildState *GraphBuildState) (canUseCache bool, expectedNodeFreshness int) {
	// If any of the node's dependencies were built instead of being cached then a build is required. We treat any node
	// with a freshness > 0 as being built. Each layer of the build completed will decrement the freshness of the node by 1.
	expectedNodeFreshness = 0
	canUseCache = true

	dependencies := pkgGraph.From(node.ID())
	for dependencies.Next() {
		dependency := dependencies.Node().(*pkggraph.PkgNode)

		dependencyFreshness, shouldRebuild := calculateExpectedFreshness(node, dependency, buildState)
		if dependencyFreshness > expectedNodeFreshness {
			expectedNodeFreshness = dependencyFreshness
		}

		if shouldRebuild {
			logger.Log.Debugf("Can't use cached version of %v because %v is rebuilding", node.FriendlyName(), dependency.FriendlyName())
			canUseCache = false
		}
	}

	return
}

// calculateExpectedFreshness calculates how "fresh" a node will be based on one of its dependencies, and if that
// dependency should cause a rebuild. This function will determine if the freshness should be attenuated based on
// the dependency type.
func calculateExpectedFreshness(currentNode, dependencyNode *pkggraph.PkgNode, buildState *GraphBuildState) (expectedFreshness int, shouldRebuild bool) {
	// Remote nodes are always 'stale' and should never generate a rebuild.
	if dependencyNode.Type == pkggraph.TypeRemoteRun {
		return 0, false
	}

	expectedFreshness = buildState.GetFreshnessOfNode(dependencyNode)
	shouldRebuild = expectedFreshness > 0
	// The transition from (* -> run) nodes is sufficient to attenuate the freshness through the graph. For BuildRequires,
	// each build node will always be accompanied by a run node (i.e., no other nodes depend directly on the build
	// node, and we would like the associated run node to inherit it's build node's freshness). We also want to
	// attenuate for runtime requires wich again will generally be a (run -> run) transition. Meta nodes may be interposed
	// between any nodes so we pass the freshness through unchanged everywhere else.
	if dependencyNode.Type == pkggraph.TypeLocalRun && expectedFreshness != 0 {
		expectedFreshness -= 1
	}

	return expectedFreshness, shouldRebuild
}
