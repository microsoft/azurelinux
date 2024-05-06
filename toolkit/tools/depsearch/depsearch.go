// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"
	"os"
	"path/filepath"
	"sort"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/exe"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/depsearch"
	"github.com/microsoft/azurelinux/toolkit/tools/scheduler/schedulerutils"

	"gonum.org/v1/gonum/graph"
	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app = kingpin.New("depsearch", "Returns a list of everything that depends on a given package or spec")

	inputGraphFile  = exe.InputFlag(app, "Path to the DOT graph file to search.")
	outputGraphFile = app.Flag("output", "Path to save the graph.").String()

	pkgsToSearch  = app.Flag("packages", "Space seperated list of packages to search from.").String()
	specsToSearch = app.Flag("specs", "Space seperated list of specfiles to search from.").String()
	goalsToSearch = app.Flag("goals", "Space seperated list of goal names to search (Try 'ALL' or 'PackagesToBuild').").String()

	reverseSearch      = app.Flag("reverse", "Reverse the search to give a traditional dependency list for the packages instead of dependants.").Bool()
	runtimeFilterLevel = app.Flag("runtime-filter-level", "Only consider only runtime dependencies beyond this layer of the graph. -1 to disable filter, 0 for no build nodes, 1 for searched nodes' build nodes, etc.").Default("-1").Int()

	printTree       = app.Flag("tree", "Print output as a simple tree instead of a list").Bool()
	verbosity       = app.Flag("verbosity", "Print the full node details (4), limited details (3), RPM (2), or SPEC name (1) for each result").Default("1").Int()
	maxDepth        = app.Flag("max-depth", "Maximum depth into the tree to scan, -1 for unlimited").Default("-1").Int()
	printDuplicates = app.Flag("print-duplicates", "In tree mode, if there is a duplicate node in the tree don't replace it with '...'").Bool()
	filterFile      = app.Flag("rpm-filter-file", "Filter the returned packages based on this list of *.rpm filenames (defaults to the x86_64 toolchain manifest './resources/manifests/package/toolchain_x86_64.txt' if it exists)").ExistingFile()
	filter          = app.Flag("rpm-filter", "Only print any packages that are missing from the rpm-filter-file (useful for debugging toolchain package issues for example)").Bool()

	logFlags = exe.SetupLogFlags(app)
)

func main() {
	var (
		outputGraph *pkggraph.PkgGraph
		root        *pkggraph.PkgNode
	)

	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(logFlags)

	// only understand verbosity from 1 - 4 (spec, rpm, details, full node)
	if verbosity == nil || *verbosity > 4 || *verbosity < 1 {
		verbosity = new(int)
		*verbosity = 1
	}

	if !(*maxDepth == -1 || *maxDepth >= 1) {
		logger.Log.Fatalf("Invalid max depth %d, valid ranges are -1, >=1", *maxDepth)
	}

	// Only one of runtimeOnlyPlusBuild or runtimeOnly can be set
	if *runtimeFilterLevel < -1 {
		logger.Log.Fatalf("Invalid runtime filter level '%d', valid ranges are -1, >=0", *runtimeFilterLevel)
	}

	// We can color the entries when using --tree, or limit the output in all modes with --rpm-filter
	depsearch.ConfigureFilterFiles(filterFile, filter)
	if len(*filterFile) > 0 && (*filter || *printTree) {
		logger.Log.Infof("Applying package filter from (%s)", *filterFile)
	} else {
		logger.Log.Infof("Filter file (%s) not applicable here", *filterFile)
	}

	pkgSearchList := exe.ParseListArgument(*pkgsToSearch)
	specSearchList := exe.ParseListArgument(*specsToSearch)
	goalSearchList := exe.ParseListArgument(*goalsToSearch)

	graph, err := pkggraph.ReadDOTGraphFile(*inputGraphFile)
	if err != nil {
		logger.Log.Panicf("Failed to read DOT graph with error: %s", err)
	}

	// Generate a list of nodes to search from
	nodeListPkg := depsearch.SearchForPkg(graph, pkgSearchList)
	nodeListSpec := depsearch.SearchForSpec(graph, specSearchList)
	nodeListGoal := depsearch.SearchForGoal(graph, goalSearchList)

	nodeLists := append(nodeListPkg, append(nodeListSpec, nodeListGoal...)...)
	nodeSet := sliceutils.RemoveDuplicatesFromSlice(nodeLists)

	if len(nodeSet) == 0 {
		logger.Log.Panicf("Could not find any nodes matching pkgs:[%s] or specs:[%s] or goals[%s]", *pkgsToSearch, *specsToSearch, *goalsToSearch)
	} else {
		logger.Log.Infof("Found %d nodes to consider", len(nodeSet))
	}

	if *reverseSearch {
		logger.Log.Infof("Reversed search will list all the dependencies of the provided packages")
		outputGraph, root, err = depsearch.BuildRequiresGraph(graph, nodeSet)
	} else {
		logger.Log.Infof("Forward search will list all dependants which rely on any of the provided packages")
		outputGraph, root, err = depsearch.BuildDependsOnGraph(graph, nodeSet)
	}

	if err != nil {
		logger.Log.Panicf("Failed to generate graph to run depsearch on: %s", err)
	}

	depsearch.PrintSpecs(outputGraph, *printTree, *filter, *filterFile, *printDuplicates, *verbosity, *maxDepth, *runtimeFilterLevel, root)

	if len(*outputGraphFile) > 0 {
		pkggraph.WriteDOTGraphFile(outputGraph, *outputGraphFile)
	}
}
