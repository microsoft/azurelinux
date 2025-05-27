// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package pkggraph

import (
	"strings"
	"testing"

	"github.com/sirupsen/logrus"
	"github.com/stretchr/testify/assert"
)

func TestDefaultGraphPrinterCreatedOK(t *testing.T) {
	printer := NewGraphPrinter()
	assert.NotNil(t, printer)
	assert.False(t, printer.printNodesOnce)
}

func TestCustomOutputAppliesOK(t *testing.T) {
	const nodeName = "node"

	var buffer strings.Builder

	printer := NewGraphPrinter(
		GraphPrinterOutput(&buffer),
	)

	graph := NewPkgGraph()
	assert.NotNil(t, graph)

	rootNode, err := addNodeToGraph(graph, nodeName)
	assert.NoError(t, err)

	printer.Print(graph, rootNode)

	output := buffer.String()
	assert.Contains(t, output, nodeName)
}

func TestPrintingLargerGraphOK(t *testing.T) {
	const (
		rootName       = "root"
		child1Name     = "child1"
		child2Name     = "child2"
		grandchildName = "grandchild"
	)

	var buf strings.Builder
	printer := NewGraphPrinter(
		GraphPrinterOutput(&buf),
	)

	// Create a graph with multiple nodes and edges.
	graph := NewPkgGraph()
	assert.NotNil(t, graph)

	// Add root node.
	rootNode, err := addNodeToGraph(graph, rootName)
	assert.NoError(t, err)

	// Add children.
	child1, err := addNodeToGraph(graph, child1Name)
	assert.NoError(t, err)

	child2, err := addNodeToGraph(graph, child2Name)
	assert.NoError(t, err)

	// Add grandchild.
	grandchild, err := addNodeToGraph(graph, grandchildName)
	assert.NoError(t, err)

	// Add edges.
	err = graph.AddEdge(rootNode, child1)
	assert.NoError(t, err)

	err = graph.AddEdge(rootNode, child2)
	assert.NoError(t, err)

	err = graph.AddEdge(child1, grandchild)
	assert.NoError(t, err)

	err = printer.Print(graph, rootNode)
	assert.NoError(t, err)

	// Check output contains all nodes.
	output := buf.String()
	assert.Contains(t, output, rootName)
	assert.Contains(t, output, "── "+child1Name)
	assert.Contains(t, output, "── "+child2Name)
	assert.Contains(t, output, "   └── "+grandchildName)
}

func TestPrintGraphWithCyclesOK(t *testing.T) {
	const (
		node1Name = "node1"
		node2Name = "node2"
	)

	var buf strings.Builder

	printer := NewGraphPrinter(
		GraphPrinterOutput(&buf),
	)

	// Create a graph with a cycle.
	graph := NewPkgGraph()

	// Add nodes.
	node1, err := addNodeToGraph(graph, node1Name)
	assert.NoError(t, err)

	node2, err := addNodeToGraph(graph, node2Name)
	assert.NoError(t, err)

	// Create a cycle.
	err = graph.AddEdge(node1, node2)
	assert.NoError(t, err)

	err = graph.AddEdge(node2, node1)
	assert.NoError(t, err)

	// Print the graph assuming 'node1' is the root.
	err = printer.Print(graph, node1)
	assert.NoError(t, err)

	// Check output contains both nodes with 'node1' at the root level.
	output := buf.String()
	assert.Contains(t, output, node1Name)
	assert.Contains(t, output, "└── "+node2Name)

	buf.Reset()

	// Print the graph assuming 'node2' is the root.
	err = printer.Print(graph, node2)
	assert.NoError(t, err)

	// Check output contains both nodes with 'node2' at the root level.
	output = buf.String()
	assert.Contains(t, output, node2Name)
	assert.Contains(t, output, "└── "+node1Name)
}

func TestPrintNilGraphReturnsError(t *testing.T) {
	var buf strings.Builder

	printer := NewGraphPrinter(
		GraphPrinterOutput(&buf),
	)

	err := printer.Print(nil, nil)
	assert.Error(t, err)

	// Output should be empty since error occurred.
	assert.Empty(t, buf.String())
}

func TestPrintNilRootReturnsError(t *testing.T) {
	var buf strings.Builder

	printer := NewGraphPrinter(
		GraphPrinterOutput(&buf),
	)

	graph := NewPkgGraph()

	err := printer.Print(graph, nil)
	assert.Error(t, err)

	// Output should be empty since error occurred.
	assert.Empty(t, buf.String())
}

func TestPrintNodeNotInGraphReturnsError(t *testing.T) {
	var buf strings.Builder

	printer := NewGraphPrinter(
		GraphPrinterOutput(&buf),
	)

	graph := NewPkgGraph()

	err := printer.Print(graph, &PkgNode{})
	assert.Error(t, err)

	// Output should be empty since error occurred.
	assert.Empty(t, buf.String())
}
func TestAllNilModifiersHandledCorrectly(t *testing.T) {
	assert.NotPanics(t, func() {
		NewGraphPrinter(nil, nil, nil)
	})
}

func TestMixedNilAndValidModifiersHandledCorrectly(t *testing.T) {
	var (
		buf     strings.Builder
		printer GraphPrinter
	)

	assert.NotPanics(t, func() {
		printer = NewGraphPrinter(
			nil,
			GraphPrinterOutput(&buf),
			nil,
		)
	})

	// Verify that valid modifiers were applied
	assert.Equal(t, &buf, printer.output)
}

func TestLogOutputModifierAppliedCorrectly(t *testing.T) {
	// Test with GraphPrinterLogOutput
	printer := NewGraphPrinter(
		GraphPrinterLogOutput(logrus.InfoLevel),
	)

	// Verify the output is a loggerOutputWrapper with the correct log level
	logOutput, isLoggerOutput := printer.output.(loggerOutputWrapper)
	assert.True(t, isLoggerOutput)
	assert.Equal(t, logrus.InfoLevel, logOutput.logLevel)
}

func TestPrintNodesOnceModifierAppliedCorrectly(t *testing.T) {
	printer := NewGraphPrinter(
		GraphPrinterPrintNodesOnce(),
	)

	assert.True(t, printer.printNodesOnce)
}

func TestPrintNodesOnceFunctionalityWorks(t *testing.T) {
	const (
		rootName   = "root"
		child1Name = "child1"
		child2Name = "child2"
		sharedName = "shared"
	)

	// Create a graph where both child1 and child2 depend on the same shared node:
	// root -> child1 -> shared
	//      -> child2 -> shared
	graph := NewPkgGraph()
	assert.NotNil(t, graph)

	rootNode, err := addNodeToGraph(graph, rootName)
	assert.NoError(t, err)

	child1, err := addNodeToGraph(graph, child1Name)
	assert.NoError(t, err)

	child2, err := addNodeToGraph(graph, child2Name)
	assert.NoError(t, err)

	sharedNode, err := addNodeToGraph(graph, sharedName)
	assert.NoError(t, err)

	err = graph.AddEdge(rootNode, child1)
	assert.NoError(t, err)

	err = graph.AddEdge(rootNode, child2)
	assert.NoError(t, err)

	err = graph.AddEdge(child1, sharedNode)
	assert.NoError(t, err)

	err = graph.AddEdge(child2, sharedNode)
	assert.NoError(t, err)

	testCases := []struct {
		name              string
		printNodesConfig  graphPrinterModifier
		outputContains    []string
		outputNotContains []string
	}{
		{
			name:              "print repeated nodes",
			printNodesConfig:  nil,
			outputContains:    []string{rootName, child1Name, child2Name, sharedName},
			outputNotContains: []string{seenNodeSuffix},
		},
		{
			name:              "don't print repeated nodes",
			printNodesConfig:  GraphPrinterPrintNodesOnce(),
			outputContains:    []string{rootName, child1Name, child2Name, seenNodeSuffix, seenNodeSuffix},
			outputNotContains: []string{},
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.name, func(t *testing.T) {
			var buf strings.Builder
			printer := NewGraphPrinter(
				GraphPrinterOutput(&buf),
				testCase.printNodesConfig,
			)

			err = printer.Print(graph, rootNode)
			assert.NoError(t, err)
			output := buf.String()

			// Check tree structure
			for _, contains := range testCase.outputContains {
				assert.Contains(t, output, contains)
			}

			for _, notContains := range testCase.outputNotContains {
				assert.NotContains(t, output, notContains)
			}
		})
	}
}
