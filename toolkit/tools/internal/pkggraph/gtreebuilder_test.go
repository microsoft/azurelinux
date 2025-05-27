// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package pkggraph

import (
	"strings"
	"testing"

	"github.com/ddddddO/gtree"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/pkgjson"
	"github.com/stretchr/testify/assert"
)

func TestNewGTreeBuilderDefaultsOK(t *testing.T) {
	builder := newGTreeBuilder(false)
	assert.NotNil(t, builder)
	assert.False(t, builder.printNodesOnce)
	assert.NotNil(t, builder.seenNodes)
	assert.Empty(t, builder.seenNodes)
	assert.Nil(t, builder.treeRoot)
}

func TestNewGTreeBuilderSetPrintNodesOnceWorks(t *testing.T) {
	builder := newGTreeBuilder(true)
	assert.NotNil(t, builder)
	assert.True(t, builder.printNodesOnce)
	assert.NotNil(t, builder.seenNodes)
	assert.Empty(t, builder.seenNodes)
	assert.Nil(t, builder.treeRoot)
}

func TestBuildTreeWithNilRootNodeErrorsOut(t *testing.T) {
	builder := newGTreeBuilder(false)
	_, err := builder.buildTree(NewPkgGraph(), nil)
	assert.Error(t, err)
}

func TestBuildTreeWithNilGraphErrorsOut(t *testing.T) {
	builder := newGTreeBuilder(false)
	_, err := builder.buildTree(nil, createTestNode("test-node"))
	assert.Error(t, err)
}

func TestBuildTreeNodeWithNilParentSetsTreeRoot(t *testing.T) {
	builder := newGTreeBuilder(false)

	pkgNode := createTestNode("test-node")

	treeNode := builder.buildTreeNode(nil, pkgNode)

	assert.NotNil(t, treeNode)
	assert.Equal(t, builder.treeRoot, treeNode)
}

func TestBuildNodeTextForUnseenNodeOK(t *testing.T) {
	builder := newGTreeBuilder(false)

	pkgNode := createTestNode("test-node")

	text := builder.buildNodeText(pkgNode)
	assert.Contains(t, text, "test-node")
	assert.NotContains(t, text, seenNodeSuffix)

}

func TestBuildNodeTextForSeenNodeOK(t *testing.T) {
	builder := newGTreeBuilder(false)

	pkgNode := createTestNode("test-node")

	// Mark the node as seen
	builder.seenNodes[pkgNode] = true

	// Test when node has been seen before
	text := builder.buildNodeText(pkgNode)
	assert.Contains(t, text, "test-node")
	assert.Contains(t, text, seenNodeSuffix)
}

func TestBuildTreeWithDFSWithoutLoopsWorks(t *testing.T) {
	var buf strings.Builder

	graph := NewPkgGraph()

	// Build graph: root -> child1
	rootNode, err := addNodeToGraph(graph, "root")
	assert.NoError(t, err)

	child1, err := addNodeToGraph(graph, "child1")
	assert.NoError(t, err)

	err = graph.AddEdge(rootNode, child1)
	assert.NoError(t, err)

	// Build the tree
	builder := newGTreeBuilder(false)
	builder.buildTreeWithDFS(nil, rootNode, graph)

	err = gtree.OutputProgrammably(&buf, builder.treeRoot)
	assert.NoError(t, err)

	// Check tree structure
	output := buf.String()
	assert.Contains(t, output, "root")
	assert.Contains(t, output, "child1")
}

func TestBuildTreeWithDFSWithLoopWorks(t *testing.T) {
	var buf strings.Builder

	graph := NewPkgGraph()

	// Build graph: A -> B -> A
	nodeA, err := addNodeToGraph(graph, "A")
	assert.NoError(t, err)

	nodeB, err := addNodeToGraph(graph, "B")
	assert.NoError(t, err)

	err = graph.AddEdge(nodeA, nodeB)
	assert.NoError(t, err)

	err = graph.AddEdge(nodeB, nodeA)
	assert.NoError(t, err)

	// Build the tree
	builder := newGTreeBuilder(false)
	builder.buildTreeWithDFS(nil, nodeA, graph)

	err = gtree.OutputProgrammably(&buf, builder.treeRoot)
	assert.NoError(t, err)

	// Check tree structure
	output := buf.String()
	assert.Contains(t, output, "A")
	assert.Contains(t, output, "B")
}

func TestBuildTreeWithDFSPrintRepeatedNodes(t *testing.T) {
	const (
		rootName   = "root"
		child1Name = "child1"
		child2Name = "child2"
	)

	graph := NewPkgGraph()

	// Build graph:
	// root -> child1 -> child2
	// 		-> child2
	rootNode, err := addNodeToGraph(graph, rootName)
	assert.NoError(t, err)

	child1, err := addNodeToGraph(graph, child1Name)
	assert.NoError(t, err)

	child2, err := addNodeToGraph(graph, child2Name)
	assert.NoError(t, err)

	err = graph.AddEdge(rootNode, child1)
	assert.NoError(t, err)

	err = graph.AddEdge(child1, child2)
	assert.NoError(t, err)

	err = graph.AddEdge(rootNode, child2)
	assert.NoError(t, err)

	testCases := []struct {
		name              string
		printNodesOnce    bool
		outputContains    []string
		outputNotContains []string
	}{
		{
			name:              "print repeated nodes",
			printNodesOnce:    false,
			outputContains:    []string{rootName, child1Name, child2Name},
			outputNotContains: []string{seenNodeSuffix},
		},
		{
			name:              "don't print repeated nodes",
			printNodesOnce:    true,
			outputContains:    []string{rootName, child1Name, child2Name, seenNodeSuffix},
			outputNotContains: []string{},
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.name, func(t *testing.T) {
			var buf strings.Builder

			// Build the tree
			builder := newGTreeBuilder(testCase.printNodesOnce)
			builder.buildTreeWithDFS(nil, rootNode, graph)

			err = gtree.OutputProgrammably(&buf, builder.treeRoot)
			assert.NoError(t, err)

			// Check tree structure
			output := buf.String()
			for _, contains := range testCase.outputContains {
				assert.Contains(t, output, contains)
			}

			for _, notContains := range testCase.outputNotContains {
				assert.NotContains(t, output, notContains)
			}
		})
	}
}

func addNodeToGraph(graph *PkgGraph, nodeName string) (*PkgNode, error) {
	return graph.AddPkgNode(&pkgjson.PackageVer{Name: nodeName}, StateMeta, TypeLocalRun, NoSRPMPath, NoRPMPath, NoSpecPath, NoSourceDir, NoArchitecture, NoSourceRepo)
}

func createTestNode(name string) *PkgNode {
	return &PkgNode{
		VersionedPkg: &pkgjson.PackageVer{
			Name: name,
		},
		Type:  TypeLocalRun,
		State: StateMeta,
	}
}
