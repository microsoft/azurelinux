// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/juliangruber/go-intersect"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repocloner/rpmrepocloner"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repoutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/rpm"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/scheduler/schedulerutils"

	"gonum.org/v1/gonum/graph"
	"gopkg.in/alecthomas/kingpin.v2"
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

	inputSummaryFile  = app.Flag("input-summary-file", "Path to a file with the summary of packages cloned to be restored").String()
	outputSummaryFile = app.Flag("output-summary-file", "Path to save the summary of packages cloned").String()

	logFile       = exe.LogFileFlag(app)
	logLevel      = exe.LogLevelFlag(app)
	timestampFile = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)
	timestamp.BeginTiming("graphpkgfetcher", *timestampFile)
	defer timestamp.CompleteTiming()

	err := fetchPackages()
	if err != nil {
		logger.Log.Fatalf("Failed to fetch packages. Error: %s", err)
	}
}

func fetchPackages() (err error) {
	var cloner *rpmrepocloner.RpmRepoCloner
	dependencyGraph, err := pkggraph.ReadDOTGraphFile(*inputGraph)
	if err != nil {
		err = fmt.Errorf("failed to read graph to file:\n%w", err)
		return
	}

	toolchainPackages, err := schedulerutils.ReadReservedFilesList(*toolchainManifest)
	if err != nil {
		err = fmt.Errorf("unable to read toolchain manifest file '%s':\n%w", *toolchainManifest, err)
		return
	}

	hasUnresolvedNodes := hasUnresolvedNodes(dependencyGraph)
	if *tryDownloadDeltaRPMs || hasUnresolvedNodes {
		// Create the worker environment
		cloner, err = rpmrepocloner.ConstructCloner(*outDir, *tmpDir, *workertar, *existingRpmDir, *existingToolchainRpmDir, *tlsClientCert, *tlsClientKey, *usePreviewRepo, *disableUpstreamRepos, *disableDefaultRepos, *repoFiles)
		if err != nil {
			err = fmt.Errorf("failed to setup new cloner:\n%w", err)
			return err
		}
		defer cloner.Close()
	}

	if hasUnresolvedNodes {
		logger.Log.Info("Found unresolved packages to cache, downloading packages")
		err = resolveGraphNodes(dependencyGraph, *inputSummaryFile, toolchainPackages, cloner, *stopOnFailure)
		if err != nil {
			err = fmt.Errorf("failed to resolve graph:\n%w", err)
			return err
		}
	} else {
		logger.Log.Info("No unresolved packages to cache")
	}

	// Write the graph to file (even if we are going to download delta RPMs, we want to save the graph with the resolved nodes first)
	err = pkggraph.WriteDOTGraphFile(dependencyGraph, *outputGraph)
	if err != nil {
		err = fmt.Errorf("failed to write cache graph to file:\n%w", err)
		return
	}

	// Optional delta build cache hydration
	if *tryDownloadDeltaRPMs {
		logger.Log.Info("Attempting to download delta RPMs for build nodes")
		err = downloadDeltaNodes(dependencyGraph, cloner)
		if err != nil {
			err = fmt.Errorf("failed to download delta RPMs:\n%w", err)
			return
		}
		// Update the package graph with the paths to the delta RPMs we downloaded
		err = pkggraph.WriteDOTGraphFile(dependencyGraph, *outputGraph)
		if err != nil {
			err = fmt.Errorf("failed to write cache graph to file:\n%w", err)
			return
		}
	}

	// If we grabbed any RPMs, we need to convert them into a local repo
	if *tryDownloadDeltaRPMs || hasUnresolvedNodes {
		logger.Log.Info("Configuring downloaded RPMs as a local repository")
		err = cloner.ConvertDownloadedPackagesIntoRepo()
		if err != nil {
			err = fmt.Errorf("failed to convert downloaded RPMs into a repo:\n%w", err)
			return err
		}

		if strings.TrimSpace(*outputSummaryFile) != "" {
			err = repoutils.SaveClonedRepoContents(cloner, *outputSummaryFile)
			if err != nil {
				err = fmt.Errorf("failed to save cloned repo contents:\n%w", err)
				return err
			}
		}
	}
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
	packageVersToBuild, err := parseAndGeneratePackageList(dependencyGraph, *pkgsToBuild, *pkgsToRebuild, *pkgsToIgnore, *imageConfig, *baseDirPath)
	if err != nil {
		err = fmt.Errorf("unable to generate package build list to calculate delta downloads: %w", err)
		return
	}

	// The scheduler utils expect to pick a graph up from a file, so we will write the graph we wrote it to a file and
	// now we read it back in and optimize it. We will heavily modify this graph so it should not be used for anything
	// else.
	isGraphOptimized, deltaPkgGraphCopy, _, err := schedulerutils.InitializeGraph(*outputGraph, packageVersToBuild, useImplicitForOptimization)
	if err != nil {
		err = fmt.Errorf("failed to initialize graph for delta package downloading: %w", err)
		return
	}

	if !isGraphOptimized {
		logger.Log.Warnf("Delta fetcher was unable to prune the build graph. All possible build nodes will be included so delta package downloading will be very slow!")
	}

	if len(deltaPkgGraphCopy.AllBuildNodes()) > 0 {
		err = downloadAllAvailableDeltaRPMs(dependencyGraph, deltaPkgGraphCopy, cloner, *stopOnFailure)
		if err != nil {
			err = fmt.Errorf("failed to download delta RPMs: %w", err)
			return
		}
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

func parseAndGeneratePackageList(dependencyGraph *pkggraph.PkgGraph, pkgsToBuild, pkgsToRebuild, pkgsToIgnore, imageConfig, baseDirPath string) (finalPackagesToBuild []*pkgjson.PackageVer, err error) {
	// Generate the list of packages that need to be built.
	// If none are requested then all packages will be built.
	packagesToBuild, err := schedulerutils.PackageNamesToBuiltPackages(exe.ParseListArgument(pkgsToBuild), dependencyGraph)
	if err != nil {
		err = fmt.Errorf("unable to find build nodes for the packages to build, error:\n%w", err)
		return
	}

	packagesToRebuild, err := schedulerutils.PackageNamesToBuiltPackages(exe.ParseListArgument(pkgsToRebuild), dependencyGraph)
	if err != nil {
		err = fmt.Errorf("unable to find build nodes for the packages to rebuild, error:\n%w", err)
		return
	}

	prunedIgnoredPackageNames, unknownNames, err := schedulerutils.PruneUnknownPackages(exe.ParseListArgument(pkgsToIgnore), dependencyGraph)
	if err != nil {
		err = fmt.Errorf("failed to prune unknown package/spec names from the ignored list, error:\n%w", err)
		return
	}

	if len(unknownNames) != 0 {
		logger.Log.Warnf("The following ignored items matched neither a spec nor a package name: %v.", unknownNames)
		return
	}

	packagesToIgnore, err := schedulerutils.PackageNamesToBuiltPackages(prunedIgnoredPackageNames, dependencyGraph)
	if err != nil {
		err = fmt.Errorf("unable to find build nodes for the ignored packages, error:\n%w", err)
		return
	}

	ignoredAndRebuiltPackages := intersect.Hash(packagesToIgnore, packagesToRebuild)
	if len(ignoredAndRebuiltPackages) != 0 {
		err = fmt.Errorf("can't ignore and force a rebuild of a package at the same time. Abusing packages: %v", ignoredAndRebuiltPackages)
		return
	}

	finalPackagesToBuild, err = schedulerutils.CalculatePackagesToBuild(packagesToBuild, packagesToRebuild, imageConfig, baseDirPath, dependencyGraph)
	if err != nil {
		err = fmt.Errorf("unable to generate package build list, error:\n%w", err)
		return
	}

	return
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
	cachingSucceeded := true
	if strings.TrimSpace(inputSummaryFile) == "" {
		// Cache an RPM for each unresolved node in the graph.
		fetchedPackages := make(map[string]bool)
		prebuiltPackages := make(map[string]bool)
		unresolvedNodes := findUnresolvedNodes(dependencyGraph.AllRunNodes())

		timestamp.StartEvent("clone graph", nil)

		for _, n := range unresolvedNodes {
			resolveErr := resolveSingleNode(cloner, n, downloadDependencies, toolchainPackages, fetchedPackages, prebuiltPackages, *outDir)
			// Failing to clone a dependency should not halt a build.
			// The build should continue and attempt best effort to build as many packages as possible.
			if resolveErr != nil {
				logger.Log.Warnf("Failed to resolve graph node '%s':\n%s", n, resolveErr)
				cachingSucceeded = false
				errorMessage := strings.Builder{}
				errorMessage.WriteString(fmt.Sprintf("Failed to resolve all nodes in the graph while resolving '%s'\n", n))
				errorMessage.WriteString("Nodes which have this as a dependency:\n")
				for _, dependant := range graph.NodesOf(dependencyGraph.To(n.ID())) {
					errorMessage.WriteString(fmt.Sprintf("\t'%s' depends on '%s'\n", dependant.(*pkggraph.PkgNode), n))
				}
				logger.Log.Debugf(errorMessage.String())
			}
		}
		timestamp.StopEvent(nil) // clone graph
	} else {
		timestamp.StartEvent("restore packages", nil)

		// If an input summary file was provided, simply restore the cache using the file.
		err = repoutils.RestoreClonedRepoContents(cloner, inputSummaryFile)
		cachingSucceeded = err == nil

		timestamp.StopEvent(nil) // restore packages
	}
	if stopOnFailure && !cachingSucceeded {
		return fmt.Errorf("failed to cache unresolved nodes")
	}
	return
}

// downloadAllAvailableDeltaRPMs scans a graph and for each build node in the graph and tries to replace it with a cached node instead.
// to satisfy it.
//   - realDependencyGraph: The graph to use to find the packages we need to build. Should have any caching operations already
//     performed on it. Will be updated with the paths to the delta RPMs we download.
//   - dependencyGraphDeltaCopy: A copy of the graph we will use to try to optimize the build nodes. This graph should be
//     optimized to only contain the nodes we need to build.
//   - cloner: The cloner to use to download the RPMs
//   - stopOnFailure: If true, will stop the build if we fail to download any delta RPMs.
func downloadAllAvailableDeltaRPMs(realDependencyGraph, dependencyGraphDeltaCopy *pkggraph.PkgGraph, cloner *rpmrepocloner.RpmRepoCloner, stopOnFailure bool) (err error) {
	timestamp.StartEvent("downloading delta nodes", nil)
	defer timestamp.StopEvent(nil)

	// First scan the copy of the graph we tried to optimize for all the SRPMs we need to build. We will use this list to
	// match against all the nodes in the full graph.
	srpmPaths := make(map[string]bool)
	for _, n := range dependencyGraphDeltaCopy.AllBuildNodes() {
		srpmPaths[n.SrpmPath] = true
	}

	// We don't want to download implicit nodes since they will be included in another node with the same SRPM. Keep a list
	// of them so we can fix them up later.
	skippedNodes := []*pkggraph.PkgNode{}
	// We will need to keep track of the original path to delta path mapping so we can fix up the implicit nodes later.
	originalPathToDeltaPathMap := make(map[string]string)

	// For each build node, try to update it to a delta node with a downloaded RPM backing it.
	logger.Log.Debugf("Resolving build nodes")
	for _, n := range realDependencyGraph.AllBuildNodes() {
		// Implicit nodes cause us troubles since we don't know exactly which RPMs they will build (so the cache fetcher
		// will pull all of the possible matches). Since we are already matching against SRPMs, we can safely skip these
		// nodes since they will be included in another node with the same SRPM.
		if n.Implicit {
			logger.Log.Debugf("Skipping implicit delta build node %s", n)
			skippedNodes = append(skippedNodes, n)
			continue
		}

		// If this node isn't part of the optimized graph, skip it.
		if _, ok := srpmPaths[n.SrpmPath]; !ok {
			logger.Log.Debugf("Skipping non-optimized delta build node %s", n)
			continue
		}

		logger.Log.Debugf("Resolving build node %s", n)
		if n.State == pkggraph.StateBuild {
			foundMatch, err := downloadSingleDeltaRPM(realDependencyGraph, n, cloner, *outDir, &originalPathToDeltaPathMap)
			if err != nil {
				return fmt.Errorf("failed to download delta RPM for build node %s: %w", n, err)
			}
			if !foundMatch {
				// Throw any nodes we fail to resolve the fist time into a list so we can try to resolve them again later.
				// This will help with cases were a new sub-package is added to a build node, but we won't be able to download
				// the delta RPM since it doesn't exist yet.
				skippedNodes = append(skippedNodes, n)
			}
		}
	}

	// Fix up the implicit nodes to point to the correct delta RPMs that we parsed earlier.
	for _, n := range skippedNodes {
		logger.Log.Debugf("Fixing up skipped node %s", n)
		err = fixupDeltaImplicitNode(realDependencyGraph, n, &originalPathToDeltaPathMap)
		if err != nil {
			return fmt.Errorf("failed to fixup skipped node %s: %w", n, err)
		}
	}

	return
}

// downloadSingleDeltaRPM attempts to download a single delta RPM for a build node. If the delta RPM is available
// it will be downloaded and the build node will be updated to point to the new RPM. The associated run node will
// also be updated to point to the new RPM since the scheduler uses the run node to find the RPM to install.
//   - realDependencyGraph: The graph to update
//   - realBuildNode: The build node to update. This node should be from the real graph as we will be updating it directly.
//     to find the actual build node in the graph.
//   - cloner: The cloner to use to download the RPMs
//   - deltaRpmDir: The directory to download the RPMs into (likely the same as the normal RPM cache)
//   - pathMap: A map of the original path to the delta path for each RPM that was downloaded. This is used to fix up
//     the implicit nodes later.
func downloadSingleDeltaRPM(realDependencyGraph *pkggraph.PkgGraph, realBuildNode *pkggraph.PkgNode, cloner *rpmrepocloner.RpmRepoCloner, deltaRpmDir string, pathMap *map[string]string) (foundMatch bool, err error) {
	const downloadDependencies = false
	var lookup *pkggraph.LookupNode

	// Find the real build node in the graph we want to keep (we will be discarding the graph the node was passed in from so we can't use it)
	if realBuildNode.Type != pkggraph.TypeBuild {
		err = fmt.Errorf("node '%s' is not a build node, can't download delta RPM", realBuildNode)
		return false, err
	}

	timestamp.StartEvent(fmt.Sprintf("downloading delta node %s", realBuildNode.VersionedPkg.Name), nil)
	defer timestamp.StopEvent(nil)

	lookup, err = realDependencyGraph.FindExactPkgNodeFromPkg(realBuildNode.VersionedPkg)
	if err != nil {
		err = fmt.Errorf("can't find build node '%s' in graph: %w", realBuildNode, err)
		return false, err
	}
	if lookup == nil || lookup.RunNode == nil {
		err = fmt.Errorf("can't find run lookup '%v' in graph", lookup)
		return false, err
	}

	if lookup.BuildNode != realBuildNode {
		err = fmt.Errorf("real build node '%v' does not match build node in the graph lookup '%v'", realBuildNode, lookup.BuildNode)
		return false, err
	}

	realRunNode := lookup.RunNode
	// We need to copy the node since the fetcher may on occasion choose a different package to provide something than
	// we want. We only consider a delta node valid if the .rpm matches exactly. If we tryy and fail to download a delta
	// the node would be left in a bad state.
	nodeCopy := realBuildNode.Copy()

	// Get the final output path for the build node if we don't convert it to a delta node
	originalRpmPath := realBuildNode.RpmPath
	foundFinalRPM, _ := file.IsFile(originalRpmPath)

	// Only download dependencies for delta RPMs if we don't already have the RPM in the out/RPMS folder
	if !foundFinalRPM {
		// Flag the node as a delta node now so the resolver knows this isn't a critical issue if it fails to resolve
		nodeCopy.State = pkggraph.StateDelta
		resolveErr := resolveSingleNode(cloner, nodeCopy, downloadDependencies, nil, make(map[string]bool), make(map[string]bool), deltaRpmDir)
		// Failing to clone a dependency should not halt a build.
		// The build should continue and attempt best effort to build as many packages as possible.
		if resolveErr != nil {
			logger.Log.Warnf("Can't find delta RPM to download for %s-%s: %s", nodeCopy.VersionedPkg.Name, nodeCopy.VersionedPkg.Version, resolveErr)
			return false, nil
		}
		logger.Log.Tracef("Updating real node '%s' with info from newly cached delta node '%s'", realBuildNode, nodeCopy)

		// Check that the RPM we are getting matches the expected out/RPM path using the base name of the file path
		cachedRPMPath := nodeCopy.RpmPath
		if filepath.Base(cachedRPMPath) != filepath.Base(originalRpmPath) {
			logger.Log.Warnf("cached delta RPM '%s' does not match expected RPM '%s', skipping", filepath.Base(cachedRPMPath), filepath.Base(originalRpmPath))
			return false, nil
		} else {
			logger.Log.Infof("Delta RPM found for '%s-%s'.", realBuildNode.VersionedPkg.Name, realBuildNode.VersionedPkg.Version)
		}

		realBuildNode.State = pkggraph.StateDelta
		realRunNode.State = pkggraph.StateDelta

		// Record the original path to delta path mapping so we can fix up the implicit nodes later.
		(*pathMap)[originalRpmPath] = cachedRPMPath
		realRunNode.RpmPath = cachedRPMPath
		realBuildNode.RpmPath = cachedRPMPath

		logger.Log.Tracef("PathMap updated: %v", *pathMap)
		logger.Log.Debugf("Converted delta build node is now: '%s'", realBuildNode)
		logger.Log.Debugf("Converted delta run node is now: '%s'", realRunNode)
	} else {
		logger.Log.Infof("Already have a RPM for '%s' at '%s'.", realBuildNode.VersionedPkg.Name, originalRpmPath)
	}

	return true, err
}

// fixupDeltaImplicitNode will fix up the build and run nodes associated with an implicit delta RPM node. They need to
// have their RPM paths updated to point to the delta RPMs we downloaded due to another node.
//   - pkgGraph: The graph to update
//   - implicitNode: The implicit build node to update, this node need not be in the actual graph and will be used as a reference
//     to find the actual build node in the graph.
//   - pathMap: The map of original RPM paths to delta RPM paths that we have already downloaded.
func fixupDeltaImplicitNode(realPkgGraph *pkggraph.PkgGraph, implicitNode *pkggraph.PkgNode, pathMap *map[string]string) (err error) {
	var lookup *pkggraph.LookupNode

	logger.Log.Debugf("Implicit node '%s' is a delta RPM, fixing up associated build and run nodes.", implicitNode)

	lookup, err = realPkgGraph.FindExactPkgNodeFromPkg(implicitNode.VersionedPkg)
	if err != nil {
		err = fmt.Errorf("can't find implicit lookup node '%s' in graph: %w", implicitNode, err)
		return
	}
	if lookup == nil || lookup.BuildNode == nil || lookup.RunNode == nil {
		err = fmt.Errorf("can't find implicit build and run lookup '%v' in graph", lookup)
		return
	}

	realBuildNode := lookup.BuildNode
	realRunNode := lookup.RunNode

	// Check if we have a path saved for this rpm
	dstPath := realRunNode.RpmPath
	if deltaPath, ok := (*pathMap)[dstPath]; ok {
		logger.Log.Tracef("Found delta RPM for '%s' at '%s', updating build and run nodes.", implicitNode, dstPath)
		realBuildNode.State = pkggraph.StateDelta
		realRunNode.State = pkggraph.StateDelta

		// Update the build and run nodes to point to the delta RPM
		realBuildNode.RpmPath = deltaPath
		realRunNode.RpmPath = deltaPath
	} else {
		logger.Log.Tracef("Can't find delta RPM for '%s' at '%s', skipping implicit delta update.", implicitNode, dstPath)
		return
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

			preBuilt, err = cloner.Clone(cloneDeps, desiredPackage)
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

	logger.Log.Infof("Choosing '%s' to provide '%s'.", filepath.Base(node.RpmPath), node.VersionedPkg.Name)

	return
}

func assignRPMPath(node *pkggraph.PkgNode, outDir string, resolvedPackages []string) (err error) {
	rpmPaths := []string{}
	for _, resolvedPackage := range resolvedPackages {
		rpmPaths = append(rpmPaths, rpmPackageToRPMPath(resolvedPackage, outDir))
	}

	node.RpmPath = rpmPaths[0]
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

		node.RpmPath = rpmPackageToRPMPath(resolvedRPMs[0], outDir)
	}

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
