// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package pkggraph

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"

	"gonum.org/v1/gonum/graph"
)

const (
	invalid = iota
	unvisited
	inProgress
	done
)

type dfsData struct {
	state  map[int64]int
	parent map[int64]int64
	cycle  []int64
}

// FindAnyDirectedCycle returns any single cycle in the graph, if one exists.
// Multiple instances of this routine should not be run at the same time on a given graph.
func (g *PkgGraph) FindAnyDirectedCycle() (nodes []*PkgNode, err error) {
	const goalNodeName = "_dfs_root_"

	metadata := dfsData{
		make(map[int64]int),
		make(map[int64]int64),
		make([]int64, 0),
	}

	// Create a temporary root node, by using a constant goalNodeName, it will act as a mutex against concurrent
	// cycle searches on a given graph as this below call will fail if there is already a goal node with the same value.
	rootNode, err := g.AddGoalNode(goalNodeName, nil, nil, false)
	if err != nil {
		return
	}

	// This call will also remove all edges connected to the temporary root node.
	defer g.RemoveNode(rootNode.ID())

	// Seed the initial metadata state.
	metadata.parent[rootNode.ID()] = -1
	metadata.state[rootNode.ID()] = unvisited

	foundCycle, err := cycleDFS(g, rootNode.ID(), &metadata)
	if err != nil {
		return
	}

	if foundCycle {
		// Convert the slice of node IDs to references to the actual nodes.
		for _, id := range metadata.cycle {
			nodes = append(nodes, g.Node(id).(*PkgNode).This)
		}
	}

	return
}

// cycleDFS implements a custom DFS that updates metaData.cycle with the first cycle it finds in a given graph.
func cycleDFS(g *PkgGraph, rootID int64, metaData *dfsData) (foundCycle bool, err error) {
	// Recursing on a node that has already been visited indicates a fatal error with the search.
	if metaData.state[rootID] != unvisited {
		err = fmt.Errorf("node (%d) is in a bad state (%d)", rootID, metaData.state[rootID])
		return
	}

	// Mark that rootID is actively being searched ("inProgress").
	//
	// If all of its neighbors have been recursively exhausted then rootID will be marked as "done"
	// to indicate that no cycle was found in all walks containing rootID.
	//
	// However, if any neighbors of rootID are currently marked as "inProgress" this indicates that
	// the current walk has encountered a cycle.
	//
	// Example:
	//    a → c → a
	//    ↓   ↓
	//    b   b
	//
	// 1) visit(a)
	//   - mark "a" as "inProgress".
	//   - neighbor "b" is "unvisited", visit.
	// 2) visit(b)
	//   - mark "b" as "inProgress".
	//   - no neighbors.
	//   - mark "b" as "done".
	// 3) Resume visit(a)
	//   - neighbor "c" is "unvisited", visit.
	// 4) visit(c)
	//   - mark "c" as "inProgress".
	//   - neighbor "b" is "done", skip.
	//   - neighbor "a" is "inProgress", thus a cycle between "c" and "a" is found.

	metaData.state[rootID] = inProgress

	for _, neighbor := range graph.NodesOf(g.From(rootID)) {
		v := neighbor.ID()
		if _, exists := metaData.state[v]; !exists {
			metaData.state[v] = unvisited
		}

		switch metaData.state[v] {
		case done:
			continue
		case unvisited:
			metaData.parent[v] = rootID
			foundCycle, err = cycleDFS(g, v, metaData)
			if err != nil || foundCycle {
				return
			}
		case inProgress:
			updateMetadataWithCycle(g, metaData, rootID, v)
			foundCycle = true
			return
		default:
			err = fmt.Errorf("node (%d) is in a bad state (%d)", v, metaData.state[v])
			return
		}
	}

	metaData.state[rootID] = done
	return
}

// updateMetadataWithCycle records the cycle between startID and endID in metaData.cycle.
func updateMetadataWithCycle(g *PkgGraph, metaData *dfsData, startID, endID int64) {
	// Construct a cycle that starts and ends with the same node id by backtracking
	// from startID to endID
	// 	a -> b -> ... -> a
	logger.Log.Debug("Found cycle")
	metaData.cycle = []int64{endID}
	for startID != endID {
		metaData.cycle = append(metaData.cycle, startID)
		logger.Log.Tracef("%s needed by %s", g.Node(startID).(*PkgNode).FriendlyName(), g.Node(metaData.parent[startID]).(*PkgNode).FriendlyName())
		startID = metaData.parent[startID]
	}
	metaData.cycle = append(metaData.cycle, endID)
}
