// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package depsearch

import (
	"fmt"
	"path/filepath"
	"sort"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"
	"github.com/microsoft/azurelinux/toolkit/tools/scheduler/schedulerutils"

	"gonum.org/v1/gonum/graph"
)

const (
	defaultFilterPath = "./resources/manifests/package/toolchain_x86_64.txt"
	colorReset        = "\033[0m"
	colorRed          = "\033[31m"
)

var (
	reservedFiles map[string]bool
)

type treeNode struct {
	lines []string
}

type treeSearch struct {
	graph *pkggraph.PkgGraph

	// Don't print a node twice, just add '...' instead to save space
	alreadyAdded map[*pkggraph.PkgNode]bool
	// These nodes were caught by the filter and should be marked
	filteredNodes map[*pkggraph.PkgNode]bool
	// These nodes are not in the filter list
	normalNodes map[*pkggraph.PkgNode]bool

	nodesVisited, nodesTotal int
}

func ConfigureFilterFiles(filterFile *string, filter *bool) {
	setDefault := false
	if len(*filterFile) == 0 {
		*filterFile = defaultFilterPath
		setDefault = true
	}
	isFile, err := file.PathExists(*filterFile)
	if err != nil {
		logger.Log.Panicf("Failed to query if filter file (%s) exists: %s", *filterFile, err)
	}

	// If we are just trying to use the default, its fine if its missing.
	if !isFile && setDefault {
		logger.Log.Warnf("Default toolchain filter file (%s) not found, setting to ''", *filterFile)
		*filterFile = ""
	}

	if len(*filterFile) == 0 && *filter {
		logger.Log.Panic("Must pass a --rpm-filter-file to use the filter function, consider './resources/manifests/package/toolchain_x86_64.txt'")
	}
}

func SearchForGoal(graph *pkggraph.PkgGraph, goals []string) (list []*pkggraph.PkgNode) {
	for _, goal := range goals {
		n := graph.FindGoalNode(goal)
		if n != nil {
			list = append(list, n)
		}
	}
	return
}

func SearchForPkg(graph *pkggraph.PkgGraph, packages []string) (list []*pkggraph.PkgNode) {
	for _, n := range graph.AllPreferredRunNodes() {
		nodeName := n.VersionedPkg.Name
		for _, searchName := range packages {
			if nodeName == searchName {
				list = append(list, n)
			}
		}
	}
	return
}

func SearchForSpec(graph *pkggraph.PkgGraph, specs []string) (list []*pkggraph.PkgNode) {
	for _, n := range graph.AllPreferredRunNodes() {
		nodeSpec := n.SpecName()
		for _, searchSpec := range specs {
			if nodeSpec == searchSpec {
				list = append(list, n)
			}
		}
	}
	return
}

func BuildRequiresGraph(graphIn *pkggraph.PkgGraph, nodeList []*pkggraph.PkgNode) (graphOut *pkggraph.PkgGraph, root *pkggraph.PkgNode, err error) {
	// Make a copy of the graph
	newGraph, err := graphIn.DeepCopy()
	if err != nil {
		return
	}

	// Add a goal node to all the things we care about
	root = newGraph.AddMetaNode(nil, nodeList)
	graphOut, err = newGraph.CreateSubGraph(root)
	if err != nil {
		return
	}

	return
}

func BuildDependsOnGraph(graphIn *pkggraph.PkgGraph, nodeList []*pkggraph.PkgNode) (graphOut *pkggraph.PkgGraph, root *pkggraph.PkgNode, err error) {
	// Make a copy of the graph
	reversedGraph, err := graphIn.DeepCopy()
	if err != nil {
		return
	}

	// Then reverse every edge in the graph
	for _, edge := range graph.EdgesOf(reversedGraph.Edges()) {
		reversedGraph.RemoveEdge(edge.From().ID(), edge.To().ID())
		reversedGraph.SetEdge(edge.ReversedEdge())
	}

	// Add a goal node to all the things we care about
	root = reversedGraph.AddMetaNode(nil, nodeList)
	graphOut, err = reversedGraph.CreateSubGraph(root)
	if err != nil {
		return
	}

	return
}

func formatNode(n *pkggraph.PkgNode, verbosity int) string {
	switch verbosity {
	case 1:
		return n.SpecName()
	case 2:
		return filepath.Base(n.RpmPath)
	case 3:
		return fmt.Sprintf("'%s' from node '%s'", filepath.Base(n.RpmPath), n.FriendlyName())
	case 4:
		return fmt.Sprintf("(%v)'%#v'", n.VersionedPkg, *n)
	default:
		logger.Log.Fatalf("Invalid verbosity level %v", verbosity)
	}
	return ""
}

func isFilteredFile(path, filterFile string) bool {
	if len(filterFile) > 0 {
		if len(reservedFiles) == 0 {
			reservedFileList, err := schedulerutils.ReadReservedFilesList(filterFile)
			if err != nil {
				logger.Log.Fatalf("Failed to load filter file (%s): %s", filterFile, err)
			}
			reservedFiles = sliceutils.SliceToSet[string](reservedFileList)
		}
		base := filepath.Base(path)

		return len(path) > 0 && reservedFiles[base]
	} else {
		return false
	}
}

func createSearch(g *pkggraph.PkgGraph, root *pkggraph.PkgNode) (t *treeSearch, err error) {
	newSearch := &treeSearch{
		graph:         g,
		alreadyAdded:  make(map[*pkggraph.PkgNode]bool),
		filteredNodes: make(map[*pkggraph.PkgNode]bool),
		normalNodes:   make(map[*pkggraph.PkgNode]bool),
		nodesVisited:  0,
	}

	//Calculate the number of nodes we might visit:
	subGraph, err := g.CreateSubGraph(root)
	if err != nil {
		logger.Log.Fatalf("Failed to calculate number of nodes: %s", err)
	}

	//This is the worst case possible number of searche to make
	possibleEdges := subGraph.Edges().Len() * subGraph.Nodes().Len()
	newSearch.nodesTotal = possibleEdges

	return newSearch, nil
}

func (t *treeSearch) FilteredNodes() (nodes []*pkggraph.PkgNode) {
	nodes = []*pkggraph.PkgNode{}
	for n := range t.filteredNodes {
		nodes = append(nodes, n)
	}
	return nodes
}

func (t *treeSearch) NonFilteredNodes() (nodes []*pkggraph.PkgNode) {
	nodes = []*pkggraph.PkgNode{}
	for n := range t.normalNodes {
		nodes = append(nodes, n)
	}
	return nodes
}

// Call this ever time a node is processed, will print an update ever 100 nodes
func (t *treeSearch) printProgress() {
	if t.nodesVisited%10000 == 0 {
		logger.Log.Infof("Scanned %d nodes", t.nodesVisited)
	}
	t.nodesVisited++
}

// Run a DFS and generate a string representation of the tree. Optionally ignore all branches that only container nodes in
//
//	the filter list (ie given the toolchain manifest, only print those branches which container non-toolchain packages)
func (t *treeSearch) treeNodeToString(n *pkggraph.PkgNode, depth, maxDepth int, filter bool, filterFile string, verbosity int, generateStrings, printDuplicates bool, runtimeFilterLevel int) (lines []string, hasNonToolchain bool) {
	t.printProgress()
	// We only care about run nodes for the purposes of detecting toolchain files
	hasNonToolchain = n.Type == pkggraph.TypeLocalBuild && !isFilteredFile(n.RpmPath, filterFile)

	if !printDuplicates && t.alreadyAdded[n] {
		return []string{}, false
	} else {
		t.alreadyAdded[n] = true
	}

	thisNode := formatNode(n, verbosity)
	if isFilteredFile(n.RpmPath, filterFile) {
		// Highlight nodes that are in the filter file list in red, and add them to the list
		if generateStrings {
			lines = append(lines, "__"+colorRed+thisNode+colorReset)
		}
		if n.Type == pkggraph.TypeLocalRun {
			// We only want to record run nodes for the purposes of listing packages in non-tree mode
			t.filteredNodes[n] = true
		}
	} else {
		// Non filtered files print normally
		if generateStrings {
			lines = append(lines, "__"+thisNode)
		}
		if n.Type == pkggraph.TypeLocalRun {
			// We only want to record run nodes for the purposes of listing packages in non-tree mode
			t.normalNodes[n] = true
		}
	}

	var childrenTreeNodes []treeNode
	nodes := t.graph.From(n.ID())
	// Bail out early if we exceed max depth, maxDepth of -1 means no limit.
	if depth < maxDepth || maxDepth == -1 {
		var (
			childLines                  []string
			childHasMissingToolchainPkg = false
			haveDuplicatedEntry         = false
		)
		for nodes.Next() {
			child := nodes.Node().(*pkggraph.PkgNode)

			// If we are only looking for runtime, skip build nodes (except for the root nodes: goal + each package node we care about)
			if runtimeFilterLevel != -1 && depth > runtimeFilterLevel && child.Type == pkggraph.TypeLocalBuild {
				continue
			}
			childLines, childHasMissingToolchainPkg = t.treeNodeToString(child, depth+1, maxDepth, filter, filterFile, verbosity, generateStrings, printDuplicates, runtimeFilterLevel)
			hasNonToolchain = hasNonToolchain || childHasMissingToolchainPkg

			// A child will return an empty string list if it, and all its children, are either duplicates or have been filtered out
			if len(childLines) > 0 {
				tn := treeNode{lines: childLines}
				childrenTreeNodes = append(childrenTreeNodes, tn)
			} else {
				haveDuplicatedEntry = true
			}
		}

		// If we have duplicated entires (ie empty strings), and we aren't removing all non-filtered entries, represent them with a '...'
		//  as the last entry instead of the node name.
		if haveDuplicatedEntry && !filter {
			childrenTreeNodes = append(childrenTreeNodes, treeNode{lines: []string{"..."}})
		}

		if len(childrenTreeNodes) > 0 && generateStrings {
			firstN := childrenTreeNodes[:len(childrenTreeNodes)-1]
			last := childrenTreeNodes[len(childrenTreeNodes)-1]
			for _, tn := range firstN {
				for _, l := range tn.lines {
					lines = append(lines, "   |"+l)
				}
			}
			lines = append(lines, "   |"+last.lines[0])
			for _, l := range last.lines[1:] {
				lines = append(lines, "   "+l)
			}
		}
	} else {
		lines = append(lines, "   |-->")
		// We are bailing out early, we don't know if this should be filtered, assume the worst
		hasNonToolchain = true
	}

	if !hasNonToolchain && filter && depth > 0 {
		return []string{}, false
	}

	return lines, hasNonToolchain
}

func PrintSpecs(graph *pkggraph.PkgGraph, tree, filter bool, filterFile string, printDuplicates bool, verbosity, maxDepth, runtimeFilterLevel int, root *pkggraph.PkgNode) {
	t, err := createSearch(graph, root)
	if err != nil {
		logger.Log.Fatalf("Failed to start search: %s", err)
	}
	// May as well use the tree searh to parse all the filtered packages etc, even if we are
	//    just printing a list
	lines, _ := t.treeNodeToString(root, 0, maxDepth, filter, filterFile, verbosity, tree, printDuplicates, runtimeFilterLevel)
	if tree {
		for _, l := range lines {
			fmt.Println(l)
		}
	} else {
		results := make(map[string]bool)
		if !filter {
			// Only include toolchain packages if we aren't trying to find packages that have
			// infiltrated the toolchain
			for _, n := range t.FilteredNodes() {
				results[formatNode(n, verbosity)] = true
			}
		}
		// Always include normal nodes
		for _, n := range t.NonFilteredNodes() {
			results[formatNode(n, verbosity)] = true
		}

		// Contert to list and sort
		printLines := sliceutils.SetToSlice[string](results)
		sort.Strings(printLines)
		for _, l := range printLines {
			fmt.Println(l)
		}
	}
}
