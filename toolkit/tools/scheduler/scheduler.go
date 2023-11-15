// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"
	"os"
	"os/signal"
	"path/filepath"
	"runtime"
	"sync"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/ccachemanager"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/profile"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/scheduler/buildagents"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/scheduler/schedulerutils"

	"golang.org/x/sys/unix"
	"gopkg.in/alecthomas/kingpin.v2"
)

const (
	// default worker count to 0 to automatically scale with the number of logical CPUs.
	defaultWorkerCount   = "0"
	defaultBuildAttempts = "1"
	defaultCheckAttempts = "1"
	defaultExtraLayers   = "0"
)

var (
	defaultFreshness = fmt.Sprintf("%d", schedulerutils.NodeFreshnessAbsoluteMax)
	defaultTimeout   = "99h"
)

// schedulerChannels represents the communication channels used by a build agent.
// Unlike BuildChannels, schedulerChannels holds bidirectional channels that
// only the top-level scheduler should have. BuildChannels contains directional channels.
type schedulerChannels struct {
	Requests         chan *schedulerutils.BuildRequest
	PriorityRequests chan *schedulerutils.BuildRequest
	Results          chan *schedulerutils.BuildResult
	Cancel           chan struct{}
	Done             chan struct{}
}

var (
	app = kingpin.New("scheduler", "A tool to schedule package builds from a dependency graph.")

	inputGraphFile  = exe.InputFlag(app, "Path to the DOT graph file to build.")
	outputGraphFile = exe.OutputFlag(app, "Path to save the built DOT graph file.")

	outputCSVFile    = app.Flag("output-build-state-csv-file", "Path to save the CSV file.").Required().String()
	workDir          = app.Flag("work-dir", "The directory to create the build folder").Required().String()
	workerTar        = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz").Required().ExistingFile()
	repoFile         = app.Flag("repo-file", "Full path to local.repo").Required().ExistingFile()
	rpmDir           = app.Flag("rpm-dir", "The directory to use as the local repo and to submit RPM packages to").Required().ExistingDir()
	toolchainDirPath = app.Flag("toolchain-rpms-dir", "Directory that contains already built toolchain RPMs. Should contain top level directories for architecture.").Required().ExistingDir()
	srpmDir          = app.Flag("srpm-dir", "The output directory for source RPM packages").Required().String()
	cacheDir         = app.Flag("cache-dir", "The cache directory containing downloaded dependency RPMS from Mariner Base").Required().ExistingDir()
	buildLogsDir     = app.Flag("build-logs-dir", "Directory to store package build logs").Required().ExistingDir()

	imageConfig = app.Flag("image-config-file", "Optional image config file to extract a package list from.").String()
	baseDirPath = app.Flag("base-dir", "Base directory for relative file paths from the config. Defaults to config's directory.").ExistingDir()

	distTag                    = app.Flag("dist-tag", "The distribution tag SRPMs will be built with.").Required().String()
	distroReleaseVersion       = app.Flag("distro-release-version", "The distro release version that the SRPM will be built with.").Required().String()
	distroBuildNumber          = app.Flag("distro-build-number", "The distro build number that the SRPM will be built with.").Required().String()
	rpmmacrosFile              = app.Flag("rpmmacros-file", "Optional file path to an rpmmacros file for rpmbuild to use.").ExistingFile()
	buildAttempts              = app.Flag("build-attempts", "Sets the number of times to try building a package.").Default(defaultBuildAttempts).Int()
	checkAttempts              = app.Flag("check-attempts", "Sets the minimum number of times to test a package if the tests fail.").Default(defaultCheckAttempts).Int()
	extraLayers                = app.Flag("extra-layers", "Sets the number of additional layers in the graph beyond the goal packages to buid.").Default(defaultExtraLayers).Int()
	maxCascadingRebuilds       = app.Flag("max-cascading-rebuilds", "Sets the maximum number of cascading dependency rebuilds caused by package being rebuilt (leave unset for unbounded).").Default(defaultFreshness).Uint()
	noCleanup                  = app.Flag("no-cleanup", "Whether or not to delete the chroot folder after the build is done").Bool()
	noCache                    = app.Flag("no-cache", "Disables using prebuilt cached packages.").Bool()
	stopOnFailure              = app.Flag("stop-on-failure", "Stop on failed build").Bool()
	toolchainManifest          = app.Flag("toolchain-manifest", "Path to a list of RPMs which are created by the toolchain. RPMs from this list will are considered 'prebuilt' and will not be rebuilt").ExistingFile()
	optimizeWithCachedImplicit = app.Flag("optimize-with-cached-implicit", "Optimize the build process by allowing cached implicit packages to be used to optimize the initial build graph instead of waiting for a real package build to provide the nodes.").Bool()
	useCcache                  = app.Flag("use-ccache", "Automatically install and use ccache during package builds").Bool()
	ccacheDir                  = app.Flag("ccache-dir", "The directory used to store ccache outputs").String()
	ccacheConfig               = app.Flag("ccache-config", "The ccache configuration file path.").String()
	allowToolchainRebuilds     = app.Flag("allow-toolchain-rebuilds", "Allow toolchain packages to rebuild without causing an error.").Bool()
	maxCPU                     = app.Flag("max-cpu", "Max number of CPUs used for package building").Default("").String()
	timeout                    = app.Flag("timeout", "Max duration for any individual package build/test").Default(defaultTimeout).Duration()

	validBuildAgentFlags = []string{buildagents.TestAgentFlag, buildagents.ChrootAgentFlag}
	buildAgent           = app.Flag("build-agent", "Type of build agent to build packages with.").PlaceHolder(exe.PlaceHolderize(validBuildAgentFlags)).Required().Enum(validBuildAgentFlags...)
	buildAgentProgram    = app.Flag("build-agent-program", "Path to the build agent that will be invoked to build packages.").String()
	workers              = app.Flag("workers", "Number of concurrent build agents to spawn. If set to 0, will automatically set to the logical CPU count.").Default(defaultWorkerCount).Int()

	pkgsToIgnore = app.Flag("ignored-packages", "Space separated list of specs ignoring rebuilds if their dependencies have been updated. Will still build if all of the spec's RPMs have not been built.").String()

	pkgsToBuild   = app.Flag("packages", "Space separated list of top-level packages that should be built. Omit this argument to build all packages.").String()
	pkgsToRebuild = app.Flag("rebuild-packages", "Space separated list of base package names packages that should be rebuilt.").String()

	testsToIgnore = app.Flag("ignored-tests", "Space separated list of package tests that should not be ran.").String()
	testsToRun    = app.Flag("tests", "Space separated list of tests that should be ran. Omit this argument to run package tests.").String()
	testsToRerun  = app.Flag("rerun-tests", "Space separated list of package tests that should be re-ran.").String()

	logFile       = exe.LogFileFlag(app)
	logLevel      = exe.LogLevelFlag(app)
	logColor      = exe.LogColorFlag(app)
	profFlags     = exe.SetupProfileFlags(app)
	timestampFile = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel, *logColor)

	prof, err := profile.StartProfiling(profFlags)
	if err != nil {
		logger.Log.Warnf("Could not start profiling: %s", err)
	}
	defer prof.StopProfiler()

	if *workers <= 0 {
		*workers = runtime.NumCPU()
		logger.Log.Debugf("No worker count supplied, discovered %d logical CPUs.", *workers)
	}

	if *buildAttempts <= 0 {
		logger.Log.Fatalf("Value in --build-attempts must be greater than zero. Found %d.", *buildAttempts)
	}

	dependencyGraph, err := pkggraph.ReadDOTGraphFile(*inputGraphFile)
	if err != nil {
		logger.Log.Fatalf("Failed to read DOT graph with error:\n%s", err)
	}

	finalPackagesToBuild, packagesToRebuild, packagesToIgnore, err := schedulerutils.ParseAndGeneratePackageBuildList(dependencyGraph, exe.ParseListArgument(*pkgsToBuild), exe.ParseListArgument(*pkgsToRebuild), exe.ParseListArgument(*pkgsToIgnore), *imageConfig, *baseDirPath)
	if err != nil {
		logger.Log.Fatalf("Failed to generate package list with error:\n%s", err)
	}

	finalTestsToRun, testsToRerun, ignoredTests, err := schedulerutils.ParseAndGeneratePackageTestList(dependencyGraph, exe.ParseListArgument(*testsToRun), exe.ParseListArgument(*testsToRerun), exe.ParseListArgument(*testsToIgnore), *imageConfig, *baseDirPath)
	if err != nil {
		logger.Log.Fatalf("Failed to generate tests list with error:\n%s", err)
	}

	toolchainPackages, err := schedulerutils.ReadReservedFilesList(*toolchainManifest)
	if err != nil {
		logger.Log.Fatalf("unable to read toolchain manifest file '%s': %s.", *toolchainManifest, err)
	}

	// Setup a build agent to handle build requests from the scheduler.
	buildAgentConfig := &buildagents.BuildAgentConfig{
		Program:      *buildAgentProgram,
		CacheDir:     *cacheDir,
		RepoFile:     *repoFile,
		RpmDir:       *rpmDir,
		ToolchainDir: *toolchainDirPath,
		SrpmDir:      *srpmDir,
		WorkDir:      *workDir,
		WorkerTar:    *workerTar,

		DistTag:              *distTag,
		DistroReleaseVersion: *distroReleaseVersion,
		DistroBuildNumber:    *distroBuildNumber,
		RpmmacrosFile:        *rpmmacrosFile,

		NoCleanup:    *noCleanup,
		UseCcache:    *useCcache,
		CCacheDir:    *ccacheDir,
		CCacheConfig: *ccacheConfig,
		MaxCpu:       *maxCPU,
		Timeout:      *timeout,

		LogDir:   *buildLogsDir,
		LogLevel: *logLevel,
	}

	agent, err := buildagents.BuildAgentFactory(*buildAgent)
	if err != nil {
		logger.Log.Fatalf("Unable to select build agent, error: %s.", err)
	}

	err = agent.Initialize(buildAgentConfig)
	if err != nil {
		logger.Log.Fatalf("Unable to initialize build agent, error: %s.", err)
	}

	// Setup cleanup routines to ensure no builds are left running when scheduler is exiting.
	// Ensure no outstanding agents are running on graceful exit
	defer cancelOutstandingBuilds(agent)
	// On a SIGINT or SIGTERM stop all agents.
	signals := make(chan os.Signal, 1)
	signal.Notify(signals, unix.SIGINT, unix.SIGTERM)
	go cancelBuildsOnSignal(signals, agent)

	err = buildGraph(*inputGraphFile, *outputGraphFile, agent, *workers, *buildAttempts, *checkAttempts, *extraLayers, *maxCascadingRebuilds, *stopOnFailure, !*noCache, finalPackagesToBuild, packagesToRebuild, packagesToIgnore, finalTestsToRun, testsToRerun, ignoredTests, toolchainPackages, *optimizeWithCachedImplicit, *allowToolchainRebuilds)
	if err != nil {
		logger.Log.Fatalf("Unable to build package graph.\nFor details see the build summary section above.\nError: %s.", err)
	}

	if *useCcache {
		logger.Log.Infof("  ccache is enabled. processing multi-package groups under (%s)...", *ccacheDir)
		ccacheManager, ccacheErr := ccachemanager.CreateManager(*ccacheDir, *ccacheConfig)
		if ccacheErr == nil {
			ccacheErr = ccacheManager.UploadMultiPkgGroupCCaches()
			if ccacheErr != nil {
				logger.Log.Warnf("Failed to archive CCache artifacts:\n%v.", err)
			}
		} else {
			logger.Log.Warnf("Failed to initialize the ccache manager:\n%v", err)
		}
	}
}

// cancelOutstandingBuilds stops any builds that are currently running.
func cancelOutstandingBuilds(agent buildagents.BuildAgent) {
	err := agent.Close()
	if err != nil {
		logger.Log.Errorf("Unable to close build agent, error: %s", err)
	}

	// Issue a SIGINT to all children processes to allow them to gracefully exit.
	shell.PermanentlyStopAllChildProcesses(unix.SIGINT)
}

// cancelBuildsOnSignal will stop any builds running on SIGINT/SIGTERM.
func cancelBuildsOnSignal(signals chan os.Signal, agent buildagents.BuildAgent) {
	sig := <-signals
	logger.Log.Error(sig)

	cancelOutstandingBuilds(agent)
	os.Exit(1)
}

// buildGraph builds all packages in the dependency graph requested.
// It will save the resulting graph to outputFile.
func buildGraph(inputFile, outputFile string, agent buildagents.BuildAgent, workers, buildAttempts, checkAttempts, extraLayers int, maxCascadingRebuilds uint, stopOnFailure, canUseCache bool, packagesToBuild, packagesToRebuild, ignoredPackages, testsToRun, testsToRerun, ignoredTests []*pkgjson.PackageVer, toolchainPackages []string, optimizeWithCachedImplicit bool, allowToolchainRebuilds bool) (err error) {
	// graphMutex guards pkgGraph from concurrent reads and writes during build.
	var graphMutex sync.RWMutex

	// If optimizeWithCachedImplicit is true, we can use the cached implicit dependencies to aggressively prune the graph during the first pass. We will still
	// try to avoid using the cached implicit dependencies until we have no other choice during the build, but since the graph is pruned, we will
	// avoid building packages that are not needed. Obviously we can only do this if the cache is enabled.
	allowEarlyImplicitOptimization := (canUseCache && optimizeWithCachedImplicit)
	_, pkgGraph, goalNode, err := schedulerutils.InitializeGraphFromFile(inputFile, packagesToBuild, testsToRun, allowEarlyImplicitOptimization, extraLayers)
	if err != nil {
		return
	}

	// Setup and start the worker pool and scheduler routine.
	numberOfNodes := pkgGraph.Nodes().Len()

	channels := startWorkerPool(agent, workers, buildAttempts, checkAttempts, numberOfNodes, &graphMutex, ignoredPackages, ignoredTests)
	logger.Log.Infof("Building %d nodes with %d workers", numberOfNodes, workers)

	// After this call pkgGraph will be given to multiple routines and accessing it requires acquiring the mutex.
	builtGraph, err := buildAllNodes(stopOnFailure, canUseCache, packagesToRebuild, testsToRerun, pkgGraph, &graphMutex, goalNode, channels, maxCascadingRebuilds, toolchainPackages, allowToolchainRebuilds)

	if builtGraph != nil {
		graphMutex.RLock()
		defer graphMutex.RUnlock()

		saveErr := pkggraph.WriteDOTGraphFile(builtGraph, outputFile)
		if saveErr != nil {
			logger.Log.Errorf("Failed to save built graph, error: %s", saveErr)
		}
	}

	return
}

// startWorkerPool starts the worker pool and returns the communication channels between the workers and the scheduler.
// channelBufferSize controls how many entries in the channels can be buffered before blocking writes to them.
func startWorkerPool(agent buildagents.BuildAgent, workers, buildAttempts, checkAttempts, channelBufferSize int, graphMutex *sync.RWMutex, ignoredPackages, ignoredTests []*pkgjson.PackageVer) (channels *schedulerChannels) {
	channels = &schedulerChannels{
		Requests:         make(chan *schedulerutils.BuildRequest, channelBufferSize),
		PriorityRequests: make(chan *schedulerutils.BuildRequest, channelBufferSize),
		Results:          make(chan *schedulerutils.BuildResult, channelBufferSize),
		Cancel:           make(chan struct{}),
		Done:             make(chan struct{}),
	}

	// Downcast the bidirectional scheduler channels into directional channels for the build workers.
	directionalChannels := &schedulerutils.BuildChannels{
		Requests:         channels.Requests,
		PriorityRequests: channels.PriorityRequests,
		Results:          channels.Results,
		Cancel:           channels.Cancel,
		Done:             channels.Done,
	}

	// Start the workers now so they begin working as soon as a new job is queued.
	for i := 0; i < workers; i++ {
		logger.Log.Debugf("Starting worker #%d", i)
		go schedulerutils.BuildNodeWorker(directionalChannels, agent, graphMutex, buildAttempts, checkAttempts, ignoredPackages, ignoredTests)
	}

	return
}

// buildAllNodes will build all nodes in a given dependency graph.
// This routine only contains control flow logic for build scheduling.
// It iteratively:
// - Calculates any unblocked nodes.
// - Submits these nodes to the worker pool to be processed.
// - Grabs a single build result from the worker pool.
// - Attempts to satisfy any unresolved dynamic dependencies with new implicit provides from the build result.
// - Attempts to subgraph the graph to only contain the requested packages if possible.
// - Repeat.
func buildAllNodes(stopOnFailure, canUseCache bool, packagesToRebuild, testsToRerun []*pkgjson.PackageVer, pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex, goalNode *pkggraph.PkgNode, channels *schedulerChannels, maxCascadingRebuilds uint, reservedFiles []string, allowToolchainRebuilds bool) (builtGraph *pkggraph.PkgGraph, err error) {
	var (
		// stopBuilding tracks if the build has entered a failed state and this routine should stop as soon as possible.
		stopBuilding bool
		// useCachedImplicit tracks if cached implicit provides can be used to satisfy unresolved dynamic dependencies.
		// Local packages are preferred over cached remotes ones to satisfy these unresolved dependencies, however
		// the scheduler does not know what packages provide which implicit provides until the packages have been built.
		// Therefore the scheduler will attempt to build all possible packages without consuming any cached dynamic dependencies first.

		// Even when --optimize-with-cached-implicit is passed to the tool we will want to wait until all local packages have
		// been built before using cached implicit provides. This is because the local packages may provide updated versions
		// of the cached implicit provides. --optimize-with-cached-implicit is instead used to aggressively optimize the graph
		// by using cached implicit provides to satisfy unresolved dynamic dependencies during the first pass of the optimizer.
		useCachedImplicit bool
		isGraphOptimized  bool
	)

	// Start the build at the leaf nodes.
	// The build will bubble up through the graph as it processes nodes.
	buildState := schedulerutils.NewGraphBuildState(reservedFiles, maxCascadingRebuilds)
	buildRunsTests := len(pkgGraph.AllTestNodes()) > 0
	nodesToBuild := schedulerutils.LeafNodes(pkgGraph, graphMutex, goalNode, buildState, useCachedImplicit)

	for {
		logger.Log.Debugf("Found %d unblocked nodes: %v.", len(nodesToBuild), nodesToBuild)

		// Each node that is ready to build must be converted into a build request and submitted to the worker pool.
		newRequests := schedulerutils.ConvertNodesToRequests(pkgGraph, graphMutex, nodesToBuild, packagesToRebuild, testsToRerun, buildState, canUseCache)
		for _, req := range newRequests {
			buildState.RecordBuildRequest(req)
			// Decide which priority the build should be. Generally we want to get any remote or prebuilt nodes out of the
			// way as quickly as possible since they may help us optimize the graph early.
			// Meta nodes may also be blocking something we want to examine and give higher priority (priority inheritance from
			// the hypothetical high priority node hidden further into the tree)
			switch req.Node.Type {
			case pkggraph.TypePreBuilt:
				channels.PriorityRequests <- req

				// For now all build nodes are of equal priority
			case pkggraph.TypeGoal:
				fallthrough
			case pkggraph.TypePureMeta:
				fallthrough
			case pkggraph.TypeLocalRun:
				fallthrough
			case pkggraph.TypeRemoteRun:
				fallthrough
			case pkggraph.TypeLocalBuild:
				fallthrough
			default:
				channels.Requests <- req
			}
		}
		nodesToBuild = nil

		// If there are no active builds running or results waiting to check try enabling cached packages for unresolved
		// dynamic dependencies to unblock more nodes. Otherwise, there is nothing left that can be built.
		if len(buildState.ActiveBuilds()) == 0 && len(channels.Results) == 0 {
			if useCachedImplicit {
				err = fmt.Errorf("could not build all packages")
				break
			} else {
				logger.Log.Warn("Enabling cached packages to satisfy unresolved dynamic dependencies.")
				useCachedImplicit = true
				nodesToBuild = schedulerutils.LeafNodes(pkgGraph, graphMutex, goalNode, buildState, useCachedImplicit)
				continue
			}
		}

		// Process the the next build result
		res := <-channels.Results

		schedulerutils.PrintBuildResult(res)
		err = buildState.RecordBuildResult(res, allowToolchainRebuilds)
		if err != nil {
			// Failures to manipulate the graph or build state are fatal.
			err = fmt.Errorf("error recording build result:\n%w", err)
			stopBuilding = true
		}

		if !stopBuilding {
			if res.Err == nil {
				if res.Node.Type == pkggraph.TypeLocalBuild && res.WasDelta {
					logger.Log.Tracef("This is a delta result, update the graph with the new delta files for '%v'.", res.Node)
					// We will need to update the graph with paths to any delta files that were actually rebuilt.
					err = setAssociatedDeltaPaths(res, pkgGraph, graphMutex)
					if err != nil {
						// Failures to manipulate the graph are fatal. The ancillary delta nodes may be in an invalid state
						// and we won't be able to track which RPMs were built or used delta files.
						err = fmt.Errorf("error setting delta paths for ancillary nodes:\n%w", err)
						stopBuilding = true
					}
				}

				// If the graph has already been optimized and is now solvable without any additional information
				// then skip processing any new implicit provides.
				if !stopBuilding && !isGraphOptimized {
					var (
						didOptimize bool
						newGraph    *pkggraph.PkgGraph
						newGoalNode *pkggraph.PkgNode
					)
					didOptimize, newGraph, newGoalNode, err = updateGraphWithImplicitProvides(res, pkgGraph, graphMutex, useCachedImplicit)
					if err != nil {
						// Failures to manipulate the graph are fatal.
						// There is no guarantee the graph is still a directed acyclic graph and is solvable.
						stopBuilding = true
					} else if didOptimize {
						isGraphOptimized = true
						// Replace the graph and goal node pointers.
						// Any outstanding builds of nodes that are no longer in the graph will gracefully handle this.
						// When querying their edges, the graph library will return an empty iterator (graph.Empty).
						pkgGraph = newGraph
						goalNode = newGoalNode
					}
				}

				nodesToBuild = schedulerutils.FindUnblockedNodesFromResult(res, pkgGraph, graphMutex, buildState)
			} else if stopOnFailure {
				stopBuilding = true
				err = res.Err
			}
		}

		// stopBuilding will be set to true here only if the build has failed. We also set it to true if the goal node is available
		// but only after this check is made. In that case we will call doneBuild() instead.
		if stopBuilding {
			// If the build has failed, stop all outstanding builds.
			stopBuild(channels, buildState)
			err = fmt.Errorf("fatal error building package graph:\n%w", err)
			// Save out the current graph state for debugging
			builtGraph = pkgGraph
			return
		}

		// If the goal node is available, mark the build as stopping.
		// There may still be outstanding builds if the graph was recently subgraphed
		// due to an unresolved implicit provide being satisfied and nodes that are no
		// longer in the graph are building.
		if buildState.IsNodeAvailable(goalNode) {
			logger.Log.Infof("All packages built")
			stopBuilding = true
		}

		activeSRPMs := buildState.ActiveSRPMs()
		activeSRPMsCount := len(activeSRPMs)
		if stopBuilding && activeSRPMsCount == 0 {
			break
		}

		if res.Node.Type == pkggraph.TypeLocalBuild || res.Node.Type == pkggraph.TypeTest {
			logger.Log.Infof("%d currently active build(s): %v.", activeSRPMsCount, activeSRPMs)

			if buildRunsTests {
				activeTests := buildState.ActiveTests()

				logger.Log.Infof("%d currently active test(s): %v.", len(activeTests), activeTests)
			}
		}
	}

	// Let the workers know they are done
	doneBuild(channels, buildState)
	// Give the workers time to finish so they don't mess up the summary we want to print.
	// Some nodes may still be busy with long running builds we don't care about anymore, so we don't
	// want to actually block here.
	time.Sleep(time.Second)

	builtGraph = pkgGraph
	schedulerutils.PrintBuildSummary(builtGraph, graphMutex, buildState, allowToolchainRebuilds)
	schedulerutils.RecordBuildSummary(builtGraph, graphMutex, buildState, *outputCSVFile)
	if !allowToolchainRebuilds && (len(buildState.ConflictingRPMs()) > 0 || len(buildState.ConflictingSRPMs()) > 0) {
		err = fmt.Errorf("toolchain packages rebuilt. See build summary for details. Use 'ALLOW_TOOLCHAIN_REBUILDS=y' to suppress this error if rebuilds were expected")
	}
	return
}

// updateGraphWithImplicitProvides will update the graph with new implicit provides if available.
// It will also attempt to subgraph the graph if it becomes solvable with the new implicit provides.
func updateGraphWithImplicitProvides(res *schedulerutils.BuildResult, pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex, useCachedImplicit bool) (didOptimize bool, newGraph *pkggraph.PkgGraph, newGoalNode *pkggraph.PkgNode, err error) {
	// acquire a writer lock since this routine will collapse nodes
	graphMutex.Lock()
	defer graphMutex.Unlock()

	didInjectAny, err := schedulerutils.InjectMissingImplicitProvides(res, pkgGraph, useCachedImplicit)
	if err != nil {
		logger.Log.Errorf("Failed to add implicit provides for (%s). Error: %s", res.Node.FriendlyName(), err)
	} else if didInjectAny {
		// Failure to optimize the graph is non fatal as there may simply be unresolved dynamic dependencies
		var subgraphErr error
		newGraph, newGoalNode, subgraphErr = schedulerutils.OptimizeGraph(pkgGraph, useCachedImplicit)
		if subgraphErr == nil {
			logger.Log.Infof("Created solvable subgraph with new implicit provide information")
			didOptimize = true
		}
	}

	return
}

// setAssociatedDeltaPaths sets the RpmPath for all of the request's ancillary nodes (both build and run) to the actual
// RPM paths. A delta node will normally point at the cached RPM path, but we want to point it at the actual RPM if we built it.
// This function should only be called on delta build nodes.
func setAssociatedDeltaPaths(res *schedulerutils.BuildResult, pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex) (err error) {
	graphMutex.Lock()
	defer graphMutex.Unlock()

	// Build map of basename to full path for built files. This will allow us to find the actual RPM path we built for
	// any given .rpm file built from our ancillary nodes.
	builtFileMap := make(map[string]string)
	for _, builtFile := range res.BuiltFiles {
		// We should not expect to see multiple built files with the same basename
		baseName := filepath.Base(builtFile)
		logger.Log.Tracef("Built delta file: %s", builtFile)
		builtFileMap[baseName] = builtFile
	}

	// Now we can scan for all the run nodes that use the cached RPM path and update them to the actual RPM path.
	for _, node := range pkgGraph.AllPreferredRunNodes() {
		// Get base path of the .rpm for the node and find the built file in the map
		rpmBasePath := filepath.Base(node.RpmPath)
		builtFile, ok := builtFileMap[rpmBasePath]
		if ok {
			// We only care about nodes that are deltas
			if node.State == pkggraph.StateDelta {
				// Update the node to point at the actual RPM path from our map of built files
				logger.Log.Debugf("Updating delta run node '%s' path from '%s' to '%s'", node, node.RpmPath, builtFile)
				node.RpmPath = builtFile
			} else if !node.Implicit && node.RpmPath != builtFile {
				// Implicit nodes will point to the cached RPM path, but we don't care about them and will update their
				// paths to the actual RPM path in a later step so ignore them here.
				// Sanity check that any non-delta node has an exact match to the real RPM path
				err = fmt.Errorf("non-delta run node '%s' has unexpected path '%s' (expected non-delta path of '%s')", node, node.RpmPath, builtFile)
				return
			}
		}
	}

	return
}

func drainChannels(channels *schedulerChannels, buildState *schedulerutils.GraphBuildState) {
	// For any workers that are current parked with no buffered requests, close the
	// requests channel to wake up any build workers waiting on a request to be buffered.
	// Upon being woken up by a closed requests channel, the build worker will stop.
	close(channels.Requests)
	close(channels.PriorityRequests)

	// Drain the request buffers to sync the build state with the new number of outstanding builds.
	for req := range channels.PriorityRequests {
		buildState.RemoveBuildRequest(req)
	}
	for req := range channels.Requests {
		buildState.RemoveBuildRequest(req)
	}
}

func doneBuild(channels *schedulerChannels, buildState *schedulerutils.GraphBuildState) {
	// Close the done channel. The build workers will finish processing any work, then return
	// upon seeing this channel is closed.
	close(channels.Done)

	drainChannels(channels, buildState)
}

// stopBuild will stop all future builds from being scheduled by sending a cancellation signal
// to the worker pool and draining any outstanding build requests.
func stopBuild(channels *schedulerChannels, buildState *schedulerutils.GraphBuildState) {
	logger.Log.Error("Stopping build")

	// Close the cancel channel to prevent and buffered requests from being built.
	// Upon seeing the cancel channel is closed, the build worker will stop instead
	// of processing a new request.
	close(channels.Cancel)

	drainChannels(channels, buildState)
}
