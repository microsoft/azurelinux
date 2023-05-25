// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package spectosrpm

import (
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"sync"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/directory"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/rpm"
)

// specState holds the state of a SPEC file: if it should be packed and the resulting SRPM if it is.
type SpecState struct {
	SpecFile string
	SrpmFile string
	ToPack   bool
	Err      error
}

func buildSearchMap(specsDir string) (specsMap map[string][]string, err error) {
	// Walk the directory tree to find all SPEC files and put them in the map by base name.
	specsMap = make(map[string][]string)
	err = filepath.Walk(specsDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if filepath.Ext(path) != ".spec" {
			return nil
		}

		// Strip the .spec from the file path and add it to the map.
		specName := filepath.Base(path)
		specName = strings.TrimSuffix(specName, ".spec")
		specsMap[specName] = append(specsMap[specName], path)

		return nil
	})
	return
}

// findSPECFiles finds all SPEC files that should be considered for packing.
// Takes into consideration a packList if provided.
func FindSPECFiles(specsDir string, packList map[string]bool) (specFiles []string, err error) {
	logger.Log.Debugf("Searching for SPEC files in %s", specsDir)
	if len(packList) == 0 {
		specSearch := filepath.Join(specsDir, "**/*.spec")
		specFiles, err = filepath.Glob(specSearch)
	} else {
		var specMap map[string][]string
		specMap, err = buildSearchMap(specsDir)
		if err != nil {
			err = fmt.Errorf("error building SPEC search map: %w", err)
			return nil, err
		}
		for specName := range packList {
			specFile := specMap[specName]
			if len(specFile) != 1 {
				if strings.HasPrefix(specName, "msopenjdk-11") {
					logger.Log.Debugf("Ignoring missing match for '%s', which is externally-provided and thus doesn't have a local spec.", specName)
					continue
				} else {
					err = fmt.Errorf("unexpected number of matches (%d) for spec file (%s)", len(specFile), specName)
					return
				}
			}
			specFiles = append(specFiles, specFile[0])
		}
	}

	return
}

// calculateSPECsToRepack will check which SPECs should be packed.
// If the resulting SRPM does not exist, or is older than a modification to
// one of the files used by the SPEC then it is repacked.
func CalculateSPECsToRepack(specFiles []string, distTag, outDir string, nestedSourcesDir, repackAll, dryRun, runCheck bool, workers int) (states []*SpecState, err error) {
	var wg sync.WaitGroup

	requests := make(chan string, len(specFiles))
	results := make(chan *SpecState, len(specFiles))
	cancel := make(chan struct{})

	if !dryRun {
		logger.Log.Infof("Calculating SPECs to repack")
	} else {
		logger.Log.Debugf("Calculating SPECs to repack (dryrun)")
	}

	arch, err := rpm.GetRpmArch(runtime.GOARCH)
	if err != nil {
		return
	}

	// Start the workers now so they begin working as soon as a new job is buffered.
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go specsToPackWorker(requests, results, cancel, &wg, distTag, outDir, arch, nestedSourcesDir, repackAll, dryRun, runCheck)
	}

	for _, specFile := range specFiles {
		requests <- specFile
	}

	// Signal to the workers that there are no more new spec files
	close(requests)

	// Transfer the results from the channel into states.
	//
	// While the channel itself could be returned and passed to the consumer of
	// the results, additional functionality would have to be added to limit the total workers
	// in use at any given time.
	//
	// Since this worker pool and future worker pools in the application are opening file descriptors
	// if too many are active at once it can exhaust the file descriptor limit.
	// Currently all functions that employ workers pool of size `workers` are serialized,
	// resulting in `workers` being the upper capacity at any given time.
	totalToRepack := 0
	states = make([]*SpecState, len(specFiles))
	for i := 0; i < len(specFiles); i++ {
		result := <-results
		states[i] = result

		if result.Err != nil {
			logger.Log.Errorf("Failed to check (%s). Error: %s", result.SpecFile, result.Err)
			err = result.Err
			close(cancel)
			break
		}

		if result.ToPack {
			totalToRepack++
		}
	}

	logger.Log.Debug("Waiting for outstanding workers to finish")
	wg.Wait()

	if err != nil {
		return
	}

	if !dryRun {
		logger.Log.Infof("Packing %d/%d SPECs", totalToRepack, len(specFiles))
	} else {
		logger.Log.Debugf("Would pack %d/%d SPECs (dryrun)", totalToRepack, len(specFiles))
	}
	return
}

// specsToPackWorker will process a channel of spec files that should be checked if packing is needed.
func specsToPackWorker(requests <-chan string, results chan<- *SpecState, cancel <-chan struct{}, wg *sync.WaitGroup, distTag, outDir string, arch string, nestedSourcesDir, repackAll, dryRun, runCheck bool) {
	const (
		queryFormat         = `%{NAME}-%{VERSION}-%{RELEASE}.src.rpm`
		nestedSourceDirName = "SOURCES"
	)

	const (
		srpmQueryResultsIndex   = iota
		expectedQueryResultsLen = iota
	)

	defer wg.Done()

	for specFile := range requests {
		select {
		case <-cancel:
			logger.Log.Debug("Cancellation signal received")
			return
		default:
		}

		result := &SpecState{
			SpecFile: specFile,
		}

		containingDir := filepath.Dir(specFile)

		// Find the SRPM that this SPEC will produce.
		defines := rpm.DefaultDefinesWithDist(runCheck, distTag)

		// Allow the user to configure if the SPEC sources are in a nested 'SOURCES' directory.
		// Otherwise assume source files are next to the SPEC file.
		sourceDir := containingDir
		if nestedSourcesDir {
			sourceDir = filepath.Join(sourceDir, nestedSourceDirName)
		}
		specQueryResults, err := rpm.QuerySPEC(specFile, sourceDir, queryFormat, arch, defines, rpm.QueryHeaderArgument)

		if err != nil {
			if err.Error() == rpm.NoCompatibleArchError {
				logger.Log.Infof("Skipping SPEC (%s) due to incompatible build architecture", specFile)
			} else {
				result.Err = err
			}

			results <- result
			continue
		}

		if len(specQueryResults) != expectedQueryResultsLen {
			result.Err = fmt.Errorf("unexpected query results, wanted (%d) results but got (%d), results: %v", expectedQueryResultsLen, len(specQueryResults), specQueryResults)
			results <- result
			continue
		}

		// Resolve the full path of the SRPM that would be packed from this SPEC file.
		producedSRPM := specQueryResults[srpmQueryResultsIndex]
		fullSRPMPath := filepath.Join(outDir, producedSRPM)
		result.SrpmFile = fullSRPMPath

		if repackAll {
			result.ToPack = true
			results <- result
			continue
		}

		// Sanity check that SRPMS is meant to be built for the machine architecture
		isCompatible, err := rpm.SpecArchIsCompatible(specFile, sourceDir, arch, defines)
		if err != nil {
			result.Err = err
			results <- result
			continue
		}

		if !isCompatible {
			logger.Log.Infof(`Skipping (%s) since it cannot be built on current architecture.`, specFile)
			results <- result
			continue
		}

		// If we are forcing a full repack, or just doing a dry run (ie don't actually pack anything, just give us the files that might be packed)
		if dryRun {
			result.ToPack = true
			results <- result
			continue
		}

		// Check if the SRPM is already on disk and if so its modification time.
		srpmInfo, err := os.Stat(fullSRPMPath)
		if err != nil {
			logger.Log.Debugf("Updating (%s) since (%s) is not yet built", specFile, fullSRPMPath)
			result.ToPack = true
			results <- result
			continue
		}

		// Check if a file used by the SPEC has been modified since the resulting SRPM was previously packed.
		specModTime, latestFile, err := directory.LastModifiedFile(containingDir)
		if err != nil {
			result.Err = fmt.Errorf("failed to query modification time for SPEC (%s). Error: %s", specFile, err)
			results <- result
			continue
		}

		if specModTime.After(srpmInfo.ModTime()) {
			logger.Log.Debugf("Updating (%s) since (%s) has changed", specFile, latestFile)
			result.ToPack = true
		}

		results <- result
	}
}
