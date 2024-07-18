// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

/*
Package licensecheck provides a tool for searching RPMs for bad licenses, as well as several directly callable functions.
The core of the tool is the LicenseChecker struct, which is responsible for searching RPMs for bad licenses. The tool is
based on a 'simpletoolchroot' which is a wrapper that allows for easy chroot creation and cleanup.

The lifecycle of the LicenseChecker is as follows:

1. Create a new LicenseChecker with New()

2. Call CheckLicenses() to search for bad licenses

3. Either:
  - Call FormatResults() to get a formatted string of the results
  - Call GetAllResults() to get all the results, split into buckets.

4. Call CleanUp() to tear down the chroot

Also provided are several directly callable functions (these expect to be run in an environment with the necessary
macros, i.e. a chroot): CheckRpmLicenses(), IsALicenseFile(), IsASkippedLicenseFile()

The LicenseCheckerResult struct is used to store the results of the search. It contains the path to the RPM, a list of
bad documents, a list of bad files, and a list of duplicated documents. The bad documents are %doc files that are not
at least also in the license files. The bad files are general files that are misplaced in the licenses directory.

The duplicated documents are %doc files that are also in the license files. These are not technically bad, but are messy
and should be cleaned up.
*/
package licensecheck

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"sort"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/rpm"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/simpletoolchroot"
)

const licensePrefix = "/usr/share/licenses"

// LicenseChecker is a tool for searching RPMs for bad licenses
type LicenseChecker struct {
	simpleToolChroot *simpletoolchroot.SimpleToolChroot // The chroot to scan the RPMs in
	distTag          string                             // The distribution tag to use when parsing RPMs
	licenseNames     LicenseNames                       // The regexes used to match license files
	exceptions       LicenseExceptions                  // Files that should be ignored
	results          []LicenseCheckResult               // The results of the search
	jobSemaphore     chan struct{}                      // Limit the number of parallel jobs
}

// New creates a new license checker. If this returns successfully the caller is responsible for calling CleanUp().
// - buildDirPath: The path to create the chroot inside
// - workerTarPath: The path to the worker tarball
// - rpmDirPath: The path to the directory containing the RPMs
// - nameFilePath: The path to the .json file containing license names
// - exceptionFilePath: Optional, the path to the .json file containing license exceptions to ignore
// - distTag: The distribution tag to use when parsing RPMs
func New(buildDirPath, workerTarPath, rpmDirPath, nameFilePath, exceptionFilePath, distTag string,
) (newLicenseChecker *LicenseChecker, err error) {
	const chrootName = "license_chroot"

	newLicenseChecker = &LicenseChecker{
		distTag:          distTag,
		simpleToolChroot: &simpletoolchroot.SimpleToolChroot{},
		jobSemaphore:     make(chan struct{}, runtime.NumCPU()*2),
	}

	err = newLicenseChecker.simpleToolChroot.InitializeChroot(buildDirPath, chrootName, workerTarPath, rpmDirPath)
	if err != nil {
		err = fmt.Errorf("failed to initialize chroot:\n%w", err)
		return nil, err
	}
	defer func() {
		if err != nil {
			cleanupErr := newLicenseChecker.Cleanup()
			if cleanupErr != nil {
				// Append the cleanup error to the existing error
				err = fmt.Errorf("%w\nfailed to cleanup after failing to create a new LicenseChecker:\n%w", err, cleanupErr)
			}
		}
	}()

	newLicenseChecker.licenseNames, err = LoadLicenseNames(nameFilePath)
	if err != nil {
		err = fmt.Errorf("failed to load license names:\n%w", err)
		return nil, err
	}

	if exceptionFilePath != "" {
		newLicenseChecker.exceptions, err = LoadLicenseExceptions(exceptionFilePath)
		if err != nil {
			err = fmt.Errorf("failed to load license exceptions:\n%w", err)
			return nil, err
		}
	}

	return newLicenseChecker, err
}

// Cleanup tears down the chroot. If the chroot was created it will be cleaned up. Reset the struct to its initial state.
func (l *LicenseChecker) Cleanup() error {
	if l.simpleToolChroot != nil {
		err := l.simpleToolChroot.CleanUp()
		if err != nil {
			return fmt.Errorf("failed to cleanup chroot:\n%w", err)
		}
		l.simpleToolChroot = nil
	}
	return nil
}

// CheckLicenses will scan all .rpm files in the chroot for bad licenses. New unfiltered results will be returned but
// also appended to the internal results list which can be accessed with GetResults().
func (l *LicenseChecker) CheckLicenses(quiet bool) (latestResults []LicenseCheckResult, err error) {
	if l.simpleToolChroot == nil {
		return nil, fmt.Errorf("license checker is not initialized, use New() to create a new license checker")
	}

	err = l.simpleToolChroot.RunInChroot(func() (searchErr error) {
		latestResults, searchErr = l.runLicenseCheckInChroot(quiet)
		return searchErr
	})
	if err != nil {
		return nil, fmt.Errorf("failed to scan for license issues:\n%w", err)
	}

	// Sort the results by RPM path
	// This is done to ensure that the output is deterministic
	sort.Slice(latestResults, func(i, j int) bool {
		return latestResults[i].RpmPath < latestResults[j].RpmPath
	})
	l.results = append(l.results, latestResults...)

	return latestResults, nil
}

// GetResults returns the cumulative results of the search, split into:
// - All results: Every scan result
// - Any result that has at least one warning
// - Any result that has at least one error
func (l *LicenseChecker) GetResults(mode LicenseCheckMode) (all, warnings, errors []LicenseCheckResult) {
	_, warnings, errors = SortAndFilterResults(l.results, mode)
	return l.results, warnings, errors
}

type licenseCheckReturn struct {
	finding LicenseCheckResult
	err     error
}

// runLicenseCheckInChroot searches for bad licenses amongst the RPMs mounted into the chroot. This function is meant
// to be called from inside the chroot's context.
func (l *LicenseChecker) runLicenseCheckInChroot(quiet bool) (findings []LicenseCheckResult, err error) {
	const searchReportIntervalPercent = 10 // Report progress to the user every 10%

	// Find all the rpms in the chroot
	rpmsToSearchPaths, err := l.findRpmPaths()
	if err != nil {
		return nil, fmt.Errorf("failed to walk rpm directory:\n%w", err)
	}
	if len(rpmsToSearchPaths) == 0 {
		logger.Log.Warnf("No rpms found in (%s)", l.simpleToolChroot.ChrootRelativeMountDir())
		return nil, nil
	}

	// Scan each rpm in parallel
	ctx, cancelFunc := context.WithCancel(context.Background())
	defer cancelFunc()
	resultsChannel := make(chan licenseCheckReturn, len(rpmsToSearchPaths))
	if !quiet {
		logger.Log.Infof("Queuing %d rpms for license check", len(rpmsToSearchPaths))
	}
	go l.queueWorkers(ctx, rpmsToSearchPaths, resultsChannel)
	if !quiet {
		logger.Log.Infof("Checking RPMs for license issues")
	}

	// Wait for all the workers to finish, updating the progress as results come in
	numProcessed := 0
	lastReportPercent := 0
	for range rpmsToSearchPaths {
		result := <-resultsChannel
		if result.err != nil {
			// Signal the workers to stop if there is an error
			err = fmt.Errorf("failed to search rpm for license issues:\n%w", result.err)
			cancelFunc()
			return nil, err
		}

		// Report progress to the user every 10%
		numProcessed++
		percentProcessed := (numProcessed * 100) / len(rpmsToSearchPaths)
		if percentProcessed-lastReportPercent >= searchReportIntervalPercent && !quiet {
			logger.Log.Infof("Checked %d/%d rpms (%d%%)", numProcessed, len(rpmsToSearchPaths), percentProcessed)
			lastReportPercent = percentProcessed
		}
		findings = append(findings, result.finding)
	}
	return
}

// findRpmPaths walks the chroots's mount directory to find all *.rpm files. The paths are returned relative to the
// chroot's root.
func (l *LicenseChecker) findRpmPaths() (foundRpmPaths []string, err error) {
	const rpmExtension = ".rpm"
	err = filepath.Walk(l.simpleToolChroot.ChrootRelativeMountDir(), func(path string, info os.FileInfo, walkErr error) error {
		if walkErr != nil {
			return walkErr
		}
		if info.IsDir() {
			return nil
		}
		if !strings.HasSuffix(path, rpmExtension) {
			return nil
		}

		foundRpmPaths = append(foundRpmPaths, path)
		return nil
	})
	if err != nil {
		err = fmt.Errorf("failed to walk directory:\n%w", err)
		return nil, err
	}
	return foundRpmPaths, nil
}

// queueWorkers queues up workers to search the RPMs in parallel. Each worker will wait on the jobSemaphore before starting.
// This function will return once all workers have been queued.
func (l *LicenseChecker) queueWorkers(ctx context.Context, rpmsToSearchPaths []string, resultsChannel chan licenseCheckReturn) {
	for _, rpmPath := range rpmsToSearchPaths {
		// Wait for the semaphore, or allow cancel before running
		select {
		case l.jobSemaphore <- struct{}{}:
		case <-ctx.Done():
			return
		}
		go func(rpmPath string) {
			defer func() {
				<-l.jobSemaphore
			}()

			logger.Log.Debugf("Searching (%s)", filepath.Base(rpmPath))
			searchResult, err := CheckRpmLicenses(rpmPath, l.distTag, l.licenseNames, l.exceptions)
			logger.Log.Debugf("Finished searching (%s)", filepath.Base(rpmPath))
			if err != nil {
				logger.Log.Errorf("License check worker failed with error: %v", err)
				resultsChannel <- licenseCheckReturn{err: err}
				return
			}
			resultsChannel <- licenseCheckReturn{finding: searchResult, err: nil}
		}(rpmPath)
	}
}

// CheckRpmLicenses checks the licenses of an RPM at the given path. It returns result struct holding all the license
// issues found. This function will use the host's macros to query the RPM so it is expected to be called in a chroot.
// - rpmPath: The path to the RPM to check relative to the chroot's root.
func CheckRpmLicenses(rpmPath, distTag string, licenseNames LicenseNames, exceptions LicenseExceptions) (result LicenseCheckResult, err error) {
	defines := rpm.DefaultDistroDefines(false, distTag)

	_, files, _, documentFiles, licenseFiles, err := rpm.QueryPackageFiles(rpmPath, defines)
	if err != nil {
		return LicenseCheckResult{}, fmt.Errorf("failed to query package contents:\n%w", err)
	}

	pkgNameLines, err := rpm.QueryPackage(rpmPath, "%{NAME}", defines)
	if err != nil {
		return LicenseCheckResult{}, fmt.Errorf("failed to query package:\n%w", err)
	}
	if len(pkgNameLines) != 1 {
		return LicenseCheckResult{}, fmt.Errorf("failed to query package:\nexpected 1 package name, got %d", len(pkgNameLines))
	}
	pkgName := pkgNameLines[0]

	badDocFiles, badOtherFiles, duplicatedDocs := interpretResults(pkgName, files, documentFiles, licenseFiles, licenseNames, exceptions)

	result = LicenseCheckResult{
		RpmPath:        rpmPath,
		PackageName:    pkgName,
		BadDocs:        badDocFiles,
		BadFiles:       badOtherFiles,
		DuplicatedDocs: duplicatedDocs,
	}

	return result, nil
}

// interpretResults scans file lists for packing issues:
// - badDocFiles: %doc files that appear to be licenses, but are not at least also in the license files
// - badOtherFiles: files that are misplaced in the licenses directory
// - duplicatedDocs: %doc files that are also in the license files
func interpretResults(pkgName string, files, documentFiles, licenseFiles []string, licenseNames LicenseNames, exceptions LicenseExceptions) (badDocFiles, badOtherFiles, duplicatedDocs []string) {
	badDocFiles = []string{}
	badOtherFiles = []string{}
	duplicatedDocs = []string{}

	// Check the documentation files
	for _, documentFile := range documentFiles {
		if licenseNames.IsALicenseFile(pkgName, documentFile) && !exceptions.ShouldIgnoreFile(pkgName, documentFile) {
			if isDocumentInLicenseFiles(documentFile, licenseFiles) {
				duplicatedDocs = append(duplicatedDocs, documentFile)
			} else {
				badDocFiles = append(badDocFiles, documentFile)
			}
		}
	}

	// Make sure we don't put random files in the license directory. They need to be %license.
	licenseFileSet := sliceutils.SliceToSet(licenseFiles)
	for _, file := range files {
		if isFileMisplacedInLicensesFolder(file, licenseFileSet) && !exceptions.ShouldIgnoreFile(pkgName, file) {
			badOtherFiles = append(badOtherFiles, file)
		}
	}

	sort.Strings(badDocFiles)
	sort.Strings(duplicatedDocs)
	sort.Strings(badOtherFiles)

	return badDocFiles, badOtherFiles, duplicatedDocs
}

// isDocumentInLicenseFiles checks if a document file is in the list of license files (based on basename of the file).
func isDocumentInLicenseFiles(documentFile string, licenseFiles []string) bool {
	docBasename := filepath.Base(documentFile)
	for _, licenseFile := range licenseFiles {
		licenseBasename := filepath.Base(licenseFile)
		if strings.Contains(licenseBasename, docBasename) {
			return true
		}
	}
	return false
}

// isFileMisplacedInLicensesFolder returns true if the filePath is present in the /usr/share/licenses/<pkg> tree but is
// not included in the set of license files. Every file in /usr/share/licenses/<pkg> should be a license file and tagged.
// - filePath: The path to the file to check. Directories are not included as %license so only actual file paths should
// be passed.
// -
// - licenseFileSet: A set of all the license files in the package. This is used to check if the file is a license file.
func isFileMisplacedInLicensesFolder(filePath string, licenseFileSet map[string]bool) bool {
	// Files that don't start with '/usr/share/licenses' are by definition not misplaced in the licenses folder
	if !strings.HasPrefix(filePath, licensePrefix) {
		return false
	} else {
		// If the path appears in the license set, it's correctly tagged.
		isARealLicenseFile := licenseFileSet[filePath]
		return !isARealLicenseFile
	}
}
