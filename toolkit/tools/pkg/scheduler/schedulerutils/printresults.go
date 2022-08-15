// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"encoding/csv"
	"os"
	"path/filepath"
	"sync"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
)

// PrintBuildResult prints a build result to the logger.
func PrintBuildResult(res *BuildResult) {
	baseSRPMName := res.Node.SRPMFileName()

	if res.Err != nil {
		logger.Log.Errorf("Failed to build %s, error: %s, for details see: %s", baseSRPMName, res.Err, res.LogFile)
		return
	}

	if res.Node.Type == pkggraph.TypeBuild {
		if res.Skipped {
			logger.Log.Warnf("Skipped build for '%s' per user request. RPMs expected to be present: %v", baseSRPMName, res.BuiltFiles)
		} else if res.UsedCache {
			logger.Log.Infof("Prebuilt: %s -> %v", baseSRPMName, res.BuiltFiles)
		} else {
			logger.Log.Infof("Built: %s -> %v", baseSRPMName, res.BuiltFiles)
		}
	} else {
		logger.Log.Debugf("Processed node %s", res.Node.FriendlyName())
	}
}

// RecordBuildSummary stores the summary in to a csv.
func RecordBuildSummary(pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex, buildState *GraphBuildState, outputPath string) {

	graphMutex.RLock()
	defer graphMutex.RUnlock()

	failedSRPMs := make(map[string]*pkggraph.PkgNode)
	failures := buildState.BuildFailures()
	for _, failure := range failures {
		failedSRPMs[failure.Node.SrpmPath] = failure.Node
	}

	prebuiltSRPMs := make(map[string]*pkggraph.PkgNode)
	builtSRPMs := make(map[string]*pkggraph.PkgNode)
	unbuiltSRPMs := make(map[string]*pkggraph.PkgNode)
	unresolvedDependencies := make(map[string]bool)

	buildNodes := pkgGraph.AllBuildNodes()
	for _, node := range buildNodes {
		if buildState.IsNodeCached(node) {
			prebuiltSRPMs[node.SrpmPath] = node
			continue
		} else if buildState.IsNodeAvailable(node) {
			builtSRPMs[node.SrpmPath] = node
			continue
		}

		_, found := failedSRPMs[node.SrpmPath]
		if !found {
			unbuiltSRPMs[node.SrpmPath] = node
		}
	}

	for _, node := range pkgGraph.AllRunNodes() {
		if node.State == pkggraph.StateUnresolved {
			unresolvedDependencies[node.VersionedPkg.String()] = true
		}
	}

	csvBlob := [][]string{{"Package", "State", "Blocker"}}

	for srpm := range builtSRPMs {
		csvBlob = append(csvBlob, []string{filepath.Base(builtSRPMs[srpm].SrpmPath), "Built"})
	}

	for srpm := range prebuiltSRPMs {
		csvBlob = append(csvBlob, []string{filepath.Base(prebuiltSRPMs[srpm].SrpmPath), "PreBuilt"})
	}

	for srpm := range failedSRPMs {
		node := failedSRPMs[srpm]
		csvRow := []string{filepath.Base(node.SrpmPath), "Failed"}

		// Failed nodes shouldn't have any blockers
		blocking_nodes_str := ""
		fromNodes := pkgGraph.From(node.ID())
		for fromNodes.Next() {
			fromNode := fromNodes.Node().(*pkggraph.PkgNode)
			if _, found := failedSRPMs[fromNode.SrpmPath]; found {
				blocking_nodes_str += filepath.Base(fromNode.SrpmPath) + "-FAIL "
			}
			if _, found := unbuiltSRPMs[fromNode.SrpmPath]; found {
				blocking_nodes_str += filepath.Base(fromNode.SrpmPath) + "-UNBUILT "
			}
		}

		csvRow = append(csvRow, blocking_nodes_str)
		csvBlob = append(csvBlob, csvRow)
	}

	for srpm := range unbuiltSRPMs {
		node := unbuiltSRPMs[srpm]
		csvRow := []string{filepath.Base(node.SrpmPath), "Unbuilt"}

		blocking_nodes_str := ""
		fromNodes := pkgGraph.From(node.ID())
		for fromNodes.Next() {
			fromNode := fromNodes.Node().(*pkggraph.PkgNode)
			if _, found := failedSRPMs[fromNode.SrpmPath]; found {
				blocking_nodes_str += filepath.Base(fromNode.SrpmPath) + "-FAIL "
			}
			if _, found := unbuiltSRPMs[fromNode.SrpmPath]; found {
				blocking_nodes_str += filepath.Base(fromNode.SrpmPath) + "-UNBUILT "
			}
		}

		csvRow = append(csvRow, blocking_nodes_str)
		csvBlob = append(csvBlob, csvRow)
	}

	csvFile, err := os.Create(outputPath)
	if err != nil {
		logger.Log.Warnf("Unable to create '%s' file. Error: %s", outputPath, err)
		return
	}
	defer csvFile.Close()

	csvWriter := csv.NewWriter(csvFile)
	err = csvWriter.WriteAll(csvBlob)
	if err != nil {
		logger.Log.Warnf("Failed to write to CSV file '%s'. Error: %s", outputPath, err)
	}
}

// PrintBuildSummary prints the summary of the entire build to the logger.
func PrintBuildSummary(pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex, buildState *GraphBuildState) {
	graphMutex.RLock()
	defer graphMutex.RUnlock()

	failedSRPMs := make(map[string]bool)
	failures := buildState.BuildFailures()
	for _, failure := range failures {
		failedSRPMs[failure.Node.SrpmPath] = true
	}

	prebuiltSRPMs := make(map[string]bool)
	builtSRPMs := make(map[string]bool)
	unbuiltSRPMs := make(map[string]bool)
	unresolvedDependencies := make(map[string]bool)
	rpmConflicts := buildState.ConflictingRPMs()
	srpmConflicts := buildState.ConflictingSRPMs()

	buildNodes := pkgGraph.AllBuildNodes()
	for _, node := range buildNodes {
		if buildState.IsNodeCached(node) {
			prebuiltSRPMs[node.SrpmPath] = true
			continue
		} else if buildState.IsNodeAvailable(node) {
			builtSRPMs[node.SrpmPath] = true
			continue
		}

		_, found := failedSRPMs[node.SrpmPath]
		if !found {
			unbuiltSRPMs[node.SrpmPath] = true
		}
	}

	for _, node := range pkgGraph.AllRunNodes() {
		if node.State == pkggraph.StateUnresolved {
			unresolvedDependencies[node.VersionedPkg.String()] = true
		}
	}

	logger.Log.Info("---------------------------")
	logger.Log.Info("--------- Summary ---------")
	logger.Log.Info("---------------------------")

	logger.Log.Infof("Number of built SRPMs:             %d", len(builtSRPMs))
	logger.Log.Infof("Number of prebuilt SRPMs:          %d", len(prebuiltSRPMs))
	logger.Log.Infof("Number of failed SRPMs:            %d", len(failures))
	logger.Log.Infof("Number of blocked SRPMs:           %d", len(unbuiltSRPMs))
	logger.Log.Infof("Number of unresolved dependencies: %d", len(unresolvedDependencies))
	if len(rpmConflicts) > 0 || len(srpmConflicts) > 0 {
		logger.Log.Errorf("Number of toolchain RPM conflicts: %d", len(rpmConflicts))
		logger.Log.Errorf("Number of toolchain SRPM conflicts: %d", len(srpmConflicts))
	} else {
		logger.Log.Infof("Number of toolchain RPM conflicts: %d", len(rpmConflicts))
		logger.Log.Infof("Number of toolchain SRPM conflicts: %d", len(srpmConflicts))
	}

	if len(builtSRPMs) != 0 {
		logger.Log.Info("Built SRPMs:")
		for srpm := range builtSRPMs {
			logger.Log.Infof("--> %s", filepath.Base(srpm))
		}
	}

	if len(prebuiltSRPMs) != 0 {
		logger.Log.Info("Prebuilt SRPMs:")
		for srpm := range prebuiltSRPMs {
			logger.Log.Infof("--> %s", filepath.Base(srpm))
		}
	}

	if len(failures) != 0 {
		logger.Log.Info("Failed SRPMs:")
		for _, failure := range failures {
			logger.Log.Infof("--> %s , error: %s, for details see: %s", failure.Node.SRPMFileName(), failure.Err, failure.LogFile)
		}
	}

	if len(unbuiltSRPMs) != 0 {
		logger.Log.Info("Blocked SRPMs:")
		for srpm := range unbuiltSRPMs {
			logger.Log.Infof("--> %s", filepath.Base(srpm))
		}
	}

	if len(unresolvedDependencies) != 0 {
		logger.Log.Info("Unresolved dependencies:")
		for dependency := range unresolvedDependencies {
			logger.Log.Infof("--> %s", dependency)
		}
	}

	if len(rpmConflicts) != 0 {
		logger.Log.Error("RPM Conflicts with toolchain:")
		for _, conflict := range rpmConflicts {
			logger.Log.Errorf("--> %s", conflict)
		}
	}

	if len(srpmConflicts) != 0 {
		logger.Log.Error("SRPM Conflicts with toolchain:")
		for _, conflict := range srpmConflicts {
			logger.Log.Errorf("--> %s", conflict)
		}
	}
}
