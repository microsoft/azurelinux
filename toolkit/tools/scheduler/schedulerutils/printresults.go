// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"path/filepath"

	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkggraph"
)

// PrintBuildResult prints a build result to the logger.
func PrintBuildResult(res *BuildResult) {
	if res.Err != nil {
		logger.Log.Errorf("Failed to build %s, error: %s, for details see: %s", filepath.Base(res.Node.SrpmPath), res.Err, res.LogFile)
		return
	}

	baseSRPMName := filepath.Base(res.Node.SrpmPath)
	if res.Node.Type == pkggraph.TypeBuild {
		if res.UsedCache {
			logger.Log.Infof("Prebuilt: %s -> %v", baseSRPMName, res.BuiltFiles)
		} else {
			logger.Log.Infof("Built: %s -> %v", baseSRPMName, res.BuiltFiles)
		}
	} else {
		logger.Log.Debugf("Processed node %s", res.Node.FriendlyName())
	}
}

// PrintBuildSummary prints the summary of the entire build to the logger.
func PrintBuildSummary(pkgGraph *pkggraph.PkgGraph, buildState *GraphBuildState) {
	failedSRPMs := make(map[string]bool)
	failures := buildState.BuildFailures()
	for _, failure := range failures {
		failedSRPMs[failure.Node.SrpmPath] = true
	}

	prebuiltSRPMs := make(map[string]bool)
	builtSRPMs := make(map[string]bool)
	unbuiltSRPMs := make(map[string]bool)

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

	logger.Log.Info("---------------------------")
	logger.Log.Info("--------- Summary ---------")
	logger.Log.Info("---------------------------")

	logger.Log.Infof("Number of built SRPMs:    %d", len(builtSRPMs))
	logger.Log.Infof("Number of prebuilt SRPMs: %d", len(prebuiltSRPMs))
	logger.Log.Infof("Number of failed SRPMs:   %d", len(failures))
	logger.Log.Infof("Number of skipped SRPMs:  %d", len(unbuiltSRPMs))

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
			logger.Log.Infof("--> %s , error: %s, for details see: %s", filepath.Base(failure.Node.SrpmPath), failure.Err, failure.LogFile)
		}
	}

	if len(unbuiltSRPMs) != 0 {
		logger.Log.Info("Skipped SRPMs:")
		for srpm := range unbuiltSRPMs {
			logger.Log.Infof("--> %s", filepath.Base(srpm))
		}
	}
}
