// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"fmt"
	"sync"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/timestamp"
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
func ConvertNodesToRequests(pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex, nodesToBuild []*pkggraph.PkgNode, packagesToRebuild, testsToRerun []*pkgjson.PackageVer, buildState *GraphBuildState, isCacheAllowed bool) (requests []*BuildRequest, err error) {
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

	newBuildReqs, err := buildNodesToRequests(pkgGraph, buildState, packagesToRebuild, testsToRerun, buildNodes, isCacheAllowed)
	if err != nil {
		err = fmt.Errorf("failed to convert build nodes to requests:\n%w", err)
		return
	}
	requests = append(requests, newBuildReqs...)
	newTestReqs, err := testNodesToRequests(pkgGraph, buildState, testsToRerun, testNodes)
	if err != nil {
		err = fmt.Errorf("failed to convert test nodes to requests:\n%w", err)
		return
	}
	requests = append(requests, newTestReqs...)

	return
}

func buildNodesToRequests(pkgGraph *pkggraph.PkgGraph, buildState *GraphBuildState, packagesToRebuild, testsToRerun []*pkgjson.PackageVer, buildNodesLists map[string][]*pkggraph.PkgNode, isCacheAllowed bool) (requests []*BuildRequest, err error) {
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

		// Check if we already queued up this build node for building.
		if buildState.IsSRPMBuildActive(defaultNode.SRPMFileName()) || buildState.IsNodeProcessed(defaultNode) {
			err = fmt.Errorf("unexpected duplicate build for (%s)", defaultNode.SRPMFileName())
			// Temporarily ignore the error, this state is unexpected but not fatal. Error return will be
			// restored later once the underlying cause of this error is fixed.
			logger.Log.Warnf(err.Error())
			err = nil
			continue
		}

		req := buildRequest(pkgGraph, buildState, packagesToRebuild, defaultNode, buildNodes, isCacheAllowed, hasADeltaNode)
		requests = append(requests, req)

		partnerTestNodeRequest := partnerTestNodesToRequest(pkgGraph, buildState, testsToRerun, buildNodes, req.UseCache)
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
		Freshness:      buildState.GetMaxFreshness(),
	}

	requiredRebuild := isRequiredRebuild(pkgGraph, request.Node, packagesToRebuild)
	if !requiredRebuild && isCacheAllowed {
		// We might be able to use the cache, set the freshness based on node's dependencies.
		request.UseCache, request.Freshness = canUseCacheForNode(pkgGraph, request.Node, buildState)
	}
	return
}

func partnerTestNodesToRequest(pkgGraph *pkggraph.PkgGraph, buildState *GraphBuildState, testsToRerun []*pkgjson.PackageVer, buildNodes []*pkggraph.PkgNode, buildUsesCache bool) (request *BuildRequest) {
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

	request = buildRequest(pkgGraph, buildState, testsToRerun, testNode, ancillaryTestNodes, buildUsesCache, isDelta)
	return
}

// testNodesToRequests converts lists of test nodes into test build requests.
// The function is expected to be only called for test nodes corresponding to build nodes,
// which have already been queued to build or finished building.
//
// NOTE: the caller must guarantee the build state does not change while this function is running.
func testNodesToRequests(pkgGraph *pkggraph.PkgGraph, buildState *GraphBuildState, testsToRerun []*pkgjson.PackageVer, testNodesLists map[string][]*pkggraph.PkgNode) (requests []*BuildRequest, err error) {
	const isDelta = false

	for _, testNodes := range testNodesLists {
		defaultTestNode := testNodes[0]
		srpmFileName := defaultTestNode.SRPMFileName()

		// Check if we already queued up this build node for building.
		if buildState.IsSRPMTestActive(srpmFileName) || buildState.IsNodeProcessed(defaultTestNode) {
			err = fmt.Errorf("unexpected duplicate test for (%s)", srpmFileName)
			// Temporarily ignore the error, this state is unexpected but not fatal. Error return will be
			// restored later once the underlying cause of this error is fixed.
			logger.Log.Warnf(err.Error())
			err = nil
			continue
		}

		buildUsedCache := buildState.IsSRPMCached(srpmFileName)
		if buildRequest := buildState.ActiveBuildFromSRPM(srpmFileName); buildRequest != nil {
			buildUsedCache = buildRequest.UseCache
		}

		testRequest := buildRequest(pkgGraph, buildState, testsToRerun, defaultTestNode, testNodes, buildUsedCache, isDelta)
		requests = append(requests, testRequest)
	}

	return
}

// isRequiredRebuild checks if a node is required to be rebuilt due to:
// - missing RPMs or
// - user explicitly requesting the node to be rebuilt.
func isRequiredRebuild(pkgGraph *pkggraph.PkgGraph, node *pkggraph.PkgNode, packagesToRebuild []*pkgjson.PackageVer) bool {
	return nodeHasMissingRPMs(pkgGraph, node) || nodeRequestedForRebuildByUser(node, packagesToRebuild)
}

// canUseCacheForNode checks if the cache can be used for a given node by:
//   - Assume the node is stale to begin (freshness == 0).
//   - Check if all dependencies of the node were cached, and calculate the expected freshness of the node based on the freshest dependency.
//   - If all dependencies are cached (freshness == 0, aka stale) then the node will keep freshness 0 and may use the cache.
//   - If any dependency is fresh (aka freshness > 0) then the node can't use the cache and will inherit the freshness of
//     the freshest dependency (possibly adjusted by -1 for certain edges).
func canUseCacheForNode(pkgGraph *pkggraph.PkgGraph, node *pkggraph.PkgNode, buildState *GraphBuildState) (canUseCache bool, freshness uint) {
	freshness = 0
	canUseCache = true

	// If any of the node's dependencies were built instead of being cached then a build is required. We treat any node
	// with a freshness > 0 as being built. Each layer of the build completed will decrement the freshness of the node by 1.
	dependencies := pkgGraph.From(node.ID())
	for dependencies.Next() {
		dependency := dependencies.Node().(*pkggraph.PkgNode)

		inheritedFreshness, shouldRebuild := calculateExpectedFreshness(dependency, buildState)
		if inheritedFreshness > freshness {
			freshness = inheritedFreshness
		}

		if shouldRebuild {
			logger.Log.Debugf("Can't use cached version of %v because %v has been rebuilt with a freshness of %d", node.FriendlyName(), dependency.FriendlyName(), inheritedFreshness)
			canUseCache = false
		}
	}

	return
}

// calculateExpectedFreshness calculates how "fresh" a node will be based on one of its dependencies, and if that
// dependency should cause a rebuild. This function will determine if the freshness should be attenuated based on
// the dependency type.
func calculateExpectedFreshness(dependencyNode *pkggraph.PkgNode, buildState *GraphBuildState) (expectedFreshness uint, shouldRebuild bool) {
	// Remote nodes are always 'stale' and should never generate a rebuild.
	if dependencyNode.Type == pkggraph.TypeRemoteRun {
		return 0, false
	}

	expectedFreshness = buildState.GetFreshnessOfNode(dependencyNode)
	shouldRebuild = expectedFreshness > 0
	// The transition from (* -> run) nodes is sufficient to attenuate the freshness throughout the graph. For BuildRequires,
	// each build node will always be accompanied by a run node (i.e., no other nodes depend directly on the build
	// node, and we would like the associated run node to inherit its build node's freshness). We also want to
	// attenuate for runtime requires which again will generally be a (run -> run) transition. Meta nodes may be interposed
	// between any nodes so we pass the freshness through unchanged everywhere else.
	if dependencyNode.Type == pkggraph.TypeLocalRun && expectedFreshness != 0 {
		expectedFreshness -= 1
	}

	return expectedFreshness, shouldRebuild
}

// nodeHasMissingRPMs checks if all RPMs expected from the node's SRPM are present.
// If any of the RPMs produced by the SRPM are missing, we must build the SRPM and reset the freshness of the node.
func nodeHasMissingRPMs(pkgGraph *pkggraph.PkgGraph, node *pkggraph.PkgNode) (rpmsMissing bool) {
	expectedFiles, missingFiles := pkggraph.FindRPMFiles(node.SrpmPath, pkgGraph, nil)

	rpmsMissing = len(missingFiles) != 0
	if rpmsMissing && len(missingFiles) < len(expectedFiles) {
		logger.Log.Infof("SRPM (%s) will be rebuilt due to partially missing components: %v", node.SRPMFileName(), missingFiles)
	}

	return
}

// nodeRequestedForRebuildByUser checks if the user has explicitly requested the node to be rebuilt.
func nodeRequestedForRebuildByUser(node *pkggraph.PkgNode, packagesToRebuild []*pkgjson.PackageVer) (rebuildRequested bool) {
	packageVer := node.VersionedPkg
	rebuildRequested = sliceutils.Contains(packagesToRebuild, packageVer, sliceutils.PackageVerMatch)
	if rebuildRequested {
		logger.Log.Infof("SRPM (%s) will be rebuilt due to user request.", packageVer)
	}

	return
}
