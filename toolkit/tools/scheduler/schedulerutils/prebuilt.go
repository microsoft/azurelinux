// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"sync"

	"microsoft.com/pkggen/internal/file"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkggraph"
)

// isSRPMPrebuilt checks if an SRPM is prebuilt, returning true if so along with a slice of corresponding prebuilt RPMs.
func isSRPMPrebuilt(srpmPath string, pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex) (isPrebuilt bool, rpmFiles []string) {
	rpmFiles = rpmsProvidedBySRPM(srpmPath, pkgGraph, graphMutex)
	isPrebuilt = findAllRPMS(rpmFiles)
	return
}

// rpmsProvidedBySRPM returns all RPMs produced from a SRPM file.
func rpmsProvidedBySRPM(srpmPath string, pkgGraph *pkggraph.PkgGraph, graphMutex *sync.RWMutex) (rpmFiles []string) {
	graphMutex.RLock()
	defer graphMutex.RUnlock()

	rpmsMap := make(map[string]bool)
	runNodes := pkgGraph.AllRunNodes()
	for _, node := range runNodes {
		if node.SrpmPath != srpmPath {
			continue
		}

		if node.RpmPath == "" || node.RpmPath == "<NO_RPM_PATH>" {
			continue
		}

		rpmsMap[node.RpmPath] = true
	}

	rpmFiles = make([]string, 0, len(rpmsMap))
	for rpm := range rpmsMap {
		rpmFiles = append(rpmFiles, rpm)
	}

	return
}

// findAllRPMS returns true if all RPMs requested are found on disk.
func findAllRPMS(rpmsToFind []string) bool {
	for _, rpm := range rpmsToFind {
		isFile, _ := file.IsFile(rpm)

		if !isFile {
			logger.Log.Debugf("Did not find (%s)", rpm)
			return false
		}
	}

	return true
}
