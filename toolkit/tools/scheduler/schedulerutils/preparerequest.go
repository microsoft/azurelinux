// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"sync"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/sliceutils"
)

// ConvertNodesToRequests converts a slice of nodes into a slice of build requests.
// - It will determine if the cache can be used for prebuilt nodes.
// - It will group similar build nodes together into AncillaryNodes.
func ConvertNodesToRequests(pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex, nodesToBuild []*pkggraph.PkgNode, packagesToRebuild []string, buildState *GraphBuildState, isCacheAllowed bool, deltaBuild bool) (requests []*BuildRequest) {
	graphMutex.RLock()
	defer graphMutex.RUnlock()

	// Group build nodes together as they will be unblocked all at once for any given SRPM,
	// and building a single build node will result in all of them becoming available.
	buildNodes := make(map[string][]*pkggraph.PkgNode)

	for _, node := range nodesToBuild {
		if node.Type == pkggraph.TypeBuild {
			buildNodes[node.SrpmPath] = append(buildNodes[node.SrpmPath], node)
			continue
		}

		req := &BuildRequest{
			Node:           node,
			PkgGraph:       pkgGraph,
			AncillaryNodes: []*pkggraph.PkgNode{node},
			IsDelta:        node.State == pkggraph.StateDelta,
		}

		req.CanUseCache = isCacheAllowed && canUseCacheForNode(pkgGraph, req.Node, packagesToRebuild, buildState, deltaBuild)

		requests = append(requests, req)
	}

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
			Node:           nodes[defaultNode],
			PkgGraph:       pkgGraph,
			AncillaryNodes: nodes,
			IsDelta:        hasADeltaNode,
		}

		req.CanUseCache = isCacheAllowed && canUseCacheForNode(pkgGraph, req.Node, packagesToRebuild, buildState, deltaBuild)

		requests = append(requests, req)
	}

	return
}

// canUseCacheForNode checks if the cache can be used for a given node.
// - It will check if the node corresponds to an entry in packagesToRebuild.
// - It will check if all dependencies of the node were also cached. Exceptions:
//   - "TypePreBuilt" nodes must use the cache and have no dependencies to check.
func canUseCacheForNode(pkgGraph *pkggraph.PkgGraph, node *pkggraph.PkgNode, packagesToRebuild []string, buildState *GraphBuildState, deltaBuild bool) (canUseCache bool) {
	// The "TypePreBuilt" nodes always use the cache.
	if node.Type == pkggraph.TypePreBuilt {
		canUseCache = true
		return
	}

	// Check if the node corresponds to an entry in packagesToRebuild
	specName := node.SpecName()
	// Some nodes have no VersionedPkg, but get the name if it exists otherwise use ""
	pkgName := ""
	if node.VersionedPkg != nil {
		pkgName = node.VersionedPkg.Name
	}
	canUseCache = !sliceutils.Contains(packagesToRebuild, specName, sliceutils.StringMatch) &&
		!sliceutils.Contains(packagesToRebuild, pkgName, sliceutils.StringMatch)
	if !canUseCache {
		logger.Log.Debugf("Marking (%s) for rebuild per user request", specName)
		return
	}

	// If delta build enabled, then we can use the cache, unless a dependency of this package is rebuilding
	if deltaBuild == true {
		logger.Log.Warnf("Delta build: Using cached version of %v regardles of rebuilding dependencies", node.FriendlyName())
		canUseCache = true
		return
	}

	// If any of the node's dependencies were built instead of being cached then a build is required.
	dependencies := pkgGraph.From(node.ID())
	for dependencies.Next() {
		dependency := dependencies.Node().(*pkggraph.PkgNode)

		if !buildState.IsNodeCached(dependency) {
			logger.Log.Debugf("Can't use cached version of %v because %v is rebuilding", node.FriendlyName(), dependency.FriendlyName())
			canUseCache = false
			break
		}
	}

	return
}
