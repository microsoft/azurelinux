// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"math"
	"path/filepath"
	"sort"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/sliceutils"
)

// nodeState represents the build state of a single node
type nodeState struct {
	available bool
	cached    bool
	usedDelta bool
	freshness int
}

const (
	// Negative values indicate that the node was rebuilt due to missing files and should gain the maximum configured freshness value.
	NodeFreshnessRebuildRequired int = -1
	// The highest possible freshness value, used to force unbounded cascading rebuilds.
	NodeFreshnessAbsoluteMax int = math.MaxInt
)

// GraphBuildState represents the build state of a graph.
type GraphBuildState struct {
	activeBuilds     map[int64]*BuildRequest
	nodeToState      map[*pkggraph.PkgNode]*nodeState
	maxFreshness     int
	failures         []*BuildResult
	reservedFiles    map[string]bool
	conflictingRPMs  map[string]bool
	conflictingSRPMs map[string]bool
}

// NewGraphBuildState returns a new GraphBuildState.
//   - reservedFiles is a list of reserved files which should NOT be rebuilt. Any files that ARE rebuilt will be recorded.
//   - maxFreshness is how fresh a newly rebuilt node is. Each dependant node will have a freshness of 'n-1', etc. until
//     '0' where the subsequent nodes will no longer be rebuilt. 'maxFreshness < 0' will cause unbounded cascading rebuilds,
//     while 'maxFreshness = 0' will cause no cascading rebuilds.
func NewGraphBuildState(reservedFiles []string, maxFreshness int) (g *GraphBuildState) {
	filesMap := make(map[string]bool)
	for _, file := range reservedFiles {
		filesMap[file] = true
	}

	//Use max int to represent infinity. This will cause unbounded cascading rebuilds so long as we build less that 2^31
	// or more likely 2^63 packages (i.e., ~2.3 billion packages)
	if maxFreshness < 0 {
		logger.Log.Debugf("maxFreshness was set to %d, unbounded cascading rebuilds (maxFreshness = %d)", maxFreshness, NodeFreshnessAbsoluteMax)
		maxFreshness = NodeFreshnessAbsoluteMax
	}

	return &GraphBuildState{
		activeBuilds:     make(map[int64]*BuildRequest),
		nodeToState:      make(map[*pkggraph.PkgNode]*nodeState),
		reservedFiles:    filesMap,
		conflictingRPMs:  make(map[string]bool),
		conflictingSRPMs: make(map[string]bool),
		maxFreshness:     maxFreshness,
	}
}

// DidNodeFail returns true if the requested node failed to be made available.
func (g *GraphBuildState) DidNodeFail(node *pkggraph.PkgNode) bool {
	state := g.nodeToState[node]
	return state != nil && !state.available
}

// IsNodeProcessed returns true if the requested node is has been processed already.
func (g *GraphBuildState) IsNodeProcessed(node *pkggraph.PkgNode) bool {
	return g.nodeToState[node] != nil
}

// IsNodeAvailable returns true if the requested node is available for other nodes to build with.
func (g *GraphBuildState) IsNodeAvailable(node *pkggraph.PkgNode) bool {
	state := g.nodeToState[node]
	return state != nil && state.available
}

// IsNodeCached returns true if the requested node has been cached.
func (g *GraphBuildState) IsNodeCached(node *pkggraph.PkgNode) bool {
	state := g.nodeToState[node]
	return state != nil && state.cached
}

// GetMaxFreshness returns the maximum freshness a node can have. (ie if a package is directly rebuilt due to user
// request, or missing files, it will have this freshness. Each dependant node will have a freshness of 'n-1', etc.
func (g *GraphBuildState) GetMaxFreshness() int {
	return g.maxFreshness
}

// GetFreshnessOfNode returns the freshness of a node.
func (g *GraphBuildState) GetFreshnessOfNode(node *pkggraph.PkgNode) int {
	return g.nodeToState[node].freshness
}

// IsNodeDelta returns true if the requested node was pre-downloaded as a delta package.
func (g *GraphBuildState) IsNodeDelta(node *pkggraph.PkgNode) bool {
	state := g.nodeToState[node]
	return state != nil && state.usedDelta
}

// ActiveBuilds returns a map of Node IDs to BuildRequests that represents all outstanding builds.
func (g *GraphBuildState) ActiveBuilds() map[int64]*BuildRequest {
	return g.activeBuilds
}

// ActiveSRPMs returns a list of all SRPMs, which are currently being built.
func (g *GraphBuildState) ActiveSRPMs() (builtSRPMs []string) {
	for _, buildRequest := range g.activeBuilds {
		if buildRequest.Node.Type == pkggraph.TypeLocalBuild {
			builtSRPMs = append(builtSRPMs, buildRequest.Node.SRPMFileName())
		}
	}

	return
}

// BuildFailures returns a slice of all failed builds.
func (g *GraphBuildState) BuildFailures() []*BuildResult {
	return g.failures
}

// ConflictingRPMs will return a list of *.rpm files which should not have been rebuilt.
// This list is based on the manifest of pre-built toolchain rpms.
func (g *GraphBuildState) ConflictingRPMs() (rpms []string) {
	rpms = sliceutils.SetToSlice(g.conflictingRPMs)
	sort.Strings(rpms)

	return rpms
}

// ConflictingSRPMs will return a list of *.src.rpm files which created rpms that should not have been rebuilt.
// This list is based on the manifest of pre-built toolchain rpms.
func (g *GraphBuildState) ConflictingSRPMs() (srpms []string) {
	srpms = sliceutils.SetToSlice(g.conflictingSRPMs)
	sort.Strings(srpms)

	return srpms
}

// RecordBuildRequest records a build request in the graph build state.
func (g *GraphBuildState) RecordBuildRequest(req *BuildRequest) {
	logger.Log.Debugf("Recording build request: %s", req.Node.FriendlyName())
	g.activeBuilds[req.Node.ID()] = req
}

// RemoveBuildRequest removes a build request from the graph build state.
func (g *GraphBuildState) RemoveBuildRequest(req *BuildRequest) {
	logger.Log.Debugf("Removing build request: %s", req.Node.FriendlyName())
	delete(g.activeBuilds, req.Node.ID())
}

func (g *GraphBuildState) isConflictWithToolchain(fileToCheck string) (hadConflict bool) {
	base := filepath.Base(fileToCheck)
	return g.reservedFiles[base]
}

// RecordBuildResult records a build result in the graph build state.
// - It will record the result as a failure if applicable.
// - It will record all ancillary nodes of the result.
func (g *GraphBuildState) RecordBuildResult(res *BuildResult, allowToolchainRebuilds bool) {

	logger.Log.Debugf("Recording build result: %s", res.Node.FriendlyName())

	delete(g.activeBuilds, res.Node.ID())

	if res.Err != nil {
		g.failures = append(g.failures, res)
	}

	// 'NodeFreshnessRebuildRequired' is a special value that indicates that the node was rebuilt due to  missing files
	// (user requested rebuilds are already at the max freshness). In this case, we want to reset the freshness to the
	// max, so that subsequent dependant nodes will be rebuilt. Also ensure that the freshness is not greater than the max.
	freshness := res.ActualFreshness
	if freshness < 0 || freshness > g.GetMaxFreshness() {
		if freshness != NodeFreshnessRebuildRequired {
			logger.Log.Debugf("Unexpected freshness value of '%d' for node '%s'. Defaulting to max freshness '%d'", freshness, res.Node.FriendlyName(), g.GetMaxFreshness())
		}
		freshness = g.GetMaxFreshness()
	}

	state := &nodeState{
		available: res.Err == nil,
		cached:    res.UsedCache,
		usedDelta: res.WasDelta,
		freshness: freshness,
	}

	for _, node := range res.AncillaryNodes {
		g.nodeToState[node] = state
	}

	if !allowToolchainRebuilds && !res.Skipped && !res.UsedCache {
		for _, file := range res.BuiltFiles {
			if g.isConflictWithToolchain(file) {
				g.conflictingRPMs[filepath.Base(file)] = true
				g.conflictingSRPMs[filepath.Base(res.Node.SrpmPath)] = true
			}
		}
	} else {
		logger.Log.Debugf("skipping checking conflicts since this is either not a built node (%v) or the ALLOW_TOOLCHAIN_REBUILDS flag was set to 'y'", res.Node)
	}

	return
}
