// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"
	"os"
	"strings"

	"gonum.org/v1/gonum/graph"
	"gopkg.in/alecthomas/kingpin.v2"
	"microsoft.com/pkggen/internal/exe"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/packagerepo/repocloner/rpmrepocloner"
	"microsoft.com/pkggen/internal/packagerepo/repoutils"
	"microsoft.com/pkggen/internal/pkggraph"
	"microsoft.com/pkggen/internal/pkgjson"
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
	useUpdateRepo        = app.Flag("use-update-repo", "Pull packages from the upstream update repo").Bool()
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
	err = cloner.Initialize(*outDir, *tmpDir, *workertar, *existingRpmDir, *useUpdateRepo, *usePreviewRepo, *repoFiles)
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
		for _, n := range dependencyGraph.AllRunNodes() {
			if n.State == pkggraph.StateUnresolved {
				err = resolveSingleNode(cloner, n)
				if err != nil {
					errorMessage := strings.Builder{}
					errorMessage.WriteString(fmt.Sprintf("Failed to resolve all nodes in the graph while resolving '%s'\n", n))
					errorMessage.WriteString("Nodes which have this as a dependency:\n")
					for _, dependant := range graph.NodesOf(dependencyGraph.To(n.ID())) {
						errorMessage.WriteString(fmt.Sprintf("\t'%s' depends on '%s'\n", dependant.(*pkggraph.PkgNode), n))
					}
					logger.Log.Error(errorMessage.String())
					return
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

// resolveSingleNode caches the RPM for a single node
func resolveSingleNode(cloner *rpmrepocloner.RpmRepoCloner, node *pkggraph.PkgNode) (err error) {
	const cloneDeps = true

	desiredPackage := node.VersionedPkg
	desiredPackageList := []*pkgjson.PackageVer{desiredPackage}

	logger.Log.Debugf("Adding node %s to the cache", node.FriendlyName())
	// Some unresolved nodes are virtual file requirements (such as /usr/sbin/groupadd from shadow-utils).
	// The spec file may not explicitly provide it, so we need to try finding a package which supplies the file.
	if strings.HasPrefix(node.VersionedPkg.Name, "/") {
		logger.Log.Debugf("Searching for a package which supplies %s", node.VersionedPkg.Name)
		err = cloner.SearchAndClone(cloneDeps, desiredPackage)
	} else {
		err = cloner.Clone(cloneDeps, desiredPackageList...)
	}
	if err != nil {
		logger.Log.Errorf("Failed to clone %s from RPM repo. Error: %s", node, err)
	} else {
		node.State = pkggraph.StateCached
	}
	return
}
