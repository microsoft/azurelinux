// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repocloner/rpmrepocloner"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repoutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/rpm"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/profile"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/scheduler/schedulerutils"

	"gonum.org/v1/gonum/graph"
	"gopkg.in/alecthomas/kingpin.v2"
)

const (
	defaultExtraLayers = "0"
)

var (
	app = kingpin.New("graphpkgfetcher", "A tool to download a unresolved packages in a graph into a given directory.")

	inputGraph  = exe.InputStringFlag(app, "Path to the graph file to read")
	outputGraph = exe.OutputFlag(app, "Updated graph file with unresolved nodes marked as resolved")
	outDir      = exe.OutputDirFlag(app, "Directory to download packages into.")

	existingRpmDir          = app.Flag("rpm-dir", "Directory that contains already built RPMs. Should contain top level directories for architecture.").Required().ExistingDir()
	existingToolchainRpmDir = app.Flag("toolchain-rpms-dir", "Directory that contains already built toolchain RPMs. Should contain top level directories for architecture.").Required().ExistingDir()
	tmpDir                  = app.Flag("tmp-dir", "Directory to store temporary files while downloading.").String()

	workertar            = app.Flag("tdnf-worker", "Full path to worker_chroot.tar.gz").Required().ExistingFile()
	repoFiles            = app.Flag("repo-file", "Full path to a repo file").Required().ExistingFiles()
	usePreviewRepo       = app.Flag("use-preview-repo", "Pull packages from the upstream preview repo").Bool()
	disableDefaultRepos  = app.Flag("disable-default-repos", "Disable pulling packages from PMC repos").Bool()
	disableUpstreamRepos = app.Flag("disable-upstream-repos", "Disables pulling packages from upstream repos").Bool()
	toolchainManifest    = app.Flag("toolchain-manifest", "Path to a list of RPMs which are created by the toolchain. Will mark RPMs from this list as prebuilt.").ExistingFile()

	tlsClientCert = app.Flag("tls-cert", "TLS client certificate to use when downloading files.").String()
	tlsClientKey  = app.Flag("tls-key", "TLS client key to use when downloading files.").String()

	stopOnFailure = app.Flag("stop-on-failure", "Stop if failed to cache all unresolved nodes.").Bool()

	tryDownloadDeltaRPMs = app.Flag("try-download-delta-rpms", "Automatically download the RPMs we will try to build into the cache if they are available, so we can skip building them later.").Bool()
	imageConfig          = app.Flag("image-config-file", "Optional image config file to extract a package list from. Used with '--try-download-delta-rpms'").String()
	baseDirPath          = app.Flag("base-dir", "Base directory for relative file paths from the config. Defaults to config's directory. Used with '--try-download-delta-rpms'").ExistingDir()
	pkgsToIgnore         = app.Flag("ignored-packages", "Space separated list of specs ignoring rebuilds if their dependencies have been updated. Will still build if all of the spec's RPMs have not been built.").String()
	pkgsToBuild          = app.Flag("packages", "Space separated list of top-level packages that should be built. Omit this argument to build all packages.").String()
	pkgsToRebuild        = app.Flag("rebuild-packages", "Space separated list of base package names packages that should be rebuilt.").String()
	extraLayers          = app.Flag("extra-layers", "Sets the number of additional layers in the graph beyond the goal packages to buid.").Default(defaultExtraLayers).Int()

	testsToIgnore = app.Flag("ignored-tests", "Space separated list of package tests that should not be ran.").String()
	testsToRun    = app.Flag("tests", "Space separated list of package tests that should be ran. Omit this argument to run all package tests.").String()
	testsToRerun  = app.Flag("rerun-tests", "Space separated list of package tests that should be re-ran.").String()

	inputSummaryFile  = app.Flag("input-summary-file", "Path to a file with the summary of packages cloned to be restored").String()
	outputSummaryFile = app.Flag("output-summary-file", "Path to save the summary of packages cloned").String()

	logFlags      = exe.SetupLogFlags(app)
	profFlags     = exe.SetupProfileFlags(app)
	timestampFile = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(logFlags)

	prof, err := profile.StartProfiling(profFlags)
	if err != nil {
		logger.Log.Warnf("Could not start profiling: %s", err)
	}
	defer prof.StopProfiler()

	timestamp.BeginTiming("graphpkgfetcher", *timestampFile)
	defer timestamp.CompleteTiming()

	dependencyGraph, err := pkggraph.ReadDOTGraphFile(*inputGraph)
	if err != nil {
		logger.Log.Fatalf("Failed to read graph to file: %s", err)
	}

	hasUnresolvedNodes := hasUnresolvedNodes(dependencyGraph)
	if hasUnresolvedNodes || *tryDownloadDeltaRPMs {
		err = fetchPackages(dependencyGraph, hasUnresolvedNodes, *tryDownloadDeltaRPMs)
		if err != nil {
			logger.Log.Fatalf("Failed to fetch packages. Error: %s", err)
		}
	}

	// Write the final graph to file
	err = pkggraph.WriteDOTGraphFile(dependencyGraph, *outputGraph)
	if err != nil {
		logger.Log.Fatalf("Failed to write cache graph to file: %s", err)
	}
}

func fetchPackages(dependencyGraph *pkggraph.PkgGraph, hasUnresolvedNodes, tryDownloadDeltaRPMs bool) (err error) {
	// Create the worker environment
	cloner, err := setupCloner()
	if err != nil {
		err = fmt.Errorf("failed to setup cloner:\n%w", err)
		return
	}
	defer cloner.Close()

	if hasUnresolvedNodes {
		var toolchainPackages []string
		logger.Log.Info("Found unresolved packages to cache, downloading packages")
		toolchainPackages, err = schedulerutils.ReadReservedFilesList(*toolchainManifest)
		if err != nil {
			err = fmt.Errorf("unable to read toolchain manifest file '%s':\n%w", *toolchainManifest, err)
			return
		}

		err = resolveGraphNodes(dependencyGraph, *inputSummaryFile, toolchainPackages, cloner, *stopOnFailure)
		if err != nil {
			err = fmt.Errorf("failed to resolve graph:\n%w", err)
			return
		}
	} else {
		logger.Log.Info("No unresolved packages to cache")
	}

	// Optional delta build cache hydration
	if tryDownloadDeltaRPMs {
		logger.Log.Info("Attempting to download delta RPMs for build nodes")
		err = downloadDeltaNodes(dependencyGraph, cloner)
		if err != nil {
			err = fmt.Errorf("failed to download delta RPMs:\n%w", err)
			return
		}
	}

	// If we grabbed any RPMs, we need to convert them into a local repo
	err = cloner.ConvertDownloadedPackagesIntoRepo()
	if err != nil {
		err = fmt.Errorf("failed to convert downloaded RPMs into a repo:\n%w", err)
		return
	}

	if strings.TrimSpace(*outputSummaryFile) != "" {
		err = repoutils.SaveClonedRepoContents(cloner, *outputSummaryFile)
		if err != nil {
			err = fmt.Errorf("failed to save cloned repo contents:\n%w", err)
			return
		}
	}

	return
}

func setupCloner() (cloner *rpmrepocloner.RpmRepoCloner, err error) {
	// Create the worker environment
	cloner, err = rpmrepocloner.ConstructCloner(*outDir, *tmpDir, *workertar, *existingRpmDir, *existingToolchainRpmDir, *tlsClientCert, *tlsClientKey, *repoFiles)
	if err != nil {
		err = fmt.Errorf("failed to setup new cloner:\n%w", err)
		return
	}

	enabledRepos := rpmrepocloner.RepoFlagAll
	if !*usePreviewRepo {
		enabledRepos = enabledRepos & ^rpmrepocloner.RepoFlagPreview
	}
	if *disableUpstreamRepos {
		enabledRepos = enabledRepos & ^rpmrepocloner.RepoFlagUpstream
	}
	if *disableDefaultRepos {
		enabledRepos = enabledRepos & ^rpmrepocloner.RepoFlagMarinerDefaults
	}
	cloner.SetEnabledRepos(enabledRepos)
	return
}

// downloadDeltaNodes will look at the final cached graph we saved and see if any RPMS can be download instead of built.
// If the previous part of the fetcher worked well we should be able to download only the delta RPMs we need
// to build our packages or image (i.e. we should be able to create a subgraph just like we would for the build step)
//   - dependencyGraph: The graph to use to find the packages we need to build. Should have any caching operations already
//     performed on it. Will be updated with the paths to the delta RPMs we download.
//   - cloner: The cloner to use to download the RPMs
//
// We also access the package list related globals:
//   - pkgsToBuild: The list of packages to build
//   - pkgsToRebuild: The list of packages to rebuild
//   - pkgsToIgnore: The list of packages to ignore
//   - imageConfig: The image config to use to find the packages we need to build
//   - baseDirPath: The base directory to use to find the packages we need to build
func downloadDeltaNodes(dependencyGraph *pkggraph.PkgGraph, cloner *rpmrepocloner.RpmRepoCloner) (err error) {
	const (
		useImplicitForOptimization = true
	)

	timestamp.StartEvent("delta package download", nil)
	defer timestamp.StopEvent(nil)

	// Generate the list of packages that need to be built. If none are requested then all packages will be built. We
	// don't care about explicit rebuilds here since we are going to rebuild them anyway.
	packageVersToBuild, _, _, err := schedulerutils.ParseAndGeneratePackageBuildList(dependencyGraph, exe.ParseListArgument(*pkgsToBuild), exe.ParseListArgument(*pkgsToRebuild), exe.ParseListArgument(*pkgsToIgnore), *imageConfig, *baseDirPath)
	if err != nil {
		err = fmt.Errorf("unable to generate package build list to calculate delta downloads:\n%w", err)
		return
	}

	// Generate the list of tests that need to be ran. If none are requested then all packages will be built. We
	// don't care about explicit rebuilds here since we are going to rebuild them anyway.
	testVersToRun, _, _, err := schedulerutils.ParseAndGeneratePackageTestList(dependencyGraph, exe.ParseListArgument(*testsToRun), exe.ParseListArgument(*testsToRerun), exe.ParseListArgument(*testsToIgnore), *imageConfig, *baseDirPath)
	if err != nil {
		err = fmt.Errorf("unable to generate package build list to calculate delta downloads:\n%w", err)
		return
	}

	// We will heavily modify this graph so it should not be used for anything else, create a copy of it to work with.
	deltaPkgGraphCopy, err := dependencyGraph.DeepCopy()
	if err != nil {
		err = fmt.Errorf("failed to copy graph for delta package downloading:\n%w", err)
		return
	}

	isGraphOptimized, deltaPkgGraphCopy, _, err := schedulerutils.PrepareGraphForBuild(deltaPkgGraphCopy, packageVersToBuild, testVersToRun, useImplicitForOptimization, *extraLayers)
	if err != nil {
		err = fmt.Errorf("failed to initialize graph for delta package downloading:\n%w", err)
		return
	}

	if !isGraphOptimized {
		logger.Log.Warnf("Delta fetcher was unable to prune the build graph. All possible build nodes will be included so delta package downloading will be very slow!")
	}

	err = downloadAllAvailableDeltaRPMs(dependencyGraph, deltaPkgGraphCopy, cloner)
	if err != nil {
		err = fmt.Errorf("failed to download delta RPMs:\n%w", err)
		return
	}

	return
}

// hasUnresolvedNodes scans through the graph to see if there is anything to do
func hasUnresolvedNodes(graph *pkggraph.PkgGraph) bool {
	for _, n := range graph.AllRunNodes() {
		if n.State == pkggraph.StateUnresolved {
			return true
		}
	}
	return false
}

func findUnresolvedNodes(runNodes []*pkggraph.PkgNode) (unreslovedNodes []*pkggraph.PkgNode) {
	for _, n := range runNodes {
		if n.State == pkggraph.StateUnresolved {
			unreslovedNodes = append(unreslovedNodes, n)
		}
	}
	return
}

// resolveGraphNodes scans a graph and for each unresolved node in the graph clones the RPMs needed
// to satisfy it.
func resolveGraphNodes(dependencyGraph *pkggraph.PkgGraph, inputSummaryFile string, toolchainPackages []string, cloner *rpmrepocloner.RpmRepoCloner, stopOnFailure bool) (err error) {
	const downloadDependencies = true

	timestamp.StartEvent("Clone packages", nil)
	defer timestamp.StopEvent(nil)

	if strings.TrimSpace(inputSummaryFile) != "" {
		// If an input summary file was provided, simply restore the cache using the file.
		err = repoutils.RestoreClonedRepoContents(cloner, inputSummaryFile)
		if err != nil {
			return fmt.Errorf("failed to restore external packages cache from '%s':\n%w", inputSummaryFile, err)
		}

		previousEnabledRepos := cloner.GetEnabledRepos()
		cloner.SetEnabledRepos(rpmrepocloner.RepoFlagToolchain | rpmrepocloner.RepoFlagDownloadedCache)
		defer cloner.SetEnabledRepos(previousEnabledRepos)
	}

	// Cache an RPM for each unresolved node in the graph.
	cachingSucceeded := true
	fetchedPackages := make(map[string]bool)
	prebuiltPackages := make(map[string]bool)
	unresolvedNodes := findUnresolvedNodes(dependencyGraph.AllRunNodes())
	unresolvedNodesCount := len(unresolvedNodes)

	timestamp.StartEvent("clone graph", nil)
	for i, n := range unresolvedNodes {
		progressHeader := fmt.Sprintf("Cache progress %d%%", (i*100)/unresolvedNodesCount)
		resolveErr := resolveSingleNode(cloner, n, downloadDependencies, toolchainPackages, fetchedPackages, prebuiltPackages, *outDir)
		if resolveErr == nil {
			logger.Log.Infof("%s: choosing '%s' to provide '%s'.", progressHeader, filepath.Base(n.RpmPath), n.VersionedPkg.Name)
			continue
		}

		// Failing to clone a dependency should not halt a build.
		// The build should continue and attempt best effort to build as many packages as possible.
		logger.Log.Warnf("%s: failed to resolve graph node '%s':\n%s", progressHeader, n, resolveErr)
		cachingSucceeded = false
		errorMessage := strings.Builder{}
		errorMessage.WriteString(fmt.Sprintf("Failed to resolve all nodes in the graph while resolving '%s'\n", n))
		errorMessage.WriteString("Nodes which have this as a dependency:\n")
		for _, dependant := range graph.NodesOf(dependencyGraph.To(n.ID())) {
			errorMessage.WriteString(fmt.Sprintf("\t'%s' depends on '%s'\n", dependant.(*pkggraph.PkgNode), n))
		}
		logger.Log.Debugf(errorMessage.String())
	}
	timestamp.StopEvent(nil) // clone graph
	if stopOnFailure && !cachingSucceeded {
		return fmt.Errorf("failed to cache unresolved nodes")
	}
	return
}

// downloadAllAvailableDeltaRPMs scans a graph and for each build node in the graph and tries to replace it with a cached node instead.
// to satisfy it. Delta nodes will be saved to the cache directory set for the cloner.
//   - realDependencyGraph: The graph to use to find the packages we need to build. Should have any caching operations already
//     performed on it. Will be updated with the paths to the delta RPMs we download.
//   - dependencyGraphDeltaCopy: A copy of the graph we will use to try to optimize the build nodes. This graph should be
//     optimized to only contain the nodes we need to build.
//   - cloner: The cloner to use to download the RPMs
func downloadAllAvailableDeltaRPMs(realDependencyGraph, dependencyGraphDeltaCopy *pkggraph.PkgGraph, cloner *rpmrepocloner.RpmRepoCloner) (err error) {
	timestamp.StartEvent("downloading delta nodes", nil)
	defer timestamp.StopEvent(nil)

	// First scan the copy of the graph we tried to optimize for all the SRPMs we need to build. We will use this list to
	// match against all the nodes in the full graph.
	srpmPaths := make(map[string]bool)
	for _, n := range dependencyGraphDeltaCopy.AllBuildNodes() {
		srpmPaths[n.SrpmPath] = true
	}

	// For each build node, try to update it to a delta node with a downloaded RPM backing it.
	logger.Log.Debugf("Resolving build nodes")
	buildNodes := realDependencyGraph.AllBuildNodes()
	for i, n := range buildNodes {
		// If this node isn't part of the optimized graph, skip it.
		if _, ok := srpmPaths[n.SrpmPath]; !ok {
			logger.Log.Debugf("Skipping non-optimized delta build node %s", n)
			continue
		}

		logger.Log.Debugf("Resolving build node %s", n)
		err = downloadSingleDeltaRPM(realDependencyGraph, n, cloner)
		if err != nil {
			return fmt.Errorf("failed to download delta RPM for build node %s:\n%w", n, err)
		}
		if n.State == pkggraph.StateDelta {
			logger.Log.Infof("Delta Progress %d%%: delta RPM found for '%s-%s'.", (i*100)/len(buildNodes), n.VersionedPkg.Name, n.VersionedPkg.Version)
		} else {
			logger.Log.Infof("Delta Progress %d%%: skipped getting delta RPM for '%s' at '%s'.", (i*100)/len(buildNodes), n.VersionedPkg.Name, n.RpmPath)
		}
	}

	return
}

// downloadSingleDeltaRPM attempts to download a single delta RPM for a build node. If the delta RPM is available
// it will be downloaded and the build node will be updated to point to the new RPM. The associated run node will
// also be updated to point to the new RPM since the scheduler uses the run node to find the RPM to install. If a
// delta RPM is not available, the build node will be left alone an no error will be returned.
//   - realDependencyGraph: The graph to update
//   - buildNode: The build node to update. This node should be from the real graph as we will be updating it directly.
//     to find the actual build node in the graph.
//   - cloner: The cloner to use to download the RPMs
func downloadSingleDeltaRPM(realDependencyGraph *pkggraph.PkgGraph, buildNode *pkggraph.PkgNode, cloner *rpmrepocloner.RpmRepoCloner) (err error) {
	const downloadDependencies = false
	var lookup *pkggraph.LookupNode

	// Replace all '/' with '_' in the package name to get a valid timestamp name
	// e.g. "bin/ls" -> "bin_ls"
	tsName := strings.ReplaceAll(buildNode.VersionedPkg.Name, "/", "_")
	timestamp.StartEvent(fmt.Sprintf("downloading delta node %s", tsName), nil)
	defer timestamp.StopEvent(nil)

	lookup, err = realDependencyGraph.FindExactPkgNodeFromPkg(buildNode.VersionedPkg)
	if err != nil {
		err = fmt.Errorf("can't find build node '%s' in graph:\n%w", buildNode, err)
		return err
	}
	if lookup == nil || lookup.RunNode == nil {
		err = fmt.Errorf("can't find run lookup '%v' in graph", lookup)
		return err
	}

	runNode := lookup.RunNode

	// Get the final output path for the build node if we don't convert it to a delta node
	originalRpmPath := buildNode.RpmPath
	foundFinalRPM, err := file.PathExists(originalRpmPath)
	if err != nil {
		return fmt.Errorf("can't check if final RPM '%s' exists:\n%w", originalRpmPath, err)
	}

	// Only download dependencies for delta RPMs if we don't already have the RPM in the out/RPMS folder
	if foundFinalRPM {
		return
	}
	// We have the expected rpm path, take the base name and strip .rpm off to get a name we can pass to tdnf
	// to download the delta RPM
	// e.g. "/home/user/repo/out/RPMS/x86_64/pkg-1.0-1.cm2.x86_64.rpm" -> "pkg-1.0-1.cm2.x86_64"
	fullyQualifiedRpmName := filepath.Base(originalRpmPath)
	fullyQualifiedRpmName = strings.TrimSuffix(fullyQualifiedRpmName, ".rpm")

	// Convert the name back into the expected path in the RPM cache. This is where the cloner is expected to put
	// the RPM when it downloads it.
	cachedRPMPath := rpmPackageToRPMPath(fullyQualifiedRpmName, cloner.CloneDirectory())
	foundCacheRPM, err := file.PathExists(cachedRPMPath)
	if err != nil {
		return fmt.Errorf("can't check if cached RPM '%s' exists:\n%w", cachedRPMPath, err)
	}

	// We will likely try to download the delta RPM multiple times across different nodes, so only do it if we don't
	// already have it in the cache.
	if !foundCacheRPM {
		// Avoid any processing since we know the exact RPM we want to download
		_, err = cloner.CloneByName(downloadDependencies, fullyQualifiedRpmName)
		if err != nil {
			logger.Log.Warnf("Can't find delta RPM to download for %s: %s (local copy may be newer than published version)", fullyQualifiedRpmName, err)
			return nil
		}
	} else {
		logger.Log.Debugf("Found pre-cached delta RPM for %s, skipping download", fullyQualifiedRpmName)
	}

	foundCacheRPM, err = file.PathExists(cachedRPMPath)
	if err != nil {
		return fmt.Errorf("can't check if cached RPM '%s' exists:\n%w", cachedRPMPath, err)
	}
	if foundCacheRPM {
		buildNode.State = pkggraph.StateDelta
		runNode.State = pkggraph.StateDelta

		// Update the build and run nodes to point to the new RPM in the cache
		runNode.RpmPath = cachedRPMPath
		buildNode.RpmPath = cachedRPMPath

		logger.Log.Debugf("Converted delta build node is now: '%s'", buildNode)
		logger.Log.Debugf("Converted delta run node is now: '%s'", runNode)
	} else {
		logger.Log.Warnf("Delta download for '%s' did not generate the correct delta RPM: '%s'", buildNode, cachedRPMPath)
		return nil
	}

	return
}

// resolveSingleNode caches the RPM for a single node.
// It will modify fetchedPackages on a successful package clone.
func resolveSingleNode(cloner *rpmrepocloner.RpmRepoCloner, node *pkggraph.PkgNode, cloneDeps bool, toolchainPackages []string, fetchedPackages, prebuiltPackages map[string]bool, outDir string) (err error) {
	logger.Log.Debugf("Adding node %s to the cache", node.FriendlyName())

	logger.Log.Debugf("Searching for a package which supplies: %s", node.VersionedPkg.Name)
	// Resolve nodes to exact package names so they can be referenced in the graph.
	resolvedPackages, err := cloner.WhatProvides(node.VersionedPkg)
	if err != nil {
		msg := fmt.Sprintf("Failed to resolve (%s) to a package. Error: %s", node.VersionedPkg, err)
		// It is not an error if an implicit node could not be resolved as it may become available later in the build.
		// If it does not become available scheduler will print an error at the end of the build.
		if node.Implicit || node.State == pkggraph.StateDelta {
			logger.Log.Debug(msg)
		} else {
			logger.Log.Warn(msg)
		}
		return
	}

	if len(resolvedPackages) == 0 {
		return fmt.Errorf("failed to find any packages providing '%v'", node.VersionedPkg)
	}

	preBuilt := false
	for _, resolvedPackage := range resolvedPackages {
		if !fetchedPackages[resolvedPackage] {
			desiredPackage := &pkgjson.PackageVer{
				Name: resolvedPackage,
			}

			preBuilt, err = cloner.CloneByPackageVer(cloneDeps, desiredPackage)
			if err != nil {
				err = fmt.Errorf("failed to clone '%s' from RPM repo:\n%w", resolvedPackage, err)
				return
			}
			fetchedPackages[resolvedPackage] = true
			prebuiltPackages[resolvedPackage] = preBuilt

			logger.Log.Debugf("Fetched '%s' as potential candidate (is pre-built: %v).", resolvedPackage, prebuiltPackages[resolvedPackage])
		}
	}

	err = assignRPMPath(node, outDir, resolvedPackages)
	if err != nil {
		err = fmt.Errorf("failed to find an RPM to provide '%s':\n%w", node.VersionedPkg.Name, err)
		return
	}

	// If a package is  available locally, and it is part of the toolchain, mark it as a prebuilt so the scheduler knows it can use it
	// immediately (especially for dynamic generator created capabilities)
	if (preBuilt || prebuiltPackages[node.RpmPath]) && isToolchainPackage(node.RpmPath, toolchainPackages) {
		logger.Log.Debugf("Using a prebuilt toolchain package to resolve this dependency")
		prebuiltPackages[node.RpmPath] = true
		node.State = pkggraph.StateUpToDate
		node.Type = pkggraph.TypePreBuilt
	} else {
		node.State = pkggraph.StateCached
	}

	return
}

func assignRPMPath(node *pkggraph.PkgNode, outDir string, resolvedPackages []string) (err error) {
	rpmPaths := []string{}
	for _, resolvedPackage := range resolvedPackages {
		rpmPaths = append(rpmPaths, rpmPackageToRPMPath(resolvedPackage, outDir))
	}

	chosenRPMPath := rpmPaths[0]
	if len(rpmPaths) > 1 {
		var resolvedRPMs []string
		logger.Log.Debugf("Found %d candidates. Resolving.", len(rpmPaths))

		resolvedRPMs, err = rpm.ResolveCompetingPackages(*tmpDir, rpmPaths...)
		if err != nil {
			logger.Log.Errorf("Failed while trying to pick an RPM providing '%s' from the following RPMs: %v", node.VersionedPkg.Name, rpmPaths)
			return
		}

		resolvedRPMsCount := len(resolvedRPMs)
		if resolvedRPMsCount == 0 {
			logger.Log.Errorf("Failed while trying to pick an RPM providing '%s'. No RPM can be installed from the following: %v", node.VersionedPkg.Name, rpmPaths)
			return
		}

		if resolvedRPMsCount > 1 {
			logger.Log.Warnf("Found %d candidates to provide '%s'. Picking the first one.", resolvedRPMsCount, node.VersionedPkg.Name)
		}

		chosenRPMPath = rpmPackageToRPMPath(resolvedRPMs[0], outDir)
	}

	node.RpmPath = chosenRPMPath

	return
}

func rpmPackageToRPMPath(rpmPackage, outDir string) string {
	// Construct the rpm path of the cloned package.
	rpmName := fmt.Sprintf("%s.rpm", rpmPackage)
	return filepath.Join(outDir, rpmName)
}

func isToolchainPackage(rpmPath string, toolchainRPMs []string) bool {
	base := filepath.Base(rpmPath)
	for _, t := range toolchainRPMs {
		if t == base {
			return true
		}
	}
	return false
}
