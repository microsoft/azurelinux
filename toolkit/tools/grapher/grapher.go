// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"
	"os"

	"gonum.org/v1/gonum/graph"
	"gonum.org/v1/gonum/graph/topo"
	"gopkg.in/alecthomas/kingpin.v2"
	"microsoft.com/pkggen/internal/exe"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkggraph"
	"microsoft.com/pkggen/internal/pkgjson"
)

var (
	app    = kingpin.New("grapher", "Dependency graph generation tool")
	input  = exe.InputFlag(app, "Input json listing all local SRPMs")
	output = exe.OutputFlag(app, "Output file to export the graph to")

	logFile          = exe.LogFileFlag(app)
	logLevel         = exe.LogLevelFlag(app)
	strictGoals      = app.Flag("strict-goals", "Don't allow missing goal packages").Bool()
	strictUnresolved = app.Flag("strict-unresolved", "Don't allow missing unresolved packages").Bool()

	depGraph = pkggraph.NewPkgGraph()
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))

	var err error
	logger.InitBestEffort(*logFile, *logLevel)

	localPackages := pkgjson.PackageRepo{}
	err = localPackages.ParsePackageJSON(*input)
	if err != nil {
		logger.Log.Panic(err)
	}

	err = populateGraph(depGraph, &localPackages)
	if err != nil {
		logger.Log.Panic(err)
	}

	err = validateGraph(depGraph)
	if err != nil {
		logger.Log.Panic(err)
	}

	// Add a default "ALL" goal to build everything local
	_, err = depGraph.AddGoalNode("ALL", nil, *strictGoals)
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
	newRunNode, err = g.AddPkgNode(pkgVer, pkggraph.StateUnresolved, pkggraph.TypeRemote, "<NO_SRPM_PATH>", "<NO_SPEC_PATH>", "<NO_SOURCE_PATH>", "<NO_ARCHITECTURE>", "<NO_REPO>")
	if err != nil {
		return
	}

	logger.Log.Infof("Adding unresolved node %s\n", newRunNode.FriendlyName())

	return
}

// addNodesForPackage creates a "Run" and "Build" node for the package described
// in the PackageVer structure. Returns pointers to the build and run Nodes
// created, or an error if one of the nodes could not be created.
func addNodesForPackage(g *pkggraph.PkgGraph, pkgVer *pkgjson.PackageVer, pkg *pkgjson.Package) (newRunNode *pkggraph.PkgNode, newBuildNode *pkggraph.PkgNode, err error) {
	nodes, err := g.FindExactPkgNodeFromPkg(pkgVer)
	if err != nil {
		return
	}
	if nodes != nil {
		logger.Log.Warnf(`Duplicate package name for package %+v read from SRPM "%s" (Previous: %+v)`, pkgVer, pkg.SrpmPath, nodes.RunNode)
		err = nil
		if nodes.RunNode != nil {
			newRunNode = nodes.RunNode
		}
		if nodes.BuildNode != nil {
			newBuildNode = nodes.BuildNode
		}
	}

	if newRunNode == nil {
		// Add "Run" node
		newRunNode, err = g.AddPkgNode(pkgVer, pkggraph.StateMeta, pkggraph.TypeRun, pkg.SrpmPath, pkg.SpecPath, pkg.SourceDir, pkg.Architecture, "<LOCAL>")
		logger.Log.Debugf("Adding run node %s with id %d\n", newRunNode.FriendlyName(), newRunNode.ID())
		if err != nil {
			return
		}
	}

	if newBuildNode == nil {
		// Add "Build" node
		newBuildNode, err = g.AddPkgNode(pkgVer, pkggraph.StateBuild, pkggraph.TypeBuild, pkg.SrpmPath, pkg.SpecPath, pkg.SourceDir, pkg.Architecture, "<LOCAL>")
		logger.Log.Debugf("Adding build node %s with id %d\n", newBuildNode.FriendlyName(), newBuildNode.ID())
		if err != nil {
			return
		}
	}

	// A "run" node has an implicit dependency on its coresponding "build" node, encode that here.
	// SetEdge panics on error, and does not support looping edges.
	newEdge := g.NewEdge(newRunNode, newBuildNode)
	defer func() {
		if r := recover(); r != nil {
			logger.Log.Panicf("Adding edge failed for %+v", pkgVer)
		}
	}()
	g.SetEdge(newEdge)

	return
}

// addSingleDependency will add an edge between packageNode and the "Run" node for the
// dependency described in the PackageVer structure. Returns an error if the
// addition failed.
func addSingleDependency(g *pkggraph.PkgGraph, packageNode *pkggraph.PkgNode, dependency *pkgjson.PackageVer) error {
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

	// SetEdge panics on error, and does not support looping edges.
	newEdge := g.NewEdge(packageNode, dependentNode)
	defer func() {
		if r := recover(); r != nil {
			logger.Log.Errorf("Failed to add edge failed between %+v and %+v", packageNode, dependency)
		}
	}()
	if newEdge.To() == newEdge.From() {
		logger.Log.Warnf("Package %+v requires itself!", packageNode)
	} else {
		g.SetEdge(newEdge)
	}

	return err
}

// addLocalPackage adds the package provided by the Package structure, and
// updates the SRPM path name
func addLocalPackage(g *pkggraph.PkgGraph, pkg *pkgjson.Package) error {
	_, _, err := addNodesForPackage(g, pkg.Provides, pkg)
	return err
}

// addDependencies adds edges for both build and runtime requirements for the
// package described in the Package structure. Returns an error if the edges
// could not be created.
func addPkgDependencies(g *pkggraph.PkgGraph, pkg *pkgjson.Package) (dependenciesAdded int, err error) {
	provide := pkg.Provides
	runDependencies := pkg.Requires
	buildDependencies := pkg.BuildRequires

	// Find the current node in the lookup list.
	logger.Log.Debugf("Adding dependencies for package %s", pkg.SrpmPath)
	nodes, err := g.FindExactPkgNodeFromPkg(provide)
	if err != nil {
		return
	}
	if nodes == nil {
		return dependenciesAdded, fmt.Errorf("can't add dependencies to a missing package %+v", pkg)
	}
	runNode := nodes.RunNode
	buildNode := nodes.BuildNode

	// For each run time and build time dependency, add the edges
	logger.Log.Tracef("Adding run dependencies")
	for _, dependency := range runDependencies {
		err = addSingleDependency(g, runNode, dependency)
		if err != nil {
			logger.Log.Errorf("Unable to add run-time dependencies for %+v", pkg)
			return
		}
		dependenciesAdded++
	}

	logger.Log.Tracef("Adding build dependencies")
	for _, dependency := range buildDependencies {
		err = addSingleDependency(g, buildNode, dependency)
		if err != nil {
			logger.Log.Errorf("Unable to add build-time dependencies for %+v", pkg)
			return
		}
		dependenciesAdded++
	}

	return
}

// populateGraph adds all the data contained in the PackageRepo structure into
// the graph.
func populateGraph(g *pkggraph.PkgGraph, repo *pkgjson.PackageRepo) (err error) {
	packages := repo.Repo

	// Scan and add each package we know about
	logger.Log.Infof("Adding all packages from %s", *input)
	// NOTE: range iterates by value, not reference. Manually access slice
	for idx := range packages {
		pkg := packages[idx]
		err = addLocalPackage(g, pkg)
		if err != nil {
			logger.Log.Errorf("Failed to add local package %+v", pkg)
			return err
		}
	}
	logger.Log.Infof("\tAdded %d packages", len(packages))

	// Rescan and add all the dependencies
	logger.Log.Infof("Adding all dependencies from %s", *input)
	dependenciesAdded := 0
	for idx := range packages {
		pkg := packages[idx]
		num, err := addPkgDependencies(g, pkg)
		if err != nil {
			logger.Log.Errorf("Failed to add dependency %+v", pkg)
			return err
		}
		dependenciesAdded += num
	}
	logger.Log.Infof("\tAdded %d dependencies", dependenciesAdded)

	return err
}

// fixCycle attempts to fix a cycle. Cycles may be acceptable if all nodes are from the same spec file.
// If a cycle can be fixed an additional meta node will be added to represent the interdependencies of the cycle.
func fixCycle(g *pkggraph.PkgGraph, cycle []*pkggraph.PkgNode) (err error) {
	specFile := cycle[0].SrpmPath
	// Omit the first element of the cycle, since it is repeated as the last element
	trimmedCycle := cycle[1:]
	logger.Log.Debugf("Found cycle starting at %s", cycle[0].FriendlyName())

	// For each node, remove any edges which point to other nodes in the cycle, and move any remaining dependencies to a new
	// meta node, then have everything in the cycle depend on the new meta node.
	groupedDependencies := make(map[int64]bool)
	for _, currentNode := range trimmedCycle {
		logger.Log.Tracef("\tCycle node: %s", currentNode.FriendlyName())
		if currentNode.SrpmPath != specFile {
			return fmt.Errorf("cycle contains packages from multiple SPEC files, unresolvable")
		}
		if currentNode.Type == pkggraph.TypeBuild {
			return fmt.Errorf("cycle contains build dependencies, unresolvable")
		}
		// Remove all links to other members of the cycle
		for _, nodeInCycle := range trimmedCycle {
			g.RemoveEdge(currentNode.ID(), nodeInCycle.ID())
		}

		// Record any other dependencies the nodes have (ie, where can we get to from here), then remove them
		fromNodes := graph.NodesOf(g.From(currentNode.ID()))
		for _, from := range fromNodes {
			groupedDependencies[from.ID()] = true
			g.RemoveEdge(currentNode.ID(), from.ID())
		}
	}

	// Convert the IDs back into actual nodes
	dependencyNodes := make([]*pkggraph.PkgNode, 0, len(groupedDependencies))
	for id := range groupedDependencies {
		dependencyNodes = append(dependencyNodes, g.Node(id).(*pkggraph.PkgNode).This)
	}

	g.AddMetaNode(trimmedCycle, dependencyNodes)

	return
}

// validateGraph makes sure the graph is a directed acyclic graph (DAG)
func validateGraph(g *pkggraph.PkgGraph) (err error) {
	cycles := topo.DirectedCyclesIn(g)
	// Try to fix the cycles if we can before reporting them
	if len(cycles) > 0 {
		for _, cycle := range cycles {
			// Convert our list to pkggraph.PkgNodes
			pkgCycle := make([]*pkggraph.PkgNode, 0, len(cycle))
			for _, node := range cycle {
				pkgCycle = append(pkgCycle, node.(*pkggraph.PkgNode).This)
			}
			err = fixCycle(g, pkgCycle)
			if err != nil {
				// Just print the error, still valuable to list all existing cycles.
				logger.Log.Errorf("Failed to resolve dependency cycle: '%s'", err)
			}
		}
	}

	// Make sure the fixups worked, otherwise report the failure
	cycles = topo.DirectedCyclesIn(g)
	if len(cycles) > 0 {
		for idx, cycle := range cycles {
			firstNode := cycle[0].(*pkggraph.PkgNode)
			cycleString := fmt.Sprintf("{%s}", firstNode.FriendlyName())
			for _, node := range cycle[1:] {
				pkgNode := node.(*pkggraph.PkgNode)
				cycleString = fmt.Sprintf("%s --> {%s}", cycleString, pkgNode.FriendlyName())
			}

			logger.Log.Errorf("Unfixable circular dependency found %d:    %s", idx, cycleString)
		}
		err = fmt.Errorf("cycles detected in dependency graph")
	}
	return
}
