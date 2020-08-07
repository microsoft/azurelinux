// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package pkggraph

import (
	"bytes"
	"encoding/base64"
	"encoding/gob"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"sort"
	"sync"

	"gonum.org/v1/gonum/graph"
	"gonum.org/v1/gonum/graph/encoding"
	"gonum.org/v1/gonum/graph/encoding/dot"
	"gonum.org/v1/gonum/graph/simple"
	"gonum.org/v1/gonum/graph/traverse"

	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkgjson"
	"microsoft.com/pkggen/internal/versioncompare"
)

// NodeState indicates if a node is a package node (build, upToDate,unresolved,cached) or a meta node (meta)
type NodeState int

// Valid values for NodeState type
const (
	StateUnknown    NodeState = iota        // Unknown state
	StateMeta       NodeState = iota        // Meta nodes do not represent actual build artifacts, but additional nodes used for managing dependencies
	StateBuild      NodeState = iota        // A package from a local SRPM which should be built from source
	StateUpToDate   NodeState = iota        // A local RPM is already built and is available
	StateUnresolved NodeState = iota        // A dependency is not available locally and must be acquired from a remote repo
	StateCached     NodeState = iota        // A dependency was not available locally, but is now available in the chache
	StateMAX        NodeState = StateCached // Max allowable state
)

// NodeType indicates the general node type (build, run, goal, remote).
type NodeType int

// Valid values for NodeType type
const (
	TypeUnknown  NodeType = iota         // Unknown type
	TypeBuild    NodeType = iota         // Package can be build if all dependency edges are satisfied
	TypeRun      NodeType = iota         // Package can be run if all dependency edges are satisfied. Will be associated with a partner build node
	TypeGoal     NodeType = iota         // Meta node which depends on a user selected subset of packages to be built.
	TypeRemote   NodeType = iota         // A non-local node which may have a cache entry
	TypePureMeta NodeType = iota         // An arbitrary meta node with no other meaning
	TypeMAX      NodeType = TypePureMeta // Max allowable type
)

// Dot encoding/decoding keys
const (
	dotKeyNodeInBase64 = "NodeInBase64"
	dotKeySRPM         = "SRPM"
	dotKeyColor        = "fillcolor"
	dotKeyFill         = "style"
)

// PkgNode represents a package.
type PkgNode struct {
	nodeID       int64               // Unique ID for the node
	VersionedPkg *pkgjson.PackageVer // JSON derived structure holding the exact version information for a graph
	State        NodeState           // The current state of the node (ie needs to be build, up-to-date, cached, etc)
	Type         NodeType            // The purpose of the node (build, run , meta goal, etc)
	SrpmPath     string              // SRPM file used to generate this package (likely shared with multiple other nodes)
	SpecPath     string              // The SPEC file extracted from the SRPM
	SourceDir    string              // The directory containing extracted sources from the SRPM
	Architecture string              // The architecture of the resulting package built.
	SourceRepo   string              // The location this package was acquired from
	GoalName     string              // Optional string for goal nodes
	This         *PkgNode            // Self reference since the graph library returns nodes by value, not reference
}

// ID implements the graph.Node interface, returns the node's unique ID
func (n PkgNode) ID() int64 {
	return n.nodeID
}

//PkgGraph implements a simple.DirectedGraph using pkggraph Nodes.
type PkgGraph struct {
	*simple.DirectedGraph
	nodeLookup map[string][]*LookupNode
}

//LookupNode represents a graph node for a package in the lookup list
type LookupNode struct {
	RunNode   *PkgNode // The "meta" run node for a package. Tracks the run-time dependencies for the package. Remote packages will only have a RunNode.
	BuildNode *PkgNode // The build node for a package. Tracks the build requirements for the package. May be nil for remote packages.
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
	case StateUpToDate:
		return "UpToDate"
	case StateUnresolved:
		return "Unresolved"
	case StateCached:
		return "Cached"
	default:
		logger.Log.Panic("Invalid NodeState encountered when serializing to string!")
		return "error"
	}
}

func (n NodeType) String() string {
	switch n {
	case TypeBuild:
		return "Build"
	case TypeRun:
		return "Run"
	case TypeGoal:
		return "Goal"
	case TypeRemote:
		return "Remote"
	case TypePureMeta:
		return "PureMeta"
	default:
		logger.Log.Panic("Invalid NodeType encountered when serializing to string!")
		return "error"
	}
}

//DOTColor returns the graphviz color to set a node to
func (n *PkgNode) DOTColor() string {
	switch n.State {
	case StateMeta:
		if n.Type == TypeGoal {
			return "deeppink"
		}
		return "aquamarine"
	case StateBuild:
		return "gold"
	case StateUpToDate:
		return "forestgreen"
	case StateUnresolved:
		return "crimson"
	case StateCached:
		return "darkorchid"
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

	// Scan all nodes, start with only the run nodes to properly initialize the lookup structures
	// (they always expect a run node to be present)
	for _, n := range graph.NodesOf(g.Nodes()) {
		pkgNode := n.(*PkgNode)
		if pkgNode.Type == TypeRun || pkgNode.Type == TypeRemote {
			g.addToLookup(pkgNode, true)
		}
	}

	// Now run again for any build nodes, or other nodes we want to track
	for _, n := range graph.NodesOf(g.Nodes()) {
		pkgNode := n.(*PkgNode)
		if pkgNode.Type != TypeRun && pkgNode.Type != TypeRemote {
			g.addToLookup(pkgNode, true)
		}
	}

	// Sort each of the lookup lists from lowest version to highest version. The RunNode is always guaranteed to be
	// a valid reference while BuildNode may be nil.
	for idx := range g.nodeLookup {
		// Validate the lookup table is well formed. Pure meta nodes created by cycles may, in some cases, create
		// build nodes which have no associated run node after passing into a subgraph. (The subgraph only requires
		// one of the cycle members but will get all of their build nodes)
		endOfValidData := 0
		for _, n := range g.nodeLookup[idx] {
			if n.RunNode != nil {
				g.nodeLookup[idx][endOfValidData] = n
				endOfValidData++
			} else {
				logger.Log.Debugf("Lookup for %s has no run node, lost in a cycle fix? Removing it", idx)
				g.RemoveNode(n.BuildNode.ID())
			}
		}
		// Prune off the invalid entries at the end of the slice
		g.nodeLookup[idx] = g.nodeLookup[idx][:endOfValidData]

		sort.Slice(g.nodeLookup[idx], func(i, j int) bool {
			intervalI, _ := g.nodeLookup[idx][i].RunNode.VersionedPkg.Interval()
			intervalJ, _ := g.nodeLookup[idx][j].RunNode.VersionedPkg.Interval()
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
	var (
		haveDuplicateNode bool = false
	)

	// Only add run, remote, or build nodes to lookup
	if pkgNode.Type != TypeBuild && pkgNode.Type != TypeRun && pkgNode.Type != TypeRemote {
		err = fmt.Errorf("%s has invalid type for lookup", pkgNode)
		return
	}

	// Check for existing lookup entries which conflict
	existingLookup, err := g.FindExactPkgNodeFromPkg(pkgNode.VersionedPkg)
	if err != nil {
		return
	}
	if existingLookup != nil {
		switch pkgNode.Type {
		case TypeBuild:
			haveDuplicateNode = existingLookup.BuildNode != nil
		case TypeRemote:
			// For the purposes of lookup, a "Remote" node provides the same utility as a "Run" node
			fallthrough
		case TypeRun:
			haveDuplicateNode = existingLookup.RunNode != nil
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
	if pkgNode.Type != TypeRemote {
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
	var (
		duplicateError = fmt.Errorf("already have a lookup entry for %s", pkgNode)
	)

	// We only care about run/build nodes or remote dependencies
	if pkgNode.Type != TypeBuild && pkgNode.Type != TypeRun && pkgNode.Type != TypeRemote {
		logger.Log.Tracef("Skipping %+v, not valid for lookup", pkgNode)
		return
	}

	_, err = g.validateNodeForLookup(pkgNode)
	if err != nil {
		return
	}

	var existingLookup *LookupNode
	logger.Log.Tracef("Adding %+v to lookup", pkgNode)
	// Get the existing package lookup, or create it
	pkgName := pkgNode.VersionedPkg.Name

	existingLookup, err = g.FindExactPkgNodeFromPkg(pkgNode.VersionedPkg)
	if err != nil {
		return err
	}
	if existingLookup == nil {
		if (!deferSort) && pkgNode.Type == TypeBuild {
			err = fmt.Errorf("can't add %s, no corresponding run node found and not defering sort", pkgNode)
			return
		}
		existingLookup = &LookupNode{nil, nil}
		g.lookupTable()[pkgName] = append(g.lookupTable()[pkgName], existingLookup)
	}

	switch pkgNode.Type {
	case TypeBuild:
		if existingLookup.BuildNode == nil {
			existingLookup.BuildNode = pkgNode.This
		} else {
			err = duplicateError
			return
		}
	case TypeRemote:
		// For the purposes of lookup, a "Remote" node provides the same utility as a "Run" node
		fallthrough
	case TypeRun:
		if existingLookup.RunNode == nil {
			existingLookup.RunNode = pkgNode.This
		} else {
			err = duplicateError
			return
		}
	}

	// Sort the updated list unless we are defering until all nodes are added
	if !deferSort {
		sort.Slice(g.lookupTable()[pkgName], func(i, j int) bool {
			intervalI, _ := g.lookupTable()[pkgName][i].RunNode.VersionedPkg.Interval()
			intervalJ, _ := g.lookupTable()[pkgName][j].RunNode.VersionedPkg.Interval()
			return intervalI.Compare(&intervalJ) < 0
		})
	}
	return
}

// NewNode creates a new pkggraph Node for the graph
func (g *PkgGraph) NewNode() graph.Node {
	node := g.DirectedGraph.NewNode()
	pkgNode := &PkgNode{nodeID: node.ID()}
	pkgNode.This = pkgNode
	return pkgNode
}

// AddPkgNode adds a new node to the package graph. Run, Build, and Unresolved nodes are recorded in the lookup table.
func (g *PkgGraph) AddPkgNode(versionedPkg *pkgjson.PackageVer, nodestate NodeState, nodeType NodeType, srpmPath, specPath, sourceDir, architecture, sourceRepo string) (newNode *PkgNode, err error) {
	newNode = &PkgNode{
		nodeID:       g.NewNode().ID(),
		VersionedPkg: versionedPkg,
		State:        nodestate,
		Type:         nodeType,
		SrpmPath:     srpmPath,
		SpecPath:     specPath,
		SourceDir:    sourceDir,
		Architecture: architecture,
		SourceRepo:   sourceRepo,
	}
	newNode.This = newNode

	// g.AddNode will panic on error (such as duplicate node IDs)
	defer func() {
		if r := recover(); r != nil {
			err = fmt.Errorf("adding node failed for %s", newNode.FriendlyName())
		}
	}()
	// Make sure the lookup table is initialized before we start (otherwise it will try to 'fix' orphaned build nodes by removing them)
	g.lookupTable()
	g.AddNode(newNode)

	// Register the package with the lookup table if needed
	err = g.addToLookup(newNode, false)

	return
}

// FindDoubleConditionalPkgNodeFromPkg has the same behavior as FindConditionalPkgNodeFromPkg but supports two conditionals
func (g *PkgGraph) FindDoubleConditionalPkgNodeFromPkg(pkgVer *pkgjson.PackageVer) (lookupEntry *LookupNode, err error) {
	var (
		requestInterval, nodeInterval pkgjson.PackageVerInterval
	)
	requestInterval, err = pkgVer.Interval()
	if err != nil {
		return
	}

	packageNodes := g.lookupTable()[pkgVer.Name]
	for _, node := range packageNodes {
		if node.RunNode == nil {
			err = fmt.Errorf("found orphaned build node '%s' for name '%s'", node.BuildNode, pkgVer.Name)
			return
		}

		nodeInterval, err = node.RunNode.VersionedPkg.Interval()
		if err != nil {
			return
		}

		if nodeInterval.Satisfies(&requestInterval) {
			// Keep going, we want the highest version which satisfies both conditionals
			lookupEntry = node
		}
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
		if node.RunNode == nil {
			err = fmt.Errorf("found orphaned build node %s for name %s", node.BuildNode, pkgVer.Name)
			return
		}

		nodeInterval, err = node.RunNode.VersionedPkg.Interval()
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
func (g *PkgGraph) AllRunNodes() []*PkgNode {
	count := 0
	for _, list := range g.lookupTable() {
		count += len(list)
	}

	nodes := make([]*PkgNode, 0, count)
	for _, list := range g.lookupTable() {
		for _, n := range list {
			if n.RunNode != nil {
				nodes = append(nodes, n.RunNode)
			}
		}
	}

	return nodes
}

// AllBuildNodes returns a list of all build nodes in the graph
func (g *PkgGraph) AllBuildNodes() []*PkgNode {
	count := 0
	for _, list := range g.lookupTable() {
		count += len(list)
	}

	nodes := make([]*PkgNode, 0, count)
	for _, list := range g.lookupTable() {
		for _, n := range list {
			if n.BuildNode != nil {
				nodes = append(nodes, n.BuildNode)
			}
		}
	}

	return nodes
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
	case TypeBuild:
		return fmt.Sprintf("%s-%s-BUILD<%s>", n.VersionedPkg.Name, n.VersionedPkg.Version, n.State.String())
	case TypeRun:
		return fmt.Sprintf("%s-%s-RUN<%s>", n.VersionedPkg.Name, n.VersionedPkg.Version, n.State.String())
	case TypeRemote:
		ver1 := fmt.Sprintf("%s%s", n.VersionedPkg.Condition, n.VersionedPkg.Version)
		ver2 := ""
		if len(n.VersionedPkg.SCondition) > 0 || len(n.VersionedPkg.SVersion) > 0 {
			ver2 = fmt.Sprintf("%s,%s%s", ver1, n.VersionedPkg.SCondition, n.VersionedPkg.SVersion)
		}
		return fmt.Sprintf("%s-%s-REMOTE<%s>", n.VersionedPkg.Name, ver2, n.State.String())
	case TypeGoal:
		return fmt.Sprintf("%s", n.GoalName)
	case TypePureMeta:
		return fmt.Sprintf("Meta(%d)", n.ID())
	default:
		return "UNKNOWN NODE TYPE"
	}
}

func (n *PkgNode) String() string {
	var version, name string
	if n.Type == TypeGoal {
		name = n.GoalName
	} else if n.VersionedPkg != nil {
		name = n.VersionedPkg.Name
		version = fmt.Sprintf("%s%s,%s%s", n.VersionedPkg.Condition, n.VersionedPkg.Version, n.VersionedPkg.SCondition, n.VersionedPkg.SVersion)
	} else {
		name = "<NO NAME>"
	}

	return fmt.Sprintf("%s(%s):<ID:%d Type:%s State:%s> from '%s' in '%s'", name, version, n.nodeID, n.Type.String(), n.State.String(), n.SrpmPath, n.SourceRepo)
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
		n.SpecPath == otherNode.SpecPath &&
		n.SourceDir == otherNode.SourceDir &&
		n.Architecture == otherNode.Architecture &&
		n.SourceRepo == otherNode.SourceRepo &&
		n.GoalName == otherNode.GoalName
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

	for _, n := range to {
		toEdge := g.NewEdge(metaNode, n)
		g.SetEdge(toEdge)
	}

	for _, n := range from {
		toEdge := g.NewEdge(n, metaNode)
		g.SetEdge(toEdge)
	}

	return
}

// AddGoalNode adds a goal node to the graph which links to existing nodes. An empty package list will add an edge to all nodes
func (g *PkgGraph) AddGoalNode(goalName string, packages []*pkgjson.PackageVer, strict bool) (goalNode *PkgNode, err error) {
	// Check if we already have a goal node with the requested name
	if g.FindGoalNode(goalName) != nil {
		err = fmt.Errorf("can't have two goal nodes named %s", goalName)
		return
	}

	goalSet := make(map[*pkgjson.PackageVer]bool)
	if len(packages) > 0 {
		logger.Log.Infof("Adding \"%s\" goal", goalName)
		for _, pkg := range packages {
			logger.Log.Tracef("\t%s-%s", pkg.Name, pkg.Version)
			goalSet[pkg] = true
		}
	} else {
		logger.Log.Infof("Adding \"%s\" goal for all nodes", goalName)
		for _, node := range g.AllRunNodes() {
			logger.Log.Tracef("\t%s-%s %d", node.VersionedPkg.Name, node.VersionedPkg.Version, node.ID())
			goalSet[node.VersionedPkg] = true
		}
	}

	// Handle failures in SetEdge() and AddNode()
	defer func() {
		if r := recover(); r != nil {
			logger.Log.Panicf("Adding edge failed for goal node.")
		}
	}()

	// Create goal node and add an edge to all requested packages
	goalNode = &PkgNode{
		State:      StateMeta,
		Type:       TypeGoal,
		SrpmPath:   "<NO_SRPM_PATH>",
		SourceRepo: "<NO_REPO>",
		nodeID:     g.NewNode().ID(),
		GoalName:   goalName,
	}
	goalNode.This = goalNode
	g.AddNode(goalNode)

	for pkg := range goalSet {
		var existingNode *LookupNode
		// Try to find an exact match first (to make sure we match revision number exactly, if available)
		existingNode, err = g.FindExactPkgNodeFromPkg(pkg)
		if err != nil {
			return
		}
		if existingNode == nil {
			// Try again with a more general search
			existingNode, err = g.FindBestPkgNode(pkg)
			if err != nil {
				return
			}
		}

		if existingNode != nil {
			logger.Log.Debugf("Found %s to satisfy %s", existingNode.RunNode, pkg)
			goalEdge := g.NewEdge(goalNode, existingNode.RunNode)
			g.SetEdge(goalEdge)
			goalSet[pkg] = false
		} else {
			logger.Log.Warnf("Could not goal package %+v", pkg)
			if strict {
				logger.Log.Warnf("Missing %+v", pkg)
				err = fmt.Errorf("could not find all goal nodes with strict=true")
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
func ReadDOTGraphFile(g graph.DirectedBuilder, filename string) (err error) {
	logger.Log.Infof("Reading DOT graph from %s", filename)

	f, err := os.Open(filename)
	if err != nil {
		return err
	}
	defer f.Close()

	err = ReadDOTGraph(g, f)

	return
}

// ReadDOTGraph de-serializes a graph from a DOT formatted object
func ReadDOTGraph(g graph.DirectedBuilder, input io.Reader) (err error) {
	bytes, err := ioutil.ReadAll(input)
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
