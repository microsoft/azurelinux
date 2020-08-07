// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package formats

import (
	"fmt"
	"io"
	"strings"

	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkggraph"
)

type commandFormatter = func(string) string

// Makefile implements Unravel, producing a Makefile which expresses the build order
type Makefile struct {
	graph     *pkggraph.PkgGraph
	cmdFormat commandFormatter
}

// NewMakefile returns new *Makefile, saving internally the graph representation
// The original graph representation is not retained nor modified
// command is used to format SRPM into a worker invocation
// Input to the command is going to be the package's SRPM name (with .src.rpm)
func NewMakefile(g *pkggraph.PkgGraph, command func(string) string) *Makefile {
	copyG, err := g.DeepCopy()
	if err != nil {
		logger.Log.Panic("Error when copying graph: ", err)
	}

	return &Makefile{
		graph:     copyG,
		cmdFormat: command,
	}
}

// Save saves the makefile representation using the provided io.StringWriter
func (m *Makefile) Save(w io.StringWriter) (err error) {

	// Guards against including target multiple times; this is
	// possible since nodes are packages, but there might be
	// multiple packages per spec file and unit of build is spec file, not a package

	targetRecipeCreated := make(map[string]bool)

	for _, currentNode := range m.graph.AllNodes() {
		var currentNodeAsTarget string
		logger.Log.Tracef("Processing depnode %s", currentNode)
		if currentNode.State != pkggraph.StateBuild && currentNode.State != pkggraph.StateMeta {
			continue
		}

		currentNodeAsTarget, err = formatNodeAsTarget(currentNode)
		if err != nil {
			return
		}

		dependencies := m.graph.From(currentNode.ID())

		// Write out targets for meta(runtime) or build nodes (once)
		if !(targetRecipeCreated[currentNodeAsTarget]) {
			// All targets should be phony, the graph tools will have already determined what needs rebuilding
			w.WriteString(fmt.Sprintf("\n.PHONY: %s\n", currentNodeAsTarget))
			switch {
			case currentNode.State == pkggraph.StateMeta:
				// Runtime node target should not do anything, hence empty recipe
				w.WriteString(fmt.Sprintf("%s: ;\n", currentNodeAsTarget))
			case currentNode.State == pkggraph.StateBuild:
				// Build node target should call the command according to the passed cmdFormat
				w.WriteString(fmt.Sprintf("%s:\n\t%s\n", currentNodeAsTarget, m.cmdFormat(currentNode.SrpmPath)))
			}

			// Mark the target as created to avoid redefining targets
			targetRecipeCreated[currentNodeAsTarget] = true
		}

		// Mark the current node as a prerequisite for each of the dependencies
		var dependencyList string
		for dependencies.Next() {
			var dependencyAsTarget string
			dependency := dependencies.Node().(*pkggraph.PkgNode)
			// Only care about the runtime and build nodes

			if dependency.State != pkggraph.StateBuild && dependency.State != pkggraph.StateMeta {
				continue
			}

			dependencyAsTarget, err = formatNodeAsTarget(dependency)
			if err != nil {
				return
			}

			// dependencyList will be a space seperated list of targets
			dependencyList = fmt.Sprintf("%s %s", dependencyList, dependencyAsTarget)
			logger.Log.Tracef("\tDependency of %s -> %s", currentNodeAsTarget, dependencyAsTarget)
		}
		// Write out the dependency list, if there are any entries.
		if dependencyList != "" {
			w.WriteString(fmt.Sprintf("%s: %s\n", currentNodeAsTarget, dependencyList))
		}
	}
	return
}

// formatTarget outputs a string without characters forbidden in the makefile target name
func formatTarget(s string) string {
	var sb strings.Builder
	for _, c := range s {
		if c != ':' {
			sb.WriteRune(c)
		}
	}
	return sb.String()
}

// formatNodeAsTarget returns a valid makefile target name for the node
func formatNodeAsTarget(n *pkggraph.PkgNode) (target string, err error) {
	switch n.Type {
	case pkggraph.TypeGoal:
		target = fmt.Sprintf("GOAL_%s", n.GoalName)
	case pkggraph.TypePureMeta:
		target = fmt.Sprintf("PUREMETA_%d", n.ID())
	case pkggraph.TypeBuild:
		target = fmt.Sprintf("BUILD_%s", n.SrpmPath)
	case pkggraph.TypeRun:
		target = fmt.Sprintf("RUN_%d_%s_%s", n.ID(), n.SrpmPath, n.VersionedPkg.Name)

	default:
		err = fmt.Errorf("unexpected node encountered: %s", n)
	}
	target = formatTarget(target)
	return

}
