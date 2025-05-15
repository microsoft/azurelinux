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

const seenNodeSuffix = "... [SEEN]"

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
	output         io.Writer
	printNodesOnce bool
}

type graphPrinterModifier func(*GraphPrinter)

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
func NewGraphPrinter(modifiers ...graphPrinterModifier) GraphPrinter {
	printer := GraphPrinter{
		output: loggerOutputWrapper{
			logLevel: logrus.DebugLevel,
		},
		printNodesOnce: false,
	}

	for _, modifier := range modifiers {
		if modifier != nil {
			modifier(&printer)
		}
	}

	return printer
}

// GraphPrinterOutput is a config modifier passed to the graph printer's constructor
// to define the output writer for the graph printer.
func GraphPrinterOutput(output io.Writer) graphPrinterModifier {
	return func(g *GraphPrinter) {
		g.output = output
	}
}

// GraphPrinterLogOutput is a config modifier passed to the graph printer's constructor
// making the printer's output be logged at the specified log level.
func GraphPrinterLogOutput(logLevel logrus.Level) graphPrinterModifier {
	return func(g *GraphPrinter) {
		g.output = loggerOutputWrapper{
			logLevel: logLevel,
		}
	}
}

// GraphPrinterPrintOnce is a config modifier passed to the graph printer's constructor
// to define whether the printer should print each node only once.
func GraphPrinterPrintNodesOnce() graphPrinterModifier {
	return func(g *GraphPrinter) {
		g.printNodesOnce = true
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
func (l loggerOutputWrapper) Write(bytes []byte) (int, error) {
	// Remove the trailing newline character from the log message,
	// as it's unnecessary when logging.
	line := strings.TrimSuffix(string(bytes), "\n")
	logger.Log.Log(l.logLevel, line)
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
func (t *gTreeBuilder) buildTree(graph *PkgGraph, rootNode *PkgNode) (*gtree.Node, error) {
	if graph == nil {
		return nil, fmt.Errorf("graph is nil")
	}

	if rootNode == nil {
		return nil, fmt.Errorf("root node is nil")
	}

	t.resetState()
	t.buildTreeWithDFS(nil, rootNode, graph)

	return t.treeRoot, nil
}

func (tb *gTreeBuilder) resetState() {
	tb.seenNodes = make(map[*PkgNode]bool)
	tb.treeRoot = nil
}

// buildTreeWithDFS builds the tree using depth-first search.
// It converts a general graph into a tree structure.
// It uses a map to keep track of seen nodes to avoid cycles.
func (t *gTreeBuilder) buildTreeWithDFS(treeParent *gtree.Node, pkgNode *PkgNode, graph *PkgGraph) {
	if pkgNode == nil {
		return
	}

	// We add a node before the "seen" check because we always
	// want to add the node to the tree. If it's been seen before,
	// we just mark it as seen as part of the text displayed for the node.
	treeNode := t.buildTreeNode(treeParent, pkgNode)

	if t.seenNodes[pkgNode] {
		return
	}

	t.seenNodes[pkgNode] = true

	children := graph.From(pkgNode.ID())
	for children.Next() {
		t.buildTreeWithDFS(treeNode, children.Node().(*PkgNode), graph)
	}

	// As we traverse the graph back up, setting the node as unseen
	// allows us to print it again if we encounter it later
	// in a DIFFERENT branch of the tree.
	if !t.printNodesOnce {
		t.seenNodes[pkgNode] = false
	}
}

// buildTreeNode creates a new tree node and adds it to the parent
// or sets it as the root if the parent is nil.
func (t *gTreeBuilder) buildTreeNode(treeParent *gtree.Node, pkgNode *PkgNode) *gtree.Node {
	nodeText := t.buildNodeText(pkgNode)
	if treeParent == nil {
		t.treeRoot = gtree.NewRoot(nodeText)
		return t.treeRoot
	}
	return treeParent.Add(nodeText)
}

// buildNodeText formats the node text based on whether it's been seen before.
func (t *gTreeBuilder) buildNodeText(pkgNode *PkgNode) string {
	if t.seenNodes[pkgNode] {
		return pkgNode.FriendlyName() + seenNodeSuffix
	}
	return pkgNode.FriendlyName()
}
