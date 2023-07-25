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

	switch res.Node.Type {
	case pkggraph.TypeLocalBuild:
		if res.Ignored {
			logger.Log.Warnf("Ignored build for '%s' per user request. RPMs expected to be present: %v", baseSRPMName, res.BuiltFiles)
		} else if res.UsedCache {
			logger.Log.Infof("Prebuilt: %s -> %v", baseSRPMName, res.BuiltFiles)
		} else {
			logger.Log.Infof("Built: %s -> %v", baseSRPMName, res.BuiltFiles)
		}
	case pkggraph.TypeTest:
		logger.Log.Infof("Tested: %s", baseSRPMName)
	default:
		logger.Log.Debugf("Processed node %s", res.Node.FriendlyName())
	}
}

// RecordBuildSummary stores the summary in to a csv.
func RecordBuildSummary(pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex, buildState *GraphBuildState, outputPath string) {
	graphMutex.RLock()
	defer graphMutex.RUnlock()

	failedRegularSRPMs, prebuiltSRPMs, prebuiltDeltaSRPMs, builtRegularSRPMs, blockedRegularSRPMs := getRegularSRPMsState(pkgGraph, buildState)
	failedRegularNodes := buildResultsSetToNodesSet(failedRegularSRPMs)

	failedTestSRPMs, builtTestSRPMs, blockedTestSRPMs := getTestSRPMsState(pkgGraph, buildState)
	failedTestNodes := buildResultsSetToNodesSet(failedTestSRPMs)

	csvBlob := [][]string{{"Package", "State", "Blocker", "IsTest"}}

	csvBlob = append(csvBlob, successfulPackagesCVSRows(builtRegularSRPMs, "Built", false)...)
	csvBlob = append(csvBlob, successfulPackagesCVSRows(prebuiltSRPMs, "PreBuilt", false)...)
	csvBlob = append(csvBlob, successfulPackagesCVSRows(prebuiltDeltaSRPMs, "PreBuiltDelta", false)...)
	// Failed nodes shouldn't have any blockers
	csvBlob = append(csvBlob, unbuiltPackagesCVSRows(pkgGraph, failedRegularNodes, failedRegularNodes, blockedRegularSRPMs, false)...)
	csvBlob = append(csvBlob, unbuiltPackagesCVSRows(pkgGraph, blockedRegularSRPMs, failedRegularNodes, blockedRegularSRPMs, false)...)

	csvBlob = append(csvBlob, successfulPackagesCVSRows(builtTestSRPMs, "Built", true)...)
	csvBlob = append(csvBlob, unbuiltPackagesCVSRows(pkgGraph, failedTestNodes, failedTestNodes, blockedTestSRPMs, true)...)
	csvBlob = append(csvBlob, unbuiltPackagesCVSRows(pkgGraph, blockedTestSRPMs, failedTestNodes, blockedTestSRPMs, true)...)

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
func PrintBuildSummary(pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex, buildState *GraphBuildState, allowToolchainRebuilds bool) {
	graphMutex.RLock()
	defer graphMutex.RUnlock()

	failedRegularSRPMs, prebuiltSRPMs, prebuiltDeltaSRPMs, builtRegularSRPMs, blockedRegularSRPMs := getRegularSRPMsState(pkgGraph, buildState)
	failedTestSRPMs, builtTestSRPMs, blockedTestSRPMs := getTestSRPMsState(pkgGraph, buildState)

	unresolvedDependencies := make(map[string]bool)
	rpmConflicts := buildState.ConflictingRPMs()
	srpmConflicts := buildState.ConflictingSRPMs()

	conflictsLogger := logger.Log.Errorf
	if allowToolchainRebuilds || (len(rpmConflicts) == 0 && len(srpmConflicts) == 0) {
		conflictsLogger = logger.Log.Infof
	}

	for _, node := range pkgGraph.AllRunNodes() {
		if node.State == pkggraph.StateUnresolved {
			unresolvedDependencies[node.VersionedPkg.String()] = true
		}
	}

	logger.Log.Info("---------------------------")
	logger.Log.Info("--------- Summary ---------")
	logger.Log.Info("---------------------------")

	logger.Log.Infof("Number of built regular SRPMs:     %d", len(builtRegularSRPMs))
	logger.Log.Infof("Number of built test SRPMs:        %d", len(builtTestSRPMs))
	logger.Log.Infof("Number of prebuilt SRPMs:          %d", len(prebuiltSRPMs))
	logger.Log.Infof("Number of prebuilt delta SRPMs:    %d", len(prebuiltDeltaSRPMs))
	logger.Log.Infof("Number of failed regular SRPMs:    %d", len(failedRegularSRPMs))
	logger.Log.Infof("Number of failed test SRPMs:       %d", len(failedTestSRPMs))
	logger.Log.Infof("Number of blocked regular SRPMs:   %d", len(blockedRegularSRPMs))
	logger.Log.Infof("Number of blocked test SRPMs:      %d", len(blockedTestSRPMs))
	logger.Log.Infof("Number of unresolved dependencies: %d", len(unresolvedDependencies))

	if allowToolchainRebuilds && (len(rpmConflicts) > 0 || len(srpmConflicts) > 0) {
		logger.Log.Infof("Toolchain RPMs conflicts are ignored since ALLOW_TOOLCHAIN_REBUILDS=y")
	}

	if len(rpmConflicts) > 0 || len(srpmConflicts) > 0 {
		conflictsLogger("Number of toolchain RPM conflicts: %d", len(rpmConflicts))
		conflictsLogger("Number of toolchain SRPM conflicts: %d", len(srpmConflicts))
	}

	if len(builtRegularSRPMs) != 0 {
		logger.Log.Info("Built regular SRPMs:")
		for srpm := range builtRegularSRPMs {
			logger.Log.Infof("--> %s", filepath.Base(srpm))
		}
	}

	if len(builtTestSRPMs) != 0 {
		logger.Log.Info("Built test SRPMs:")
		for srpm := range builtTestSRPMs {
			logger.Log.Infof("--> %s", filepath.Base(srpm))
		}
	}

	if len(prebuiltSRPMs) != 0 {
		logger.Log.Info("Prebuilt regular SRPMs:")
		for srpm := range prebuiltSRPMs {
			logger.Log.Infof("--> %s", filepath.Base(srpm))
		}
	}

	if len(prebuiltDeltaSRPMs) != 0 {
		logger.Log.Info("Skipped SRPMs (i.e., delta mode is on, packages are already available in a repo):")
		for srpm := range prebuiltDeltaSRPMs {
			logger.Log.Infof("--> %s", filepath.Base(srpm))
		}
	}

	if len(failedRegularSRPMs) != 0 {
		logger.Log.Info("Failed regular SRPMs:")
		for _, failure := range failedRegularSRPMs {
			logger.Log.Infof("--> %s , error: %s, for details see: %s", failure.Node.SRPMFileName(), failure.Err, failure.LogFile)
		}
	}

	if len(failedTestSRPMs) != 0 {
		logger.Log.Info("Failed test SRPMs:")
		for _, failure := range failedTestSRPMs {
			logger.Log.Infof("--> %s , error: %s, for details see: %s", failure.Node.SRPMFileName(), failure.Err, failure.LogFile)
		}
	}

	if len(blockedRegularSRPMs) != 0 {
		logger.Log.Info("Blocked regular SRPMs:")
		for srpm := range blockedRegularSRPMs {
			logger.Log.Infof("--> %s", filepath.Base(srpm))
		}
	}

	if len(blockedTestSRPMs) != 0 {
		logger.Log.Info("Blocked test SRPMs:")
		for srpm := range blockedTestSRPMs {
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
		conflictsLogger("RPM conflicts with toolchain: ")
		for _, conflict := range rpmConflicts {
			conflictsLogger("--> %s", conflict)
		}
	}

	if len(srpmConflicts) != 0 {
		conflictsLogger("SRPM conflicts with toolchain: ")
		for _, conflict := range srpmConflicts {
			conflictsLogger("--> %s", conflict)
		}
	}
}

func buildResultsSetToNodesSet(statesSet map[string]*BuildResult) (result map[string]*pkggraph.PkgNode) {
	result = make(map[string]*pkggraph.PkgNode, len(statesSet))
	for srpm, state := range statesSet {
		result[srpm] = state.Node
	}

	return
}

func getRegularSRPMsState(pkgGraph *pkggraph.PkgGraph, buildState *GraphBuildState) (failedRegularSRPMs map[string]*BuildResult, prebuiltSRPMs, prebuiltDeltaSRPMs, builtRegularSRPMs map[string]bool, blockedRegularSRPMs map[string]*pkggraph.PkgNode) {
	failedRegularSRPMs = make(map[string]*BuildResult)
	prebuiltSRPMs = make(map[string]bool)
	prebuiltDeltaSRPMs = make(map[string]bool)
	builtRegularSRPMs = make(map[string]bool)
	blockedRegularSRPMs = make(map[string]*pkggraph.PkgNode)

	// Check: do we only have build nodes (regular and test) in 'buildState'?
	for _, failure := range buildState.BuildFailures() {
		if failure.Node.Type == pkggraph.TypeLocalBuild {
			failedRegularSRPMs[failure.Node.SrpmPath] = failure
		}
	}

	for _, node := range pkgGraph.AllBuildNodes() {
		// A node can be a delta if it was build or cached. If it was cached we used the cached rpm. If it is not cached
		// that means it was built and we discard the delta rpm.
		if buildState.IsNodeCached(node) {
			if buildState.IsNodeDelta(node) {
				prebuiltDeltaSRPMs[node.SrpmPath] = true
			} else {
				prebuiltSRPMs[node.SrpmPath] = true
			}
			continue
		} else if buildState.IsNodeAvailable(node) {
			builtRegularSRPMs[node.SrpmPath] = true
			continue
		}

		_, found := failedRegularSRPMs[node.SrpmPath]
		if !found {
			blockedRegularSRPMs[node.SrpmPath] = node
		}
	}

	return
}

func getTestSRPMsState(pkgGraph *pkggraph.PkgGraph, buildState *GraphBuildState) (failedTestSRPMs map[string]*BuildResult, builtTestSRPMs map[string]bool, blockedTestSRPMs map[string]*pkggraph.PkgNode) {
	failedTestSRPMs = make(map[string]*BuildResult)
	builtTestSRPMs = make(map[string]bool)
	blockedTestSRPMs = make(map[string]*pkggraph.PkgNode)

	for _, failure := range buildState.BuildFailures() {
		if failure.Node.Type == pkggraph.TypeTest {
			failedTestSRPMs[failure.Node.SrpmPath] = failure
		}
	}

	for _, node := range pkgGraph.AllTestNodes() {
		if buildState.IsNodeAvailable(node) {
			builtTestSRPMs[node.SrpmPath] = true
			continue
		}

		_, found := failedTestSRPMs[node.SrpmPath]
		if !found {
			blockedTestSRPMs[node.SrpmPath] = node
		}
	}

	return
}

func successfulPackagesCVSRows(unblockedPackages map[string]bool, state string, isTest bool) (csvRows [][]string) {
	const emptyBlockers = ""

	isTestCell := testCellValue(isTest)

	csvRows = [][]string{}
	for srpm := range unblockedPackages {
		csvRows = append(csvRows, []string{filepath.Base(srpm), state, emptyBlockers, isTestCell})
	}

	return
}

func testCellValue(isTest bool) string {
	if isTest {
		return "1"
	}

	return "0"
}

func unbuiltPackagesCVSRows(pkgGraph *pkggraph.PkgGraph, unbuiltPackages, failedPackages, blockedPackages map[string]*pkggraph.PkgNode, isTest bool) (csvRows [][]string) {
	isTestCell := testCellValue(isTest)

	csvRows = [][]string{}
	for srpm, node := range unbuiltPackages {
		blockingNodesCell := ""
		fromNodes := pkgGraph.From(node.ID())
		for fromNodes.Next() {
			fromNode := fromNodes.Node().(*pkggraph.PkgNode)
			if _, found := failedPackages[fromNode.SrpmPath]; found {
				blockingNodesCell += filepath.Base(fromNode.SrpmPath) + "-FAIL "
			}
			if _, found := blockedPackages[fromNode.SrpmPath]; found {
				blockingNodesCell += filepath.Base(fromNode.SrpmPath) + "-UNBUILT "
			}
		}

		csvRow := []string{filepath.Base(srpm), "Failed", blockingNodesCell, isTestCell}
		csvRows = append(csvRows, csvRow)
	}

	return
}
