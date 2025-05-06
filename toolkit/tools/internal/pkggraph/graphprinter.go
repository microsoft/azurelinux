// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package pkggraph

import (
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/sirupsen/logrus"
)

type GraphPrinter struct {
	config
}

type config struct {
	indentChar  rune
	indentShift int
}

type configModifier func(*config)

// defaultConfig creates GraphPrinter's default settings.
// The default settings are:
// - Indent character: " " (space)
// - Indent shift: 2
func defaultConfig() *config {
	return &config{
		indentChar:  ' ',
		indentShift: 2,
	}
}

// NewGraphPrinter creates a new GraphPrinter.
// It accepts a variadic number of 'With*' modifiers to customize the printer's behavior.
// The default settings are:
// - Indent character: " " (space)
// - Indent shift: 2
func NewGraphPrinter(configModifiers ...configModifier) *GraphPrinter {
	config := defaultConfig()
	for _, modifier := range configModifiers {
		modifier(config)
	}
	return &GraphPrinter{
		config: *config,
	}
}

// WithIndentChar is a config modifier passed to the graph printer's constructor
// to define the character used for indentation in the graph printer.
func WithIndentChar(indentChar rune) configModifier {
	return func(c *config) {
		c.indentChar = indentChar
	}
}

// WithIndentShift is a config modifier passed to the graph printer's constructor
// to define the number of times the indent character is repeated for each level of indentation.
func WithIndentShift(indentShift int) configModifier {
	return func(c *config) {
		c.indentShift = indentShift
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

		logger.Log.Logf(logLevel, "%s%s\n", strings.Repeat(string(g.indentChar), indent), node.FriendlyName())

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
