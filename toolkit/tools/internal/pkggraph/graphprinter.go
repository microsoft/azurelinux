// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package pkggraph

import (
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/sirupsen/logrus"
)

type GraphPrinter struct {
	indentChar  string
	indentShift int
}

// NewDefaultGraphPrinter creates a new GraphPrinter with default settings.
// The default settings are:
// - Indent character: " " (space)
// - Indent shift: 2
func NewDefaultGraphPrinter() *GraphPrinter {
	return NewGraphPrinter(" ", 2)
}

// NewGraphPrinter creates a new GraphPrinter with custom settings.
// The 'indentChar' parameter specifies the character used for indentation.
// The 'indentShift' parameter specifies the number of times the indent character is repeated for each level of indentation.
func NewGraphPrinter(indentChar string, indentShift int) *GraphPrinter {
	return &GraphPrinter{
		indentChar:  indentChar,
		indentShift: indentShift,
	}
}

// Print prints the graph in the following manner:
// - Each line represents a node in the graph.
// - Each node is represented by its ID.
// - Children of each node have an indentation level based on their depth in the graph.+
//
// The 'logLevel' parameter controls the logging level of the output.
func (g GraphPrinter) Print(graph *PkgGraph, rootNode *PkgNode, logLevel logrus.Level) {
	var dfsPrint func(*PkgNode)

	indent := 0
	// Use a set to keep track of seen nodes to avoid infinite loops.
	seenNodes := make(map[int64]bool)

	dfsPrint = func(node *PkgNode) {
		if node == nil || seenNodes[node.ID()] {
			return
		}

		logger.Log.Logf(logLevel, "%s%s\n", strings.Repeat(g.indentChar, indent), node.FriendlyName())

		seenNodes[node.ID()] = true
		indent += g.indentShift

		children := graph.From(node.ID())
		for children.Next() {
			child := children.Node().(*PkgNode)
			if child == nil {
				continue
			}
			dfsPrint(child)
		}

		indent += -g.indentShift
		seenNodes[node.ID()] = false
	}

	dfsPrint(rootNode)
}

// PrintDebug prints the graph at the debug level.
func (g GraphPrinter) PrintDebug(graph *PkgGraph, rootNode *PkgNode) {
	g.Print(graph, rootNode, logrus.DebugLevel)
}
