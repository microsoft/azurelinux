// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package pkggraph

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestDFSFindCycle(t *testing.T) {
	g, err := buildTestGraphHelper()
	assert.NoError(t, err)
	assert.NotNil(t, g)

	// Create a cycle
	addEdgeHelper(g, *pkgCBuild, *pkgARun)

	// Check the correctness of the disconnected components rooted in pkgARun, and pkgC2Run
	checkTestGraph(t, g)

	cycle, err := g.FindAnyDirectedCycle()
	assert.NoError(t, err)
	assert.NotNil(t, cycle)
	assert.Equal(t, 7, len(cycle))
	assert.Equal(t, cycle[0], cycle[len(cycle)-1])
}

func TestDFSNoCycle(t *testing.T) {
	g, err := buildTestGraphHelper()
	assert.NoError(t, err)
	assert.NotNil(t, g)

	// Check the correctness of the disconnected components rooted in pkgARun, and pkgC2Run
	checkTestGraph(t, g)

	cycle, err := g.FindAnyDirectedCycle()
	assert.NoError(t, err)
	assert.Nil(t, cycle)
}
