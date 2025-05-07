// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package pkggraph

import (
	"fmt"
	"io"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/sirupsen/logrus"
)

type GraphPrinter struct {
	graphPrinterConfig
}

type graphPrinterConfig struct {
	indentString string
	output       io.StringWriter
}

type graphPrinterConfigModifier func(*graphPrinterConfig)

type loggerOutputWrapper struct {
	logLevel logrus.Level
}

// Write implements the io.StringWriter interface.
func (d *loggerOutputWrapper) WriteString(s string) (int, error) {
	logger.Log.Log(d.logLevel, s)
	return len(s), nil
}

// NewGraphPrinter creates a new GraphPrinter.
// It accepts a variadic number of 'GraphPrinter*' modifiers to customize the printer's behavior.
// The default settings are:
// - Indent character: " " (space)
// - Indent shift: 2
func NewGraphPrinter(configModifiers ...graphPrinterConfigModifier) *GraphPrinter {
	config := &graphPrinterConfig{
		indentString: "  ",
		output: &loggerOutputWrapper{
			logLevel: logrus.DebugLevel,
		},
	}

	for _, modifier := range configModifiers {
		modifier(config)
	}

	return &GraphPrinter{
		graphPrinterConfig: *config,
	}
}

// GraphPrinterIndentString is a config modifier passed to the graph printer's constructor
// to define the string used for indentation in the graph printer.
func GraphPrinterIndentString(indentString string) graphPrinterConfigModifier {
	return func(c *graphPrinterConfig) {
		c.indentString = indentString
	}
}

// GraphPrinterOutput is a config modifier passed to the graph printer's constructor
// to define the output writer for the graph printer.
func GraphPrinterOutput(output io.StringWriter) graphPrinterConfigModifier {
	return func(c *graphPrinterConfig) {
		c.output = output
	}
}

// GraphPrinterLogOutput is a config modifier passed to the graph printer's constructor
// making the printer's output be logged at the specified log level.
func GraphPrinterLogOutput(logLevel logrus.Level) graphPrinterConfigModifier {
	return func(c *graphPrinterConfig) {
		c.output = &loggerOutputWrapper{
			logLevel: logLevel,
		}
	}
}

// Print prints the graph in the following manner:
// - Each line represents a node in the graph.
// - Each node is represented by its friendly name.
// - Children of each node have an indentation level based on their depth in the graph.
func (g GraphPrinter) Print(graph *PkgGraph, rootNode *PkgNode) error {
	var dfsPrint func(*PkgNode) error

	if graph == nil {
		return fmt.Errorf("graph is nil")
	}

	if rootNode == nil {
		return fmt.Errorf("root node is nil")
	}

	if !graph.HasNode(rootNode) {
		return fmt.Errorf("root node '%s' not found in the graph", rootNode.FriendlyName())
	}

	level := 0
	// Use a set to keep track of seen nodes to avoid infinite loops.
	seenNodes := make(map[*PkgNode]bool)

	// Walking the graph manually to be able to track the depth level.
	dfsPrint = func(node *PkgNode) error {
		if node == nil || seenNodes[node] {
			return nil
		}

		line := fmt.Sprintf("%s%s\n", strings.Repeat(string(g.indentString), level), node.FriendlyName())
		_, err := g.output.WriteString(line)
		if err != nil {
			return fmt.Errorf("failed to write to output: %w", err)
		}

		seenNodes[node] = true
		level += 1

		children := graph.From(node.ID())
		for children.Next() {
			child := children.Node().(*PkgNode)
			if child == nil {
				continue
			}
			err := dfsPrint(child)
			if err != nil {
				return err
			}
		}

		level -= 1
		seenNodes[node] = false

		return nil
	}

	return dfsPrint(rootNode)
}
