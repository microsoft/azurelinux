// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A tool for validating the license files of RPM packages in a set of directories.

package main

import (
	"fmt"
	"os"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/exe"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/licensecheck"

	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app = kingpin.New("licensecheck", "A tool for validating the license files of RPM packages.")

	rpmDirs       = app.Flag("rpm-dirs", "Directories to recursively scan for RPMs to validate").Required().ExistingDirs()
	nameFile      = app.Flag("name-file", "File containing license names to check for.").Required().ExistingFile()
	exceptionFile = app.Flag("exception-file", "File containing license exceptions.").ExistingFile()
	pedantic      = app.Flag("pedantic", "Enable pedantic mode, warnings are errors.").Bool()

	buildDirPath = app.Flag("build-dir", "Directory to store temporary files.").Required().String()
	distTag      = app.Flag("dist-tag", "The distribution tag.").Required().String()
	workerTar    = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz.").Required().ExistingFile()

	logFlags   = exe.SetupLogFlags(app)
	resultFile = app.Flag("results-file", "The file to store the search result.").Default("").String()
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(logFlags)

	results, numFailures, numWarnings := scanDirectories(*rpmDirs, *buildDirPath, *workerTar, *nameFile, *exceptionFile, *distTag, *pedantic)

	if *resultFile != "" {
		logger.Log.Infof("Writing results to file (%s)", *resultFile)
		err := licensecheck.SaveLicenseCheckResults(*resultFile, results)
		if err != nil {
			logger.Log.Fatalf("Failed to write results to file:\n%v", err)
		}
	}

	printSummary(numFailures, numWarnings)
}

func scanDirectories(rpmDirs []string, buildDirPath, workerTar, nameFile, exceptionFile, distTag string, pedantic bool) (results []licensecheck.LicenseCheckResult, failed int, warnings int) {
	totalResults := []licensecheck.LicenseCheckResult{}
	totalFailedPackages := 0
	totalWarningPackages := 0
	for _, rpmDir := range rpmDirs {
		errorResults, warningResults, err := validateRpmDir(buildDirPath, workerTar, rpmDir, nameFile, exceptionFile, distTag, pedantic)
		if err != nil {
			logger.Log.Fatalf("Failed to search RPM directory:\n%v", err)
		}
		totalFailedPackages += len(errorResults)
		totalWarningPackages += len(warningResults)
		totalResults = append(totalResults, errorResults...)
		totalResults = append(totalResults, warningResults...)
	}
	return totalResults, totalFailedPackages, totalWarningPackages
}

func printSummary(numFailures, numWarnings int) {
	const explanation = `
Errors/warnings fall into three buckets:
	1. 'bad %doc files': A %doc documentation file that the tool believes to be a license file.
	2. 'bad general file': A file that is placed into '/usr/share/licenses/' that is not flagged as
		a license file. These files should use %license instead of %doc. Ideally whey should also
		not be placed in a directory manually. (e.g. prefer '%license COPYING' over
		'%license %{_docdir}/%{name}/COPYING')
	3. 'duplicated license files': A license file that is both a %license and a %doc file, pick one.")
		This is a warning, unless the tool is run in pedantic mode, in which case it is an error.
How to fix:
	- 'False positives': In all cases, a detection may be suppressed by using the exception file:
		{{.exceptionFile}}.
		This file contains per-package and global exceptions in the form of regexes.
	- 'bad %%doc files': Mark it using %license, ideally without using a buildroot path (e.g. use '%license COPYING').
	- 'bad general file': Mark it using %license, ideally without using a buildroot path (e.g. use '%license COPYING').
	- 'duplicated license files': If they are actually equivalent, remove the copy in the documentation.
	- Query package contents with 'rpm -ql <package>.rpm' to see all files, 'rpm -qL <package>.rpm' to
		see only the license files, and 'rpm -qd <package>.rpm' to see only the documentation files.`

	if numFailures > 0 {
		logger.Log.Info(strings.ReplaceAll(explanation, "{{.exceptionFile}}", *exceptionFile))
		logger.Log.Errorf("Found %d packages with license errors", numFailures)
		logger.Log.Warnf("Found %d packages with non-fatal license issues", numWarnings)
		os.Exit(1)
	} else if numWarnings > 0 {
		logger.Log.Info(strings.ReplaceAll(explanation, "{{.exceptionFile}}", *exceptionFile))
		logger.Log.Warnf("Found %d packages with non-fatal license issues", numWarnings)
	} else {
		logger.Log.Infof("No license issues found")
	}
}

// validateRpmDir scans the given directory for RPMs and validates their licenses. It will return all findings split into warnings and failures.
// Each call to this function will generate a new chroot environment and clean it up after the scan.
func validateRpmDir(buildDirPath, workerTar, rpmDir, nameFile, exceptionFile, distTag string, pedantic bool,
) (warningResults, failedResults []licensecheck.LicenseCheckResult, err error) {
	logger.Log.Infof("Preparing license check environment for (%s)", rpmDir)
	licenseChecker, err := licensecheck.New(buildDirPath, workerTar, rpmDir, nameFile, exceptionFile, distTag)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to initialize RPM license checker:\n%w", err)
	}
	defer func() {
		cleanupErr := licenseChecker.CleanUp()
		if cleanupErr != nil {
			if err == nil {
				err = fmt.Errorf("failed to cleanup after RPM license checker:\n%w", cleanupErr)
			} else {
				// Append the cleanup error to the existing error
				err = fmt.Errorf("%w\nfailed to cleanup after RPM license checker failed:\n%w", err, cleanupErr)
			}
		}
	}()

	logger.Log.Infof("Scanning (%s) for license issues", rpmDir)
	err = licenseChecker.CheckLicenses()
	if err != nil {
		return nil, nil, fmt.Errorf("failed to generate license scan:\n%w", err)
	}

	resultsString := licenseChecker.FormatResults(pedantic)
	logger.Log.Infof("Search results for (%s):\n%s", rpmDir, resultsString)

	_, warningResults, failedResults = licenseChecker.GetAllResults(pedantic)

	return failedResults, warningResults, nil
}
