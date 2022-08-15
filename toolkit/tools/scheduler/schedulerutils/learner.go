// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"strconv"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
)

type RpmIdentity struct {
	FullName   string
	Name       string
	Version    string
	Release    int64
	MarinerVer string
	Arch       string
}

type LearnerResult struct {
	Rpm              RpmIdentity
	BuildTime        float32
	ImplicitProvides []string
}

type Learner struct {
	Results           map[string]LearnerResult
	ImplicitProviders map[string][]string
}

func NewLearner() (l *Learner) {
	return &Learner{
		Results:           make(map[string]LearnerResult),
		ImplicitProviders: make(map[string][]string),
	}
}

func LoadLearner() (l *Learner) {
	l = NewLearner()

	content, err := ioutil.ReadFile("./learner_dump.json") // the file is currently assumed to be in the local toolkit directory
	if err != nil {
		fmt.Println("Err")
	}
	json.Unmarshal(content, l)

	return
}

func (l *Learner) RecordUnblocks(dynamicDep *pkgjson.PackageVer, provider *pkggraph.PkgNode) {
	rpmId, err := ParseRpmIdentity(provider.RpmPath)
	if err != nil {
		logger.Log.Warnf("Failed to parse rpm identity for fullRpmPath: %s \n err: %s", provider.RpmPath, err)
	}

	learnerResult, exists := l.Results[rpmId.FullName]
	if !exists {
		l.Results[rpmId.FullName] = LearnerResult{
			Rpm:              rpmId,
			BuildTime:        0,
			ImplicitProvides: []string{dynamicDep.Name},
		}
	} else {
		learnerResult.ImplicitProvides = append(learnerResult.ImplicitProvides, dynamicDep.Name)
		l.Results[rpmId.FullName] = learnerResult
	}
	providers, exists := l.ImplicitProviders[dynamicDep.Name]
	if !exists {
		l.ImplicitProviders[dynamicDep.Name] = []string{rpmId.FullName}
	} else {
		l.ImplicitProviders[dynamicDep.Name] = append(providers, rpmId.FullName)
	}
}

func (l *Learner) RecordBuildTime(res *BuildResult) {
	if res.Node.Type == pkggraph.TypeBuild {
		rpmId, err := ParseRpmIdentity(res.Node.RpmPath)
		if err != nil {
			logger.Log.Warnf("Failed to parse rpm identity for fullRpmPath: %s \n err: %s", res.Node.RpmPath, err)
		}

		learnerResult, exists := l.Results[rpmId.FullName]
		if !exists {
			l.Results[rpmId.FullName] = LearnerResult{
				Rpm:              rpmId,
				BuildTime:        res.BuildTime,
				ImplicitProvides: make([]string, 0),
			}
		} else {
			learnerResult.BuildTime = res.BuildTime
			l.Results[rpmId.FullName] = learnerResult
		}
	}
}

func (l *Learner) GetExpectedBuildTime(rpmPath string) (buildTime float64) {
	logger.Log.Debugf("debuggy! %s", rpmPath)
	rpmId, err := ParseRpmIdentity(rpmPath)
	if err != nil {
		logger.Log.Warnf("Failed to parse rpm identity for fullRpmPath: %s \n err: %s", rpmPath, err)
	}

	buildTime = float64(l.Results[rpmId.FullName].BuildTime)
	return
}

// weighsIndividualNode determines the "weight" of a node by summing all build times
// between the goal node and the individual node
func (l *Learner) WeighNodeCriticalPath(node *pkggraph.PkgNode, pkgGraph *pkggraph.PkgGraph, goalNode *pkggraph.PkgNode) float64 {
	if node == goalNode {
		return 0.0
	}

	if node.Type != pkggraph.TypeBuild {
		return 0.0
	}

	maxWeight := 0.0
	dependents := pkgGraph.To(node.ID())
	for dependents.Next() {
		dependent := dependents.Node().(*pkggraph.PkgNode)
		maxWeight = math.Max(maxWeight, l.WeighNodeCriticalPath(dependent, pkgGraph, goalNode))
	}
	nodeBuildTime := l.GetExpectedBuildTime(node.RpmPath)
	return nodeBuildTime + maxWeight

}

func (l *Learner) Dump(path string) {
	j, err := json.MarshalIndent(l, "", "  ")
	if err != nil {
		logger.Log.Error(err)
	}
	file, err := os.Create(path)
	if err != nil {
		logger.Log.Error(err)
	}
	defer file.Close()
	_, err = file.Write(j)
	if err != nil {
		logger.Log.Errorf("Failed to write learner payload, err: %s", err)
	}
	file.Sync()
}

func ParseRpmIdentity(fullRpmPath string) (rpmId RpmIdentity, err error) {
	pathParts := strings.Split(fullRpmPath, "/")
	fullName := pathParts[len(pathParts)-1]

	nameParts := strings.Split(fullName, "-")
	name := nameParts[0]
	ver := nameParts[1]
	trailing := nameParts[2]

	trailingParts := strings.Split(trailing, ".")
	rel, err := strconv.ParseInt(trailingParts[0], 10, 64)
	if err != nil {
		return
	}
	marinerVer := trailingParts[1]
	arch := trailingParts[2]

	rpmId = RpmIdentity{
		FullName:   fullName,
		Name:       name,
		Version:    ver,
		Release:    rel,
		MarinerVer: marinerVer,
		Arch:       arch,
	}
	return
}
