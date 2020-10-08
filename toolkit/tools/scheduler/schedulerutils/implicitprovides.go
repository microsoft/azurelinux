// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"fmt"
	"path/filepath"
	"strings"

	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkggraph"
	"microsoft.com/pkggen/internal/pkgjson"
	"microsoft.com/pkggen/internal/rpm"
)

// InjectMissingImplicitProvides will inject implicit provide nodes into the graph from a build result if they satisfy any unresolved nodes.
func InjectMissingImplicitProvides(res *BuildResult, pkgGraph *pkggraph.PkgGraph, useCachedImplicit bool) (didInjectAny bool, err error) {
	for _, rpmFile := range res.BuiltFiles {
		var (
			provides       []string
			provideToNodes map[*pkgjson.PackageVer][]*pkggraph.PkgNode
		)

		provides, err = rpm.QueryRPMProvides(rpmFile)
		if err != nil {
			err = fmt.Errorf("failed to query (%s) for provides, error: %s", rpmFile, err)
			return
		}

		packageProvides := parseProvides(provides)
		provideToNodes, err = matchProvidesToUnresolvedNodes(packageProvides, pkgGraph, useCachedImplicit)
		if err != nil {
			return
		}

		for provide, nodes := range provideToNodes {
			err = replaceNodesWithProvides(res, pkgGraph, provide, nodes, rpmFile)
			if err != nil {
				return
			}

			didInjectAny = true
		}
	}

	return
}

// replaceNodesWithProvides will replace a slice of nodes with a new node with the given provides in the graph.
func replaceNodesWithProvides(res *BuildResult, pkgGraph *pkggraph.PkgGraph, provides *pkgjson.PackageVer, nodes []*pkggraph.PkgNode, rpmFileProviding string) (err error) {
	var (
		providesNode *pkggraph.PkgNode
		parentNode   *pkggraph.PkgNode
	)

	// pkgGraph.AddNode will panic on error (such as duplicate node IDs)
	defer func() {
		if r := recover(); r != nil {
			err = fmt.Errorf("replacing unresolved nodes (%v) with (%s) failed, error: %s", nodes, provides, r)
		}

		if err != nil {
			pkgGraph.RemovePkgNode(providesNode)
		}
	}()

	// Mirror the attributes of the node that resulted in this provides
	providingRPMBaseName := filepath.Base(rpmFileProviding)

	for _, node := range res.AncillaryNodes {
		if node.Type != pkggraph.TypeBuild {
			continue
		}

		expectedRPMName := fmt.Sprintf("%s-%s.%s.rpm", node.VersionedPkg.Name, node.VersionedPkg.Version, node.Architecture)
		if providingRPMBaseName == expectedRPMName {
			logger.Log.Debugf("Linked implicit provide (%s) to build node (%s)", provides, node.FriendlyName())
			parentNode = node
			break
		}
	}

	if parentNode == nil {
		// If there is no clear match between the implicit provide and which node produced it,
		// default to the primary build node.
		parentNode = res.Node
		logger.Log.Warnf("Unable to find suitable parent node for implicit provides (%s), defaulting to (%s)", provides, parentNode.FriendlyName())
	}

	providesNode, err = pkgGraph.AddPkgNode(provides, pkggraph.StateMeta, pkggraph.TypeRun, parentNode.SrpmPath, parentNode.RpmPath, parentNode.SpecPath, parentNode.SourceDir, parentNode.Architecture, parentNode.SourceRepo)
	providesNode.Implicit = true
	logger.Log.Debugf("Adding run node %s with id %d\n", providesNode.FriendlyName(), providesNode.ID())
	if err != nil {
		return
	}

	// Create and edge for the dependency of providesNode on parentNode
	parentEdge := pkgGraph.NewEdge(providesNode, parentNode)
	pkgGraph.SetEdge(parentEdge)

	// Mirror the dependents of the unresolved nodes to the new provides node
	for _, node := range nodes {
		dependents := pkgGraph.To(node.ID())

		for dependents.Next() {
			dependent := dependents.Node().(*pkggraph.PkgNode)

			// Create and edge for the dependency of what used to depend on the unresolved node to the new provides node
			dependentEdge := pkgGraph.NewEdge(dependent, providesNode)
			pkgGraph.SetEdge(dependentEdge)
		}
	}

	// Remove replaced nodes last to ensure all the above operations
	// can be undone incase of failure.
	for _, node := range nodes {
		pkgGraph.RemovePkgNode(node)
	}

	return
}

// implicitPackagesToUnresolvedNodesInGraph returns a map of package names to unresolved implicit nodes.
func implicitPackagesToUnresolvedNodesInGraph(pkgGraph *pkggraph.PkgGraph, useCachedImplicit bool) (nameToNodes map[string][]*pkggraph.PkgNode) {
	nameToNodes = make(map[string][]*pkggraph.PkgNode)

	// Depending on the node order that the graph was created, there may be multiple unresolved nodes for a single package.
	//
	// Example:
	// --> assume foo is unresolved
	// --> multiple packages need foo but at different version
	//
	// Parse order (A)
	// --> foo >= 5.0 -- create unresolved node
	// --> foo >= 4.0 -- re-use existing node
	// --> foo >= 3.0 -- re-use existing node
	// Unresolved nodes for foo: 1
	//
	// Parse order (B)
	// --> foo >= 3.0 -- create unresolved node
	// --> foo >= 4.0 -- create unresolved node
	// --> foo >= 3.0 -- create unresolved node
	// Unresolved nodes for foo: 3

	for _, n := range pkgGraph.AllRunNodes() {
		if !n.Implicit {
			continue
		}

		// When graphpkgfetcher runs, it will attempt to resolve all unresolved nodes.
		// Some of these may be implicit and it may find an upstream package that satisfies it.
		// Only consider these as resolved if useCachedImplicit is set.
		if n.State == pkggraph.StateCached {
			if useCachedImplicit {
				continue
			}
		} else if n.State != pkggraph.StateUnresolved {
			continue
		}

		nameToNodes[n.VersionedPkg.Name] = append(nameToNodes[n.VersionedPkg.Name], n)
	}

	return
}

// matchProvidesToUnresolvedNodes matches a list of provides to unresolved nodes that they satisfy in the graph.
func matchProvidesToUnresolvedNodes(provides []*pkgjson.PackageVer, pkgGraph *pkggraph.PkgGraph, useCachedImplicit bool) (matches map[*pkgjson.PackageVer][]*pkggraph.PkgNode, err error) {
	matches = make(map[*pkgjson.PackageVer][]*pkggraph.PkgNode)
	implicitPackagesToUnresolvedoNodes := implicitPackagesToUnresolvedNodesInGraph(pkgGraph, useCachedImplicit)

	// An unresolved node can only be satisfied by a single provide, prevent duplicate matching
	nodeToSatisfier := make(map[*pkggraph.PkgNode]*pkgjson.PackageVer)

	for _, provide := range provides {
		for _, node := range implicitPackagesToUnresolvedoNodes[provide.Name] {
			var (
				provideInterval pkgjson.PackageVerInterval
				nodeInterval    pkgjson.PackageVerInterval
			)

			provideInterval, err = provide.Interval()
			if err != nil {
				return
			}

			nodeInterval, err = node.VersionedPkg.Interval()
			if err != nil {
				return
			}

			if provideInterval.Satisfies(&nodeInterval) {
				satisfiedBy, found := nodeToSatisfier[node]
				if found {
					logger.Log.Warnf("Provides (%s) found that satifies an already satisfied unresolved node (%s) by (%s)", provide, node.FriendlyName(), satisfiedBy)
					continue
				}

				logger.Log.Infof("Satisfiying unresolved dynamic dependency (%s) with (%s)", node.FriendlyName(), provide)
				matches[provide] = append(matches[provide], node)
				nodeToSatisfier[node] = provide
			}
		}
	}

	return
}

// parseProvides converts a list of RPM provides into PackageVer structs.
func parseProvides(provides []string) (packageProvides []*pkgjson.PackageVer) {
	const (
		nameIndex    = iota
		versionIndex = iota
		maxIndex     = iota
	)

	const condition = "="

	packageProvides = make([]*pkgjson.PackageVer, 0, len(provides))

	for _, provide := range provides {
		provideSplit := strings.Split(provide, condition)

		pkgVer := &pkgjson.PackageVer{
			Name: strings.TrimSpace(provideSplit[nameIndex]),
		}

		if len(provideSplit) == maxIndex {
			pkgVer.Condition = condition
			version := strings.TrimSpace(provideSplit[versionIndex])
			pkgVer.Version = version
		}

		packageProvides = append(packageProvides, pkgVer)
	}

	return
}
