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

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"

	"github.com/fatih/color"
)

// Data on normal package builds extracted from GraphBuildState for use in the build summary.
type srpmBuildDataContainer struct {
	failedSRPMs        map[string]*BuildResult
	prebuiltSRPMs      map[string]bool
	prebuiltDeltaSRPMs map[string]bool
	builtSRPMs         map[string]bool
	blockedSRPMs       map[string]*pkggraph.PkgNode
}

// Data on package tests extracted from GraphBuildState for use in the build summary.
type srpmTestDataContainer struct {
	failedSRPMsTests  map[string]*BuildResult
	skippedSRPMsTests map[string]bool
	passedSRPMsTests  map[string]bool
	blockedSRPMsTests map[string]*pkggraph.PkgNode
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
		} else if res.CheckFailed {
			logger.Log.Warnf("Failed test: %s", baseSRPMName)
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

	srpmBuildData := getSRPMsState(pkgGraph, buildState)
	failedBuildNodes := buildResultsSetToNodesSet(srpmBuildData.failedSRPMs)

	srpmTestData := getSRPMsTestsState(pkgGraph, buildState)
	failedTestNodes := buildResultsSetToNodesSet(srpmTestData.failedSRPMsTests)

	csvBlob := [][]string{{"Package", "State", "Blocker", "IsTest"}}

	csvBlob = append(csvBlob, successfulPackagesCSVRows(srpmBuildData.builtSRPMs, "Built", false)...)
	csvBlob = append(csvBlob, successfulPackagesCSVRows(srpmBuildData.prebuiltSRPMs, "PreBuilt", false)...)
	csvBlob = append(csvBlob, successfulPackagesCSVRows(srpmBuildData.prebuiltDeltaSRPMs, "PreBuiltDelta", false)...)
	// Failed nodes shouldn't have any blockers
	csvBlob = append(csvBlob, unbuiltPackagesCSVRows(pkgGraph, failedBuildNodes, failedBuildNodes, srpmBuildData.blockedSRPMs, false)...)
	csvBlob = append(csvBlob, unbuiltPackagesCSVRows(pkgGraph, srpmBuildData.blockedSRPMs, failedBuildNodes, srpmBuildData.blockedSRPMs, false)...)

	csvBlob = append(csvBlob, successfulPackagesCSVRows(srpmTestData.passedSRPMsTests, "Built", true)...)
	csvBlob = append(csvBlob, unbuiltPackagesCSVRows(pkgGraph, failedTestNodes, failedTestNodes, srpmTestData.blockedSRPMsTests, true)...)
	csvBlob = append(csvBlob, unbuiltPackagesCSVRows(pkgGraph, srpmTestData.blockedSRPMsTests, failedTestNodes, srpmTestData.blockedSRPMsTests, true)...)

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

	srpmBuildData := getSRPMsState(pkgGraph, buildState)
	srpmTestData := getSRPMsTestsState(pkgGraph, buildState)

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

	printSummary(srpmBuildData, srpmTestData, unresolvedDependencies, rpmConflicts, srpmConflicts, allowToolchainRebuilds, conflictsLogger)

	if len(srpmBuildData.prebuiltSRPMs) != 0 {
		logger.Log.Info(color.GreenString("Prebuilt SRPMs:"))
		keys := mapToSortedSlice(srpmBuildData.prebuiltSRPMs)
		for _, prebuiltSRPM := range keys {
			logger.Log.Infof("--> %s", filepath.Base(prebuiltSRPM))
		}
	}

	if len(srpmBuildData.prebuiltDeltaSRPMs) != 0 {
		logger.Log.Info(color.GreenString("Skipped SRPMs (i.e., delta mode is on, packages are already available in a repo):"))
		keys := mapToSortedSlice(srpmBuildData.prebuiltDeltaSRPMs)
		for _, prebuiltDeltaSRPM := range keys {
			logger.Log.Infof("--> %s", filepath.Base(prebuiltDeltaSRPM))
		}
	}

	if len(srpmTestData.skippedSRPMsTests) != 0 {
		logger.Log.Info(color.GreenString("Skipped SRPMs tests:"))
		keys := mapToSortedSlice(srpmTestData.skippedSRPMsTests)
		for _, skippedSRPMsTest := range keys {
			logger.Log.Infof("--> %s", filepath.Base(skippedSRPMsTest))
		}
	}

	if len(srpmBuildData.builtSRPMs) != 0 {
		logger.Log.Info(color.GreenString("Built SRPMs:"))
		keys := mapToSortedSlice(srpmBuildData.builtSRPMs)
		for _, builtSRPM := range keys {
			logger.Log.Infof("--> %s ", filepath.Base(builtSRPM))
		}
	}

	if len(srpmTestData.passedSRPMsTests) != 0 {
		logger.Log.Info(color.GreenString("Passed SRPMs tests:"))
		keys := mapToSortedSlice(srpmTestData.passedSRPMsTests)
		for _, testedSRPM := range keys {
			logger.Log.Infof("--> %s", filepath.Base(testedSRPM))
		}
	}

	if len(unresolvedDependencies) != 0 {
		logger.Log.Info(color.RedString("Unresolved dependencies:"))
		keys := mapToSortedSlice(unresolvedDependencies)
		for _, unresolvedDependency := range keys {
			logger.Log.Infof("--> %s", filepath.Base(unresolvedDependency))
		}
	}

	if len(srpmBuildData.blockedSRPMs) != 0 {
		logger.Log.Info(color.RedString("Blocked SRPMs:"))
		keys := mapToSortedSlice(srpmBuildData.blockedSRPMs)
		for _, blockedSRPM := range keys {
			logger.Log.Infof("--> %s", filepath.Base(blockedSRPM))
		}
	}

	if len(srpmTestData.blockedSRPMsTests) != 0 {
		logger.Log.Info(color.RedString("Blocked SRPMs tests:"))
		keys := mapToSortedSlice(srpmTestData.blockedSRPMsTests)
		for _, blockedSRPMsTest := range keys {
			logger.Log.Infof("--> %s", filepath.Base(blockedSRPMsTest))
		}
	}

	if len(rpmConflicts) != 0 {
		conflictsLogger(color.RedString("RPM conflicts with toolchain:"))
		sort.Strings(rpmConflicts)
		for _, conflict := range rpmConflicts {
			conflictsLogger("--> %s", conflict)
		}
	}

	if len(srpmConflicts) != 0 {
		conflictsLogger(color.RedString("SRPM conflicts with toolchain:"))
		sort.Strings(srpmConflicts)
		for _, conflict := range srpmConflicts {
			conflictsLogger("--> %s", conflict)
		}
	}

	if len(srpmBuildData.failedSRPMs) != 0 {
		logger.Log.Info(color.RedString("Failed SRPMs:"))
		keys := mapToSortedSlice(srpmBuildData.failedSRPMs)
		for _, key := range keys {
			failure := srpmBuildData.failedSRPMs[key]
			logger.Log.Infof("--> %s , error: %s, for details see: %s", failure.Node.SRPMFileName(), failure.Err, failure.LogFile)
		}
	}

	if len(srpmTestData.failedSRPMsTests) != 0 {
		logger.Log.Info(color.RedString("Failed SRPMs tests:"))
		keys := mapToSortedSlice(srpmTestData.failedSRPMsTests)
		for _, key := range keys {
			failure := srpmTestData.failedSRPMsTests[key]
			logger.Log.Infof("--> %s , for details see: %s", failure.Node.SRPMFileName(), failure.LogFile)
		}
	}

	printSummary(srpmBuildData, srpmTestData, unresolvedDependencies, rpmConflicts, srpmConflicts, allowToolchainRebuilds, conflictsLogger)
}

func buildResultsSetToNodesSet(statesSet map[string]*BuildResult) (result map[string]*pkggraph.PkgNode) {
	result = make(map[string]*pkggraph.PkgNode, len(statesSet))
	for srpm, state := range statesSet {
		result[srpm] = state.Node
	}

	return
}

func getSRPMsState(pkgGraph *pkggraph.PkgGraph, buildState *GraphBuildState) (srpmData srpmBuildDataContainer) {
	srpmData = srpmBuildDataContainer{
		failedSRPMs:        make(map[string]*BuildResult),
		prebuiltSRPMs:      make(map[string]bool),
		prebuiltDeltaSRPMs: make(map[string]bool),
		builtSRPMs:         make(map[string]bool),
		blockedSRPMs:       make(map[string]*pkggraph.PkgNode),
	}

	for _, failure := range buildState.BuildFailures() {
		if failure.Node.Type == pkggraph.TypeLocalBuild {
			srpmData.failedSRPMs[failure.Node.SrpmPath] = failure
		}
	}

	for _, node := range pkgGraph.AllBuildNodes() {
		// A node can be a delta if it was build or cached. If it was cached we used the cached rpm. If it is not cached
		// that means it was built and we discard the delta rpm.
		if buildState.IsNodeCached(node) {
			if buildState.IsNodeDelta(node) {
				srpmData.prebuiltDeltaSRPMs[node.SrpmPath] = true
			} else {
				srpmData.prebuiltSRPMs[node.SrpmPath] = true
			}
			continue
		} else if buildState.IsNodeAvailable(node) {
			srpmData.builtSRPMs[node.SrpmPath] = true
			continue
		}

		_, found := srpmData.failedSRPMs[node.SrpmPath]
		if !found {
			srpmData.blockedSRPMs[node.SrpmPath] = node
		}
	}

	return
}

func getSRPMsTestsState(pkgGraph *pkggraph.PkgGraph, buildState *GraphBuildState) (srpmTestData srpmTestDataContainer) {
	srpmTestData = srpmTestDataContainer{
		failedSRPMsTests:  make(map[string]*BuildResult),
		skippedSRPMsTests: make(map[string]bool),
		passedSRPMsTests:  make(map[string]bool),
		blockedSRPMsTests: make(map[string]*pkggraph.PkgNode),
	}

	for _, failure := range buildState.BuildFailures() {
		if failure.Node.Type == pkggraph.TypeTest {
			srpmTestData.failedSRPMsTests[failure.Node.SrpmPath] = failure
		}
	}

	for _, node := range pkgGraph.AllTestNodes() {
		if buildState.IsNodeCached(node) {
			srpmTestData.skippedSRPMsTests[node.SrpmPath] = true
			continue
		}

		if _, testFailed := srpmTestData.failedSRPMsTests[node.SrpmPath]; testFailed {
			continue
		}

		if buildState.IsNodeAvailable(node) {
			srpmTestData.passedSRPMsTests[node.SrpmPath] = true
		} else {
			srpmTestData.blockedSRPMsTests[node.SrpmPath] = node
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

// printSummary prints summarized numbers of the build to the logger.
func printSummary(srpmBuildData srpmBuildDataContainer, srpmTestData srpmTestDataContainer, unresolvedDependencies map[string]bool, rpmConflicts, srpmConflicts []string, allowToolchainRebuilds bool, conflictsLogger func(format string, args ...interface{})) {
	logger.Log.Info("---------------------------")
	logger.Log.Info("--------- Summary ---------")
	logger.Log.Info("---------------------------")

	logger.Log.Infof(color.GreenString(summaryLine("Number of prebuilt SRPMs:", len(srpmBuildData.prebuiltSRPMs))))
	logger.Log.Infof(color.GreenString(summaryLine("Number of prebuilt delta SRPMs:", len(srpmBuildData.prebuiltDeltaSRPMs))))
	logger.Log.Infof(color.GreenString(summaryLine("Number of skipped SRPMs tests:", len(srpmTestData.skippedSRPMsTests))))
	logger.Log.Infof(color.GreenString(summaryLine("Number of built SRPMs:", len(srpmBuildData.builtSRPMs))))
	logger.Log.Infof(color.GreenString(summaryLine("Number of passed SRPMs tests:", len(srpmTestData.passedSRPMsTests))))
	printErrorInfoByCondition(len(unresolvedDependencies) > 0, summaryLine("Number of unresolved dependencies:", len(unresolvedDependencies)))
	printErrorInfoByCondition(len(srpmBuildData.blockedSRPMs) > 0, summaryLine("Number of blocked SRPMs:", len(srpmBuildData.blockedSRPMs)))
	printErrorInfoByCondition(len(srpmTestData.blockedSRPMsTests) > 0, summaryLine("Number of blocked SRPMs tests:", len(srpmTestData.blockedSRPMsTests)))
	printErrorInfoByCondition(len(srpmBuildData.failedSRPMs) > 0, summaryLine("Number of failed SRPMs:", len(srpmBuildData.failedSRPMs)))
	printErrorInfoByCondition(len(srpmTestData.failedSRPMsTests) > 0, summaryLine("Number of failed SRPMs tests:", len(srpmTestData.failedSRPMsTests)))
	if allowToolchainRebuilds && (len(rpmConflicts) > 0 || len(srpmConflicts) > 0) {
		logger.Log.Infof("Toolchain RPMs conflicts are ignored since ALLOW_TOOLCHAIN_REBUILDS=y")
	}

	printErrorInfoByCondition(!allowToolchainRebuilds && len(rpmConflicts) > 0, summaryLine("Number of toolchain RPM conflicts:", len(rpmConflicts)))
	printErrorInfoByCondition(!allowToolchainRebuilds && len(srpmConflicts) > 0, summaryLine("Number of toolchain SRPM conflicts:", len(srpmConflicts)))
}

// printErrorInfoByCondition prints error or info level logs depending on the input condition.
// If the condition is true, it prints an error level log and an info level one otherwise.
func printErrorInfoByCondition(condition bool, format string, arg ...any) {
	if condition {
		logger.Log.Errorf(color.RedString(format, arg...))
	} else {
		logger.Log.Infof(color.GreenString(format, arg...))
	}
}

// summaryLine returns padded and type-formatted string for build summary.
func summaryLine(message string, count int) string {
	return fmt.Sprintf("%-36s%d", message, count)
}

// mapToSortedSlice converts a map[string]V to a sorted slice containing the map's keys.
func mapToSortedSlice[V any](inputMap map[string]V) []string {
	outputSlice := sliceutils.MapToSlice(inputMap)
	sort.Strings(outputSlice)
	return outputSlice
}
