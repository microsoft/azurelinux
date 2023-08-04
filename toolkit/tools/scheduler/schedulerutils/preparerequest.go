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
//
// Explanation of handling of the test nodes:
//  1. The virtual B -> T edge guarantees the build node are unblocked and analyzed first.
//  2. Once the build node is unblocked, analyze its partner test node in partnerTestNodesToRequest().
//     We remove the virtual edge and the test node either gets immediately queued or is blocked on some extra dependencies.
//     Blocking is decided by canUseCacheForNode().
//  3. If the test node ends up being blocked, it gets re-analyzed later once its dependencies are done.
//     The test nodes unblocked this way end up inside the 'testNodes' list in ConvertNodesToRequests()
//     and are queued for building in the testNodesToRequests() function.
//     At this point the partner build nodes for these test nodes have either already finished building or are being built,
//     thus the check for active and cached SRPMs inside testNodesToRequests().
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

	requests = append(requests, buildNodesToRequests(pkgGraph, buildState, packagesToRebuild, buildNodes, isCacheAllowed)...)
	requests = append(requests, testNodesToRequests(pkgGraph, buildState, packagesToRebuild, testNodes)...)

	return
}

func buildNodesToRequests(pkgGraph *pkggraph.PkgGraph, buildState *GraphBuildState, packagesToRebuild []*pkgjson.PackageVer, buildNodesLists map[string][]*pkggraph.PkgNode, isCacheAllowed bool) (requests []*BuildRequest) {
	for _, buildNodes := range buildNodesLists {
		// Check if any of the build nodes is a delta node and mark it. We will use this to determine if the
		// build is a delta build that might have pre-built .rpm files available.
		hasADeltaNode := false
		for _, node := range buildNodes {
			if node.State == pkggraph.StateDelta {
				hasADeltaNode = true
				break
			}
		}

		defaultNode := buildNodes[0]
		req := buildRequest(pkgGraph, buildState, packagesToRebuild, defaultNode, buildNodes, isCacheAllowed, hasADeltaNode)

		if req.UseCache {
			expectedFiles, missingFiles := pkggraph.FindRPMFiles(defaultNode.SrpmPath, pkgGraph, nil)
			if len(missingFiles) > 0 && len(missingFiles) < len(expectedFiles) {
				logger.Log.Infof("SRPM '%s' will be rebuilt due to partially missing components: %v", defaultNode.SRPMFileName(), missingFiles)
			}

			req.ExpectedFiles = expectedFiles
			req.UseCache = len(missingFiles) == 0
		}

		requests = append(requests, req)

		partnerTestNodeRequest := partnerTestNodesToRequest(pkgGraph, buildState, packagesToRebuild, buildNodes, req.UseCache)
		if partnerTestNodeRequest != nil {
			requests = append(requests, partnerTestNodeRequest)
		}
	}

	return
}

func buildNodeToTestNode(pkgGraph *pkggraph.PkgGraph, buildNode *pkggraph.PkgNode) (testNode *pkggraph.PkgNode) {
	dependents := pkgGraph.To(buildNode.ID())
	for dependents.Next() {
		dependent := dependents.Node().(*pkggraph.PkgNode)

		if dependent.Type == pkggraph.TypeTest {
			testNode = dependent
			break
		}
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

	request.UseCache = isCacheAllowed && canUseCacheForNode(pkgGraph, request.Node, packagesToRebuild, buildState)
	return
}

func partnerTestNodesToRequest(pkgGraph *pkggraph.PkgGraph, buildState *GraphBuildState, packagesToRebuild []*pkgjson.PackageVer, buildNodes []*pkggraph.PkgNode, buildUsesCache bool) (request *BuildRequest) {
	const isDelta = false

	defaultBuildNode := buildNodes[0]
	testNode := buildNodeToTestNode(pkgGraph, defaultBuildNode)
	if testNode == nil {
		return
	}

	ancillaryTestNodes := []*pkggraph.PkgNode{}
	for _, buildNode := range buildNodes {
		testNode = buildNodeToTestNode(pkgGraph, buildNode)

		// Removing edges even if tests are blocked by other dependencies,
		// so that they can get unblocked once these other dependencies are available.
		pkgGraph.RemoveEdge(testNode.ID(), buildNode.ID())

		ancillaryTestNodes = append(ancillaryTestNodes, testNode)
	}

	if !isNodeUnblocked(pkgGraph, buildState, testNode) {
		return
	}

	return &BuildRequest{
		Node:           testNode,
		PkgGraph:       pkgGraph,
		AncillaryNodes: ancillaryTestNodes,
		IsDelta:        isDelta,
		UseCache:       buildUsesCache && canUseCacheForNode(pkgGraph, testNode, packagesToRebuild, buildState),
	}
}

// testNodesToRequests converts lists of test nodes into test build requests.
// The function is expected to be only called for test nodes corresponding to build nodes,
// which have already been queued to build or finished building.
//
// NOTE: the caller must guarantee the build state does not change while this function is running.
func testNodesToRequests(pkgGraph *pkggraph.PkgGraph, buildState *GraphBuildState, packagesToRebuild []*pkgjson.PackageVer, testNodesLists map[string][]*pkggraph.PkgNode) (requests []*BuildRequest) {
	const isDelta = false

	for _, testNodes := range testNodesLists {
		defaultTestNode := testNodes[0]
		srpmFileName := defaultTestNode.SRPMFileName()

		buildUsedCache := buildState.IsSRPMCached(srpmFileName)
		if buildRequest := buildState.ActiveBuildFromSRPM(srpmFileName); buildRequest != nil {
			buildUsedCache = buildRequest.UseCache
		}

		testRequest := buildRequest(pkgGraph, buildState, packagesToRebuild, defaultTestNode, testNodes, buildUsedCache, isDelta)
		requests = append(requests, testRequest)
	}

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
