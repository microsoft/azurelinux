// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
)

func LoadLearner() (l *Learner) {
	l = NewLearner()

	content, err := ioutil.ReadFile("./learner_dump.json") // the file is inside the local directory
	if err != nil {
		fmt.Println("Err")
	}
	json.Unmarshal(content, l)

	return
}

// weighsIndividualNode determines the "weight" of a node by summing all build times
// between the goal node and the individual node
func WeighNodeCriticalPath(node *pkggraph.PkgNode, pkgGraph *pkggraph.PkgGraph, goalNode *pkggraph.PkgNode, l *Learner) float64 {
	if node == goalNode {
		return 0.0
	}

	if node.Type != pkggraph.TypeBuild{
		return 0.0
	}

	maxWeight := 0.0
	dependents := pkgGraph.To(node.ID())
	for dependents.Next() {
		dependent := dependents.Node().(*pkggraph.PkgNode)
		maxWeight = math.Max(maxWeight, WeighNodeCriticalPath(dependent, pkgGraph, goalNode, l))
	}
	nodeBuildTime := getBuildTime(l, node.RpmPath)
	return nodeBuildTime + maxWeight

}

func getBuildTime(l *Learner, rpmPath string) (buildTime float64) {
	logger.Log.Debugf("debuggy! %s", rpmPath)
	rpmId, err := ParseRpmIdentity(rpmPath)
	if err != nil {
		logger.Log.Warnf("Failed to parse rpm identity for fullRpmPath: %s \n err: %s", rpmPath, err)
	}

	buildTime = float64(l.Results[rpmId.FullName].BuildTime)
	return
}
