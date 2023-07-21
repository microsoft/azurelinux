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

	// Group build and test nodes together as they will be unblocked all at once for any given SRPM,
	// and building a single build node will result in all of them becoming available.
	buildNodes := make(map[string][]*pkggraph.PkgNode)
	testNodes := make(map[string][]*pkggraph.PkgNode)

	for _, node := range nodesToBuild {
		if node.Type == pkggraph.TypeLocalBuild {
			buildNodes[node.SrpmPath] = append(buildNodes[node.SrpmPath], node)
			continue
		}

		if node.Type == pkggraph.TypeTest {
			testNodes[node.SrpmPath] = append(testNodes[node.SrpmPath], node)
			continue
		}

		ancillaryNodes := []*pkggraph.PkgNode{node}
		isDelta := node.State == pkggraph.StateDelta
		req := buildRequest(pkgGraph, buildState, packagesToRebuild, node, ancillaryNodes, isCacheAllowed, isDelta)

		requests = append(requests, req)
	}

	requests = append(requests, groupedNodesToRequests(pkgGraph, buildState, packagesToRebuild, buildNodes, isCacheAllowed)...)
	requests = append(requests, groupedNodesToRequests(pkgGraph, buildState, packagesToRebuild, testNodes, isCacheAllowed)...)

	return
}

func groupedNodesToRequests(pkgGraph *pkggraph.PkgGraph, buildState *GraphBuildState, packagesToRebuild []*pkgjson.PackageVer, groupedNodes map[string][]*pkggraph.PkgNode, isCacheAllowed bool) (requests []*BuildRequest) {
	for _, nodes := range groupedNodes {
		// Check if any of the nodes in groupedNodes is a delta node and mark it. We will use this to determine if the
		// build is a delta build that might have pre-built .rpm files available.
		hasADeltaNode := false
		for _, node := range nodes {
			if node.State == pkggraph.StateDelta {
				hasADeltaNode = true
				break
			}
		}

		defaultNode := nodes[0]
		req := buildRequest(pkgGraph, buildState, packagesToRebuild, defaultNode, nodes, isCacheAllowed, hasADeltaNode)

		requests = append(requests, req)
	}

	return
}

func buildRequest(pkgGraph *pkggraph.PkgGraph, buildState *GraphBuildState, packagesToRebuild []*pkgjson.PackageVer, builtNode *pkggraph.PkgNode, ancillaryNodes []*pkggraph.PkgNode, isCacheAllowed, isDelta bool) (request *BuildRequest) {
	request = &BuildRequest{
		Node:           builtNode,
		PkgGraph:       pkgGraph,
		AncillaryNodes: ancillaryNodes,
		IsDelta:        isDelta,
	}

	request.CanUseCache = isCacheAllowed && canUseCacheForNode(pkgGraph, request.Node, packagesToRebuild, buildState)
	return
}

// canUseCacheForNode checks if the cache can be used for a given node.
// - It will check if the node corresponds to an entry in packagesToRebuild.
// - It will check if all dependencies of the node were also cached. Exceptions:
//   - "TypePreBuilt" nodes must use the cache and have no dependencies to check.
func canUseCacheForNode(pkgGraph *pkggraph.PkgGraph, node *pkggraph.PkgNode, packagesToRebuild []*pkgjson.PackageVer, buildState *GraphBuildState) (canUseCache bool) {
	// The "TypePreBuilt" nodes always use the cache.
	if node.Type == pkggraph.TypePreBuilt {
		canUseCache = true
		return
	}

	// Check if the node corresponds to an entry in packagesToRebuild
	packageVer := node.VersionedPkg
	canUseCache = !sliceutils.Contains(packagesToRebuild, packageVer, sliceutils.PackageVerMatch)
	if !canUseCache {
		logger.Log.Debugf("Marking (%s) for rebuild per user request", packageVer)
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
