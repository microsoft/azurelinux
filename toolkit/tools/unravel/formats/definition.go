// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package formats

import (
	"bytes"
	"encoding/gob"
	"io"
	"sync"

	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkggraph"
)

var (
	registerTypesOnce sync.Once
)

// BlockingPkgs is a generic type that is a list of package names. The bool is present for easy lookup.
type BlockingPkgs map[string]bool

// BlockPkgsList is a generic type that is a list of package names, each mapping to another list of packages names.
type BlockPkgsList map[string]BlockingPkgs

// Unravel is an interface that allows to unravel the graph and save it using a custom format
type Unravel interface {
	Save(io.StringWriter) error
}

// GraphToMaps takes PkgGraph and returns two blockPkgsLists,
// The first one says what packages are blocking a queried package
// The second one says what packages are blocked by a queried package
func GraphToMaps(g *pkggraph.PkgGraph) (blocking, blockedBy BlockPkgsList) {
	blocking = make(BlockPkgsList)
	blockedBy = make(BlockPkgsList)

	// Each node is a potential dependency
	potentialDependencies := g.Nodes()

	for potentialDependencies.Next() {
		dep := potentialDependencies.Node().(*pkggraph.PkgNode)
		logger.Log.Tracef("Processing depnode %s", dep.FriendlyName())
		// All nodes need to be created in BlockedBy
		// Since a node with no dependency represents a leaf node
		// But wouldn't be created otherwise
		if blockedBy[dep.SrpmPath] == nil {
			blockedBy[dep.SrpmPath] = make(BlockingPkgs)
		}

		dependants := g.To(dep.ID())

		for dependants.Next() {
			dependant := dependants.Node().(*pkggraph.PkgNode)
			if dependant.SrpmPath == dep.SrpmPath {
				continue
			}
			if blockedBy[dependant.SrpmPath] == nil {
				blockedBy[dependant.SrpmPath] = make(BlockingPkgs)
			}
			if blocking[dep.SrpmPath] == nil {
				blocking[dep.SrpmPath] = make(BlockingPkgs)
			}

			blockedBy[dependant.SrpmPath][dep.SrpmPath] = true
			blocking[dep.SrpmPath][dependant.SrpmPath] = true
			logger.Log.Tracef("Dependency of %s -> %s", dependant.SrpmPath, dep.SrpmPath)
		}
	}
	return blocking, blockedBy
}

// registerTypes registers map types for serialization
func registerTypes() {
	gob.Register(make(BlockingPkgs))
	gob.Register(make(BlockPkgsList))
}

// DeepCopy returns a deep copy of the receiver.
// On error, the returned deepCopy is in an invalid state
func (b BlockPkgsList) DeepCopy() (deepCopy BlockPkgsList, err error) {
	registerTypesOnce.Do(registerTypes)

	var buf bytes.Buffer
	e := gob.NewEncoder(&buf)
	d := gob.NewDecoder(&buf)
	err = e.Encode(b)
	if err != nil {
		return
	}
	err = d.Decode(&deepCopy)
	return
}
