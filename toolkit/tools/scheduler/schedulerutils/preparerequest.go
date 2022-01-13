// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"sync"

	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkggraph"
	"microsoft.com/pkggen/internal/sliceutils"
)

// ConvertNodesToRequests converts a slice of nodes into a slice of build requests.
// - It will determine if the cache can be used for prebuilt nodes.
// - It will group similar build nodes together into AncillaryNodes.
func ConvertNodesToRequests(pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex, nodesToBuild []*pkggraph.PkgNode, packagesToRebuild []string, buildState *GraphBuildState, isCacheAllowed bool, forceUseCache bool, noDepRebuild string) (requests []*BuildRequest) {
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
		}

		if forceUseCache == true {
			req.CanUseCache = true
		} else {
			req.CanUseCache = isCacheAllowed && canUseCacheForNode(pkgGraph, req.Node, packagesToRebuild, buildState, noDepRebuild)
		}

		requests = append(requests, req)
	}

	for _, nodes := range buildNodes {
		const defaultNode = 0

		req := &BuildRequest{
			Node:           nodes[defaultNode],
			PkgGraph:       pkgGraph,
			AncillaryNodes: nodes,
		}

		if forceUseCache == true {
			req.CanUseCache = true
		} else {
			req.CanUseCache = isCacheAllowed && canUseCacheForNode(pkgGraph, req.Node, packagesToRebuild, buildState, noDepRebuild)
		}

		requests = append(requests, req)
	}

	return
}

// canUseCacheForNode checks if the cache can be used for a given node.
// - It will check if the node corresponds to an entry in packagesToRebuild.
// - It will check if all dependencies of the node were also cached. Exceptions:
//		- "TypePreBuilt" nodes must use the cache and have no dependencies to check.
func canUseCacheForNode(pkgGraph *pkggraph.PkgGraph, node *pkggraph.PkgNode, packagesToRebuild []string, buildState *GraphBuildState, noDepRebuild string) (canUseCache bool) {
	// The "TypePreBuilt" nodes always use the cache.
	if node.Type == pkggraph.TypePreBuilt {
		canUseCache = true
		return
	}

	// Check if the node corresponds to an entry in packagesToRebuild
	specName := node.SpecName()
	canUseCache = !sliceutils.Contains(packagesToRebuild, specName, sliceutils.StringMatch)
	if !canUseCache {
		logger.Log.Debugf("Marking (%s) for rebuild per user request", specName)
		return
	}

	// Don't rebuild package even if its dependency is newly built. Makes sense while running TestRPM
	if noDepRebuild == "y" {
		canUseCache = true
		return
	}

	// If any of the node's dependencies were built instead of being cached then a build is required.
	dependencies := pkgGraph.From(node.ID())
	for dependencies.Next() {
		dependency := dependencies.Node().(*pkggraph.PkgNode)

		if !buildState.IsNodeCached(dependency) {
			canUseCache = false
			break
		}
	}

	return
}
