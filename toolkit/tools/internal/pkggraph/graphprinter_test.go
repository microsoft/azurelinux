// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package pkggraph

import (
	"strings"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/pkgjson"
	"github.com/stretchr/testify/assert"
)

func TestDefaultGraphPrinterCreatedOK(t *testing.T) {
	assert.NotNil(t, NewGraphPrinter())
}

func TestCustomOutputAppliesOK(t *testing.T) {
	const nodeName = "node"

	var buffer strings.Builder

	printer := NewGraphPrinter(
		GraphPrinterOutput(&buffer),
	)

	assert.NotNil(t, printer)

	graph := NewPkgGraph()
	assert.NotNil(t, graph)

	rootNode, err := graph.AddPkgNode(&pkgjson.PackageVer{Name: nodeName}, StateMeta, TypeLocalRun, NoSRPMPath, NoRPMPath, NoSpecPath, NoSourceDir, NoArchitecture, NoSourceRepo)
	assert.NoError(t, err)

	printer.Print(graph, rootNode)

	output := buffer.String()
	assert.Contains(t, output, nodeName)
}

func TestCustomIndentStringAppliesOK(t *testing.T) {
	const (
		customIndent = "----"
		rootName     = "root"
		child1Name   = "child1"
	)

	var buffer strings.Builder

	printer := NewGraphPrinter(
		GraphPrinterIndentString(customIndent),
		GraphPrinterOutput(&buffer),
	)

	// Create a simple graph to print.
	graph := NewPkgGraph()
	assert.NotNil(t, graph)

	rootNode, err := graph.AddPkgNode(&pkgjson.PackageVer{Name: rootName}, StateMeta, TypeLocalRun, NoSRPMPath, NoRPMPath, NoSpecPath, NoSourceDir, NoArchitecture, NoSourceRepo)
	assert.NoError(t, err)

	childNode, err := graph.AddPkgNode(&pkgjson.PackageVer{Name: child1Name}, StateMeta, TypeLocalRun, NoSRPMPath, NoRPMPath, NoSpecPath, NoSourceDir, NoArchitecture, NoSourceRepo)
	assert.NoError(t, err)

	// Add edge from root to child.
	err = graph.AddEdge(rootNode, childNode)
	assert.NoError(t, err)

	// Print the graph.
	err = printer.Print(graph, rootNode)
	assert.NoError(t, err)

	// Check output contains our custom indent.
	output := buffer.String()
	assert.Contains(t, output, customIndent)
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
	rootNode, err := graph.AddPkgNode(&pkgjson.PackageVer{Name: rootName}, StateMeta, TypeLocalRun, NoSRPMPath, NoRPMPath, NoSpecPath, NoSourceDir, NoArchitecture, NoSourceRepo)
	assert.NoError(t, err)

	// Add children.
	child1, err := graph.AddPkgNode(&pkgjson.PackageVer{Name: child1Name}, StateMeta, TypeLocalRun, NoSRPMPath, NoRPMPath, NoSpecPath, NoSourceDir, NoArchitecture, NoSourceRepo)
	assert.NoError(t, err)

	child2, err := graph.AddPkgNode(&pkgjson.PackageVer{Name: child2Name}, StateMeta, TypeLocalRun, NoSRPMPath, NoRPMPath, NoSpecPath, NoSourceDir, NoArchitecture, NoSourceRepo)
	assert.NoError(t, err)

	// Add grandchild.
	grandchild, err := graph.AddPkgNode(&pkgjson.PackageVer{Name: grandchildName}, StateMeta, TypeLocalRun, NoSRPMPath, NoRPMPath, NoSpecPath, NoSourceDir, NoArchitecture, NoSourceRepo)
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
	assert.Contains(t, output, strings.Repeat(printer.indentString, 0)+rootName)
	assert.Contains(t, output, strings.Repeat(printer.indentString, 1)+child1Name)
	assert.Contains(t, output, strings.Repeat(printer.indentString, 1)+child2Name)
	assert.Contains(t, output, strings.Repeat(printer.indentString, 2)+grandchildName)
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
	node1, err := graph.AddPkgNode(&pkgjson.PackageVer{Name: node1Name}, StateMeta, TypeLocalRun, NoSRPMPath, NoRPMPath, NoSpecPath, NoSourceDir, NoArchitecture, NoSourceRepo)
	assert.NoError(t, err)

	node2, err := graph.AddPkgNode(&pkgjson.PackageVer{Name: node2Name}, StateMeta, TypeLocalRun, NoSRPMPath, NoRPMPath, NoSpecPath, NoSourceDir, NoArchitecture, NoSourceRepo)
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
	assert.Contains(t, output, strings.Repeat(printer.indentString, 0)+node1Name)
	assert.Contains(t, output, strings.Repeat(printer.indentString, 1)+node2Name)

	buf.Reset()

	// Print the graph assuming 'node2' is the root.
	err = printer.Print(graph, node2)
	assert.NoError(t, err)

	// Check output contains both nodes with 'node2' at the root level.
	output = buf.String()
	assert.Contains(t, output, strings.Repeat(printer.indentString, 0)+node2Name)
	assert.Contains(t, output, strings.Repeat(printer.indentString, 1)+node1Name)
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
