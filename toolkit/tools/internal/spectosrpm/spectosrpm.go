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
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/sliceutils"
)

type srpmState int

const (
	SRPMStateMissing   srpmState = iota // SRPM does not exist
	SRPMStateOutOfDate                  // SRPM exists but is older than a file used by the SPEC
	SRPMStateUpToDate                   // SRPM exists and is up to date
	SRPMStateInvalid                    // Unable to parse the SRPM, or not applicable to this arch
	SRPMStateKeep                       // SRPM is not meant to be packed but should be retained
)

func (s srpmState) ShouldRepack() bool {
	return s == SRPMStateMissing || s == SRPMStateOutOfDate
}

// specState holds the state of a SPEC file: if it should be packed and the resulting SRPM if it is.
type SpecState struct {
	SpecFile     string
	SrpmFile     string
	CurrentState srpmState
	Err          error
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
// The output sets will be disjoint (i.e. a SPEC file will not be in both sets)
func FindSPECFiles(specsDir string, packList, keepList map[string]bool) (specFilesToPackMap, specFilesToKeepMap map[string]bool, err error) {
	logger.Log.Debugf("Searching for SPEC files in %s", specsDir)
	specFilesToKeepMap = make(map[string]bool)
	specFilesToPackMap = make(map[string]bool)
	// If we are packing everything (aka no packList) then we don't care about the keepList, we are going to keep everything
	// anyways.
	if len(packList) == 0 {
		var allSpecFiles []string
		specSearch := filepath.Join(specsDir, "**/*.spec")
		allSpecFiles, err = filepath.Glob(specSearch)
		// The sets are disjoint, so we don't need to check if we are keeping a SPEC file that we are also packing.
		specFilesToPackMap = sliceutils.SliceToSet[string](allSpecFiles)
	} else {
		var specMap map[string][]string
		specMap, err = buildSearchMap(specsDir)
		if err != nil {
			err = fmt.Errorf("error building SPEC search map: %w", err)
			return nil, nil, err
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
			specFilesToPackMap[specFile[0]] = true
		}
		// We many also want to keep some SPEC files that we are not packing
		// (e.g. toolchain SPECs will be packed via another mechanism and must always be kept).
		for specName := range keepList {
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
			if !specFilesToPackMap[specFile[0]] {
				// Only add the SPEC file to the keep list if it is not already in the pack list.
				specFilesToKeepMap[specFile[0]] = true
			}
		}
	}

	logger.Log.Debugf("Pack list: %v", sliceutils.SetToSlice(specFilesToPackMap))
	logger.Log.Debugf("Keep list: %v", sliceutils.SetToSlice(specFilesToKeepMap))

	return
}

// calculateSPECsToRepack will check which SPECs should be packed.
// If the resulting SRPM does not exist, or is older than a modification to
// one of the files used by the SPEC then it is repacked.
func CalculateSPECsToRepack(specFilesToPackage, specFilesToKeep map[string]bool, distTag, outDir string, nestedSourcesDir, repackAll, runCheck bool, workers int) (states []*SpecState, err error) {
	var wg sync.WaitGroup

	specFiles := sliceutils.SetToSlice(specFilesToPackage)
	specFiles = append(specFiles, sliceutils.SetToSlice(specFilesToKeep)...)

	requests := make(chan string, len(specFiles))
	results := make(chan *SpecState, len(specFiles))
	cancel := make(chan struct{})

	logger.Log.Infof("Calculating SPECs to repack")

	arch, err := rpm.GetRpmArch(runtime.GOARCH)
	if err != nil {
		return
	}

	// Start the workers now so they begin working as soon as a new job is buffered.
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go specsToPackWorker(requests, specFilesToKeep, results, cancel, &wg, distTag, outDir, arch, nestedSourcesDir, repackAll, runCheck)
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

	// Dont spam the user with progress updates, just update every 20%. We can be a bit off here since this is VERY
	// fast, and if we skip an update because the granularity is too coarse (ie not enough packages that we hit an
	// exact 20%), it's not a big deal.
	printedProgress := map[int]bool{0: false, 20: false, 40: false, 60: false, 80: false, 100: false}
	for i := 0; i < len(specFiles); i++ {
		result := <-results
		states[i] = result

		if result.Err != nil {
			logger.Log.Errorf("Failed to check (%s). Error: %s", result.SpecFile, result.Err)
			err = result.Err
			close(cancel)
			break
		}

		if result.CurrentState.ShouldRepack() {
			totalToRepack++
		}

		progress := int((i + 1) * 100 / len(specFiles))
		if progress%20 == 0 && !printedProgress[progress] {
			printedProgress[progress] = true
			logger.Log.Infof("Checking SPECs to repack: %d%%", progress)
		}
	}

	logger.Log.Debug("Waiting for outstanding workers to finish")
	wg.Wait()

	if err != nil {
		return
	}

	logger.Log.Infof("Packing %d/%d SPECs", totalToRepack, len(specFilesToPackage))
	return
}

// specsToPackWorker will process a channel of spec files that should be checked if packing is needed.
func specsToPackWorker(requests <-chan string, keepMap map[string]bool, results chan<- *SpecState, cancel <-chan struct{}, wg *sync.WaitGroup, distTag, outDir string, arch string, nestedSourcesDir, repackAll, runCheck bool) {
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
			SpecFile:     specFile,
			CurrentState: SRPMStateInvalid,
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

		if repackAll && !keepMap[specFile] {
			result.CurrentState = SRPMStateOutOfDate
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
			result.CurrentState = SRPMStateInvalid
			results <- result
			continue
		}

		// If we have just marked this SPEC as a keep, then we can skip the rest of the checks.
		if keepMap[specFile] {
			result.CurrentState = SRPMStateKeep
			results <- result
			continue
		}

		// Check if the SRPM is already on disk and if so its modification time.
		srpmInfo, err := os.Stat(fullSRPMPath)
		if err != nil {
			logger.Log.Debugf("Updating (%s) since (%s) is not yet built", specFile, fullSRPMPath)
			result.CurrentState = SRPMStateMissing
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
			result.CurrentState = SRPMStateOutOfDate
		}

		result.CurrentState = SRPMStateUpToDate
		results <- result
	}
}
