// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/sliceutils"

	"gonum.org/v1/gonum/graph"
	graphpath "gonum.org/v1/gonum/graph/path"
	"gonum.org/v1/gonum/graph/traverse"
	"gopkg.in/alecthomas/kingpin.v2"
)

const (
	defaultMaxResults = "10"
)

// mapPair represents a key/value pair in a map[string][]string.
// What the key and value represent are defined by the functions that use this.
type mapPair struct {
	key   string
	value []string
}

var (
	app            = kingpin.New("graphanalytics", "A tool to print analytics of a given dependency graph.")
	inputGraphFile = exe.InputFlag(app, "Path to the DOT graph file to analyze.")
	maxResults     = app.Flag("max-results", "The number of results to print per category. Set 0 to print unlimited.").Default(defaultMaxResults).Int()
	logFlags       = exe.SetupLogFlags(app)
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))

	logger.InitBestEffort(logFlags)

	err := analyzeGraph(*inputGraphFile, *maxResults)
	if err != nil {
		logger.Log.Fatalf("Unable to analyze dependency graph, error: %s", err)
	}
}

// analyzeGraph analyzes and prints various attributes of a graph file.
func analyzeGraph(inputFile string, maxResults int) (err error) {
	pkgGraph, err := pkggraph.ReadDOTGraphFile(inputFile)
	if err != nil {
		return
	}

	printDirectlyMostUnresolved(pkgGraph, maxResults)
	printDirectlyClosestToBeingUnblocked(pkgGraph, maxResults)

	printIndirectlyMostUnresolved(pkgGraph, maxResults)
	printIndirectlyClosestToBeingUnblocked(pkgGraph, maxResults)

	return
}

// printIndirectlyMostUnresolved will print the top unresolved packages that are indirectly most blocking.
func printIndirectlyMostUnresolved(pkgGraph *pkggraph.PkgGraph, maxResults int) {
	unresolvedPackageDependents := make(map[string][]string)

	for _, node := range pkgGraph.AllNodes() {
		if node.Type != pkggraph.TypeLocalRun &&
			node.Type != pkggraph.TypeLocalBuild &&
			node.Type != pkggraph.TypeTest {
			continue
		}

		// Traverse each package (not unresolved or failed) to find all unresolved nodes that are blocking it.
		if node.State == pkggraph.StateUnresolved || node.State == pkggraph.StateBuildError {
			continue
		}

		dependentName := nodeDependencyName(node)

		search := traverse.BreadthFirst{}
		search.Walk(pkgGraph, node, func(n graph.Node, d int) (stopSearch bool) {
			dependencyNode := n.(*pkggraph.PkgNode)

			if dependencyNode.State == pkggraph.StateUnresolved {
				unresolvedPkgName := dependencyNode.VersionedPkg.Name
				insertIfMissing(unresolvedPackageDependents, unresolvedPkgName, dependentName)
			}

			return
		})
	}

	printTitle("[INDIRECT] Most common unresolved dependencies")
	printMap(unresolvedPackageDependents, "total dependents", maxResults)
}

// printDirectlyMostUnresolved will print the top unresolved packages that are directly most blocking.
func printDirectlyMostUnresolved(pkgGraph *pkggraph.PkgGraph, maxResults int) {
	unresolvedPackageDependents := make(map[string][]string)

	for _, node := range pkgGraph.AllRunNodes() {
		if node.State != pkggraph.StateUnresolved {
			continue
		}

		pkgName := node.VersionedPkg.Name

		dependents := pkgGraph.To(node.ID())
		for dependents.Next() {
			dependent := dependents.Node().(*pkggraph.PkgNode)

			// Do not consider goal nodes
			if dependent.Type == pkggraph.TypeGoal {
				continue
			}

			dependentName := nodeDependencyName(dependent)
			insertIfMissing(unresolvedPackageDependents, pkgName, dependentName)
		}
	}

	printTitle("[DIRECT] Most common unresolved dependencies")
	printMap(unresolvedPackageDependents, "direct dependents", maxResults)
}

// printDirectlyClosestToBeingUnblocked will print the packages with the fewest unresolved direct build requires.
func printDirectlyClosestToBeingUnblocked(pkgGraph *pkggraph.PkgGraph, maxResults int) {
	srpmsBlockedBy := make(map[string][]string)

	for _, node := range pkgGraph.AllNodes() {
		if node.Type != pkggraph.TypeLocalBuild {
			continue
		}

		if node.State == pkggraph.StateUnresolved {
			continue
		}

		pkgSRPM := node.SRPMFileName()

		dependencies := pkgGraph.From(node.ID())
		for dependencies.Next() {
			dependency := dependencies.Node().(*pkggraph.PkgNode)

			// Only consider blocking nodes.
			if dependency.State != pkggraph.StateBuild &&
				dependency.State != pkggraph.StateBuildError &&
				dependency.State != pkggraph.StateUnresolved {
				continue
			}

			// Skip requirements that come from the same srpm.
			dependencySRPM := dependency.SRPMFileName()
			if pkgSRPM == dependencySRPM {
				continue
			}

			dependencyName := nodeDependencyName(dependency)
			insertIfMissing(srpmsBlockedBy, pkgSRPM, dependencyName)
		}
	}

	printTitle("[DIRECT] SRPMs closest to being ready to build")
	printReversedMap(srpmsBlockedBy, "unmet dependencies", maxResults)
}

// printDirectlyClosestToBeingUnblocked will print the packages with the fewest unresolved indrect build requires.
func printIndirectlyClosestToBeingUnblocked(pkgGraph *pkggraph.PkgGraph, maxResults int) {
	srpmsBlockedByPaths := make(map[string][][]graph.Node)

	for _, node := range pkgGraph.AllNodes() {
		if node.Type != pkggraph.TypeLocalBuild {
			continue
		}

		if node.State == pkggraph.StateUnresolved {
			continue
		}

		pkgSRPM := node.SRPMFileName()

		search := traverse.BreadthFirst{}
		search.Walk(pkgGraph, node, func(n graph.Node, d int) (stopSearch bool) {
			dependency := n.(*pkggraph.PkgNode)

			// Only consider unresolved or failed build nodes.
			if dependency.State != pkggraph.StateUnresolved && dependency.State != pkggraph.StateBuildError {
				return
			}

			// Skip requirements that come from the same srpm.
			dependencySRPM := dependency.SRPMFileName()
			if pkgSRPM == dependencySRPM {
				return
			}

			// Find the path from the blocked node to its blocker.
			dependencyPath, _ := graphpath.AStar(node, dependency, pkgGraph, graphpath.NullHeuristic)
			dependencyPathNodes, _ := dependencyPath.To(dependency.ID())

			insertIfMissingLastPathNode(srpmsBlockedByPaths, pkgSRPM, dependencyPathNodes)

			return
		})

	}

	srpmsBlockedByExpanded := make(map[string][]string)
	for pkgSRPM, dependencies := range srpmsBlockedByPaths {
		for _, dependencyPathNodes := range dependencies {
			// Skip the first node containing the origin.
			nodesPath := convertNodePathToStringPath(dependencyPathNodes[1:])

			srpmsBlockedByExpanded[pkgSRPM] = append(srpmsBlockedByExpanded[pkgSRPM], nodesPath)
		}
	}

	printTitle("[INDIRECT] SRPMs closest to being ready to build")
	printReversedMap(srpmsBlockedByExpanded, "total unmet dependencies", maxResults)
}

// nodeDependencyName returns a common dependency name for a node that will be shared across similair Meta/Run/Build nodes for the same package.
func nodeDependencyName(node *pkggraph.PkgNode) (name string) {
	// Prefer the SRPM name if possible, otherwise use the unversioned package name
	name = node.SRPMFileName()
	if name == "" || name == pkggraph.NoSRPMPath {
		name = node.VersionedPkg.Name
	}

	return
}

// nodeRPMName returns the name of the RPM providing this node
func nodeRPMName(node *pkggraph.PkgNode) (name string) {
	// Prefer the SRPM name if possible, otherwise use the unversioned package name
	name = filepath.Base(node.RpmPath)
	if name == "" || name == pkggraph.NoRPMPath {
		name = node.VersionedPkg.Name
	}

	return
}

// printTitle prints a formatted title
func printTitle(title string) {
	logger.Log.Info("")
	logger.Log.Info("================================================")
	logger.Log.Info(title)
	logger.Log.Info("================================================")
}

// sortMap returns a sorted slice of a map. If inverse is set, it will return the smallest entries first.
// It will sort entries by the number of values each key has. For keys with the same number of entries, it will
// sort alphabetically.
func sortMap(mapToSort map[string][]string, inverse bool) (pairList []mapPair) {
	pairList = make([]mapPair, 0, len(mapToSort))
	for key, value := range mapToSort {
		pairList = append(pairList, mapPair{key, value})
	}

	sort.Slice(pairList, func(i, j int) bool {
		iValueLen := len(pairList[i].value)
		jValueLen := len(pairList[j].value)

		if iValueLen == jValueLen {
			return pairList[i].key < pairList[j].key
		}

		if inverse {
			return iValueLen < jValueLen
		}

		return iValueLen > jValueLen
	})

	return
}

// insertIfMissing appends a value to the key in a map if it is not present.
//
// Will alter data.
func insertIfMissing(data map[string][]string, key string, value string) {
	if !sliceutils.Contains(data[key], value, sliceutils.StringMatch) {
		data[key] = append(data[key], value)
	}
}

// insertIfMissingLastPathNode appends a value to the key in a map if it is not present.
// The function compares last nodes of each stored path with the last node of the new path
// and inserts the new path only if it introduces a new last node.
//
// Will alter data.
func insertIfMissingLastPathNode(data map[string][][]graph.Node, key string, value []graph.Node) {
	if !sliceutils.Contains(data[key], value, finalPathNodeSRPMMatch) {
		data[key] = append(data[key], value)
	}
}

// printMap will sort and print the smallest entries, using the valueDescription in the format.
func printReversedMap(data map[string][]string, valueDescription string, maxResults int) {
	const inverse = true
	pairList := sortMap(data, inverse)
	printSlice(pairList, valueDescription, maxResults)
}

// printMap will sort and print the largest entries, using the valueDescription in the format.
func printMap(data map[string][]string, valueDescription string, maxResults int) {
	const inverse = false
	pairList := sortMap(data, inverse)
	printSlice(pairList, valueDescription, maxResults)
}

// printSlice prints the first maxResults entries, using the valueDescription in the format.
func printSlice(pairList []mapPair, valueDescription string, maxResults int) {
	for i, pair := range pairList {
		if maxResults != 0 && i >= maxResults {
			break
		}

		logger.Log.Infof("%d: %s - %d %s", i+1, pair.key, len(pair.value), valueDescription)
		for _, value := range pair.value {
			logger.Log.Debugf("--> %s", value)
		}
	}
}

// finalPathNodeSRPMMatch checks if two '[]graph.Node' paths finish with the same final SRPM.
func finalPathNodeSRPMMatch(expected, given interface{}) bool {
	expectedPath := expected.([]graph.Node)
	givenPath := given.([]graph.Node)

	expectedPathLastNode := expectedPath[len(expectedPath)-1].(*pkggraph.PkgNode)
	givenPathLastNode := givenPath[len(givenPath)-1].(*pkggraph.PkgNode)

	return nodeDependencyName(expectedPathLastNode) == nodeDependencyName(givenPathLastNode)
}

// convertNodePathToStringPath converts the graph node slice into a string in the following format:
//
//	<last_node>: <first_node> [<optional_node_SRPM_name>] -> <second_node> [<optional_node_SRPM_name>] -> (...) -> <last_node> [<optional_node_SRPM_name>]
func convertNodePathToStringPath(nodePath []graph.Node) string {
	var pathStrings []string
	var stringBuilder strings.Builder

	finalNode := nodePath[len(nodePath)-1].(*pkggraph.PkgNode)

	stringBuilder.WriteString(nodeDependencyName(finalNode))
	stringBuilder.WriteString(": ")

	previousPackageName := ""
	for _, pathNode := range nodePath {
		packageNode := pathNode.(*pkggraph.PkgNode)
		packageRPMName := nodeRPMName(packageNode)
		packageDependencyName := nodeDependencyName(packageNode)
		if packageRPMName != packageDependencyName {
			packageRPMName += fmt.Sprintf(" [%s]", packageDependencyName)
		}

		// Meta nodes, and run nodes may end up having the same name as build nodes and we don't need to see them twice.
		if previousPackageName != packageRPMName {
			pathStrings = append(pathStrings, packageRPMName)
			previousPackageName = packageRPMName
		}
	}

	stringBuilder.WriteString(strings.Join(pathStrings, " -> "))

	return stringBuilder.String()
}
