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
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/rpm"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/simpletoolchroot"
)

const (
	chrootName      = "license_chroot"
	licensePrefix   = "/usr/share/licenses"
	numParallelJobs = 20
)

var jobSemaphore = make(chan struct{}, numParallelJobs) // Limit the number of parallel jobs

// LicenseCheckResult is the result of a license check on an single RPM
type LicenseCheckResult struct {
	RpmPath        string   `json:"RpmPath"`
	BadDocs        []string `json:"BadDocs,omitempty"`
	BadFiles       []string `json:"BadFiles,omitempty"`
	DuplicatedDocs []string `json:"DuplicatedDocs,omitempty"`
	err            error    `json:"-"`
}

// LicenseChecker is a tool for searching RPMs for bad licenses
type LicenseChecker struct {
	simpleToolChroot *simpletoolchroot.SimpleToolChroot // The chroot to scan the RPMs in
	distTag          string                             // The distribution tag to use when parsing RPMs
	exceptions       LicenseExceptions                  // Files that should be ignored
	results          []LicenseCheckResult               // The results of the search
}

// HasBadResult returns true if the result contains at least one bad document or file.
func (r *LicenseCheckResult) HasBadResult() bool {
	return len(r.BadDocs) > 0 || len(r.BadFiles) > 0
}

// HasWarningResult returns true if the result contains at least one duplicated documents.
func (r *LicenseCheckResult) HasWarningResult() bool {
	return len(r.DuplicatedDocs) > 0
}

// SaveLicenseCheckResults saves a list of all warnings and errors to a json file.
func SaveLicenseCheckResults(savePath string, resultsList []LicenseCheckResult) error {
	// Create parent dir if missing
	err := os.MkdirAll(filepath.Dir(savePath), os.ModePerm)
	if err != nil {
		return fmt.Errorf("failed to create directory for results file. Error:\n%w", err)
	}

	sortedList := sortAndFilterResults(resultsList)
	err = jsonutils.WriteJSONFile(savePath, sortedList)
	if err != nil {
		return fmt.Errorf("failed to save license check results. Error:\n%w", err)
	}
	return nil
}

// sortAndFilterResults returns a copy of the list that is sorted and contains only warnings and errors.
func sortAndFilterResults(results []LicenseCheckResult) (sortedList []LicenseCheckResult) {
	sortedList = make([]LicenseCheckResult, len(results))
	for i, result := range results {
		if result.HasBadResult() || result.HasWarningResult() {
			sortedList[i] = result
		}
	}
	sort.Slice(sortedList, func(i, j int) bool {
		return sortedList[i].RpmPath < sortedList[j].RpmPath
	})
	return sortedList
}

// New creates a new license checker. If this returns successfully the caller is responsible for calling CleanUp().
// - buildDirPath: The path to create the chroot inside
// - workerTarPath: The path to the worker tarball
// - rpmDirPath: The path to the directory containing the RPMs
// - exceptionFilePath: Optional, the path to the .json file containing license exceptions to ignore
// - distTag: The distribution tag to use when parsing RPMs
func New(buildDirPath, workerTarPath, rpmDirPath, exceptionFilePath, distTag string) (newLicenseChecker *LicenseChecker, err error) {
	newLicenseChecker = &LicenseChecker{
		distTag:          distTag,
		simpleToolChroot: &simpletoolchroot.SimpleToolChroot{},
	}

	err = newLicenseChecker.simpleToolChroot.InitializeChroot(buildDirPath, chrootName, workerTarPath, rpmDirPath)
	if err != nil {
		newLicenseChecker.CleanUp()
		err = fmt.Errorf("failed to initialize chroot. Error:\n%w", err)
		return nil, err
	}

	if exceptionFilePath != "" {
		newLicenseChecker.exceptions, err = LoadLicenseExceptions(exceptionFilePath)
		if err != nil {
			newLicenseChecker.CleanUp()
			err = fmt.Errorf("failed to load license exceptions. Error:\n%w", err)
			return nil, err
		}
	}

	return newLicenseChecker, err
}

// CleanUp tears down the chroot. If the chroot was created it will be cleaned up. Reset the struct to its initial state.
func (l *LicenseChecker) CleanUp() error {
	if l.simpleToolChroot != nil {
		err := l.simpleToolChroot.CleanUp()
		if err != nil {
			return fmt.Errorf("failed to cleanup chroot. Error:\n%w", err)
		}
		l.simpleToolChroot = nil
	}
	return nil
}

// CheckLicenses will scan all .rpm files in the chroot for bad licenses. The results can be accessed with FormatResults() or GetAllResults().
func (l *LicenseChecker) CheckLicenses() error {
	if l.simpleToolChroot == nil {
		return fmt.Errorf("chroot has not been initialized")
	}

	l.results = []LicenseCheckResult{}

	err := l.simpleToolChroot.RunInChroot(func() (searchErr error) {
		l.results, searchErr = l.runLicenseCheckInChroot()
		return searchErr
	})
	if err != nil {
		return fmt.Errorf("failed to search for licenses. Error:\n%w", err)
	}

	for _, result := range l.results {
		if result.err != nil {
			logger.Log.Errorf("Failed to search %s. Error: %v", result.RpmPath, result.err)
		}
	}

	// Sort the results by RPM path
	// This is done to ensure that the output is deterministic
	sort.Slice(l.results, func(i, j int) bool {
		return l.results[i].RpmPath < l.results[j].RpmPath
	})
	return nil
}

// FormatResults formats the results of the search to a string. Results will be ordered as follows:
// - Packages with warnings only, sorted alphabetically
// - Packages with errors (and possibly warnings), sorted alphabetically
func (l *LicenseChecker) FormatResults(pedantic bool) string {
	var sb strings.Builder
	results := sortAndFilterResults(l.results)

	// Print warnings first, but only if they don't also have an error
	if !pedantic {
		for _, result := range results {
			if result.HasWarningResult() && !result.HasBadResult() {
				sb.WriteString(printWarning(result))
			}
		}
	}

	// Now print the errors
	for _, result := range results {
		if result.HasBadResult() || (pedantic && result.HasWarningResult()) {
			sb.WriteString(printError(result, pedantic))
			if !pedantic && result.HasWarningResult() {
				// If pedantic was set, the warning was already printed as an error.
				// Otherwise print the warning now.
				sb.WriteString(printWarning(result))
			}
		}
	}

	return sb.String()
}

// GetAllResults returns the results of the search, split into:
// - All results: Every scan result
// - Any result that has at least one warning
// - Any result that has at least one error
// There may be overlap between the lists. If pedantic is true, warnings will be treated as errors.
func (l *LicenseChecker) GetAllResults(pedantic bool) (all, warnings, errors []LicenseCheckResult) {
	all = []LicenseCheckResult{}
	warnings = []LicenseCheckResult{}
	errors = []LicenseCheckResult{}
	for _, result := range l.results {
		all = append(all, result)
		if result.HasBadResult() || (pedantic && result.HasWarningResult()) {
			errors = append(errors, result)
		}
		if result.HasWarningResult() && !pedantic {
			warnings = append(warnings, result)
		}
	}
	return all, warnings, errors
}

func printWarning(result LicenseCheckResult) string {
	var sb strings.Builder
	sb.WriteString(fmt.Sprintf("WARN: '%s' has license warnings:\n", filepath.Base(result.RpmPath)))
	sb.WriteString(fmt.Sprintf("\tduplicated license files:\n\t\t%s\n", strings.Join(result.DuplicatedDocs, "\n\t\t")))
	return sb.String()
}

func printError(result LicenseCheckResult, pedantic bool) string {
	var sb strings.Builder
	sb.WriteString(fmt.Sprintf("ERROR: '%s' has license errors:\n", filepath.Base(result.RpmPath)))
	if len(result.BadDocs) > 0 {
		sb.WriteString(fmt.Sprintf("\tbad %%doc files:\n\t\t%s\n", strings.Join(result.BadDocs, "\n\t\t")))
	}
	if len(result.BadFiles) > 0 {
		sb.WriteString(fmt.Sprintf("\tbad general file:\n\t\t%s\n", strings.Join(result.BadFiles, "\n\t\t")))
	}
	if pedantic && len(result.DuplicatedDocs) > 0 {
		sb.WriteString(fmt.Sprintf("\tduplicated license files:\n\t\t%s\n", strings.Join(result.DuplicatedDocs, "\n\t\t")))
	}
	return sb.String()
}

// runLicenseCheckInChroot searches for bad licenses amongst the RPMs mounted into the chroot. This function is meant
// to be called from inside the chroot's context.
func (l *LicenseChecker) runLicenseCheckInChroot() (results []LicenseCheckResult, err error) {
	const searchReportIntervalPercent = 10

	// Find all the rpms in the chroot
	rpmsToSearchPaths, err := l.findRpmPaths()
	if err != nil {
		return nil, fmt.Errorf("failed to walk srpm directory. Error:\n%w", err)
	}
	if len(rpmsToSearchPaths) == 0 {
		logger.Log.Warnf("No rpms found in %s", l.simpleToolChroot.ChrootRelativeMountDir())
		return nil, nil
	}

	// Scan each rpm in parallel
	resultsChannel := make(chan LicenseCheckResult, len(rpmsToSearchPaths))
	cancel := make(chan struct{})
	logger.Log.Infof("Queuing %d rpms for search", len(rpmsToSearchPaths))
	l.queueWorkers(rpmsToSearchPaths, resultsChannel, cancel)
	logger.Log.Infof("Searching rpms...")

	// Wait for all the workers to finish, updating the progress as results come in
	numProcessed := 0
	lastReportPercent := 0
	for range rpmsToSearchPaths {
		result := <-resultsChannel
		if result.err != nil {
			// Signal the workers to stop if there is an error
			err = fmt.Errorf("failed to search srpm. Error:\n%w", result.err)
			close(cancel)
			return
		}
		numProcessed++
		percentProcessed := (numProcessed * 100) / len(rpmsToSearchPaths)
		if percentProcessed-lastReportPercent >= searchReportIntervalPercent {
			logger.Log.Infof("Checked %d/%d rpms (%d%%)", numProcessed, len(rpmsToSearchPaths), percentProcessed)
			lastReportPercent = percentProcessed
		}
		results = append(results, result)
	}
	return
}

func (s *LicenseChecker) findRpmPaths() (foundSrpmPaths []string, err error) {
	const rpmExtension = ".rpm"
	err = filepath.Walk(s.simpleToolChroot.ChrootRelativeMountDir(), func(path string, info os.FileInfo, walkErr error) error {
		if walkErr != nil {
			return walkErr
		}
		if info.IsDir() {
			return nil
		}
		if !strings.HasSuffix(path, rpmExtension) {
			return nil
		}

		foundSrpmPaths = append(foundSrpmPaths, path)
		return nil
	})
	if err != nil {
		err = fmt.Errorf("failed to walk directory. Error:\n%w", err)
		return nil, err
	}
	return foundSrpmPaths, nil
}

// queueWorkers queues up workers to search the RPMs in parallel. Each worker will wait on the jobSemaphore before starting.
func (l *LicenseChecker) queueWorkers(rpmsToSearchPaths []string, resultsChannel chan LicenseCheckResult, cancel chan struct{}) {
	for _, rpmPath := range rpmsToSearchPaths {
		go func(rpmPath string) {
			// Wait for the semaphore, or allow cancel before running
			select {
			case jobSemaphore <- struct{}{}:
			case <-cancel:
				return
			}
			defer func() {
				<-jobSemaphore
			}()

			logger.Log.Debugf("Searching (%s)", filepath.Base(rpmPath))
			searchResult, err := l.checkRpmLicenses(rpmPath)
			logger.Log.Debugf("Finished searching (%s)", filepath.Base(rpmPath))
			if err != nil {
				logger.Log.Errorf("Worker failed with error: %v", err)
				resultsChannel <- LicenseCheckResult{err: err}
				return
			}
			resultsChannel <- searchResult
		}(rpmPath)
	}
}

// checkRpmLicenses checks the licenses of an RPM at the given path. It returns a list of bad license files.
// This function will use the host's macros to query the RPM so it is expected to be called in a chroot.
func (l *LicenseChecker) checkRpmLicenses(rpmPath string) (result LicenseCheckResult, err error) {
	defines := rpm.DefaultDistroDefines(false, l.distTag)

	_, files, _, documentFiles, licenseFiles, err := rpm.QueryPackageContents(rpmPath, defines)
	if err != nil {
		return LicenseCheckResult{RpmPath: rpmPath, err: fmt.Errorf("failed to query package contents. Error:\n%w", err)}, nil
	}

	pkgNameLines, err := rpm.QueryPackage(rpmPath, "%{NAME}", defines)
	if err != nil {
		return LicenseCheckResult{RpmPath: rpmPath, err: fmt.Errorf("failed to query package. Error:\n%w", err)}, nil
	}
	if len(pkgNameLines) != 1 {
		return LicenseCheckResult{RpmPath: rpmPath, err: fmt.Errorf("failed to query package. Error: expected 1 package name, got %d", len(pkgNameLines))}, nil
	}
	pkgName := pkgNameLines[0]

	badDocFiles, badOtherFiles, duplicatedDocs := interpretResults(pkgName, files, documentFiles, licenseFiles, l.exceptions)

	return LicenseCheckResult{RpmPath: rpmPath, BadDocs: badDocFiles, BadFiles: badOtherFiles, DuplicatedDocs: duplicatedDocs}, nil
}

// interpretResults scans file lists for packing issues:
// - badDocFiles: %doc files that appear to be licenses, but are not at least also in the license files
// - badOtherFiles: files that are misplaced in the licenses directory
// - duplicatedDocs: %doc files that are also in the license files
func interpretResults(pkgName string, files, documentFiles, licenseFiles []string, exceptions LicenseExceptions) (badDocFiles, badOtherFiles, duplicatedDocs []string) {
	badDocFiles = []string{}
	badOtherFiles = []string{}
	duplicatedDocs = []string{}

	// Check the documentation files
	for _, documentFile := range documentFiles {
		if IsALicenseFile(pkgName, documentFile) && !exceptions.ShouldIgnoreFile(pkgName, documentFile) {
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

// IsALicenseFile makes a best effort guess if a file is a license file or not. This is NOT foolproof however.
// Some examples of files that may be incorrectly identified as licenses:
// - /path/to/code/gpl/README.md ("gpl")
// - /path/to/a/hash/CC05f4dcc3b5aa765d61d8327deb882cf ("cc0")
// - /path/to/freebsd-parts/file.ext ("bds")
func IsALicenseFile(pkgName, licenseFilePath string) bool {
	// Check if the file is in the list of explicit known license files
	for _, name := range licenseNamesVerbatim {
		baseName := filepath.Base(licenseFilePath)
		if strings.EqualFold(baseName, name) {
			return true
		}
	}

	return checkFilePath(pkgName, licenseFilePath, licenseNamesFuzzy) && !IsASkippedLicenseFile(pkgName, licenseFilePath)
}

// IsASkippedLicenseFile checks if a file is a known non-license file.
func IsASkippedLicenseFile(pkgName, licenseFilePath string) bool {
	return checkFilePath(pkgName, licenseFilePath, licenseNamesSkip)
}

// checkFilePath checks if a file path matches any of the given names. Any leading common path is stripped before
// matching (i.e. "/usr/share/licenses/<pkg>/file/path" -> "file/path"). The matching is a case-insensitive sub-string
// search.
func checkFilePath(pkgName, licenseFilePath string, licenseFilesMatches []string) bool {
	// For each path, strip the prefix plus package name if it exists
	// i.e. "/usr/share/licenses/<pkg>/file/path" -> "file/path"
	// Those paths would always match since they contain "license" in the name.
	strippedPath := filepath.Clean(licenseFilePath)
	pkgPrefix := filepath.Join(licensePrefix, pkgName)
	if strings.HasPrefix(licenseFilePath, licensePrefix) {
		strippedPath = strings.TrimPrefix(licenseFilePath, pkgPrefix)             // Remove the license + pkg prefix
		strippedPath = strings.TrimPrefix(strippedPath, licensePrefix)            // Remove the license prefix
		strippedPath = strings.TrimPrefix(strippedPath, string(os.PathSeparator)) // Remove the leading path separator if it exists

		// Rebuild the path without the 1st component
		if len(strippedPath) == 0 {
			// It was just the license directory
			return false
		}
	}

	for _, name := range licenseFilesMatches {
		if strings.Contains(strings.ToLower(strippedPath), strings.ToLower(name)) {
			return true
		}
	}
	return false
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
