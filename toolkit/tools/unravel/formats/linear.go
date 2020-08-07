// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package formats

import (
	"io"

	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkggraph"
)

// Linear implements Unravel, producing a linear build order
type Linear struct {
	blockedBy BlockPkgsList
	blocking  BlockPkgsList
}

func (l *Linear) getNextPackage(blockedBy BlockPkgsList) string {
	for k, v := range blockedBy {
		if len(v) == 0 {
			return k
		}
	}
	return ""
}

func (l *Linear) build(x string, w io.StringWriter) (err error) {
	if "<NO_SRPM_PATH>" != x {
		_, err = w.WriteString(x)
		if err != nil {
			return
		}
	}
	return
}

func (l *Linear) updateAfterBuild(blocking, blockedBy BlockPkgsList, pkg string) {
	// Iterate over all packages that were blockedBy by pkg
	for name := range blocking[pkg] {
		// Mark the package as no longer blockedBy by this particular package
		delete(blockedBy[name], pkg)
	}
	// The package is not blocking anything now
	delete(blocking, pkg)
	// Package is built, so it's not blocked
	delete(blockedBy, pkg)
}

// NewLinear returns new *Linear, saving internally the graph representation.
// The original graph representation is not retained nor modified
func NewLinear(g *pkggraph.PkgGraph) *Linear {
	blocking, blockedBy := GraphToMaps(g)
	return &Linear{
		blocking:  blocking,
		blockedBy: blockedBy,
	}
}

// Save saves the order using the provided writer
func (l *Linear) Save(w io.StringWriter) (err error) {
	// Emulate a linear build to produce a linear order

	// DeepCopy the graph structures since operations on maps are destructive
	blocking, err := l.blocking.DeepCopy()
	if err != nil {
		return
	}
	blockedBy, err := l.blockedBy.DeepCopy()
	if err != nil {
		return
	}
	for {
		nextPackage := l.getNextPackage(blockedBy)
		if nextPackage == "" {
			return
		}
		err = l.build(nextPackage, w)
		if err != nil {
			logger.Log.Panic(err)
		}
		l.updateAfterBuild(blocking, blockedBy, nextPackage)
	}
}
