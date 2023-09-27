// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"fmt"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/rpm"
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
			if res.Ignored {
				err = fmt.Errorf("failed to query (%s) for provides. NOTE: source spec '%s' was marked to be ignored - please check if the queried RPM is present. Error: %s", rpmFile, res.Node.SpecName(), err)
			} else {
				err = fmt.Errorf("failed to query (%s) for provides. Error: %s", rpmFile, err)
			}
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

	// Make sure the graph is still a directed acyclic graph (DAG) after manipulating it.
	err = pkgGraph.MakeDAG()
	return
}

// replaceNodesWithProvides will replace a slice of nodes with a new node with the given provides in the graph.
func replaceNodesWithProvides(res *BuildResult, pkgGraph *pkggraph.PkgGraph, provides *pkgjson.PackageVer, nodes []*pkggraph.PkgNode, rpmFileProviding string) (err error) {
	var parentNode *pkggraph.PkgNode

	// Find a local run node that is backed by the same rpm as the one providing the implicit provide.
	// Make this node the parent node for the new implicit provide node.
	// - By making a run node the parent node, it will inherit the identical runtime dependencies of the already setup node.
	for _, node := range pkgGraph.AllPreferredRunNodes() {
		// We need to filter out any non-local run nodes since cached remote nodes are not acceptable parent nodes for collapsed nodes.
		if node.Type == pkggraph.TypeLocalRun && rpmFileProviding == node.RpmPath {
			logger.Log.Debugf("Linked implicit provide (%s) to run node (%s) using file (%s)", provides, node.FriendlyName(), rpmFileProviding)
			parentNode = node
			break
		}
	}

	// If there is no clear parent node for the implicit provide error out.
	if parentNode == nil {
		return fmt.Errorf("unable to find suitable parent node for implicit provides (%s) with file (%s)", provides, rpmFileProviding)
	}

	// Collapse the unresolved nodes into a single node backed by the new implicit provide.
	_, err = pkgGraph.CreateCollapsedNode(provides, parentNode, nodes)

	return
}

// implicitPackageNamesToNodesInGraph returns a map of package names to implicit nodes. These nodes will either be unresolved,
// or in the cache.
func implicitPackageNamesToNodesInGraph(pkgGraph *pkggraph.PkgGraph, useCachedImplicit bool) (nameToNodes map[string][]*pkggraph.PkgNode) {
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

	for _, n := range pkgGraph.AllPreferredRunNodes() {
		if !n.Implicit {
			continue
		}

		// When graphpkgfetcher runs, it will attempt to resolve all unresolved nodes.
		// Some of these may be implicit and it may find an upstream package that satisfies it. The scheduler will have
		// done its best to avoid using these nodes, but may eventually have to use them if there are no other options.
		// We will allow these nodes to be switched even after the scheduler starts to use them since some packages may
		// end up needing to install multiple versions of the same package if we don't unify them.
		if n.State == pkggraph.StateCached {
			if useCachedImplicit {
				logger.Log.Warnf("Implicit node (%s) was already cached and may have been used to satisfy another node (useCachedImplicit=true). Updating implicit path regardless!", n.FriendlyName())
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
	implicitPackagesToUnresolvedNodes := implicitPackageNamesToNodesInGraph(pkgGraph, useCachedImplicit)

	// An unresolved node can only be satisfied by a single provide, prevent duplicate matching
	nodeToSatisfier := make(map[*pkggraph.PkgNode]*pkgjson.PackageVer)

	for _, provide := range provides {
		for _, node := range implicitPackagesToUnresolvedNodes[provide.Name] {
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
					logger.Log.Warnf("Provides (%s) found that satisfies an already satisfied unresolved node (%s) by (%s)", provide, node.FriendlyName(), satisfiedBy)
					continue
				}

				logger.Log.Infof("Satisfying unresolved dynamic dependency (%s) with (%s)", node.FriendlyName(), provide)
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
