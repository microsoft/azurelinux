// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
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
	activeBuilds map[int64]*BuildRequest
	nodeToState  map[*pkggraph.PkgNode]*nodeState
	failures     []*BuildResult
}

// NewGraphBuildState returns a new GraphBuildState.
func NewGraphBuildState() *GraphBuildState {
	return &GraphBuildState{
		activeBuilds: make(map[int64]*BuildRequest),
		nodeToState:  make(map[*pkggraph.PkgNode]*nodeState),
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

// BuildFailures returns a slice of all failed builds.
func (g *GraphBuildState) BuildFailures() []*BuildResult {
	return g.failures
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

// RecordBuildResult recprds a build result in the graph build state.
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

	return
}
