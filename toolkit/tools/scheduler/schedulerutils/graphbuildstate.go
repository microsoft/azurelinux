// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"path/filepath"
	"sort"

	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkggraph"
)

// nodeState represents the build state of a single node
type nodeState struct {
	available bool
	cached    bool
}

// GraphBuildState represents the build state of a graph.
type GraphBuildState struct {
	activeBuilds     map[int64]*BuildRequest
	nodeToState      map[*pkggraph.PkgNode]*nodeState
	failures         []*BuildResult
	reservedFiles    map[string]bool
	conflictingRPMs  map[string]bool
	conflictingSRPMs map[string]bool
}

// NewGraphBuildState returns a new GraphBuildState.
// - reservedFiles is a list of reserved files which should NOT be rebuilt. Any files that ARE rebuilt will be recorded.
func NewGraphBuildState(reservedFiles []string) (g *GraphBuildState) {
	filesMap := make(map[string]bool)
	for _, file := range reservedFiles {
		filesMap[file] = true
	}
	return &GraphBuildState{
		activeBuilds:     make(map[int64]*BuildRequest),
		nodeToState:      make(map[*pkggraph.PkgNode]*nodeState),
		reservedFiles:    filesMap,
		conflictingRPMs:  make(map[string]bool),
		conflictingSRPMs: make(map[string]bool),
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

// ActiveBuilds returns a map of Node IDs to BuildRequests that represents all outstanding builds.
func (g *GraphBuildState) ActiveBuilds() map[int64]*BuildRequest {
	return g.activeBuilds
}

// ActiveSRPMs returns a list of all SRPMs, which are currently being built.
func (g *GraphBuildState) ActiveSRPMs() (builtSRPMs []string) {
	for _, buildRequest := range g.activeBuilds {
		if buildRequest.Node.Type == pkggraph.TypeBuild {
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
	rpms = make([]string, len(g.conflictingRPMs))
	i := 0
	for f := range g.conflictingRPMs {
		rpms[i] = f
		i++
	}
	sort.Strings(rpms)
	return rpms
}

// ConflictingSRPMs will return a list of *.src.rpm files which created rpms that should not have been rebuilt.
// This list is based on the manifest of pre-built toolchain rpms.
func (g *GraphBuildState) ConflictingSRPMs() (srpms []string) {
	srpms = make([]string, len(g.conflictingSRPMs))
	i := 0
	for f := range g.conflictingSRPMs {
		srpms[i] = f
		i++
	}
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
func (g *GraphBuildState) RecordBuildResult(res *BuildResult) {

	logger.Log.Debugf("Recording build result: %s", res.Node.FriendlyName())

	delete(g.activeBuilds, res.Node.ID())

	if res.Err != nil {
		g.failures = append(g.failures, res)
	}

	state := &nodeState{
		available: res.Err == nil,
		cached:    res.UsedCache,
	}

	for _, node := range res.AncillaryNodes {
		g.nodeToState[node] = state
	}

	if !res.Skipped && !res.UsedCache {
		for _, file := range res.BuiltFiles {
			if g.isConflictWithToolchain(file) {
				g.conflictingRPMs[filepath.Base(file)] = true
				g.conflictingSRPMs[filepath.Base(res.Node.SrpmPath)] = true
			}
		}
	} else {
		logger.Log.Debugf("skipping checking conflicts since this is not a built node (%v)", res.Node)
	}

	return
}
