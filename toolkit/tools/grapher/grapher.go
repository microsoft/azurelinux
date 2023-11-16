// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"
	"os"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repocloner/rpmrepocloner"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/profile"

	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app    = kingpin.New("grapher", "Dependency graph generation tool")
	input  = exe.InputFlag(app, "Input json listing all local SRPMs")
	output = exe.OutputFlag(app, "Output file to export the graph to")

	logFlags              = exe.SetupLogFlags(app)
	profFlags             = exe.SetupProfileFlags(app)
	strictGoals           = app.Flag("strict-goals", "Don't allow missing goal packages").Bool()
	strictUnresolved      = app.Flag("strict-unresolved", "Don't allow missing unresolved packages").Bool()
	timestampFile         = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()
	usePMCtoResolveCycles = app.Flag("usePMCtoresolvecycles", "Cycles will be resolved by downloading rpm packages from PMC if locally unavailable").Bool()
	tlsClientCert         = app.Flag("tls-cert", "TLS client certificate to use when downloading files.").String()
	tlsClientKey          = app.Flag("tls-key", "TLS client key to use when downloading files.").String()

	resolveCyclesFromUpstream     = app.Flag("resolve-cycles-from-upstream", "Let grapher resolve cycles by marking rpms available in repo as remote").Bool()
	outDir                        = exe.OutputDirFlag(app, "Directory to download packages into.")
	existingRpmsDir               = app.Flag("rpm-dir", "Directory that contains already built RPMs. Should contain top level directories for architecture.").Required().ExistingDir()
	existingToolchainRpmDir       = app.Flag("toolchain-rpms-dir", "Directory that contains already built toolchain RPMs. Should contain top level directories for architecture.").Required().ExistingDir()
	tmpDir                        = app.Flag("tmp-dir", "Directory to store temporary files while downloading.").String()
	workerTar                     = app.Flag("tdnf-worker", "Full path to worker_chroot.tar.gz").Required().ExistingFile()
	repoFiles                     = app.Flag("repo-file", "Full path to a repo file").Required().ExistingFiles()
	usePreviewRepo                = app.Flag("use-preview-repo", "Pull packages from the upstream preview repo").Bool()
	disableDefaultRepos           = app.Flag("disable-default-repos", "Disable pulling packages from PMC repos").Bool()
	ignoreVersionToResolveSelfDep = app.Flag("ignore-version-to-resolve-selfdep", "Ignore package version while downloading package from upstream when resolving cycle").Bool()

	depGraph = pkggraph.NewPkgGraph()
)

func main() {
	const goalNodeName = "ALL"

	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(logFlags)

	prof, err := profile.StartProfiling(profFlags)
	if err != nil {
		logger.Log.Warnf("Could not start profiling: %s", err)
	}
	defer prof.StopProfiler()

	timestamp.BeginTiming("grapher", *timestampFile)
	defer timestamp.CompleteTiming()

	localPackages := pkgjson.PackageRepo{}
	err = localPackages.ParsePackageJSON(*input)
	if err != nil {
		logger.Log.Panic(err)
	}

	depGraph := pkggraph.NewPkgGraph()
	err = populateGraph(depGraph, &localPackages)
	if err != nil {
		logger.Log.Panic(err)
	}

	// Add a default "ALL" goal to build everything local
	_, err = depGraph.AddGoalNode(goalNodeName, nil, nil, *strictGoals)
	if err != nil {
		logger.Log.Panic(err)
	}

	var cloner *rpmrepocloner.RpmRepoCloner = nil
	if *resolveCyclesFromUpstream {
		cloner, err = rpmrepocloner.ConstructCloner(*outDir, *tmpDir, *workerTar, *existingRpmsDir, *existingToolchainRpmDir, *tlsClientCert, *tlsClientKey, *repoFiles)
		if err != nil {
			logger.Log.Panic(err)
		}
		enabledRepos := rpmrepocloner.RepoFlagAll
		if !*usePreviewRepo {
			enabledRepos = enabledRepos & ^rpmrepocloner.RepoFlagPreview
		}
		if *disableDefaultRepos {
			enabledRepos = enabledRepos & ^rpmrepocloner.RepoFlagMarinerDefaults
		}
		cloner.SetEnabledRepos(enabledRepos)

		defer cloner.Close()
	}
	logger.Log.Info("Running cycle resolution to fix any cycles in the dependency graph")
	err = depGraph.MakeDAGUsingUpstreamRepos(*resolveCyclesFromUpstream, *ignoreVersionToResolveSelfDep, cloner)
	if err != nil {
		logger.Log.Panic(err)
	}

	err = pkggraph.WriteDOTGraphFile(depGraph, *output)
	if err != nil {
		logger.Log.Panic(err)
	}

	logger.Log.Info("Finished generating graph.")
}

// addUnresolvedPackage adds an unresolved node to the graph representing the
// packged described in the PackgetVer structure. Returns an error if the node
// could not be created.
func addUnresolvedPackage(g *pkggraph.PkgGraph, pkgVer *pkgjson.PackageVer) (newRunNode *pkggraph.PkgNode, err error) {
	logger.Log.Debugf("Adding unresolved %s", pkgVer)
	if *strictUnresolved {
		err = fmt.Errorf("strict-unresolved does not allow unresolved packages, attempting to add %s", pkgVer)
		return
	}

	nodes, err := g.FindBestPkgNode(pkgVer)
	if err != nil {
		return
	}
	if nodes != nil {
		err = fmt.Errorf(`attempted to mark a local package "%+v" as unresolved`, pkgVer)
		return
	}

	// Create a new node
	newRunNode, err = g.AddRemoteUnresolvedNode(pkgVer)
	if err != nil {
		return
	}

	logger.Log.Infof("Adding unresolved node '%s'.", newRunNode.FriendlyName())

	return
}

// addNodesForPackage creates a "Run", "Build", and "Test" node for the package described
// in the Package structure. Returns pointers to the build and run Nodes
// created, or an error if one of the nodes could not be created.
func addNodesForPackage(g *pkggraph.PkgGraph, pkg *pkgjson.Package) (foundDuplicate bool, err error) {
	var (
		newRunNode   *pkggraph.PkgNode
		newBuildNode *pkggraph.PkgNode
		newTestNode  *pkggraph.PkgNode
	)

	nodes, err := g.FindExactPkgNodeFromPkg(pkg.Provides)
	if err != nil {
		return
	}

	if nodes != nil {
		logger.Log.Warnf(`Skipping duplicate package name for package %+v read from SRPM "%s". Original: %+v.`, pkg.Provides, pkg.SrpmPath, nodes.RunNode)
		foundDuplicate = true
		return
	}

	newRunNode, err = g.AddPkgNode(pkg.Provides, pkggraph.StateMeta, pkggraph.TypeLocalRun, pkg.SrpmPath, pkg.RpmPath, pkg.SpecPath, pkg.SourceDir, pkg.Architecture, pkggraph.LocalRepo)
	if err != nil {
		return
	}
	logger.Log.Debugf("Adding run node '%s' with id %d.", newRunNode.FriendlyName(), newRunNode.ID())

	newBuildNode, err = g.AddPkgNode(pkg.Provides, pkggraph.StateBuild, pkggraph.TypeLocalBuild, pkg.SrpmPath, pkg.RpmPath, pkg.SpecPath, pkg.SourceDir, pkg.Architecture, pkggraph.LocalRepo)
	if err != nil {
		return
	}
	logger.Log.Debugf("Adding build node '%s' with id %d.", newBuildNode.FriendlyName(), newBuildNode.ID())

	// A "run" node has an implicit dependency on its corresponding "build" node, encode that here.
	err = g.AddEdge(newRunNode, newBuildNode)
	if err != nil {
		logger.Log.Errorf("Adding run -> build edge failed for %+v", pkg.Provides)
		return
	}

	if !pkg.RunTests {
		logger.Log.Debugf("Skipping adding a test node for package %+v", pkg)
		return
	}

	newTestNode, err = g.AddPkgNode(pkg.Provides, pkggraph.StateBuild, pkggraph.TypeTest, pkg.SrpmPath, pkggraph.NoRPMPath, pkg.SpecPath, pkg.SourceDir, pkg.Architecture, pkggraph.LocalRepo)
	if err != nil {
		return
	}
	logger.Log.Debugf("Adding test node '%s' with id %d.", newTestNode.FriendlyName(), newTestNode.ID())

	// A "test" node has a dependency on its corresponding "build" node. This dependency is required
	// to guarantee we will first check if the build node needs to be built or not before we make
	// any decisions about running the tests.
	err = g.AddEdge(newTestNode, newBuildNode)
	if err != nil {
		logger.Log.Errorf("Adding test -> build edge failed for %+v", pkg.Provides)
		return
	}

	return
}

// addSingleDependency will add an edge between packageNode and the "Run" node for the
// dependency described in the PackageVer structure. Returns an error if the
// addition failed.
func addSingleDependency(g *pkggraph.PkgGraph, packageNode *pkggraph.PkgNode, dependency *pkgjson.PackageVer) (err error) {
	var dependentNode *pkggraph.PkgNode
	logger.Log.Tracef("Adding a dependency from %+v to %+v", packageNode.VersionedPkg, dependency)
	nodes, err := g.FindBestPkgNode(dependency)
	if err != nil {
		logger.Log.Errorf("Unable to check lookup list for %+v (%s)", dependency, err)
		return err
	}

	if nodes == nil {
		dependentNode, err = addUnresolvedPackage(g, dependency)
		if err != nil {
			logger.Log.Errorf(`Could not add a package "%s"`, dependency.Name)
			return err
		}
	} else {
		// All dependencies are assumed to be "Run" dependencies
		dependentNode = nodes.RunNode
	}

	if packageNode == dependentNode {
		logger.Log.Debugf("Package %+v requires itself!", packageNode)
		return nil
	}

	// Avoid creating runtime dependencies from an RPM to a different provide from the same RPM as the dependency will always be met on RPM installation.
	// Creating these edges may cause non-problematic cycles that can significantly increase memory usage and runtime during cycle resolution.
	// If there are enough of these cycles it can exhaust the system's memory when resolving them.
	// - Only check run nodes. If a build node has a reflexive cycle then it cannot be built without a bootstrap version.
	if packageNode.Type == pkggraph.TypeLocalRun &&
		dependentNode.Type == pkggraph.TypeLocalRun &&
		packageNode.RpmPath == dependentNode.RpmPath {

		logger.Log.Debugf("%+v requires %+v which is provided by the same RPM.", packageNode, dependentNode)
		return nil
	}

	err = g.AddEdge(packageNode, dependentNode)
	if err != nil {
		logger.Log.Errorf("Failed to add edge failed between %+v and %+v.", packageNode, dependency)
	}

	return err
}

// addDependencies adds edges for run-, build-, and test-time requirements for the
// package described in the Package structure. Returns an error if the edges
// could not be created.
func addPkgDependencies(g *pkggraph.PkgGraph, pkg *pkgjson.Package) (dependenciesAdded int, err error) {
	// Find the current node in the lookup list.
	logger.Log.Debugf("Adding dependencies for package %s", pkg.SrpmPath)
	nodes, err := g.FindExactPkgNodeFromPkg(pkg.Provides)
	if err != nil {
		return
	}
	if nodes == nil {
		return dependenciesAdded, fmt.Errorf("can't add dependencies to a missing package %+v", pkg)
	}

	// For each run-, build-, and test-time dependency, add the edges
	logger.Log.Tracef("Adding run dependencies")
	for _, dependency := range pkg.Requires {
		err = addSingleDependency(g, nodes.RunNode, dependency)
		if err != nil {
			logger.Log.Errorf("Unable to add run-time dependencies for %+v", pkg)
			return
		}
		dependenciesAdded++
	}

	logger.Log.Tracef("Adding build dependencies")
	for _, dependency := range pkg.BuildRequires {
		err = addSingleDependency(g, nodes.BuildNode, dependency)
		if err != nil {
			logger.Log.Errorf("Unable to add build-time dependencies for %+v", pkg)
			return
		}
		dependenciesAdded++
	}

	if nodes.TestNode == nil {
		logger.Log.Debugf("No test node for package %+v, skipping test dependencies", pkg)
		return
	}

	logger.Log.Tracef("Adding test dependencies")
	for _, dependency := range pkg.TestRequires {
		err = addSingleDependency(g, nodes.TestNode, dependency)
		if err != nil {
			logger.Log.Errorf("Unable to add test-time dependencies for %+v", pkg)
			return
		}
		dependenciesAdded++
	}

	return
}

// populateGraph adds all the data contained in the PackageRepo structure into
// the graph.
func populateGraph(graph *pkggraph.PkgGraph, repo *pkgjson.PackageRepo) (err error) {
	timestamp.StartEvent("populating graph", nil)
	defer timestamp.StopEvent(nil)

	packages := repo.Repo

	timestamp.StartEvent("add package node", nil)

	// Scan and add each package we know about
	logger.Log.Infof("Adding all packages from %s", *input)
	uniquePackages := make(map[*pkgjson.Package]bool)
	for _, pkg := range packages {
		foundDuplicate, err := addNodesForPackage(graph, pkg)
		if err != nil {
			logger.Log.Errorf("Failed to add local package %+v", pkg)
			return err
		}

		if !foundDuplicate {
			uniquePackages[pkg] = true
		}
	}
	logger.Log.Infof("\tAdded %d packages", len(packages))

	timestamp.StopEvent(nil) // add package nodes
	timestamp.StartEvent("add dependencies", nil)

	// Rescan and add all the dependencies
	logger.Log.Infof("Adding all dependencies from %s", *input)
	dependenciesAdded := 0
	for uniquePkg := range uniquePackages {
		num, err := addPkgDependencies(graph, uniquePkg)
		if err != nil {
			logger.Log.Errorf("Failed to add dependency %+v", uniquePkg)
			return err
		}
		dependenciesAdded += num
	}
	logger.Log.Infof("\tAdded %d dependencies", dependenciesAdded)

	timestamp.StopEvent(nil) // add dependencies

	return err
}
