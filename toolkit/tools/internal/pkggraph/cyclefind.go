// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package pkggraph

import (
	"fmt"

	"gonum.org/v1/gonum/graph"

	"microsoft.com/pkggen/internal/logger"
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

func createCycle(g *PkgGraph, metaData *dfsData, start, end int64) {
	metaData.cycle = append(metaData.cycle, end)
	logger.Log.Tracef("%s needed by %s", g.Node(end).(*PkgNode).FriendlyName(), g.Node(start).(*PkgNode).FriendlyName())
	for end != start {
		metaData.cycle = append(metaData.cycle, start)
		logger.Log.Tracef("%s needed by %s", g.Node(start).(*PkgNode).FriendlyName(), g.Node(metaData.parent[start]).(*PkgNode).FriendlyName())
		start = metaData.parent[start]
	}
	metaData.cycle = append(metaData.cycle, end)
}

func dfs(g *PkgGraph, u int64, metaData *dfsData) (foundCycle bool, err error) {
	if metaData.state[u] != unvisited {
		err = fmt.Errorf("Node %d is in a bad state (%d)", u, metaData.state[u])
		return
	}

	metaData.state[u] = inProgress

	foundCycle = false
	for _, neighbor := range graph.NodesOf(g.From(u)) {
		v := neighbor.ID()
		if _, exists := metaData.state[v]; !exists {
			metaData.state[v] = unvisited
		}

		switch metaData.state[v] {
		case done:
			continue
		case unvisited:
			metaData.parent[v] = u
			foundCycle, err = dfs(g, v, metaData)
			if err != nil || foundCycle {
				return
			}
		case inProgress:
			logger.Log.Debug("Found cycle!")
			createCycle(g, metaData, u, v)
			foundCycle = true
			return
		default:
			err = fmt.Errorf("Node %d is in a bad state (%d)", v, metaData.state[v])
			return
		}
	}

	metaData.state[u] = done
	return
}

// FindAnyDirectedCycle returns any single cycle in the graph, if one exists.
func (g *PkgGraph) FindAnyDirectedCycle() (nodes []PkgNode, err error) {
	const goalNodeName = "_dfs_root_"

	metadata := dfsData{
		make(map[int64]int),
		make(map[int64]int64),
		make([]int64, 0),
	}

	// Create a temporary root node, by using a constant goalNodeName, it will act as a mutex against concurrent
	// cycle searches on a given graph as this below call will fail if there is already a goal node with the same value.
	rootNode, err := g.AddGoalNode(goalNodeName, nil, false)
	if err != nil {
		return
	}

	// This call will also remove all edges connected to the temporary root node.
	defer g.RemoveNode(rootNode.ID())

	metadata.parent[rootNode.ID()] = -1
	metadata.state[rootNode.ID()] = unvisited

	foundCycle, err := dfs(g, rootNode.ID(), &metadata)
	if err != nil {
		return
	}

	if foundCycle {
		for _, id := range metadata.cycle {
			nodes = append(nodes, *g.Node(id).(*PkgNode))
		}
	}

	return
}
