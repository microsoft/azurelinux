// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package pkggraph

import (
	"bytes"
	"encoding/base64"
	"encoding/gob"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"sync"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repocloner/rpmrepocloner"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/sliceutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/versioncompare"
	"github.com/sirupsen/logrus"

	"gonum.org/v1/gonum/graph"
	"gonum.org/v1/gonum/graph/encoding"
	"gonum.org/v1/gonum/graph/encoding/dot"
	"gonum.org/v1/gonum/graph/simple"
	"gonum.org/v1/gonum/graph/traverse"
)

// NodeState indicates if a node is a package node (build, upToDate,unresolved,cached) or a meta node (meta)
type NodeState int

// Valid values for NodeState type
const (
	StateUnknown    NodeState = iota // Unknown state
	StateMeta       NodeState = iota // Meta nodes do not represent actual build artifacts, but additional nodes used for managing dependencies
	StateBuild      NodeState = iota // A package from a local SRPM which should be built from source
	StateUpToDate   NodeState = iota // A local RPM is already built and is available
	StateUnresolved NodeState = iota // A dependency is not available locally and must be acquired from a remote repo
	StateCached     NodeState = iota // A dependency was not available locally, but is now available in the chache
	StateBuildError NodeState = iota // A package from a local SRPM which failed to build
	StateDelta      NodeState = iota // Same as build state, but an attempt has been made to pre-download the .rpm to the cache
	StateMAX        NodeState = iota // Max allowable state
)

// NodeType indicates the general node type (build, run, goal, remote).
type NodeType int

// Valid values for NodeType type
const (
	TypeUnknown    NodeType = iota // Unknown type
	TypeLocalBuild NodeType = iota // Package can be build if all dependency edges are satisfied
	TypeLocalRun   NodeType = iota // Package can be run if all dependency edges are satisfied. Will be associated with a partner build node
	TypeGoal       NodeType = iota // Meta node which depends on a user selected subset of packages to be built.
	TypeRemoteRun  NodeType = iota // A non-local node which may have a cache entry
	TypePureMeta   NodeType = iota // An arbitrary meta node with no other meaning
	TypePreBuilt   NodeType = iota // A node indicating a pre-built SRPM used in breaking cyclic build dependencies
	TypeTest       NodeType = iota // A node for running the '%check' section of the underlying package
	TypeMAX        NodeType = iota // Max allowable type
)

// Constants representing empty member fields of the 'PkgNode' struct.
const (
	LocalRepo      = "<LOCAL_REPO>"
	NoArchitecture = "<NO_ARCHITECTURE>"
	NoName         = "<NO_NAME>"
	NoRPMPath      = "<NO_RPM_PATH>"
	NoSourceDir    = "<NO_SOURCE_DIR>"
	NoSourceRepo   = "<NO_SOURCE_REPO>"
	NoSpecPath     = "<NO_SPEC_PATH>"
	NoSRPMPath     = "<NO_SRPM_PATH>"
)

// Dot encoding/decoding keys
const (
	dotKeyNodeInBase64 = "NodeInBase64"
	dotKeySRPM         = "SRPM"
	dotKeyColor        = "fillcolor"
	dotKeyFill         = "style"
)

// Determines if a type of node is valid for inclusion in the lookup tables.
var lookupNodesTypes = map[NodeType]bool{
	TypeLocalBuild: true,
	TypeLocalRun:   true,
	TypeRemoteRun:  true,
	TypeTest:       true,
}

// PkgNode represents a package.
type PkgNode struct {
	nodeID       int64               // Unique ID for the node
	VersionedPkg *pkgjson.PackageVer // JSON derived structure holding the exact version information for a graph
	State        NodeState           // The current state of the node (ie needs to be build, up-to-date, cached, etc)
	Type         NodeType            // The purpose of the node (build, run , meta goal, etc)
	SrpmPath     string              // SRPM file used to generate this package (likely shared with multiple other nodes)
	RpmPath      string              // RPM file that produces this package (likely shared with multiple other nodes)
	SpecPath     string              // The SPEC file extracted from the SRPM
	SourceDir    string              // The directory containing extracted sources from the SRPM
	Architecture string              // The architecture of the resulting package built.
	SourceRepo   string              // The location this package was acquired from
	GoalName     string              // Optional string for goal nodes
	Implicit     bool                // If the package is an implicit provide
	This         *PkgNode            // Self reference since the graph library returns nodes by value, not reference
}

// ID implements the graph.Node interface, returns the node's unique ID
func (n PkgNode) ID() int64 {
	return n.nodeID
}

// PkgGraph implements a simple.DirectedGraph using pkggraph Nodes.
type PkgGraph struct {
	*simple.DirectedGraph
	nodeLookup map[string][]*LookupNode
}

// LookupNode represents a graph node for a package in the lookup list
type LookupNode struct {
	RunNode   *PkgNode // The "meta" run node for a package. Tracks the run-time dependencies for the package. Remote packages will only have a RunNode.
	BuildNode *PkgNode // The build node for a package. Tracks the build requirements for the package. May be nil for remote packages.
	TestNode  *PkgNode // The test node for a package. Tracks the test requirements for the package. Nil for non-test builds and when its spec has no '%check' section.
}

var (
	registerOnce sync.Once
)

func (n NodeState) String() string {
	switch n {
	case StateMeta:
		return "Meta"
	case StateBuild:
		return "Build"
	case StateBuildError:
		return "BuildError"
	case StateUpToDate:
		return "UpToDate"
	case StateUnresolved:
		return "Unresolved"
	case StateCached:
		return "Cached"
	case StateDelta:
		return "Delta"
	default:
		logger.Log.Panic("Invalid NodeState encountered when serializing to string!")
		return "error"
	}
}

func (n NodeType) String() string {
	switch n {
	case TypeLocalBuild:
		return "Build"
	case TypeLocalRun:
		return "Run"
	case TypeGoal:
		return "Goal"
	case TypeRemoteRun:
		return "Remote"
	case TypePureMeta:
		return "PureMeta"
	case TypePreBuilt:
		return "PreBuilt"
	case TypeTest:
		return "Test"
	default:
		logger.Log.Panic("Invalid NodeType encountered when serializing to string!")
		return "error"
	}
}

func (n *LookupNode) PackageVer() (packageVer *pkgjson.PackageVer) {
	switch {
	case n.RunNode != nil:
		return n.RunNode.VersionedPkg
	case n.TestNode != nil:
		return n.TestNode.VersionedPkg
	case n.BuildNode != nil:
		return n.BuildNode.VersionedPkg
	}

	return nil
}

// DOTColor returns the graphviz color to set a node to
func (n *PkgNode) DOTColor() string {
	switch n.State {
	case StateMeta:
		if n.Type == TypeGoal {
			return "deeppink"
		}
		return "aquamarine"
	case StateBuild:
		if n.Type == TypeTest {
			return "gold4"
		}
		return "gold"
	case StateBuildError:
		return "darkorange"
	case StateUpToDate:
		switch n.Type {
		case TypePreBuilt:
			return "greenyellow"
		case TypeTest:
			return "lime"
		default:
			return "forestgreen"
		}
	case StateUnresolved:
		return "crimson"
	case StateCached:
		return "darkorchid"
	case StateDelta:
		return "gold4"
	default:
		logger.Log.Panic("Invalid NodeState encountered when serializing to color!")
		return "error"
	}
}

// NewPkgGraph creates a new package dependency graph based on a simple.DirectedGraph
func NewPkgGraph() *PkgGraph {
	g := &PkgGraph{DirectedGraph: simple.NewDirectedGraph()}
	// Lazy initialize nodeLookup, we might be de-serializing and we need to wait until we are done
	// before populating the lookup table.
	g.nodeLookup = nil
	return g
}

// initLookup initializes the run and build node lookup table
func (g *PkgGraph) initLookup() {
	g.nodeLookup = make(map[string][]*LookupNode)

	for _, n := range graph.NodesOf(g.Nodes()) {
		g.addToLookup(n.(*PkgNode), true)
	}

	// Sort each of the lookup lists from lowest version to highest version. The RunNode or TestNode is always expected to be
	// a valid reference while BuildNode may be nil.
	for idx := range g.nodeLookup {
		// Validate the lookup table is well formed. Cases to consider:
		// 1. Pure meta nodes created by cycles may, in some cases, create build nodes,
		//    which have no associated run node after passing into a subgraph.
		//    The subgraph only requires one of the cycle members but will get all of their build nodes.
		// 2. Subgraphs for builds, which only require test runs will contain (build, test) node pairs
		//    while the run nodes are optional.
		endOfValidData := 0
		for _, n := range g.nodeLookup[idx] {
			if n.RunNode == nil && n.TestNode == nil {
				logger.Log.Debugf("Lookup for %s has neither a run node nor a test node. Lost in a cycle fix? Removing it", idx)
				g.RemoveNode(n.BuildNode.ID())
			} else {
				g.nodeLookup[idx][endOfValidData] = n
				endOfValidData++
			}
		}
		// Prune off the invalid entries at the end of the slice
		g.nodeLookup[idx] = g.nodeLookup[idx][:endOfValidData]

		sort.Slice(g.nodeLookup[idx], func(i, j int) bool {
			intervalI, _ := g.nodeLookup[idx][i].PackageVer().Interval()
			intervalJ, _ := g.nodeLookup[idx][j].PackageVer().Interval()
			return intervalI.Compare(&intervalJ) < 0
		})
	}
}

// lookupTable returns a reference to the lookup table, initialzing it first if needed.
func (g *PkgGraph) lookupTable() map[string][]*LookupNode {
	if g.nodeLookup == nil {
		g.initLookup()
	}
	return g.nodeLookup
}

// validateNodeForLookup checks if a node is valid for adding to the lookup table
func (g *PkgGraph) validateNodeForLookup(pkgNode *PkgNode) (valid bool, err error) {
	// Only add run, remote, or build nodes to lookup
	if !lookupNodesTypes[pkgNode.Type] {
		err = fmt.Errorf("%s has invalid type for lookup", pkgNode)
		return
	}

	// Check for existing lookup entries which conflict
	existingLookup, err := g.FindExactPkgNodeFromPkg(pkgNode.VersionedPkg)
	if err != nil {
		return
	}

	if existingLookup != nil {
		haveDuplicateNode := false

		switch pkgNode.Type {
		case TypeLocalBuild:
			haveDuplicateNode = existingLookup.BuildNode != nil
		case TypeLocalRun:
			haveDuplicateNode = (existingLookup.RunNode != nil) && (existingLookup.RunNode.Type == TypeLocalRun)
		case TypeRemoteRun:
			// RemoteRun nodes may have duplicates. It is possible that:
			// 1. LocalRun and RemoteRun co-exist in a graph
			// 2. Multiple RemoteRun nodes can exist in a graph
			// So, this is not considered as a duplicate node
		case TypeTest:
			haveDuplicateNode = existingLookup.TestNode != nil
		}

		if haveDuplicateNode {
			err = fmt.Errorf("already have a lookup for %s", pkgNode)
			return
		}
	}

	// Make sure we have a valid version.
	versionInterval, err := pkgNode.VersionedPkg.Interval()
	if err != nil {
		logger.Log.Errorf("Failed to create version interval for %s", pkgNode)
		return
	}

	// Basic run nodes can only provide basic conditional versions
	if pkgNode.Type != TypeRemoteRun {
		// We only support a single conditional (ie ver >= 1), or (ver = 1)
		if versionInterval.UpperBound.Compare(versioncompare.NewMax()) != 0 && versionInterval.UpperBound.Compare(versionInterval.LowerBound) != 0 {
			err = fmt.Errorf("%s is a run node and can't have double conditionals", pkgNode)
			return
		}
		if !versionInterval.LowerInclusive {
			err = fmt.Errorf("%s is a run node and can't have non-inclusive lower bounds ('ver > ?')", pkgNode)
			return
		}
	}

	valid = true
	return
}

// addToLookup adds a node to the lookup table if it is the correct type (build/run)
func (g *PkgGraph) addToLookup(pkgNode *PkgNode, deferSort bool) (err error) {
	// We only care about run/build nodes or remote dependencies
	if !lookupNodesTypes[pkgNode.Type] {
		logger.Log.Tracef("Skipping %+v, not valid for lookup", pkgNode)
		return
	}

	_, err = g.validateNodeForLookup(pkgNode)
	if err != nil {
		return
	}

	logger.Log.Tracef("Adding %+v to lookup", pkgNode)
	// Get the existing package lookup, or create it
	pkgName := pkgNode.VersionedPkg.Name

	existingLookup, err := g.FindExactPkgNodeFromPkg(pkgNode.VersionedPkg)
	if err != nil {
		return
	}

	if existingLookup == nil {
		if (!deferSort) && pkgNode.Type == TypeLocalBuild {
			err = fmt.Errorf("can't add %s, no corresponding run node found and not deferring sort", pkgNode)
			return
		}
		existingLookup = &LookupNode{}
		g.lookupTable()[pkgName] = append(g.lookupTable()[pkgName], existingLookup)
	}

	switch pkgNode.Type {
	case TypeLocalBuild:
		existingLookup.BuildNode = pkgNode.This
	case TypeLocalRun:
		// Prefer LocalRun over RemoteRun
		existingLookup.RunNode = pkgNode.This
	case TypeRemoteRun:
		// Update only if RunNoe is nil
		if existingLookup.RunNode == nil {
			existingLookup.RunNode = pkgNode.This
		}
	case TypeTest:
		existingLookup.TestNode = pkgNode.This
	}

	// Sort the updated list unless we are deferring until all nodes are added
	if !deferSort {
		sort.Slice(g.lookupTable()[pkgName], func(i, j int) bool {
			intervalI, _ := g.lookupTable()[pkgName][i].PackageVer().Interval()
			intervalJ, _ := g.lookupTable()[pkgName][j].PackageVer().Interval()
			return intervalI.Compare(&intervalJ) < 0
		})
	}
	return
}

// AddEdge creates a new edge between the provided nodes.
func (g *PkgGraph) AddEdge(from *PkgNode, to *PkgNode) (err error) {
	logger.Log.Tracef("Adding edge: %s -> %s", from.FriendlyName(), to.FriendlyName())

	newEdge := g.NewEdge(from, to)
	defer func() {
		if r := recover(); r != nil {
			err = fmt.Errorf("failed to add edge: '%s' -> '%s'", from.SrpmPath, to.SrpmPath)
		}
	}()
	g.SetEdge(newEdge)

	return
}

// NewNode creates a new pkggraph Node for the graph
func (g *PkgGraph) NewNode() graph.Node {
	node := g.DirectedGraph.NewNode()
	pkgNode := &PkgNode{nodeID: node.ID()}
	pkgNode.This = pkgNode
	return pkgNode
}

// CreateCollapsedNode creates a new run node linked to a given parent node. All nodes in nodesToCollapse will be collapsed into the new node.
// - When a node is collapsed all of its dependents will be mirrored onto the new node.
// - The parentNode must be a run node.
// - The collapsed node will inherit all attributes of the parent node minus the versionedPkg.
func (g *PkgGraph) CreateCollapsedNode(versionedPkg *pkgjson.PackageVer, parentNode *PkgNode, nodesToCollapse []*PkgNode) (newNode *PkgNode, err error) {
	// enforce parent is run node
	if parentNode.Type != TypeLocalRun {
		err = fmt.Errorf("cannot collapse nodes to a non run node (%s)", parentNode.FriendlyName())
		return
	}

	logger.Log.Debugf("Collapsing (%v) into (%s) with (%s) as a parent.", nodesToCollapse, versionedPkg, parentNode)

	// Remove the nodes to collapse from the lookup table so they do not conflict with the new node.
	// This operation can be undone on failure.
	for _, node := range nodesToCollapse {
		g.removePkgNodeFromLookup(node)
	}

	// Defer cleanup now that the graph is being manipulated.
	defer func() {
		// graph manipulation calls may panic on error (such as duplicate node IDs)
		if r := recover(); r != nil {
			err = fmt.Errorf("collapsing nodes (%v) into (%s) failed, error: %s", nodesToCollapse, versionedPkg, r)
		}

		if err != nil {
			if newNode != nil {
				g.RemovePkgNode(newNode)
			}

			// Add the nodes that were meant to be collapsed back to the lookup table.
			for _, node := range nodesToCollapse {
				lookupErr := g.addToLookup(node, false)
				if lookupErr != nil {
					logger.Log.Errorf("Failed to add node (%s) back to lookup table. Error: %s", node.FriendlyName(), lookupErr)
				}
			}
		}
	}()

	// Create a new node that the others will collapse into.
	// This new node will mirror all attributes of the parent minus the versionedPkg.
	newNode, err = g.AddPkgNode(versionedPkg, parentNode.State, parentNode.Type, parentNode.SrpmPath, parentNode.RpmPath, parentNode.SpecPath, parentNode.SourceDir, parentNode.Architecture, parentNode.SourceRepo)
	if err != nil {
		return
	}

	// Create an edge for the dependency of newNode on parentNode.
	parentEdge := g.NewEdge(newNode, parentNode)
	g.SetEdge(parentEdge)

	// Mirror the dependents of nodesToCollapse to the new node
	for _, node := range nodesToCollapse {
		dependents := g.To(node.ID())

		for dependents.Next() {
			dependent := dependents.Node().(*PkgNode)

			// Create an edge for the dependency of what used to depend on the collapsed node to the new node
			dependentEdge := g.NewEdge(dependent, newNode)
			g.SetEdge(dependentEdge)
		}
	}

	// After removing nodes errors are unrecoverable so do it last.
	for _, node := range nodesToCollapse {
		g.RemovePkgNode(node)
	}

	return
}

// AddPkgNode adds a new node to the package graph. Run, Build, and Unresolved nodes are recorded in the lookup table.
func (g *PkgGraph) AddPkgNode(versionedPkg *pkgjson.PackageVer, nodeState NodeState, nodeType NodeType, srpmPath, rpmPath, specPath, sourceDir, architecture, sourceRepo string) (newNode *PkgNode, err error) {
	newNode = &PkgNode{
		nodeID:       g.NewNode().ID(),
		VersionedPkg: versionedPkg,
		State:        nodeState,
		Type:         nodeType,
		SrpmPath:     srpmPath,
		RpmPath:      rpmPath,
		SpecPath:     specPath,
		SourceDir:    sourceDir,
		Architecture: architecture,
		SourceRepo:   sourceRepo,
		Implicit:     versionedPkg.IsImplicitPackage(),
	}
	newNode.This = newNode

	// Make sure the lookup table is initialized before we start (otherwise it will try to 'fix' orphaned build nodes by removing them)
	g.lookupTable()
	err = g.safeAddNode(newNode)
	if err != nil {
		return
	}

	// Register the package with the lookup table if needed
	err = g.addToLookup(newNode, false)

	return
}

// AddRemoteUnresolvedNode adds a new node to the package graph representing an unresolved remote dependency.
func (g *PkgGraph) AddRemoteUnresolvedNode(versionedPkg *pkgjson.PackageVer) (newNode *PkgNode, err error) {
	return g.AddPkgNode(versionedPkg, StateUnresolved, TypeRemoteRun, NoSRPMPath, NoRPMPath, NoSpecPath, NoSourceDir, NoArchitecture, NoSourceRepo)
}

// RemovePkgNode removes a node from the package graph and lookup tables.
func (g *PkgGraph) RemovePkgNode(pkgNode *PkgNode) {
	g.RemoveNode(pkgNode.ID())
	g.removePkgNodeFromLookup(pkgNode)
}

// FindDoubleConditionalPkgNodeFromPkg has the same behavior as FindConditionalPkgNodeFromPkg but supports two conditionals
func (g *PkgGraph) FindDoubleConditionalPkgNodeFromPkg(pkgVer *pkgjson.PackageVer) (lookupEntry *LookupNode, err error) {
	var (
		requestInterval, nodeInterval pkgjson.PackageVerInterval
		bestLocalNode                 *LookupNode
	)
	requestInterval, err = pkgVer.Interval()
	if err != nil {
		return
	}

	bestLocalNode = nil
	packageNodes := g.lookupTable()[pkgVer.Name]
	for _, node := range packageNodes {
		nodeInterval, err = node.PackageVer().Interval()
		if err != nil {
			return
		}

		if nodeInterval.Satisfies(&requestInterval) {
			// Only local packages will have a build node
			if node.BuildNode != nil {
				bestLocalNode = node
			}
			// Keep going, we want the highest version which satisfies both conditionals
			lookupEntry = node
		}
	}

	// If the pkgVer resolves to a remote node, and that node
	// is never found during the build, we have no way to
	// fall back to the local package at this time.
	if bestLocalNode != nil && bestLocalNode != lookupEntry {
		logger.Log.Warnf("Resolving '%s' to remote node '%s' instead of local node '%s'", pkgVer, lookupEntry.RunNode.String(), bestLocalNode.RunNode.String())
	}
	return
}

// FindExactPkgNodeFromPkg attempts to find a LookupNode which has the exactly
// correct version information listed in the PackageVer structure. Returns nil
// if no lookup entry is found.
func (g *PkgGraph) FindExactPkgNodeFromPkg(pkgVer *pkgjson.PackageVer) (lookupEntry *LookupNode, err error) {
	var (
		requestInterval, nodeInterval pkgjson.PackageVerInterval
	)
	requestInterval, err = pkgVer.Interval()
	if err != nil {
		return
	}

	packageNodes := g.lookupTable()[pkgVer.Name]

	for _, node := range packageNodes {
		nodeInterval, err = node.PackageVer().Interval()
		if err != nil {
			return
		}

		//Exact lookup must match the exact node, including conditionals.
		if requestInterval.Equal(&nodeInterval) {
			lookupEntry = node
		}
	}
	return
}

// FindBestPkgNode will search the lookup table to see if a node which satisfies the
// PackageVer structure has already been created. Returns nil if no lookup entry
// is found.
// Condition = "" is equivalent to Condition = "=".
func (g *PkgGraph) FindBestPkgNode(pkgVer *pkgjson.PackageVer) (lookupEntry *LookupNode, err error) {
	lookupEntry, err = g.FindDoubleConditionalPkgNodeFromPkg(pkgVer)
	return
}

// HasNode returns true if pkgNode points to a node that is present in the graph.
// If the object is not the same, but the ID is the same, it will return false (i.e., the node is a copy)
func (g *PkgGraph) HasNode(pkgNode *PkgNode) bool {
	if pkgNode == nil {
		return false
	}
	nodeWithSameId := g.Node(pkgNode.ID())
	if nodeWithSameId == nil {
		return false
	} else {
		// Check if they are the same node object
		return nodeWithSameId.(*PkgNode) == pkgNode
	}
}

// AllNodes returns a list of all nodes in the graph.
func (g *PkgGraph) AllNodes() []*PkgNode {
	count := g.Nodes().Len()
	nodes := make([]*PkgNode, 0, count)
	for _, n := range graph.NodesOf(g.Nodes()) {
		nodes = append(nodes, n.(*PkgNode).This)
	}
	return nodes
}

// AllNodesFrom returns a list of all nodes accessible from a root node
func (g *PkgGraph) AllNodesFrom(rootNode *PkgNode) []*PkgNode {
	count := g.Nodes().Len()
	nodes := make([]*PkgNode, 0, count)
	search := traverse.DepthFirst{}
	search.Walk(g, rootNode, func(n graph.Node) bool {
		// Visit function of DepthFirst, called once per node
		nodes = append(nodes, n.(*PkgNode).This)
		// Don't stop early, visit every node
		return false
	})
	return nodes
}

// AllRunNodes returns a list of all run nodes in the graph
// It traverses the graph and returns all nodes of type TypeLocalRun and
// TypeRemoteRun.
func (g *PkgGraph) AllRunNodes() []*PkgNode {
	nodes := make([]*PkgNode, 0, g.Nodes().Len())
	for _, n := range g.AllNodes() {
		if n.Type == TypeLocalRun || n.Type == TypeRemoteRun {
			nodes = append(nodes, n)
		}
	}
	return nodes
}

// AllPreferredRunNodes returns all RunNodes in the LookupTable
// Though a graph can contain both LocalRun and RemoteRun node for a single
// package-version, the LookupTable will have:
// 1. LocalRun Node if only LocalRun node is present in the graph
// 2. RemoteRun Node if only RemoteRun node is present in the graph
// 3. LocalRun Node if both LocalRun and RemoteRun nodes are present in the graph
// This function will return all RunNodes in the LookupTable.
func (g *PkgGraph) AllPreferredRunNodes() []*PkgNode {
	return g.allNodesOfType(func(n *LookupNode) *PkgNode {
		return n.RunNode
	})
}

// AllBuildNodes returns a list of all build nodes in the graph
func (g *PkgGraph) AllBuildNodes() []*PkgNode {
	return g.allNodesOfType(func(n *LookupNode) *PkgNode {
		return n.BuildNode
	})
}

// AllTestNodes returns a list of all test nodes in the graph
func (g *PkgGraph) AllTestNodes() []*PkgNode {
	return g.allNodesOfType(func(n *LookupNode) *PkgNode {
		return n.TestNode
	})
}

// AllImplicitNodes returns a list of all implicit remote nodes in the graph
func (g *PkgGraph) AllImplicitNodes() []*PkgNode {
	return g.allNodesOfType(func(n *LookupNode) *PkgNode {
		if n.RunNode != nil && n.RunNode.Implicit {
			return n.RunNode
		}
		return nil
	})
}

// NodesMatchingFilter returns a list of all nodes satisfying the input filter.
func (g *PkgGraph) NodesMatchingFilter(filter func(*PkgNode) bool) (nodes []*PkgNode) {
	foundNodes := 0
	nodes = make([]*PkgNode, 0, g.Nodes().Len())
	for _, n := range graph.NodesOf(g.Nodes()) {
		pkgNode := n.(*PkgNode).This
		if filter(pkgNode) {
			nodes = append(nodes, pkgNode)
			foundNodes++
		}
	}
	return nodes[:foundNodes]
}

// DOTID generates an id for a DOT graph of the form
// "pkg(ver:=xyz)<TYPE> (ID=x,STATE=state)""
func (n PkgNode) DOTID() string {
	thing := fmt.Sprintf("%s (ID=%d,TYPE=%s,STATE=%s)", n.FriendlyName(), n.ID(), n.Type.String(), n.State.String())
	return thing
}

// SetDOTID handles parsing the ID of a node from a DOT file
func (n PkgNode) SetDOTID(id string) {
	logger.Log.Tracef("Processing id %s", id)
}

// FriendlyName formats a summary of a node into a string.
func (n *PkgNode) FriendlyName() string {
	switch n.Type {
	case TypeLocalBuild:
		return fmt.Sprintf("%s-%s-BUILD<%s>", n.VersionedPkg.Name, n.VersionedPkg.Version, n.State.String())
	case TypeLocalRun:
		return fmt.Sprintf("%s-%s-RUN<%s>", n.VersionedPkg.Name, n.VersionedPkg.Version, n.State.String())
	case TypeRemoteRun:
		ver1 := fmt.Sprintf("%s%s", n.VersionedPkg.Condition, n.VersionedPkg.Version)
		ver2 := ""
		if len(n.VersionedPkg.SCondition) > 0 || len(n.VersionedPkg.SVersion) > 0 {
			ver2 = fmt.Sprintf("%s,%s%s", ver1, n.VersionedPkg.SCondition, n.VersionedPkg.SVersion)
		}
		return fmt.Sprintf("%s-%s-REMOTE<%s>", n.VersionedPkg.Name, ver2, n.State.String())
	case TypeGoal:
		return n.GoalName
	case TypePureMeta:
		return fmt.Sprintf("Meta(%d)", n.ID())
	case TypePreBuilt:
		return fmt.Sprintf("%s-%s-PREBUILT<%s>", n.VersionedPkg.Name, n.VersionedPkg.Version, n.State.String())
	case TypeTest:
		return fmt.Sprintf("%s-%s-TEST<%s>", n.VersionedPkg.Name, n.VersionedPkg.Version, n.State.String())
	default:
		return "UNKNOWN NODE TYPE"
	}
}

// SpecName returns the name of the spec associated with this node.
// Returns "." if the node doesn't have a spec file path or URL.
func (n *PkgNode) SpecName() string {
	return strings.TrimSuffix(filepath.Base(n.SpecPath), ".spec")
}

// SRPMFileName returns the name of the SRPM file associated with this node.
// Returns "." if the node doesn't have an SRPM file path or URL.
func (n *PkgNode) SRPMFileName() string {
	return filepath.Base(n.SrpmPath)
}

func (n *PkgNode) String() string {
	var version, name string
	if n.Type == TypeGoal {
		name = n.GoalName
	} else if n.VersionedPkg != nil {
		name = n.VersionedPkg.Name
		version = fmt.Sprintf("%s%s,%s%s", n.VersionedPkg.Condition, n.VersionedPkg.Version, n.VersionedPkg.SCondition, n.VersionedPkg.SVersion)
	} else {
		name = NoName
	}

	return fmt.Sprintf("%s(%s):<ID:%d Type:%s State:%s Rpm:%s> from '%s' in '%s'", name, version, n.nodeID, n.Type.String(), n.State.String(), n.RpmPath, n.SrpmPath, n.SourceRepo)
}

// Equal returns true if these nodes represent the same data
func (n *PkgNode) Equal(otherNode *PkgNode) bool {
	if n.This == otherNode.This {
		return true
	}
	if n.VersionedPkg != otherNode.VersionedPkg {
		v1 := n.VersionedPkg
		v2 := otherNode.VersionedPkg
		if v1 == nil || v2 == nil {
			return false
		}

		nInterval, _ := n.VersionedPkg.Interval()
		otherInterval, _ := otherNode.VersionedPkg.Interval()
		if !nInterval.Equal(&otherInterval) {
			return false
		}
	}
	return n.State == otherNode.State &&
		n.Type == otherNode.Type &&
		n.SrpmPath == otherNode.SrpmPath &&
		n.RpmPath == otherNode.RpmPath &&
		n.SpecPath == otherNode.SpecPath &&
		n.SourceDir == otherNode.SourceDir &&
		n.Architecture == otherNode.Architecture &&
		n.SourceRepo == otherNode.SourceRepo &&
		n.GoalName == otherNode.GoalName &&
		n.Implicit == otherNode.Implicit
}

func registerTypes() {
	logger.Log.Debug("Registering pkggraph.Node for marshalling.")
	gob.Register(PkgNode{})
}

// MarshalBinary implements the GOB encoding interface
func (n PkgNode) MarshalBinary() (data []byte, err error) {
	var outBuffer bytes.Buffer
	encoder := gob.NewEncoder(&outBuffer)
	hasPkgPtr := (n.VersionedPkg != nil)
	err = encoder.Encode(hasPkgPtr)
	if err != nil {
		err = fmt.Errorf("encoding hasPkgPtr: %s", err.Error())
		return
	}
	if hasPkgPtr {
		err = encoder.Encode(n.VersionedPkg)
		if err != nil {
			err = fmt.Errorf("encoding VersionedPkg: %s", err.Error())
			return
		}
	}
	err = encoder.Encode(n.State)
	if err != nil {
		err = fmt.Errorf("encoding State: %s", err.Error())
		return
	}
	err = encoder.Encode(n.Type)
	if err != nil {
		err = fmt.Errorf("encoding Type: %s", err.Error())
		return
	}
	err = encoder.Encode(n.SrpmPath)
	if err != nil {
		err = fmt.Errorf("encoding SrpmPath: %s", err.Error())
		return
	}
	err = encoder.Encode(n.RpmPath)
	if err != nil {
		err = fmt.Errorf("encoding RpmPath: %s", err.Error())
		return
	}
	err = encoder.Encode(n.SpecPath)
	if err != nil {
		err = fmt.Errorf("encoding SpecPath: %s", err.Error())
		return
	}
	err = encoder.Encode(n.SourceDir)
	if err != nil {
		err = fmt.Errorf("encoding SourceDir: %s", err.Error())
		return
	}
	err = encoder.Encode(n.Architecture)
	if err != nil {
		err = fmt.Errorf("encoding Architecture: %s", err.Error())
		return
	}
	err = encoder.Encode(n.SourceRepo)
	if err != nil {
		err = fmt.Errorf("encoding SourceRepo: %s", err.Error())
		return
	}
	err = encoder.Encode(n.GoalName)
	if err != nil {
		err = fmt.Errorf("encoding GoalName: %s", err.Error())
		return
	}
	err = encoder.Encode(n.Implicit)
	if err != nil {
		err = fmt.Errorf("encoding Implicit: %s", err.Error())
		return
	}
	return outBuffer.Bytes(), err
}

// UnmarshalBinary implements the GOB encoding interface
func (n *PkgNode) UnmarshalBinary(inBuffer []byte) (err error) {
	decoder := gob.NewDecoder(bytes.NewReader(inBuffer))
	var hasPkgPtr bool
	err = decoder.Decode(&hasPkgPtr)
	if err != nil {
		err = fmt.Errorf("decoding hasPkgPtr: %s", err.Error())
		return
	}
	if hasPkgPtr {
		err = decoder.Decode(&n.VersionedPkg)
		if err != nil {
			err = fmt.Errorf("decoding VersionedPkg: %s", err.Error())
			return
		}
	}
	err = decoder.Decode(&n.State)
	if err != nil {
		err = fmt.Errorf("decoding State: %s", err.Error())
		return
	}
	err = decoder.Decode(&n.Type)
	if err != nil {
		err = fmt.Errorf("decoding Type: %s", err.Error())
		return
	}
	err = decoder.Decode(&n.SrpmPath)
	if err != nil {
		err = fmt.Errorf("decoding SrpmPath: %s", err.Error())
		return
	}
	err = decoder.Decode(&n.RpmPath)
	if err != nil {
		err = fmt.Errorf("decoding RpmPath: %s", err.Error())
		return
	}
	err = decoder.Decode(&n.SpecPath)
	if err != nil {
		err = fmt.Errorf("decoding SpecPath: %s", err.Error())
		return
	}
	err = decoder.Decode(&n.SourceDir)
	if err != nil {
		err = fmt.Errorf("decoding SourceDir: %s", err.Error())
		return
	}
	err = decoder.Decode(&n.Architecture)
	if err != nil {
		err = fmt.Errorf("decoding Architecture: %s", err.Error())
		return
	}
	err = decoder.Decode(&n.SourceRepo)
	if err != nil {
		err = fmt.Errorf("decoding SourceRepo: %s", err.Error())
		return
	}
	err = decoder.Decode(&n.GoalName)
	if err != nil {
		err = fmt.Errorf("decoding GoalName: %s", err.Error())
		return
	}
	err = decoder.Decode(&n.Implicit)
	if err != nil {
		err = fmt.Errorf("decoding Implicit: %s", err.Error())
		return
	}
	n.This = n
	return
}

// SetAttribute sets a DOT attribute for the current node when parsing a DOT file
func (n *PkgNode) SetAttribute(attr encoding.Attribute) (err error) {
	var data []byte
	registerOnce.Do(registerTypes)

	switch attr.Key {
	case dotKeyNodeInBase64:
		logger.Log.Trace("Decoding base 64")
		// Encoding/decoding may not preserve the IDs, we should take the ID we were given
		// as the truth
		newID := n.nodeID
		data, err = base64.StdEncoding.DecodeString(attr.Value)
		if err != nil {
			logger.Log.Errorf("Failed to decode base 64 encoding: %s", err.Error())
			return
		}
		buffer := bytes.Buffer{}
		_, err = buffer.Write(data)
		if err != nil {
			logger.Log.Errorf("Failed to read gob data: %s", err.Error())
			return
		}

		decoder := gob.NewDecoder(&buffer)
		err = decoder.Decode(n)
		if err != nil {
			logger.Log.Errorf("Failed to decode gob data: %s", err.Error())
			return
		}
		// Restore the ID we were given by the deserializer
		n.nodeID = newID
	case dotKeySRPM:
		logger.Log.Trace("Ignoring srpm")
		// No-op, b64encoding should totally overwrite the node.
	case dotKeyColor:
		logger.Log.Trace("Ignoring color")
		// No-op, b64encoding should totally overwrite the node.
	case dotKeyFill:
		logger.Log.Trace("Ignoring fill")
		// No-op, b64encoding should totally overwrite the node.
	default:
		logger.Log.Warnf(`Unable to unmarshal an unknown key "%s".`, attr.Key)
	}

	return
}

// Attributes marshals all relevent node data into a DOT graph structure. The
// entire node is encoded using base64 and gob.
func (n *PkgNode) Attributes() []encoding.Attribute {
	registerOnce.Do(registerTypes)

	var buffer bytes.Buffer
	encoder := gob.NewEncoder(&buffer)
	err := encoder.Encode(n)
	if err != nil {
		logger.Log.Panicf("Error when encoding attributes: %s", err.Error())
	}
	nodeInBase64 := base64.StdEncoding.EncodeToString(buffer.Bytes())

	return []encoding.Attribute{
		{
			Key:   dotKeyNodeInBase64,
			Value: nodeInBase64,
		},
		{
			Key:   dotKeySRPM,
			Value: n.SrpmPath,
		},
		{
			Key:   dotKeyColor,
			Value: n.DOTColor(),
		},
		{
			Key:   dotKeyFill,
			Value: "filled",
		},
	}
}

// FindGoalNode returns a named goal node if one exists.
func (g *PkgGraph) FindGoalNode(goalName string) *PkgNode {
	for _, n := range g.AllNodes() {
		if n.Type == TypeGoal && n.GoalName == goalName {
			return n.This
		}
	}
	return nil
}

// AddMetaNode adds a generic meta node with edges: <from> -> metaNode -> <to>
func (g *PkgGraph) AddMetaNode(from []*PkgNode, to []*PkgNode) (metaNode *PkgNode) {
	// Handle failures in SetEdge() and AddNode()
	defer func() {
		if r := recover(); r != nil {
			fromNames := ""
			toNames := ""
			for _, n := range from {
				fromNames = fmt.Sprintf("%s %s", fromNames, n.FriendlyName())
			}
			for _, n := range to {
				toNames = fmt.Sprintf("%s %s", toNames, n.FriendlyName())
			}
			logger.Log.Errorf("Couldn't add meta node from [%s] to [%s]", fromNames, toNames)
			logger.Log.Panicf("Adding meta node failed.")
		}
	}()

	// Create meta node and add an edge to all requested packages
	metaNode = &PkgNode{
		State:  StateMeta,
		Type:   TypePureMeta,
		nodeID: g.NewNode().ID(),
	}
	metaNode.This = metaNode
	g.AddNode(metaNode)

	logger.Log.Trace("Adding edges TO the meta node:")
	for _, n := range from {
		logger.Log.Tracef("\t'%s' -> '%s'", n.FriendlyName(), metaNode.FriendlyName())
		edge := g.NewEdge(n, metaNode)
		g.SetEdge(edge)
	}

	logger.Log.Trace("Adding edges FROM the meta node:")
	for _, n := range to {
		logger.Log.Tracef("\t'%s' -> '%s'", metaNode.FriendlyName(), n.FriendlyName())
		edge := g.NewEdge(metaNode, n)
		g.SetEdge(edge)
	}

	return
}

// AddGoalNode adds a goal node to the graph which links to existing nodes. An empty package list will add an edge to all nodes
//   - goalName: The name of the goal node to add
//   - packages: A list of packages to add to link the goal node to. If empty, all nodes will be added to the goal node
//   - strict: If true, the goal node will fail if any of the packages are not found
func (g *PkgGraph) AddGoalNode(goalName string, packages, tests []*pkgjson.PackageVer, strict bool) (goalNode *PkgNode, err error) {
	return g.AddGoalNodeWithExtraLayers(goalName, packages, tests, strict, 0)
}

// AddGoalNodeWithExtraLayers adds a goal node to the graph which links to existing nodes. An empty package list will add an edge to all nodes
//   - goalName: The name of the goal node to add
//   - packages: A list of packages to add to link the goal node to. If empty, all nodes will be added to the goal node
//   - strict: If true, the goal node will fail if any of the packages are not found
//   - extraLayers: The number of levels to expand the goal node. Each level will add one more layer of packages beyond
//     the goal node. For example, if the goal node is "x" and extraLevels is 1, the goal node will link to all nodes
//     which depend on "x" as well as "x" itself (Specifically run nodes, all other nodes are stepped over)
func (g *PkgGraph) AddGoalNodeWithExtraLayers(goalName string, packages, tests []*pkgjson.PackageVer, strict bool, extraLayers int) (goalNode *PkgNode, err error) {
	// Check if we already have a goal node with the requested name
	if g.FindGoalNode(goalName) != nil {
		err = fmt.Errorf("can't have two goal nodes named %s", goalName)
		return
	}

	logger.Log.Debugf("Adding a goal node '%s'.", goalName)

	packagesGoalSet := g.buildGoalSet(packages, TypeLocalRun)
	testsGoalSet := g.buildGoalSet(tests, TypeTest)

	// Create goal node and add an edge to all requested packages
	goalNode = &PkgNode{
		State:      StateMeta,
		Type:       TypeGoal,
		SrpmPath:   NoSRPMPath,
		RpmPath:    NoRPMPath,
		SourceRepo: NoSourceRepo,
		nodeID:     g.NewNode().ID(),
		GoalName:   goalName,
	}
	goalNode.This = goalNode

	err = g.safeAddNode(goalNode)
	if err != nil {
		err = fmt.Errorf("failed to add goal node '%s': %s", goalName, err.Error())
		return
	}

	err = g.connectGoalEdges(goalNode, packagesGoalSet, strict, TypeLocalRun)
	if err != nil {
		err = fmt.Errorf("failed to connect goal node '%s' to packages: %s", goalName, err.Error())
		return
	}

	err = g.connectGoalEdges(goalNode, testsGoalSet, strict, TypeTest)
	if err != nil {
		err = fmt.Errorf("failed to connect goal node '%s' to tests: %s", goalName, err.Error())
		return
	}

	// Expand the goal node if requested
	if extraLayers > 0 {
		g.addGoalNodeLayers(goalNode, extraLayers)
	}

	return
}

// AddGoalNodeToNodes adds a goal node to the graph which links to a list of existing nodes.
func (g *PkgGraph) AddGoalNodeToNodes(goalName string, existingNodes []*PkgNode, extraLayers int) (goalNode *PkgNode, err error) {
	// Check if we already have a goal node with the requested name
	if g.FindGoalNode(goalName) != nil {
		err = fmt.Errorf("can't have two goal nodes named %s", goalName)
		return
	}

	logger.Log.Debugf("Adding a goal node '%s'.", goalName)

	// Create goal node and add an edge to all the other requested nodes
	goalNode = &PkgNode{
		State:      StateMeta,
		Type:       TypeGoal,
		SrpmPath:   NoSRPMPath,
		RpmPath:    NoRPMPath,
		SourceRepo: NoSourceRepo,
		nodeID:     g.NewNode().ID(),
		GoalName:   goalName,
	}
	goalNode.This = goalNode

	err = g.safeAddNode(goalNode)
	if err != nil {
		err = fmt.Errorf("failed to add goal node '%s': %s", goalName, err.Error())
		return
	}

	for _, node := range existingNodes {
		if !g.HasNode(node) {
			err = fmt.Errorf("can't add goal node '%s' from node '%s' which is not in the graph", goalName, node.FriendlyName())
			return nil, err
		}
		err = g.AddEdge(goalNode, node)
		if err != nil {
			err = fmt.Errorf("failed to add edge from goal node '%s' to node '%s': %s", goalName, node.FriendlyName(), err.Error())
			return nil, err
		}
	}

	// Expand the goal node if requested
	if extraLayers > 0 {
		g.addGoalNodeLayers(goalNode, extraLayers)
	}

	return
}

// addGoalNodeLayers will expand a goal node by some numbers of layers. For example, if the goaled node is "x" (i.e. the goal node
// points to "x") and extraLevels is 1, the goal node will now link to all nodes which depend on "x" as well as
// "x" itself. A node is considered to depend on "x" if it is a run node that has edges connecting it to "x"
// without any other run nodes in between.
//
//	E.g., if "y_run" -> "y_build" -> "<Some Meta Node>" -> "x_run" -> "x_build", and we are expanding from "x"
//	with layers=1, only "y_run" will be added to the goal nodes since "y_build" and "<Some Meta Node>" are not run nodes.
func (g *PkgGraph) addGoalNodeLayers(goalNode *PkgNode, layers int) {
	logger.Log.Debugf("Expanding goal node '%s' by %d layers", goalNode.GoalName, layers)

	var expandedGoalNodes []*PkgNode
	// Use a set to keep track of the nodes we already added so we can avoid processing them again
	expandedGoalNodesSet := make(map[*PkgNode]bool)

	// Start with the already selected nodes which make up the goal.
	initialGoalNodes := []*PkgNode{}
	for _, selectedNode := range graph.NodesOf(g.From(goalNode.ID())) {
		initialGoalNodes = append(initialGoalNodes, selectedNode.(*PkgNode))
	}

	// For each node in the current layer, add all of the nodes that depend on it, then repeat as many times as requested
	expandedGoalNodes = initialGoalNodes
	for i := 0; i < layers; i++ {
		expandedGoalNodes = append(expandedGoalNodes, g.getNextGoalLayer(expandedGoalNodesSet, expandedGoalNodes)...)
	}

	// Add the new edges if they are missing
	for _, expandedNode := range expandedGoalNodes {
		// Ensure we don't create a cycle by adding an edge from the goal node to itself
		if expandedNode == goalNode {
			continue
		}
		if !g.HasEdgeFromTo(goalNode.ID(), expandedNode.ID()) {
			logger.Log.Debugf("Adding edge from '%s' to '%s'", goalNode.FriendlyName(), expandedNode.FriendlyName())
			g.SetEdge(g.NewEdge(goalNode, expandedNode))
		}
	}
}

// getNextGoalLayer will return the next layer of goal nodes to expand. It will return a list of run nodes that depend on the current goal nodes.
// - expandedGoalNodesSet: A set of nodes that have already been expanded from. If a node is in this set we will skip it.
// - currentGoalNodes: The current layer of goal nodes to expand from.
//
// Returns a list of additional nodes that connect to currentGoalNodes (but not any nodes that are already in currentGoalNodes)
func (g *PkgGraph) getNextGoalLayer(expandedGoalNodesSet map[*PkgNode]bool, currentGoalNodes []*PkgNode) (expandedGoalNodes []*PkgNode) {

	// We will iterate over the current goal nodes and add all the nodes that depend on them to the expanded goal nodes.
	// The expandedGoalNodesSet will ensure we don't add the same node twice.
	for _, goalNode := range currentGoalNodes {
		if expandedGoalNodesSet[goalNode] {
			logger.Log.Tracef("Already expanded from '%s', skipping", goalNode.FriendlyName())
			continue
		} else {
			logger.Log.Debugf("Expanding goal nodes from '%s'", goalNode.FriendlyName())
			expandedGoalNodesSet[goalNode] = true
		}

		// Add all the nodes that depend on this node to the expanded goal nodes list. If the dependant node is a run
		// node we can stop expanding from it (A subsequent call to expandGoalNodesOnce() will expand from it further if
		// needed). If the dependant node is a build, meta, etc. node we need to keep expanding from it since we only
		// care about adding goals to run nodes. We ignore goal nodes since they should have no dependents, and may
		// potentially pull in unrelated parts of the graph.
		dependentNodes := graph.NodesOf(g.To(goalNode.ID()))
		for _, dependentNeighborGraphNode := range dependentNodes {
			dependentNode := dependentNeighborGraphNode.(*PkgNode)
			switch dependentNode.Type {
			case TypeLocalRun:
				fallthrough
			case TypeTest:
				logger.Log.Debugf("Adding '%s' to expanded goal nodes", dependentNode.FriendlyName())
				expandedGoalNodes = append(expandedGoalNodes, dependentNode)
			case TypeGoal:
				logger.Log.Tracef("Skipping '%s' since it is a goal node", dependentNode.FriendlyName())
			default:
				// If the node is not a run node we need to keep expanding from the non-run node.
				logger.Log.Tracef("Continuing to expand past '%s' since it is not a run node", dependentNode.FriendlyName())
				expandedGoalNodes = append(expandedGoalNodes, g.getNextGoalLayer(expandedGoalNodesSet, []*PkgNode{dependentNode})...)
			}
		}
	}
	return
}

// CreateSubGraph returns a new graph with which only contains the nodes accessible from rootNode.
func (g *PkgGraph) CreateSubGraph(rootNode *PkgNode) (subGraph *PkgGraph, err error) {
	search := traverse.DepthFirst{}
	subGraph = NewPkgGraph()

	newRootNode := rootNode
	subGraph.AddNode(newRootNode)
	search.Walk(g, rootNode, func(n graph.Node) bool {
		// Visit function of DepthFirst, called once per node

		// Add each neighbor of this node. Every connected node is guaranteed to be part of the new graph
		for _, neighbor := range graph.NodesOf(g.From(n.ID())) {
			newNeighbor := neighbor.(*PkgNode)
			if subGraph.Node(neighbor.ID()) == nil {
				// Make a copy of the node and add it to the subgraph
				subGraph.AddNode(newNeighbor)
			}

			newEdge := g.Edge(n.ID(), newNeighbor.ID())
			subGraph.SetEdge(newEdge)
		}

		// Don't stop early, visit every node
		return false
	})

	subgraphSize := subGraph.Nodes().Len()
	logger.Log.Debugf("Created sub graph with %d nodes rooted at \"%s\"", subgraphSize, rootNode.FriendlyName())

	return
}

// FindRPMFiles returns a list of all RPMs built by an SRPM and a list of these RPMs that are not available on the disk.
// The function will lock 'graphMutex' before performing the check if the mutex is not nil.
func FindRPMFiles(srpmPath string, pkgGraph *PkgGraph, graphMutex *sync.RWMutex) (expectedFiles, missingFiles []string) {
	expectedFiles = rpmsProvidedBySRPM(srpmPath, pkgGraph, graphMutex)
	logger.Log.Tracef("Expected RPMs from %s: %v", srpmPath, expectedFiles)
	missingFiles = findMissingFiles(expectedFiles)
	logger.Log.Tracef("Missing RPMs from %s: %v", srpmPath, missingFiles)
	return
}

// WriteDOTGraphFile writes the graph to a DOT graph format file
func WriteDOTGraphFile(g graph.Directed, filename string) (err error) {
	logger.Log.Infof("Writing DOT graph to %s", filename)
	f, err := os.Create(filename)
	if err != nil {
		return
	}
	defer f.Close()

	err = WriteDOTGraph(g, f)

	return
}

// ReadDOTGraphFile reads the graph from a DOT graph format file
func ReadDOTGraphFile(filename string) (outputGraph *PkgGraph, err error) {
	logger.Log.Infof("Reading DOT graph from %s", filename)

	f, err := os.Open(filename)
	if err != nil {
		return
	}
	defer f.Close()

	outputGraph = NewPkgGraph()
	err = ReadDOTGraph(outputGraph, f)

	return
}

// ReadDOTGraph de-serializes a graph from a DOT formatted object
func ReadDOTGraph(g graph.DirectedBuilder, input io.Reader) (err error) {
	bytes, err := io.ReadAll(input)
	if err != nil {
		return
	}
	err = dot.Unmarshal(bytes, g)
	return
}

// WriteDOTGraph serializes a graph into a DOT formatted object
func WriteDOTGraph(g graph.Directed, output io.Writer) (err error) {
	bytes, err := dot.Marshal(g, "dependency_graph", "", "")
	if err != nil {
		return
	}
	_, err = output.Write(bytes)
	return
}

// DeepCopy returns a deep copy of the receiver.
// On error, the returned deepCopy is in an invalid state
func (g *PkgGraph) DeepCopy() (deepCopy *PkgGraph, err error) {
	var buf bytes.Buffer
	err = WriteDOTGraph(g, &buf)
	if err != nil {
		return
	}
	deepCopy = NewPkgGraph()
	err = ReadDOTGraph(deepCopy, &buf)
	return
}

func (g *PkgGraph) MakeDAG() (err error) {
	return g.MakeDAGUsingUpstreamRepos(false, false, nil)
}

// MakeDAGUsingUpstreamRepos ensures the graph is a directed acyclic graph (DAG).
// If the graph is not a DAG, this routine will attempt to resolve any cycles using RPMs in the PMC to make the graph a DAG.
func (g *PkgGraph) MakeDAGUsingUpstreamRepos(resolveCyclesFromUpstream, ignoreVersionToResolveSelfDep bool, cloner *rpmrepocloner.RpmRepoCloner) (err error) {
	timestamp.StartEvent("convert to DAG", nil)
	defer timestamp.StopEvent(nil)
	var cycle []*PkgNode

	for {
		cycle, err = g.FindAnyDirectedCycle()
		if err != nil || len(cycle) == 0 {
			return
		}

		err = g.fixCycle(cycle, resolveCyclesFromUpstream, ignoreVersionToResolveSelfDep, cloner)
		if err != nil {
			return formatCycleErrorMessage(cycle, err)
		}
	}
}

// Copy returns a copy of a PkgNode. The ID of the copy is NOT unique.
func (n *PkgNode) Copy() (copy *PkgNode) {
	copy = &PkgNode{
		nodeID:       n.nodeID,
		VersionedPkg: n.VersionedPkg,
		State:        n.State,
		Type:         n.Type,
		SrpmPath:     n.SrpmPath,
		RpmPath:      n.RpmPath,
		SpecPath:     n.SpecPath,
		SourceDir:    n.SourceDir,
		Architecture: n.Architecture,
		SourceRepo:   n.SourceRepo,
		Implicit:     n.Implicit,
	}
	copy.This = copy
	return
}

// CloneNode creates a clone of the input node with a new, unique ID.
// The clone doesn't have any edges attached to it.
func (g *PkgGraph) CloneNode(pkgNode *PkgNode) (newNode *PkgNode) {
	newNode = pkgNode.Copy()
	newNode.nodeID = g.NewNode().ID()
	newNode.This = newNode

	return
}

// allNodesOfType returns a list of all non-null nodes returned by the getter.
func (g *PkgGraph) allNodesOfType(nodeGetter func(node *LookupNode) *PkgNode) []*PkgNode {
	count := 0
	for _, list := range g.lookupTable() {
		count += len(list)
	}

	nodes := make([]*PkgNode, 0, count)
	for _, list := range g.lookupTable() {
		for _, n := range list {
			if node := nodeGetter(n); node != nil {
				nodes = append(nodes, node)
			}
		}
	}

	return nodes
}

// buildGoalSet returns a set of package versions that are the goal of the graph.
func (g *PkgGraph) buildGoalSet(packageVers []*pkgjson.PackageVer, nodeType NodeType) (goalSet map[*pkgjson.PackageVer]bool) {
	if len(packageVers) > 0 {
		logger.Log.Debugf("Adding a goal for selected nodes of type '%s': %v", nodeType, packageVers)

		goalSet = make(map[*pkgjson.PackageVer]bool)
		for _, pkg := range packageVers {
			logger.Log.Tracef("\t%s-%s", pkg.Name, pkg.Version)
			goalSet[pkg] = true
		}
	} else {
		logger.Log.Debugf("Adding a goal for all nodes of type '%s'", nodeType)

		if nodeType == TypeTest {
			goalSet = pkgNodesListToPackageVerSet(g.AllTestNodes())
		} else {
			goalSet = pkgNodesListToPackageVerSet(g.AllPreferredRunNodes())
		}
	}

	if logger.Log.IsLevelEnabled(logrus.TraceLevel) {
		for node := range goalSet {
			logger.Log.Tracef("\t%s-%s", node.Name, node.Version)
		}
	}

	return
}

func (g *PkgGraph) connectGoalEdges(goalNode *PkgNode, goalSet map[*pkgjson.PackageVer]bool, strict bool, nodeType NodeType) (err error) {
	for pkg := range goalSet {
		var existingNode *PkgNode = nil
		// Try to find an exact match first (to make sure we match revision number exactly, if available)
		nodeLookup, err := g.FindExactPkgNodeFromPkg(pkg)
		if err != nil {
			return err
		}
		if nodeLookup == nil {
			// Try again with a more general search
			nodeLookup, err = g.FindBestPkgNode(pkg)
			if err != nil {
				return err
			}
		}

		if nodeLookup != nil {
			switch nodeType {
			case TypeLocalRun:
				existingNode = nodeLookup.RunNode
			case TypeTest:
				existingNode = nodeLookup.TestNode
			default:
				return fmt.Errorf("unexpected node type to connect with a goal node: %s", nodeType)
			}
		}

		if existingNode == nil {
			if strict {
				return fmt.Errorf("could not find all goal nodes with strict=true (missing %+v)", pkg)
			}

			logger.Log.Warnf("Could not goal package %+v", pkg)
			continue
		}

		logger.Log.Tracef("Found %s to satisfy %s", existingNode, pkg)

		err = g.AddEdge(goalNode, existingNode)
		if err != nil {
			return err
		}
	}

	return
}

// fixCycle attempts to fix a cycle. Cycles may be acceptable if:
// - all nodes are from the same spec file or
// - at least one of the nodes of the cycle represents a pre-built SRPM.
func (g *PkgGraph) fixCycle(cycle []*PkgNode, resolveCyclesFromUpstream, ignoreVersionToResolveSelfDep bool, cloner *rpmrepocloner.RpmRepoCloner) (err error) {
	logger.Log.Debugf("Found cycle: %v", cycle)

	// Omit the first element of the cycle, since it is repeated as the last element
	trimmedCycle := cycle[1:]

	err = g.fixIntraSpecCycle(trimmedCycle)
	if err == nil {
		return
	}

	return g.fixCyclesWithExistingRPMS(trimmedCycle, resolveCyclesFromUpstream, ignoreVersionToResolveSelfDep, cloner)
}

// fixIntraSpecCycle attempts to fix a cycle if none of the cycle nodes are build nodes.
// If a cycle can be fixed an additional meta node will be added to represent the interdependencies of the cycle.
func (g *PkgGraph) fixIntraSpecCycle(trimmedCycle []*PkgNode) (err error) {
	logger.Log.Debug("Checking if cycle contains build nodes.")

	for _, currentNode := range trimmedCycle {
		if currentNode.Type == TypeLocalBuild {
			logger.Log.Debug("Cycle contains build dependencies, cannot be solved this way.")
			return fmt.Errorf("cycle contains build dependencies, unresolvable")
		}
	}

	// Breaking the cycle by removing all edges between in-cycle nodes.
	// Their dependency on each other will be reflected by a new meta node.
	logger.Log.Debugf("Breaking cycle edges.")
	cycleLength := len(trimmedCycle)
	for i, currentNode := range trimmedCycle {
		currentNodeID := currentNode.ID()
		for j := i + 1; j < cycleLength; j++ {
			nextNode := trimmedCycle[j]
			nextNodeID := nextNode.ID()

			if g.Edge(currentNodeID, nextNodeID) != nil {
				logger.Log.Tracef("\t'%s' -> '%s'", currentNode.FriendlyName(), nextNode.FriendlyName())
				g.RemoveEdge(currentNodeID, nextNodeID)
			}

			if g.Edge(nextNodeID, currentNodeID) != nil {
				logger.Log.Tracef("\t'%s' -> '%s'", nextNode.FriendlyName(), currentNode.FriendlyName())
				g.RemoveEdge(nextNodeID, currentNodeID)
			}
		}
	}

	// For each cycle node move any dependencies from a non-cycle node to a new
	// meta node, then have the meta node depend on all cycle nodes.
	groupedDependencies := make(map[int64]bool)
	for _, currentNode := range trimmedCycle {
		logger.Log.Debugf("Breaking NON-cycle edges connected to cycle node '%s'.", currentNode.FriendlyName())

		currentNodeID := currentNode.ID()

		toNodes := g.To(currentNodeID)
		for toNodes.Next() {
			toNode := toNodes.Node().(*PkgNode)
			toNodeID := toNode.ID()

			logger.Log.Tracef("\t'%s' -> '%s'", toNode.FriendlyName(), currentNode.FriendlyName())

			groupedDependencies[toNodeID] = true
			g.RemoveEdge(toNodeID, currentNodeID)
		}
	}

	// Convert the IDs back into actual nodes
	dependencyNodes := make([]*PkgNode, 0, len(groupedDependencies))
	for id := range groupedDependencies {
		dependencyNodes = append(dependencyNodes, g.Node(id).(*PkgNode).This)
	}

	g.AddMetaNode(dependencyNodes, trimmedCycle)

	return
}

func (g *PkgGraph) replaceSRPMBuildDependency(replacedNode, newNode *PkgNode, dependencySRPMPath string) (err error) {
	parentNodes := g.To(replacedNode.ID())
	for parentNodes.Next() {
		parentNode := parentNodes.Node().(*PkgNode)
		if parentNode.Type == TypeLocalBuild && parentNode.SrpmPath == dependencySRPMPath {
			g.RemoveEdge(parentNode.ID(), replacedNode.ID())

			err = g.AddEdge(parentNode, newNode)
			if err != nil {
				logger.Log.Errorf("Adding edge failed for %v -> %v.", parentNode, newNode)
				return
			}
		}
	}

	logger.Log.Infof("Successful. Updated dependency for nodes depending on '%s'.", replacedNode.FriendlyName())
	return
}

func (g *PkgGraph) cloneAndReplaceRunToRemote(runNode *PkgNode, buildNodeToUpdate *PkgNode) (err error) {
	// Mark node as unresolved remote to be fetched by the package fetcher
	upstreamAvailableNode, err := g.AddRemoteUnresolvedNode(runNode.VersionedPkg)
	if err != nil {
		return fmt.Errorf("failed to add a remote node:\n%w", err)
	}

	logger.Log.Debugf("Added a 'Remote' node '%s' with ID %d.", upstreamAvailableNode.FriendlyName(), upstreamAvailableNode.ID())
	return g.replaceSRPMBuildDependency(runNode, upstreamAvailableNode, buildNodeToUpdate.SrpmPath)
}

// fixCyclesWithExistingRPMS attempts to fix a cycle if at least one node is a pre-built. It also searches upstream RPMS when the flag RESOLVE_CYCLES_FROM_UPSTREAM is enabled
// If a cycle can be fixed, edges representing the build dependencies of the pre-built/available-upstream node will be removed.
func (g *PkgGraph) fixCyclesWithExistingRPMS(trimmedCycle []*PkgNode, resolveCyclesFromUpstream, ignoreVersionToResolveSelfDep bool, cloner *rpmrepocloner.RpmRepoCloner) (err error) {
	logger.Log.Debug("Checking if cycle contains pre-built SRPMs.")

	var cycleStringBuilder strings.Builder

	fmt.Fprintf(&cycleStringBuilder, "{%s}", trimmedCycle[0].FriendlyName())
	for _, node := range trimmedCycle[1:] {
		fmt.Fprintf(&cycleStringBuilder, " --> {%s}", node.FriendlyName())
	}
	logger.Log.Infof("Trying to fix circular dependency found:\t%s", cycleStringBuilder.String())

	currentNode := trimmedCycle[len(trimmedCycle)-1]
	for _, previousNode := range trimmedCycle {
		// Why we're targetting only "build node -> run node" edges:
		// 1. Explicit package rebuilds create an edge between the goal node and an SRPM's run nodes.
		//    Considering that, we avoid accidentally skipping a rebuild by only removing edges between a build and a run node.
		// 2. Every build cycle must contain at least one edge between a build node and a run node from different SRPMs.
		//    These edges represent the 'BuildRequires' from the .spec file. If the cycle is breakable, the run node comes from a pre-built SRPM.
		buildToRunEdge := previousNode.Type == TypeLocalBuild && currentNode.Type == TypeLocalRun
		if !buildToRunEdge {
			currentNode = previousNode
			continue
		}
		if _, missingRPMs := FindRPMFiles(currentNode.SrpmPath, g, nil); len(missingRPMs) == 0 {
			logger.Log.Debugf("Cycle contains pre-built SRPM '%s'. Replacing edges from build nodes associated with '%s' with an edge to a new 'PreBuilt' node.",
				currentNode.SrpmPath, previousNode.SrpmPath)

			preBuiltNode := g.CloneNode(currentNode)
			preBuiltNode.State = StateUpToDate
			preBuiltNode.Type = TypePreBuilt

			logger.Log.Debugf("Adding a 'PreBuilt' node '%s' with id %d.", preBuiltNode.FriendlyName(), preBuiltNode.ID())

			err = g.replaceSRPMBuildDependency(currentNode, preBuiltNode, previousNode.SrpmPath)
			if err != nil {
				return fmt.Errorf("failed to replace a circular build dependency:\n%w", err)
			}

			return
		}
		if resolveCyclesFromUpstream {
			cycleResolved, err := g.tryReplaceLocalNodeWithUpstream(currentNode, previousNode, false, cloner)
			if err != nil {
				return fmt.Errorf("failed while trying to break a cycle with an upstream package:\n%w", err)
			}

			if cycleResolved {
				return nil
			}
		}
		currentNode = previousNode
	}

	if ignoreVersionToResolveSelfDep && resolveCyclesFromUpstream {
		logger.Log.Debug("Trying to resolve cycle by searching packages in PMC after ignoring package version.")

		currentNode = trimmedCycle[len(trimmedCycle)-1]
		for _, previousNode := range trimmedCycle {
			buildToRunEdge := previousNode.Type == TypeLocalBuild && currentNode.Type == TypeLocalRun
			if !buildToRunEdge {
				continue
			}

			cycleResolved, err := g.tryReplaceLocalNodeWithUpstream(currentNode, previousNode, true, cloner)
			if err != nil {
				return fmt.Errorf("failed while trying to break a cycle with an upstream package:\n%w", err)
			}

			if cycleResolved {
				return nil
			}

			currentNode = previousNode
		}
	}

	return fmt.Errorf("cycle can't be resolved with prebuilt/PMC RPMs. Unresolvable")
}

// removePkgNodeFromLookup removes a node from the lookup tables.
func (g *PkgGraph) removePkgNodeFromLookup(pkgNode *PkgNode) {
	pkgName := pkgNode.VersionedPkg.Name
	lookupSlice := g.lookupTable()[pkgName]

	for i, lookupNode := range lookupSlice {
		if lookupNode.BuildNode == pkgNode || lookupNode.RunNode == pkgNode || lookupNode.TestNode == pkgNode {
			g.lookupTable()[pkgName] = append(lookupSlice[:i], lookupSlice[i+1:]...)
			break
		}
	}
}

// safeAddNode catches panics from adding nodes to the graph and converts them to errors.
func (g *PkgGraph) safeAddNode(pkgNode *PkgNode) (err error) {
	defer func() {
		if r := recover(); r != nil {
			err = fmt.Errorf("adding the (%v) node failed:\n%s", pkgNode, r)
		}
	}()

	g.AddNode(pkgNode)

	return
}

func formatCycleErrorMessage(cycle []*PkgNode, err error) error {
	var cycleStringBuilder strings.Builder

	fmt.Fprintf(&cycleStringBuilder, "{%s}", cycle[0].FriendlyName())
	for _, node := range cycle[1:] {
		fmt.Fprintf(&cycleStringBuilder, " --> {%s}", node.FriendlyName())
	}
	logger.Log.Errorf("Unfixable circular dependency found:\t%s\terror: %s", cycleStringBuilder.String(), err)

	// Hydrating the toolchain RPMs was required to resolve the cycles at one point. This is no longer the case, but
	// we should leave a message here to avoid confusion.
	logger.Log.Warn("╔════════════════════════════════════════════════════════════════════════════════════════════════╗")
	logger.Log.Warn("║ 'copy-toolchain-rpms' should no longer be required to resolve cycles even when using online    ║")
	logger.Log.Warn("║ toolchain rpms. If you see this message, there is likely a legitimate cycle in the dependency  ║")
	logger.Log.Warn("║ graph.                                                                                         ║")
	logger.Log.Warn("╚════════════════════════════════════════════════════════════════════════════════════════════════╝")

	return fmt.Errorf("cycles detected in dependency graph")
}

// pkgNodesListToPackageVerSet converts a list of "*PkgNode" elements to a set of "*PackageVer" elements.
func pkgNodesListToPackageVerSet(nodes []*PkgNode) (packageVerSet map[*pkgjson.PackageVer]bool) {
	packageVerSet = make(map[*pkgjson.PackageVer]bool)
	for _, node := range nodes {
		packageVerSet[node.VersionedPkg] = true
	}

	return
}

// rpmsProvidedBySRPM returns all RPMs produced from a SRPM file.
func rpmsProvidedBySRPM(srpmPath string, pkgGraph *PkgGraph, graphMutex *sync.RWMutex) (rpmFiles []string) {
	if graphMutex != nil {
		graphMutex.RLock()
		defer graphMutex.RUnlock()
	}

	filteredNodes := pkgGraph.NodesMatchingFilter(func(node *PkgNode) bool {
		return (node.SrpmPath == srpmPath) &&
			(node.RpmPath != "") &&
			(node.RpmPath != NoRPMPath)
	})

	rpmsMap := make(map[string]bool)
	for _, node := range filteredNodes {
		rpmsMap[node.RpmPath] = true
	}

	rpmFiles = sliceutils.SetToSlice(rpmsMap)

	return
}

// findMissingFiles returns a list of files missing on disk.
//
// Also returns a list of all missing files.
func findMissingFiles(filePaths []string) (missingFiles []string) {
	for _, filePath := range filePaths {
		isFile, _ := file.IsFile(filePath)

		if !isFile {
			logger.Log.Debugf("Did not find (%s)", filePath)
			missingFiles = append(missingFiles, filePath)
		}
	}

	return
}

func (g *PkgGraph) tryReplaceLocalNodeWithUpstream(currentNode, previousNode *PkgNode, ignoreVersionToResolveSelfDep bool, cloner *rpmrepocloner.RpmRepoCloner) (isCycleBroken bool, err error) {
	isAvailableUpstream := isPackageAvailableUpsream(currentNode.VersionedPkg, ignoreVersionToResolveSelfDep, cloner)
	if !isAvailableUpstream {
		return false, nil
	}

	logger.Log.Debugf("Cycle contains a dependency '%s' that is available in upstream repo. Replacing edges from build nodes associated with '%s' with an edge to a new remote unresolved node.", currentNode.FriendlyName(), previousNode.SRPMFileName())

	err = g.cloneAndReplaceRunToRemote(currentNode, previousNode)
	if err != nil {
		return false, err
	}

	return true, nil
}

// isPackageAvailableUpsream returns true if a package is found in the upstream repository.
//
// This is used to check if an RPM is available in the repository before starting a build.
func isPackageAvailableUpsream(packageVer *pkgjson.PackageVer, ignoreVersionToResolveSelfDep bool, cloner *rpmrepocloner.RpmRepoCloner) (isAvailableUpstream bool) {
	if ignoreVersionToResolveSelfDep {
		packageVer = &pkgjson.PackageVer{Name: packageVer.Name}
	}

	// Cloner errors are not fatal - may return one when the RPM is not found.
	foundPackages, err := cloner.WhatProvides(packageVer)
	if err != nil {
		logger.Log.Debugf("Error while checking if package (%v) is available upstream: %s", packageVer, err)
		return
	}

	return len(foundPackages) > 0
}
