// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"gonum.org/v1/gonum/graph"
	"gopkg.in/alecthomas/kingpin.v2"
	"microsoft.com/pkggen/internal/exe"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/packagerepo/repocloner/rpmrepocloner"
	"microsoft.com/pkggen/internal/packagerepo/repoutils"
	"microsoft.com/pkggen/internal/pkggraph"
	"microsoft.com/pkggen/internal/pkgjson"
	"microsoft.com/pkggen/internal/rpm"
)

var (
	app = kingpin.New("graphpkgfetcher", "A tool to download a unresolved packages in a graph into a given directory.")

	inputGraph  = exe.InputStringFlag(app, "Path to the graph file to read")
	outputGraph = exe.OutputFlag(app, "Updated graph file with unresolved nodes marked as resolved")
	outDir      = exe.OutputDirFlag(app, "Directory to download packages into.")

	existingRpmDir = app.Flag("rpm-dir", "Directory that contains already built RPMs. Should contain top level directories for architecture.").Required().ExistingDir()
	tmpDir         = app.Flag("tmp-dir", "Directory to store temporary files while downloading.").String()

	workertar            = app.Flag("tdnf-worker", "Full path to worker_chroot.tar.gz").Required().ExistingFile()
	repoFiles            = app.Flag("repo-file", "Full path to a repo file").Required().ExistingFiles()
	usePreviewRepo       = app.Flag("use-preview-repo", "Pull packages from the upstream preview repo").Bool()
	disableUpstreamRepos = app.Flag("disable-upstream-repos", "Disables pulling packages from upstream repos").Bool()

	tlsClientCert = app.Flag("tls-cert", "TLS client certificate to use when downloading files.").String()
	tlsClientKey  = app.Flag("tls-key", "TLS client key to use when downloading files.").String()

	inputSummaryFile  = app.Flag("input-summary-file", "Path to a file with the summary of packages cloned to be restored").String()
	outputSummaryFile = app.Flag("output-summary-file", "Path to save the summary of packages cloned").String()

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	dependencyGraph := pkggraph.NewPkgGraph()

	err := pkggraph.ReadDOTGraphFile(dependencyGraph, *inputGraph)
	if err != nil {
		logger.Log.Panicf("Failed to read graph to file. Error: %s", err)
	}

	if hasUnresolvedNodes(dependencyGraph) {
		err = resolveGraphNodes(dependencyGraph, *inputSummaryFile, *outputSummaryFile, *disableUpstreamRepos)
		if err != nil {
			logger.Log.Panicf("Failed to resolve graph. Error: %s", err)
		}
	} else {
		logger.Log.Info("No unresolved packages to cache")
	}

	err = pkggraph.WriteDOTGraphFile(dependencyGraph, *outputGraph)
	if err != nil {
		logger.Log.Panicf("Failed to write cache graph to file. Error: %s", err)
	}
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

// resolveGraphNodes scans a graph and for each unresolved node in the graph clones the RPMs needed
// to satisfy it.
func resolveGraphNodes(dependencyGraph *pkggraph.PkgGraph, inputSummaryFile, outputSummaryFile string, disableUpstreamRepos bool) (err error) {
	// Create the worker environment
	cloner := rpmrepocloner.New()
	err = cloner.Initialize(*outDir, *tmpDir, *workertar, *existingRpmDir, *usePreviewRepo, *repoFiles)
	if err != nil {
		logger.Log.Errorf("Failed to initialize RPM repo cloner. Error: %s", err)
		return
	}
	defer cloner.Close()

	if !disableUpstreamRepos {
		tlsKey, tlsCert := strings.TrimSpace(*tlsClientKey), strings.TrimSpace(*tlsClientCert)
		err = cloner.AddNetworkFiles(tlsCert, tlsKey)
		if err != nil {
			logger.Log.Panicf("Failed to customize RPM repo cloner. Error: %s", err)
		}
	}

	if strings.TrimSpace(inputSummaryFile) == "" {
		// Cache an RPM for each unresolved node in the graph.
		fetchedPackages := make(map[string]bool)
		for _, n := range dependencyGraph.AllRunNodes() {
			if n.State == pkggraph.StateUnresolved {
				resolveErr := resolveSingleNode(cloner, n, fetchedPackages, *outDir)
				// Failing to clone a dependency should not halt a build.
				// The build should continue and attempt best effort to build as many packages as possible.
				if resolveErr != nil {
					errorMessage := strings.Builder{}
					errorMessage.WriteString(fmt.Sprintf("Failed to resolve all nodes in the graph while resolving '%s'\n", n))
					errorMessage.WriteString("Nodes which have this as a dependency:\n")
					for _, dependant := range graph.NodesOf(dependencyGraph.To(n.ID())) {
						errorMessage.WriteString(fmt.Sprintf("\t'%s' depends on '%s'\n", dependant.(*pkggraph.PkgNode), n))
					}
					logger.Log.Debugf(errorMessage.String())
				}
			}
		}
	} else {
		// If an input summary file was provided, simply restore the cache using the file.
		err = repoutils.RestoreClonedRepoContents(cloner, inputSummaryFile)
		if err != nil {
			return
		}
	}

	logger.Log.Info("Configuring downloaded RPMs as a local repository")
	err = cloner.ConvertDownloadedPackagesIntoRepo()
	if err != nil {
		logger.Log.Errorf("Failed to convert downloaded RPMs into a repo. Error: %s", err)
		return
	}

	if strings.TrimSpace(outputSummaryFile) != "" {
		err = repoutils.SaveClonedRepoContents(cloner, outputSummaryFile)
		if err != nil {
			logger.Log.Errorf("Failed to save cloned repo contents.")
			return
		}
	}

	return
}

// resolveSingleNode caches the RPM for a single node.
// It will modify fetchedPackages on a successful package clone.
func resolveSingleNode(cloner *rpmrepocloner.RpmRepoCloner, node *pkggraph.PkgNode, fetchedPackages map[string]bool, outDir string) (err error) {
	const cloneDeps = true
	logger.Log.Debugf("Adding node %s to the cache", node.FriendlyName())

	logger.Log.Debugf("Searching for a package which supplies: %s", node.VersionedPkg.Name)
	// Resolve nodes to exact package names so they can be referenced in the graph.
	resolvedPackages, err := cloner.WhatProvides(node.VersionedPkg)
	if err != nil {
		msg := fmt.Sprintf("Failed to resolve (%s) to a package. Error: %s", node.VersionedPkg, err)
		// It is not an error if an implicit node could not be resolved as it may become available later in the build.
		// If it does not become available scheduler will print an error at the end of the build.
		if node.Implicit {
			logger.Log.Debug(msg)
		} else {
			logger.Log.Error(msg)
		}
		return
	}

	if len(resolvedPackages) == 0 {
		return fmt.Errorf("failed to find any packages providing '%v'", node.VersionedPkg)
	}

	for _, resolvedPackage := range resolvedPackages {
		if !fetchedPackages[resolvedPackage] {
			desiredPackage := &pkgjson.PackageVer{
				Name: resolvedPackage,
			}

			err = cloner.Clone(cloneDeps, desiredPackage)
			if err != nil {
				logger.Log.Errorf("Failed to clone '%s' from RPM repo. Error: %s", resolvedPackage, err)
				return
			}
			fetchedPackages[resolvedPackage] = true

			logger.Log.Debugf("Fetched '%s' as potential candidate.", resolvedPackage)
		}
	}

	err = assignRPMPath(node, outDir, resolvedPackages)
	if err != nil {
		logger.Log.Errorf("Failed to find an RPM to provide '%s'. Error: %s", node.VersionedPkg.Name, err)
		return
	}

	node.State = pkggraph.StateCached

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

		resolvedRPMs, err = rpm.ResolveCompetingPackages(rpmPaths...)
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
	// To calculate the architecture grab the last segment of the resolved name since it will be in the NVRA format.
	rpmArch := rpmPackage[strings.LastIndex(rpmPackage, ".")+1:]
	return filepath.Join(outDir, rpmArch, rpmName)
}
