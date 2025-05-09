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
	output io.Writer
}

type graphPrinterConfigModifier func(*graphPrinterConfig)

// loggerOutputWrapper is a wrapper around logrus.Logger to implement the io.Writer interface.
type loggerOutputWrapper struct {
	logLevel logrus.Level
}

// Write implements the io.Writer interface.
func (d loggerOutputWrapper) Write(bytes []byte) (int, error) {
	// Remove the trailing newline character from the log message,
	// as it's unnecessary when logging.
	line := strings.TrimSuffix(string(bytes), "\n")
	logger.Log.Log(d.logLevel, line)
	return len(bytes), nil
}

// NewGraphPrinter creates a new GraphPrinter.
// It accepts a variadic number of 'GraphPrinter*' modifiers to customize the printer's behavior.
// The default settings are:
// - output: logrus logger on debug level
func NewGraphPrinter(configModifiers ...graphPrinterConfigModifier) GraphPrinter {
	config := graphPrinterConfig{
		output: loggerOutputWrapper{
			logLevel: logrus.DebugLevel,
		},
	}

	for _, modifier := range configModifiers {
		if modifier == nil {
			continue
		}
		modifier(&config)
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

// Print prints the graph. It ignores any cycles in the graph turning the graph into a tree.
// It then uses the 'gtree' package to print the tree structure.
func (g GraphPrinter) Print(graph *PkgGraph, rootNode *PkgNode) error {
	var buildTreeWithDFS func(*gtree.Node, *PkgNode)

	if graph == nil {
		return fmt.Errorf("graph is nil")
	}

	if rootNode == nil {
		return fmt.Errorf("root node is nil")
	}

	if !graph.HasNode(rootNode) {
		return fmt.Errorf("root node '%s' not found in the graph", rootNode.FriendlyName())
	}

	treeRoot := gtree.NewRoot(rootNode.FriendlyName())

	// Use a set to keep track of seen nodes to avoid infinite loops.
	seenNodes := make(map[*PkgNode]bool)

	// Walking the graph manually to keep track of 'gtree' nodes
	// and the parent-child relationships between them.
	buildTreeWithDFS = func(treeParent *gtree.Node, pkgNode *PkgNode) {
		if pkgNode == nil || seenNodes[pkgNode] {
			return
		}

		treeNode := treeRoot
		if treeParent != nil {
			treeNode = treeParent.Add(pkgNode.FriendlyName())
		}

		seenNodes[pkgNode] = true

		children := graph.From(pkgNode.ID())
		for children.Next() {
			child := children.Node().(*PkgNode)
			if child == nil {
				continue
			}
			buildTreeWithDFS(treeNode, child)
		}

		seenNodes[pkgNode] = false
	}

	buildTreeWithDFS(nil, rootNode)

	return gtree.OutputProgrammably(g.output, treeRoot)
}
