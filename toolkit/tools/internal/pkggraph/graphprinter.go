// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package pkggraph

import (
	"fmt"
	"io"
	"strings"

	"github.com/ddddddO/gtree"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/sirupsen/logrus"
)

// GraphPrinter is a type meant to print a graph in a human-readable format.
// It uses a depth-first search (DFS) algorithm to traverse the graph and print each node.
// The printer ignores any cycles in the graph and thus turns the graph into a tree.
// We use the gtree package to print the tree structure.
// See NewGraphPrinter for more details on how to customize the printer.
//
// Example:
//
//	Graph structure:
//
//	A -> B
//	A -> E
//	B -> C
//	B -> D
//	D -> A (loop)
//
//	Output starting from 'A':
//	A
//	├── B
//	│   ├── C
//	│   └── D
//	└── E
type GraphPrinter struct {
	graphPrinterConfig
}

type graphPrinterConfig struct {
	output         io.Writer
	printNodesOnce bool
}

type graphPrinterConfigModifier func(*graphPrinterConfig)

// loggerOutputWrapper is a wrapper around logrus.Logger to implement the io.Writer interface.
type loggerOutputWrapper struct {
	logLevel logrus.Level
}

// gTreeBuilder helps build a 'gtree' package's tree from a graph.
type gTreeBuilder struct {
	treeRoot       *gtree.Node
	seenNodes      map[*PkgNode]bool
	printNodesOnce bool
}

// NewGraphPrinter creates a new GraphPrinter.
// It accepts a variadic number of 'GraphPrinter*' modifiers to customize the printer's behavior.
// The default settings are:
// - output: logrus logger on debug level
// - printNodesOnce: false
func NewGraphPrinter(configModifiers ...graphPrinterConfigModifier) GraphPrinter {
	config := graphPrinterConfig{
		output: loggerOutputWrapper{
			logLevel: logrus.DebugLevel,
		},
		printNodesOnce: false,
	}

	for _, modifier := range configModifiers {
		if modifier != nil {
			modifier(&config)
		}
	}

	return GraphPrinter{
		graphPrinterConfig: config,
	}
}

// GraphPrinterOutput is a config modifier passed to the graph printer's constructor
// to define the output writer for the graph printer.
func GraphPrinterOutput(output io.Writer) graphPrinterConfigModifier {
	return func(c *graphPrinterConfig) {
		c.output = output
	}
}

// GraphPrinterLogOutput is a config modifier passed to the graph printer's constructor
// making the printer's output be logged at the specified log level.
func GraphPrinterLogOutput(logLevel logrus.Level) graphPrinterConfigModifier {
	return func(c *graphPrinterConfig) {
		c.output = loggerOutputWrapper{
			logLevel: logLevel,
		}
	}
}

// GraphPrinterPrintOnce is a config modifier passed to the graph printer's constructor
// to define whether the printer should print each node only once.
func GraphPrinterPrintNodesOnce() graphPrinterConfigModifier {
	return func(c *graphPrinterConfig) {
		c.printNodesOnce = true
	}
}

// Print prints the graph. It ignores any cycles in the graph turning the graph into a tree.
// It then uses the 'gtree' package to print the tree structure.
func (g GraphPrinter) Print(graph *PkgGraph, rootNode *PkgNode) error {
	if graph == nil {
		return fmt.Errorf("graph is nil")
	}

	if rootNode == nil {
		return fmt.Errorf("root node is nil")
	}

	if !graph.HasNode(rootNode) {
		return fmt.Errorf("root node '%s' not found in the graph", rootNode.FriendlyName())
	}

	treeBuilder := newGTreeBuilder(g.printNodesOnce)
	treeRoot, err := treeBuilder.buildTree(graph, rootNode)
	if err != nil {
		return fmt.Errorf("failed to build tree:\n%w", err)
	}

	err = gtree.OutputProgrammably(g.output, treeRoot)
	if err != nil {
		return fmt.Errorf("failed to print tree:\n%w", err)
	}

	return nil
}

// Write implements the io.Writer interface.
func (d loggerOutputWrapper) Write(bytes []byte) (int, error) {
	// Remove the trailing newline character from the log message,
	// as it's unnecessary when logging.
	line := strings.TrimSuffix(string(bytes), "\n")
	logger.Log.Log(d.logLevel, line)
	return len(bytes), nil
}

// newGTreeBuilder creates a new gTreeBuilder instance with the specified
// configuration for printing nodes once.
func newGTreeBuilder(printNodesOnce bool) *gTreeBuilder {
	result := &gTreeBuilder{
		printNodesOnce: printNodesOnce,
	}
	result.resetState()
	return result
}

// buildTree traverses the graph and constructs a tree representation.
func (tb *gTreeBuilder) buildTree(graph *PkgGraph, rootNode *PkgNode) (*gtree.Node, error) {
	if rootNode == nil {
		return nil, fmt.Errorf("root node is nil")
	}

	tb.resetState()
	tb.buildTreeWithDFS(nil, rootNode, graph)

	return tb.treeRoot, nil
}

func (tb *gTreeBuilder) resetState() {
	tb.seenNodes = make(map[*PkgNode]bool)
	tb.treeRoot = nil
}

// buildTreeWithDFS builds the tree using depth-first search.
func (tb *gTreeBuilder) buildTreeWithDFS(treeParent *gtree.Node, pkgNode *PkgNode, graph *PkgGraph) {
	if pkgNode == nil {
		return
	}

	treeNode := tb.buildTreeNode(treeParent, pkgNode)

	if tb.seenNodes[pkgNode] {
		return
	}

	tb.seenNodes[pkgNode] = true

	children := graph.From(pkgNode.ID())
	for children.Next() {
		tb.buildTreeWithDFS(treeNode, children.Node().(*PkgNode), graph)
	}

	if !tb.printNodesOnce {
		tb.seenNodes[pkgNode] = false
	}
}

// buildTreeNode creates a new tree node and adds it to the parent
// or sets it as the root if the parent is nil.
func (tb *gTreeBuilder) buildTreeNode(treeParent *gtree.Node, pkgNode *PkgNode) *gtree.Node {
	nodeText := tb.buildNodeText(pkgNode)
	if treeParent == nil {
		tb.treeRoot = gtree.NewRoot(nodeText)
		return tb.treeRoot
	}
	return treeParent.Add(nodeText)
}

// buildNodeText formats the node text based on whether it's been seen before.
func (tb *gTreeBuilder) buildNodeText(pkgNode *PkgNode) string {
	if tb.seenNodes[pkgNode] {
		return fmt.Sprintf("%s... [SEEN]", pkgNode.FriendlyName())
	}
	return pkgNode.FriendlyName()
}
