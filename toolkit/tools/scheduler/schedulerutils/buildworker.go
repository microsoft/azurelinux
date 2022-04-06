// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"fmt"
	"path/filepath"
	"sync"
	"time"

	"gonum.org/v1/gonum/graph"
	"gonum.org/v1/gonum/graph/traverse"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkggraph"
	"microsoft.com/pkggen/internal/retry"
	"microsoft.com/pkggen/internal/sliceutils"
	"microsoft.com/pkggen/scheduler/buildagents"
)

// BuildChannels represents the communicate channels used by a build agent.
type BuildChannels struct {
	Requests         <-chan *BuildRequest
	PriorityRequests <-chan *BuildRequest
	Results          chan<- *BuildResult
	Cancel           <-chan struct{}
	Done             <-chan struct{}
}

// BuildRequest represents the results of a build agent trying to build a given node.
type BuildRequest struct {
	Node           *pkggraph.PkgNode
	PkgGraph       *pkggraph.PkgGraph
	AncillaryNodes []*pkggraph.PkgNode
	CanUseCache    bool
}

// BuildResult represents the results of a build agent trying to build a given node.
type BuildResult struct {
	AncillaryNodes []*pkggraph.PkgNode
	BuiltFiles     []string
	Err            error
	LogFile        string
	Node           *pkggraph.PkgNode
	Skipped        bool
	UsedCache      bool
}

//selectNextBuildRequest selects a job based on priority:
//  1) Bail out if the jobs are cancelled
//	2) There is something in the priority queue
//	3) Any job in either normal OR priority queue
//		OR are the jobs done/cancelled
func selectNextBuildRequest(channels *BuildChannels) (req *BuildRequest, finish bool) {
	select {
	case <-channels.Cancel:
		logger.Log.Warn("Cancellation signal received")
		return nil, true
	default:
		select {
		case req = <-channels.PriorityRequests:
			logger.Log.Tracef("PRIORITY REQUEST: %v", *req)
			return req, false
		default:
			select {
			case req = <-channels.PriorityRequests:
				logger.Log.Tracef("PRIORITY REQUEST: %v", *req)
				return req, false
			case req = <-channels.Requests:
				logger.Log.Tracef("normal REQUEST: %v", *req)
				return req, false
			case <-channels.Cancel:
				logger.Log.Warn("Cancellation signal received")
				return nil, true
			case <-channels.Done:
				logger.Log.Debug("Worker finished signal received")
				return nil, true
			}
		}
	}
}

// BuildNodeWorker process all build requests, can be run concurrently with multiple instances.
func BuildNodeWorker(channels *BuildChannels, agent buildagents.BuildAgent, graphMutex *sync.RWMutex, buildAttempts int, ignoredPackages []string) {
	for req, cancelled := selectNextBuildRequest(channels); !cancelled && req != nil; req, cancelled = selectNextBuildRequest(channels) {

		res := &BuildResult{
			Node:           req.Node,
			AncillaryNodes: req.AncillaryNodes,
		}

		switch req.Node.Type {
		case pkggraph.TypeBuild:
			res.UsedCache, res.Skipped, res.BuiltFiles, res.LogFile, res.Err = buildBuildNode(req.Node, req.PkgGraph, graphMutex, agent, req.CanUseCache, buildAttempts, ignoredPackages)
			if res.Err == nil {
				setAncillaryBuildNodesStatus(req, pkggraph.StateUpToDate)
			} else {
				setAncillaryBuildNodesStatus(req, pkggraph.StateBuildError)
			}

		case pkggraph.TypeRun, pkggraph.TypeGoal, pkggraph.TypeRemote, pkggraph.TypePureMeta, pkggraph.TypePreBuilt:
			res.UsedCache = req.CanUseCache

		case pkggraph.TypeUnknown:
			fallthrough

		default:
			res.Err = fmt.Errorf("invalid node type %v on node %v", req.Node.Type, req.Node)
		}

		channels.Results <- res
	}

	logger.Log.Debug("Worker done")
}

// buildBuildNode builds a TypeBuild node, either used a cached copy if possible or building the corresponding SRPM.
func buildBuildNode(node *pkggraph.PkgNode, pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex, agent buildagents.BuildAgent, canUseCache bool, buildAttempts int, ignoredPackages []string) (usedCache, skipped bool, builtFiles []string, logFile string, err error) {
	baseSrpmName := node.SRPMFileName()
	usedCache, builtFiles = pkggraph.IsSRPMPrebuilt(node.SrpmPath, pkgGraph, graphMutex)
	skipped = sliceutils.Contains(ignoredPackages, node.SpecName(), sliceutils.StringMatch)

	if skipped {
		logger.Log.Debugf("%s explicitly marked to be skipped.", baseSrpmName)
		return
	}

	if canUseCache && usedCache {
		logger.Log.Debugf("%s is prebuilt, skipping", baseSrpmName)
		return
	}

	usedCache = false

	dependencies := getBuildDependencies(node, pkgGraph, graphMutex)

	logger.Log.Infof("Building %s", baseSrpmName)
	builtFiles, logFile, err = buildSRPMFile(agent, buildAttempts, node.SrpmPath, dependencies)
	return
}

// getBuildDependencies returns a list of all dependencies that need to be installed before the node can be built.
func getBuildDependencies(node *pkggraph.PkgNode, pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex) (dependencies []string) {
	graphMutex.RLock()
	defer graphMutex.RUnlock()

	// Use a map to avoid duplicate entries
	dependencyLookup := make(map[string]bool)

	search := traverse.BreadthFirst{}

	// Skip traversing any build nodes to avoid other package's buildrequires.
	search.Traverse = func(e graph.Edge) bool {
		toNode := e.To().(*pkggraph.PkgNode)
		return toNode.Type != pkggraph.TypeBuild
	}

	search.Walk(pkgGraph, node, func(n graph.Node, d int) (stopSearch bool) {
		dependencyNode := n.(*pkggraph.PkgNode)

		rpmPath := dependencyNode.RpmPath
		if rpmPath == "" || rpmPath == "<NO_RPM_PATH>" || rpmPath == node.RpmPath {
			return
		}

		dependencyLookup[rpmPath] = true

		return
	})

	dependencies = make([]string, 0, len(dependencyLookup))
	for depName := range dependencyLookup {
		dependencies = append(dependencies, depName)
	}

	return
}

// buildSRPMFile sends an SRPM to a build agent to build.
func buildSRPMFile(agent buildagents.BuildAgent, buildAttempts int, srpmFile string, dependencies []string) (builtFiles []string, logFile string, err error) {
	const (
		retryDuration = time.Second
	)

	logBaseName := filepath.Base(srpmFile) + ".log"
	err = retry.Run(func() (buildErr error) {
		builtFiles, logFile, buildErr = agent.BuildPackage(srpmFile, logBaseName, dependencies)
		return
	}, buildAttempts, retryDuration)

	return
}

// setAncillaryBuildNodesStatus sets the NodeState for all of the request's ancillary nodes.
func setAncillaryBuildNodesStatus(req *BuildRequest, nodeState pkggraph.NodeState) {
	for _, node := range req.AncillaryNodes {
		if node.Type == pkggraph.TypeBuild {
			node.State = nodeState
		}
	}
}
