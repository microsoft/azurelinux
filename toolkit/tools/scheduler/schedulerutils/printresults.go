// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"sync"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/sliceutils"
)

const (
	colorReset = "\033[33m"
	colorRed   = "\033[31m"
	colorGreen = "\033[32m"
	colorBlue  = "\033[34m"
)

func printInRed(inputString string) string {
	return colorRed + inputString + colorReset
}

func printInGreen(inputString string) string {
	return colorGreen + inputString + colorReset
}

func printInBlue(inputString string) string {
	return colorBlue + inputString + colorReset
}

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
		if res.Ignored {
			logger.Log.Warnf("Ignored test for '%s' per user request.", baseSRPMName)
		} else if res.UsedCache {
			logger.Log.Infof("Skipped test: %s", baseSRPMName)
		} else {
			logger.Log.Infof("Tested: %s", baseSRPMName)
		}
	default:
		logger.Log.Debugf("Processed node %s", res.Node.FriendlyName())
	}
}

// RecordBuildSummary stores the summary in to a csv.
func RecordBuildSummary(pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex, buildState *GraphBuildState, outputPath string) {
	graphMutex.RLock()
	defer graphMutex.RUnlock()

	failedSRPMs, prebuiltSRPMs, prebuiltDeltaSRPMs, builtSRPMs, blockedSRPMs := getSRPMsState(pkgGraph, buildState)
	failedBuildNodes := buildResultsSetToNodesSet(failedSRPMs)

	failedSRPMsTests, _, testedSRPMs, blockedSRPMsTests := getSRPMsTestsState(pkgGraph, buildState)
	failedTestNodes := buildResultsSetToNodesSet(failedSRPMsTests)

	csvBlob := [][]string{{"Package", "State", "Blocker", "IsTest"}}

	csvBlob = append(csvBlob, successfulPackagesCSVRows(builtSRPMs, "Built", false)...)
	csvBlob = append(csvBlob, successfulPackagesCSVRows(prebuiltSRPMs, "PreBuilt", false)...)
	csvBlob = append(csvBlob, successfulPackagesCSVRows(prebuiltDeltaSRPMs, "PreBuiltDelta", false)...)
	// Failed nodes shouldn't have any blockers
	csvBlob = append(csvBlob, unbuiltPackagesCSVRows(pkgGraph, failedBuildNodes, failedBuildNodes, blockedSRPMs, false)...)
	csvBlob = append(csvBlob, unbuiltPackagesCSVRows(pkgGraph, blockedSRPMs, failedBuildNodes, blockedSRPMs, false)...)

	csvBlob = append(csvBlob, successfulPackagesCSVRows(testedSRPMs, "Built", true)...)
	csvBlob = append(csvBlob, unbuiltPackagesCSVRows(pkgGraph, failedTestNodes, failedTestNodes, blockedSRPMsTests, true)...)
	csvBlob = append(csvBlob, unbuiltPackagesCSVRows(pkgGraph, blockedSRPMsTests, failedTestNodes, blockedSRPMsTests, true)...)

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

	failedSRPMs, prebuiltSRPMs, prebuiltDeltaSRPMs, builtSRPMs, blockedSRPMs := getSRPMsState(pkgGraph, buildState)
	failedSRPMsTests, skippedSRPMsTests, testedSRPMs, blockedSRPMsTests := getSRPMsTestsState(pkgGraph, buildState)

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

	// print summary
	printSummary(failedSRPMs, failedSRPMsTests, prebuiltSRPMs, prebuiltDeltaSRPMs, builtSRPMs, testedSRPMs, skippedSRPMsTests, unresolvedDependencies, blockedSRPMs, blockedSRPMsTests, rpmConflicts, srpmConflicts, allowToolchainRebuilds, conflictsLogger)

	if len(prebuiltSRPMs) != 0 {
		logger.Log.Info(printInGreen("Prebuilt SRPMs:"))
		keys := sliceutils.SetToSliceAll(prebuiltSRPMs)
		sort.Strings(keys)
		for _, prebuiltSRPM := range keys {
			logger.Log.Infof("--> %s", filepath.Base(prebuiltSRPM))
		}
	}

	if len(prebuiltDeltaSRPMs) != 0 {
		logger.Log.Info(printInBlue("Skipped SRPMs (i.e., delta mode is on, packages are already available in a repo):"))
		keys := sliceutils.SetToSliceAll(prebuiltDeltaSRPMs)
		sort.Strings(keys)
		for _, prebuiltDeltaSRPM := range keys {
			logger.Log.Infof("--> %s", filepath.Base(prebuiltDeltaSRPM))
		}
	}

	if len(skippedSRPMsTests) != 0 {
		logger.Log.Info(printInBlue("Skipped SRPMs tests:"))
		keys := sliceutils.SetToSliceAll(skippedSRPMsTests)
		sort.Strings(keys)
		for _, skippedSRPMsTest := range keys {
			logger.Log.Infof("--> %s", filepath.Base(skippedSRPMsTest))
		}
	}

	if len(builtSRPMs) != 0 {
		logger.Log.Info(printInGreen("Built SRPMs:"))
		keys := sliceutils.SetToSliceAll(builtSRPMs)
		sort.Strings(keys)
		for _, builtSRPM := range keys {
			logger.Log.Infof("--> %s ", filepath.Base(builtSRPM))
		}
	}

	if len(testedSRPMs) != 0 {
		logger.Log.Info(printInGreen("Tested SRPMs:"))
		keys := sliceutils.SetToSliceAll(testedSRPMs)
		sort.Strings(keys)
		for _, testedSRPM := range keys {
			logger.Log.Infof("--> %s", filepath.Base(testedSRPM))
		}
	}

	if len(unresolvedDependencies) != 0 {
		logger.Log.Info(printInRed("Unresolved dependencies:"))
		keys := sliceutils.SetToSliceAll(unresolvedDependencies)
		sort.Strings(keys)
		for _, unresolvedDependency := range keys {
			logger.Log.Infof("--> %s", filepath.Base(unresolvedDependency))
		}
	}

	if len(blockedSRPMs) != 0 {
		logger.Log.Info(printInRed("Blocked SRPMs:"))
		keys := sliceutils.SetToSliceAll(blockedSRPMs)
		sort.Strings(keys)
		for _, blockedSRPM := range keys {
			logger.Log.Infof("--> %s", filepath.Base(blockedSRPM))
		}
	}

	if len(blockedSRPMsTests) != 0 {
		logger.Log.Info(printInRed("Blocked SRPMs tests:"))
		keys := sliceutils.SetToSliceAll(blockedSRPMsTests)
		sort.Strings(keys)
		for _, blockedSRPMsTest := range keys {
			logger.Log.Infof("--> %s", filepath.Base(blockedSRPMsTest))
		}
	}

	if len(rpmConflicts) != 0 {
		conflictsLogger(printInRed("RPM conflicts with toolchain:"))
		sort.Strings(rpmConflicts)
		for _, conflict := range rpmConflicts {
			conflictsLogger("--> %s", conflict)
		}
	}

	if len(srpmConflicts) != 0 {
		conflictsLogger(printInRed("SRPM conflicts with toolchain:"))
		sort.Strings(srpmConflicts)
		for _, conflict := range srpmConflicts {
			conflictsLogger("--> %s", conflict)
		}
	}

	if len(failedSRPMs) != 0 {
		logger.Log.Info(printInRed("Failed SRPMs:"))
		keys := sliceutils.SetToSliceAll(failedSRPMs)
		sort.Strings(keys)
		for _, key := range keys {
			failure := failedSRPMs[key]
			logger.Log.Infof("--> %s , error: %s, for details see: %s", failure.Node.SRPMFileName(), failure.Err, failure.LogFile)
		}
	}

	if len(failedSRPMsTests) != 0 {
		logger.Log.Info(printInRed("Failed SRPMs tests:"))
		keys := sliceutils.SetToSliceAll(failedSRPMsTests)
		sort.Strings(keys)
		for _, key := range keys {
			failure := failedSRPMsTests[key]
			logger.Log.Infof("--> %s , error: %s, for details see: %s", failure.Node.SRPMFileName(), failure.Err, failure.LogFile)
		}
	}

	// print summary
	printSummary(failedSRPMs, failedSRPMsTests, prebuiltSRPMs, prebuiltDeltaSRPMs, builtSRPMs, testedSRPMs, skippedSRPMsTests, unresolvedDependencies, blockedSRPMs, blockedSRPMsTests, rpmConflicts, srpmConflicts, allowToolchainRebuilds, conflictsLogger)
}

func buildResultsSetToNodesSet(statesSet map[string]*BuildResult) (result map[string]*pkggraph.PkgNode) {
	result = make(map[string]*pkggraph.PkgNode, len(statesSet))
	for srpm, state := range statesSet {
		result[srpm] = state.Node
	}

	return
}

func getSRPMsState(pkgGraph *pkggraph.PkgGraph, buildState *GraphBuildState) (failedSRPMs map[string]*BuildResult, prebuiltSRPMs, prebuiltDeltaSRPMs, builtSRPMs map[string]bool, blockedSRPMs map[string]*pkggraph.PkgNode) {
	failedSRPMs = make(map[string]*BuildResult)
	prebuiltSRPMs = make(map[string]bool)
	prebuiltDeltaSRPMs = make(map[string]bool)
	builtSRPMs = make(map[string]bool)
	blockedSRPMs = make(map[string]*pkggraph.PkgNode)

	for _, failure := range buildState.BuildFailures() {
		if failure.Node.Type == pkggraph.TypeLocalBuild {
			failedSRPMs[failure.Node.SrpmPath] = failure
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
			builtSRPMs[node.SrpmPath] = true
			continue
		}

		_, found := failedSRPMs[node.SrpmPath]
		if !found {
			blockedSRPMs[node.SrpmPath] = node
		}
	}

	return
}

func getSRPMsTestsState(pkgGraph *pkggraph.PkgGraph, buildState *GraphBuildState) (failedSRPMsTests map[string]*BuildResult, skippedSRPMsTests, testedSRPMs map[string]bool, blockedSRPMsTests map[string]*pkggraph.PkgNode) {
	failedSRPMsTests = make(map[string]*BuildResult)
	skippedSRPMsTests = make(map[string]bool)
	testedSRPMs = make(map[string]bool)
	blockedSRPMsTests = make(map[string]*pkggraph.PkgNode)

	for _, failure := range buildState.BuildFailures() {
		if failure.Node.Type == pkggraph.TypeTest {
			failedSRPMsTests[failure.Node.SrpmPath] = failure
		}
	}

	for _, node := range pkgGraph.AllTestNodes() {
		if buildState.IsNodeCached(node) {
			skippedSRPMsTests[node.SrpmPath] = true
			continue
		} else if buildState.IsNodeAvailable(node) {
			testedSRPMs[node.SrpmPath] = true
			continue
		}

		_, found := failedSRPMsTests[node.SrpmPath]
		if !found {
			blockedSRPMsTests[node.SrpmPath] = node
		}
	}

	return
}

func successfulPackagesCSVRows(unblockedPackages map[string]bool, state string, isTest bool) (csvRows [][]string) {
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

func unbuiltPackagesCSVRows(pkgGraph *pkggraph.PkgGraph, unbuiltPackages, failedPackages, blockedPackages map[string]*pkggraph.PkgNode, isTest bool) (csvRows [][]string) {
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

// Helper function to print summarized numbers of the build to the logger.
func printSummary(failedSRPMs, failedSRPMsTests map[string]*BuildResult, prebuiltSRPMs, prebuiltDeltaSRPMs, builtSRPMs, testedSRPMs, skippedSRPMsTests, unresolvedDependencies map[string]bool, blockedSRPMs, blockedSRPMsTests map[string]*pkggraph.PkgNode, rpmConflicts, srpmConflicts []string, allowToolchainRebuilds bool, conflictsLogger func(format string, args ...interface{})) {
	logger.Log.Info("---------------------------")
	logger.Log.Info("--------- Summary ---------")
	logger.Log.Info("---------------------------")

	logger.Log.Infof(printInGreen("Number of prebuilt SRPMs:           " + fmt.Sprint(len(prebuiltSRPMs))))
	logger.Log.Infof(printInBlue("Number of prebuilt delta SRPMs:     " + fmt.Sprint(len(prebuiltDeltaSRPMs))))
	logger.Log.Infof(printInBlue("Number of skipped SRPMs tests:      " + fmt.Sprint(len(skippedSRPMsTests))))
	logger.Log.Infof(printInGreen("Number of built SRPMs:              " + fmt.Sprint(len(builtSRPMs))))
	logger.Log.Infof(printInGreen("Number of tested SRPMs:             " + fmt.Sprint(len(testedSRPMs))))
	logger.Log.Infof(printInRed("Number of unresolved dependencies:  " + fmt.Sprint(len(unresolvedDependencies))))
	logger.Log.Infof(printInRed("Number of blocked SRPMs:            " + fmt.Sprint(len(blockedSRPMs))))
	logger.Log.Infof(printInRed("Number of blocked SRPMs tests:      " + fmt.Sprint(len(blockedSRPMsTests))))
	logger.Log.Infof(printInRed("Number of failed SRPMs:             " + fmt.Sprint(len(failedSRPMs))))
	logger.Log.Infof(printInRed("Number of failed SRPMs tests:       " + fmt.Sprint(len(failedSRPMsTests))))

	if allowToolchainRebuilds && (len(rpmConflicts) > 0 || len(srpmConflicts) > 0) {
		logger.Log.Infof("Toolchain RPMs conflicts are ignored since ALLOW_TOOLCHAIN_REBUILDS=y")
	}

	if len(rpmConflicts) > 0 || len(srpmConflicts) > 0 {
		conflictsLogger(printInRed("Number of toolchain RPM conflicts:  " + fmt.Sprint(len(rpmConflicts))))
		conflictsLogger(printInRed("Number of toolchain SRPM conflicts: " + fmt.Sprint(len(srpmConflicts))))
	}
}
