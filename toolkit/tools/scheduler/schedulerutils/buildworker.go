// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/retry"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/rpm"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/sliceutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/scheduler/buildagents"
	"gonum.org/v1/gonum/graph"
	"gonum.org/v1/gonum/graph/traverse"
)

// BuildChannels represents the communicate channels used by a build agent.
type BuildChannels struct {
	Requests         <-chan *BuildRequest
	PriorityRequests <-chan *BuildRequest
	Results          chan<- *BuildResult
	Cancel           <-chan struct{}
	Done             <-chan struct{}
}

// BuildRequest represents a work-order to a build agent asking it to build a given node.
type BuildRequest struct {
	Node           *pkggraph.PkgNode   // The main node being analyzed for the build.
	PkgGraph       *pkggraph.PkgGraph  // The graph of all packages.
	AncillaryNodes []*pkggraph.PkgNode // For SRPM builds: other nodes stemming from the same SRPM. Empty otherwise.
	ExpectedFiles  []string            // List of RPMs built by this node.
	UseCache       bool                // Can we use a cached copy of this package instead of building it.
	IsDelta        bool                // Is this a pre-downloaded RPM (not traditional cache) that we may be able to skip rebuilding.
	Freshness      uint                // The freshness of the node (used to determine if we can skip building future nodes).
}

// BuildResult represents the results of a build agent trying to build a given node.
type BuildResult struct {
	AncillaryNodes []*pkggraph.PkgNode // For SRPM builds: other nodes stemming from the same SRPM. Empty otherwise.
	BuiltFiles     []string            // List of RPMs built by this node.
	Err            error               // Error encountered during the build.
	LogFile        string              // Path to the log file from the build.
	Node           *pkggraph.PkgNode   // The main node being analyzed for the build.
	Ignored        bool                // Indicator if the build was ignored by user request.
	UsedCache      bool                // Indicator if we used the cached artifacts (external or earlier local build) instead of building the node.
	WasDelta       bool                // Indicator if we used a pre-built component from an external repository instead of building the node.
	Freshness      uint                // The freshness of the node (used to determine if we can skip building future nodes).
}

// selectNextBuildRequest selects a job based on priority:
//  1. Bail out if the jobs are cancelled
//  2. There is something in the priority queue
//  3. Any job in either normal OR priority queue
//     OR are the jobs done/cancelled
func selectNextBuildRequest(channels *BuildChannels) (req *BuildRequest, finish bool) {
	select {
	case <-channels.Cancel:
		logger.Log.Warn("Cancellation signal received")
		return nil, true
	default:
		select {
		case req = <-channels.PriorityRequests:
			if req != nil {
				logger.Log.Tracef("PRIORITY REQUEST: %v", *req)
			}
			return req, false
		default:
			select {
			case req = <-channels.PriorityRequests:
				if req != nil {
					logger.Log.Tracef("PRIORITY REQUEST: %v", *req)
				}
				return req, false
			case req = <-channels.Requests:
				if req != nil {
					logger.Log.Tracef("normal REQUEST: %v", *req)
				}
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
func BuildNodeWorker(channels *BuildChannels, agent buildagents.BuildAgent, graphMutex *sync.RWMutex, buildAttempts int, checkAttempts int, ignoredPackages, ignoredTests []*pkgjson.PackageVer) {
	// Track the time a worker spends waiting on a task. We will add a timing node each time we finish processing a request, and stop
	// it when we pick up the next request
	for req, cancelled := selectNextBuildRequest(channels); !cancelled && req != nil; req, cancelled = selectNextBuildRequest(channels) {
		res := &BuildResult{
			Node:           req.Node,
			AncillaryNodes: req.AncillaryNodes,
			UsedCache:      req.UseCache,
			WasDelta:       req.IsDelta,
			Freshness:      req.Freshness,
		}

		switch req.Node.Type {
		case pkggraph.TypeLocalBuild:
			res.Ignored, res.BuiltFiles, res.LogFile, res.Err = buildNode(req, graphMutex, agent, buildAttempts, ignoredPackages)
			if res.Err == nil {
				setAncillaryBuildNodesStatus(req, graphMutex, pkggraph.StateUpToDate)
			} else {
				setAncillaryBuildNodesStatus(req, graphMutex, pkggraph.StateBuildError)
			}

		case pkggraph.TypeTest:
			res.Ignored, res.LogFile, res.Err = testNode(req, graphMutex, agent, checkAttempts, ignoredTests)
			if res.Err == nil {
				setAncillaryBuildNodesStatus(req, graphMutex, pkggraph.StateUpToDate)
			} else {
				setAncillaryBuildNodesStatus(req, graphMutex, pkggraph.StateBuildError)
			}

		case pkggraph.TypeLocalRun, pkggraph.TypeGoal, pkggraph.TypeRemoteRun, pkggraph.TypePureMeta, pkggraph.TypePreBuilt:
			res.UsedCache = req.UseCache

		case pkggraph.TypeUnknown:
			fallthrough

		default:
			res.Err = fmt.Errorf("invalid node type %v on node %v", req.Node.Type, req.Node)
		}

		channels.Results <- res
		// Track the time a worker spends waiting on a task
	}
	logger.Log.Debug("Worker done")
}

// buildNode builds a TypeLocalBuild node, either used a cached copy if possible or building the corresponding SRPM.
func buildNode(request *BuildRequest, graphMutex *sync.RWMutex, agent buildagents.BuildAgent, buildAttempts int, ignoredPackages []*pkgjson.PackageVer) (ignored bool, builtFiles []string, logFile string, err error) {
	node := request.Node
	baseSrpmName := node.SRPMFileName()

	basePackageName, err := rpm.GetBasePackageNameFromSpecFile(node.SpecPath)
	if err != nil {
		// This can only happen if the spec file does not have a name (only an extension).
		logger.Log.Warnf("An error occured while getting the base package name from (%s). This may result in further errors.", node.SpecPath)
	}

	ignored = sliceutils.Contains(ignoredPackages, node.VersionedPkg, sliceutils.PackageVerMatch)

	if ignored {
		logger.Log.Debugf("%s explicitly marked to be ignored.", baseSrpmName)
		return
	}

	if request.UseCache {
		logger.Log.Debugf("%s is prebuilt, skipping", baseSrpmName)
		builtFiles = request.ExpectedFiles
		return
	}

	dependencies := getBuildDependencies(node, request.PkgGraph, graphMutex)

	logger.Log.Infof("Building: %s", baseSrpmName)
	builtFiles, logFile, err = buildSRPMFile(agent, buildAttempts, basePackageName, node.SrpmPath, node.Architecture, dependencies)
	return
}

// testNode tests a TypeTest node.
func testNode(request *BuildRequest, graphMutex *sync.RWMutex, agent buildagents.BuildAgent, checkAttempts int, ignoredTests []*pkgjson.PackageVer) (ignored bool, logFile string, err error) {
	node := request.Node
	baseSrpmName := node.SRPMFileName()

	basePackageName, err := rpm.GetBasePackageNameFromSpecFile(node.SpecPath)
	if err != nil {
		// This can only happen if the spec file does not have a name (only an extension).
		logger.Log.Warnf("An error occured while getting the base package name from (%s). This may result in further errors.", node.SpecPath)
	}

	ignored = sliceutils.Contains(ignoredTests, node.VersionedPkg, sliceutils.PackageVerMatch)

	if ignored {
		logger.Log.Debugf("%s (test) explicitly marked to be ignored.", baseSrpmName)
		return
	}

	if request.UseCache {
		logger.Log.Debugf("Using cache for '%s', skipping its test run as well.", baseSrpmName)
		return
	}

	dependencies := getBuildDependencies(node, request.PkgGraph, graphMutex)

	logger.Log.Infof("Testing: %s", baseSrpmName)
	logFile, err = testSRPMFile(agent, checkAttempts, basePackageName, node.SrpmPath, node.Architecture, dependencies)
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
		return toNode.Type != pkggraph.TypeLocalBuild
	}

	search.Walk(pkgGraph, node, func(n graph.Node, d int) (stopSearch bool) {
		dependencyNode := n.(*pkggraph.PkgNode)

		rpmPath := dependencyNode.RpmPath
		if rpmPath == "" || rpmPath == pkggraph.NoRPMPath || rpmPath == node.RpmPath {
			return
		}

		dependencyLookup[rpmPath] = true

		return
	})

	dependencies = sliceutils.SetToSlice(dependencyLookup)

	return
}

// parseCheckSection reads the package build log file to determine if the %check section passed or not
func parseCheckSection(logFile string) (err error) {
	logFileObject, err := os.Open(logFile)
	// If we can't open the log file, that's a build error.
	if err != nil {
		logger.Log.Errorf("Failed to open log file '%s' while checking package test results. Error: %v", logFile, err)
		return
	}
	defer logFileObject.Close()
	for scanner := bufio.NewScanner(logFileObject); scanner.Scan(); {
		currLine := scanner.Text()
		// Anything besides 0 is a failed test
		if strings.Contains(currLine, "CHECK DONE") {
			if strings.Contains(currLine, "EXIT STATUS 0") {
				return
			}
			failedLogFile := strings.TrimSuffix(logFile, ".test.log")
			failedLogFile = fmt.Sprintf("%s-FAILED_TEST-%d.log", failedLogFile, time.Now().UnixMilli())
			err = file.Copy(logFile, failedLogFile)
			if err != nil {
				logger.Log.Errorf("Log file copy failed. Error: %v", err)
				return
			}
			err = fmt.Errorf("package test failed. Test status line: %s", currLine)
			return
		}
	}
	return
}

// buildSRPMFile sends an SRPM to a build agent to build.
func buildSRPMFile(agent buildagents.BuildAgent, buildAttempts int, basePackageName, srpmFile, outArch string, dependencies []string) (builtFiles []string, logFile string, err error) {
	const (
		retryDuration = time.Second
		runCheck      = false
	)

	logBaseName := filepath.Base(srpmFile) + ".log"
	err = retry.Run(func() (buildErr error) {
		builtFiles, logFile, buildErr = agent.BuildPackage(basePackageName, srpmFile, logBaseName, outArch, runCheck, dependencies)
		return
	}, buildAttempts, retryDuration)

	return
}

// testSRPMFile sends an SRPM to a build agent to test.
func testSRPMFile(agent buildagents.BuildAgent, checkAttempts int, basePackageName string, srpmFile string, outArch string, dependencies []string) (logFile string, err error) {
	const (
		retryDuration = time.Second
		runCheck      = true
	)

	// checkFailed is a flag to see if a non-null buildErr is from the %check section
	checkFailed := false
	logBaseName := filepath.Base(srpmFile) + ".test.log"
	err = retry.Run(func() (buildErr error) {
		checkFailed = false

		_, logFile, buildErr = agent.BuildPackage(basePackageName, srpmFile, logBaseName, outArch, runCheck, dependencies)
		if buildErr != nil {
			logger.Log.Warnf("Test build for '%s' failed on a non-test build issue. Error: %s, for details see: %s", srpmFile, buildErr, logFile)
			return
		}

		buildErr = parseCheckSection(logFile)
		checkFailed = (buildErr != nil)
		return
	}, checkAttempts, retryDuration)

	if err != nil && checkFailed {
		logger.Log.Warnf("Tests failed for '%s'. Error: %s, for details see: %s", srpmFile, err, logFile)
		err = nil
	}
	return
}

// setAncillaryBuildNodesStatus sets the NodeState for all of the request's ancillary build and test nodes.
func setAncillaryBuildNodesStatus(req *BuildRequest, graphMutex *sync.RWMutex, nodeState pkggraph.NodeState) {
	graphMutex.Lock()
	defer graphMutex.Unlock()

	for _, node := range req.AncillaryNodes {
		if node.Type == pkggraph.TypeLocalBuild || node.Type == pkggraph.TypeTest {
			node.State = nodeState
		}
	}
}
