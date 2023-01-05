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
	"sync"

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
	ImplicitProviders map[string][]pkgjson.PackageVer
}

func NewLearner() (l *Learner) {
	return &Learner{
		Results:           make(map[string]LearnerResult),
		ImplicitProviders: make(map[string][]pkgjson.PackageVer),
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

//Return value between 1-10. 10 being highest priority
func (l *Learner) DeterminePriority(pkgGraph *pkggraph.PkgGraph, node *pkggraph.PkgNode, goal *pkggraph.PkgNode, highPriorityProviders map[*pkggraph.PkgNode]bool, learner *Learner) float32 {
	var priorityLevel float32

	weightToGoalNode := l.WeighCriticalPathToGoal(node, pkgGraph, goal)

	//the higher the weight between our node and the goal node the more it should be prioritized since it's blocking a longer path.
	//TODO: normalize the weights based on overall build time so this isn't arbitrarily deciding what is "long"
	if weightToGoalNode > 20.0 {
		priorityLevel = 8.0
	}
	//if this node is part of the high priority set, overwrite pri with highest priority
	if _, ok := highPriorityProviders[node]; ok {
		priorityLevel = 10.0
	}
	return priorityLevel
}

func (l *Learner) InformGraph(pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex, useCachedImplicit bool, goalNode *pkggraph.PkgNode) map[*pkggraph.PkgNode]bool {
	logger.Log.Info(`⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣶⣿⣿⣷⣶⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
					⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣾⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀
					⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⡟⠁⣰⣿⣿⣿⡿⠿⠻⠿⣿⣿⣿⣿⣧⠀⠀⠀⠀
					⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⠏⠀⣴⣿⣿⣿⠉⠀⠀⠀⠀⠀⠈⢻⣿⣿⣇⠀⠀⠀
					⠀⠀⠀⠀⢀⣠⣼⣿⣿⡏⠀⢠⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⡀⠀⠀
					⠀⠀⠀⣰⣿⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀
					⠀⠀⢰⣿⣿⡿⣿⣿⣿⡇⠀⠘⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⢀⣸⣿⣿⣿⠁⠀⠀
					⠀⠀⣿⣿⣿⠁⣿⣿⣿⡇⠀⠀⠻⣿⣿⣿⣷⣶⣶⣶⣶⣶⣿⣿⣿⣿⠃⠀⠀⠀
					⠀⢰⣿⣿⡇⠀⣿⣿⣿⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀
					⠀⢸⣿⣿⡇⠀⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠛⠉⢉⣿⣿⠀⠀⠀⠀⠀⠀
					⠀⢸⣿⣿⣇⠀⣿⣿⣿⠀⠀⠀⠀⠀⢀⣤⣤⣤⡀⠀⠀⢸⣿⣿⣿⣷⣦⠀⠀⠀
					⠀⠀⢻⣿⣿⣶⣿⣿⣿⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣦⡀⠀⠉⠉⠻⣿⣿⡇⠀⠀
					⠀⠀⠀⠛⠿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠈⠹⣿⣿⣇⣀⠀⣠⣾⣿⣿⡇⠀⠀
					⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣦⣤⣤⣤⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀
					⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⢿⣿⣿⣿⣿⣿⣿⠿⠋⠉⠛⠋⠉⠉⠁⠀⠀⠀⠀
					⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠁`)
	// acquire a writer lock since this routine will collapse nodes
	graphMutex.Lock()
	defer graphMutex.Unlock()
	implicitPackagesToUnresolvedNodes := implicitPackagesToUnresolvedNodesInGraph(pkgGraph, useCachedImplicit)
	highPriorityProviders := make(map[*pkggraph.PkgNode]bool)
	for name, unresolvedNode := range implicitPackagesToUnresolvedNodes {
		logger.Log.Debugf("Mapping of %s to %v", name, unresolvedNode)
		if providers, ok := l.ImplicitProviders[name]; ok {
			minPathWeight := math.MaxFloat32
			var optimalProviderRunNode *pkggraph.PkgNode
			//determine provider with shortest historical build time according to learning payload.
			for _, provider := range providers {
				lookUpNode, err := pkgGraph.FindBestPkgNode(&provider)
				if err != nil {
					logger.Log.Warnf("Failed to find implicit provider defined by learnings in graph. err: %s", err)
					continue
				}
				providerWeight := l.WeighCriticalPathToLeaf(lookUpNode.BuildNode, pkgGraph)
				if providerWeight < minPathWeight {
					logger.Log.Infof("Found new best provider for %s: %v with expected total buildtime %f", name, lookUpNode.BuildNode, providerWeight)
					minPathWeight = providerWeight
					optimalProviderRunNode = lookUpNode.RunNode
				}
			}
			highPriorityProviders[optimalProviderRunNode] = true
			//logger.Log.Info("Settled on optimal provider %v with expected build time of %f", optimalProviderRunNode, minPathWeight)
			// if optimalProviderRunNode == nil {
			// 	logger.Log.Warnf("No optimal provider was found from learnings from providers: %v", providers)
			// }
		}
	}
	return highPriorityProviders
}

func (l *Learner) RecordUnblocks(dynamicDep string, provider *pkggraph.PkgNode) {
	rpmId, err := ParseRpmIdentity(provider.RpmPath)
	if err != nil {
		logger.Log.Warnf("Failed to parse rpm identity for fullRpmPath: %s \n err: %s", provider.RpmPath, err)
	}

	learnerResult, exists := l.Results[rpmId.FullName]
	if !exists {
		l.Results[rpmId.FullName] = LearnerResult{
			Rpm:              rpmId,
			BuildTime:        0,
			ImplicitProvides: []string{dynamicDep},
		}
	} else {
		learnerResult.ImplicitProvides = append(learnerResult.ImplicitProvides, dynamicDep)
		l.Results[rpmId.FullName] = learnerResult
	}
	providers, exists := l.ImplicitProviders[dynamicDep]
	if !exists {
		l.ImplicitProviders[dynamicDep] = []pkgjson.PackageVer{*provider.VersionedPkg}
	} else {
		l.ImplicitProviders[dynamicDep] = append(providers, *provider.VersionedPkg)
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

// todo: make it check for a cached/already built node, evaluate cost as 0
// weighsIndividualNode determines the "weight" of a node by summing all build times
// between the goal node and the individual node
func (l *Learner) WeighCriticalPathToGoal(node *pkggraph.PkgNode, pkgGraph *pkggraph.PkgGraph, goalNode *pkggraph.PkgNode) float64 {
	if node == goalNode {
		return 0.0
	}

	maxWeight := 0.0
	dependents := pkgGraph.To(node.ID())
	for dependents.Next() {
		dependent := dependents.Node().(*pkggraph.PkgNode)
		maxWeight = math.Max(maxWeight, l.WeighCriticalPathToGoal(dependent, pkgGraph, goalNode))
	}
	var nodeBuildTime float64
	if node.Type == pkggraph.TypeBuild {
		nodeBuildTime = l.GetExpectedBuildTime(node.RpmPath)
	} else {
		nodeBuildTime = 0
	}

	return nodeBuildTime + maxWeight
}

func (l *Learner) WeighCriticalPathToLeaf(node *pkggraph.PkgNode, pkgGraph *pkggraph.PkgGraph) float64 {
	// if node == goalNode {
	// 	return 0.0
	// }

	maxWeight := 0.0
	dependencies := pkgGraph.From(node.ID())

	// case leaf node
	if dependencies.Len() == 0 {
		if node.Type != pkggraph.TypeBuild {
			return 0.0
		}
		return l.GetExpectedBuildTime(node.RpmPath)
	}

	for dependencies.Next() {
		dependency := dependencies.Node().(*pkggraph.PkgNode)
		maxWeight = math.Max(maxWeight, l.WeighCriticalPathToLeaf(dependency, pkgGraph))
	}
	var nodeBuildTime float64
	if node.Type == pkggraph.TypeBuild {
		nodeBuildTime = l.GetExpectedBuildTime(node.RpmPath)
	} else {
		nodeBuildTime = 0
	}
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
