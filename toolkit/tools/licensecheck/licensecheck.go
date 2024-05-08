// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A tool for validating the license files of RPM packages in a set of directories.

package main

import (
	"fmt"
	"os"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/exe"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/licensecheck"

	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app = kingpin.New("licensecheck", "A tool for validating the license files of RPM packages.")

	rpmDirs       = app.Flag("rpm-dirs", "Directories to recursively scan for RPMs to validate").Required().ExistingDirs()
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

	// Run scans on each directory
	totalResults := []licensecheck.LicenseCheckResult{}
	totalFailedPackages := 0
	totalWarningPackages := 0
	for _, rpmDir := range *rpmDirs {
		errorResults, warningResults, err := validateRpmDir(*buildDirPath, *workerTar, rpmDir, *exceptionFile, *distTag, *pedantic)
		if err != nil {
			logger.Log.Fatalf("Failed to search RPM directory. Error: %v", err)
		}
		totalFailedPackages += len(errorResults)
		totalWarningPackages += len(warningResults)
		totalResults = append(totalResults, errorResults...)
		totalResults = append(totalResults, warningResults...)
	}

	// Save results
	if *resultFile != "" {
		logger.Log.Infof("Writing results to file: %s", *resultFile)
		err := licensecheck.SaveLicenseCheckResults(*resultFile, totalResults)
		if err != nil {
			logger.Log.Fatalf("Failed to write results to file. Error: %v", err)
		}
	}

	// Print summary
	if totalFailedPackages > 0 {
		printExplanation()
		logger.Log.Errorf("Found (%d) packages with license errors.", totalFailedPackages)
		logger.Log.Warnf("Found (%d) packages with non-fatal license issues.", totalWarningPackages)
		os.Exit(1)
	} else if totalWarningPackages > 0 {
		printExplanation()
		logger.Log.Warnf("Found (%d) packages with non-fatal license issues", totalWarningPackages)
	} else {
		logger.Log.Infof("No license issues found")
	}
}

func printExplanation() {
	logger.Log.Info("Errors/warnings fall into three buckets:")
	logger.Log.Infof("\t1. 'bad %%doc files': A %%doc documentation file that the tool believes to be a license file.")
	logger.Log.Infof("\t\tFiles should either be changed to %%license, or added to the exceptions file:")
	logger.Log.Infof("\t\t(%s)", *exceptionFile)
	logger.Log.Infof("\t2. 'bad general file': A file that is placed into '/usr/share/licenses/' that is not flagged as")
	logger.Log.Infof("\t\ta license file. These files should use %%license.")
	logger.Log.Infof("\t3. 'duplicated license files': A license file that is both a %%license and a %%doc file, pick one.")
	logger.Log.Infof("\t\tThis is a warning, unless the tool is run in pedantic mode, in which case it is an error.")
}

// validateRpmDir scans the given directory for RPMs and validates their licenses. It will return all findings split into warnings and failures.
// Each call to this function will generate a new chroot environment and clean it up after the scan.
func validateRpmDir(buildDirPath, workerTar, rpmDir, exceptionFile, distTag string, pedantic bool) (warningResults, failedResults []licensecheck.LicenseCheckResult, err error) {
	logger.Log.Infof("Preparing license check environment for %s...", rpmDir)
	licenseChecker, err := licensecheck.New(buildDirPath, workerTar, rpmDir, exceptionFile, distTag)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to initialize RPM license checker:\n%v", err)
	}
	defer func() {
		cleanupErr := licenseChecker.CleanUp()
		if cleanupErr != nil {
			if err == nil {
				err = cleanupErr
			} else {
				// Append the cleanup error to the existing error
				err = fmt.Errorf("%w\nfailed to cleanup after RPM license checker failed:\n%w", err, cleanupErr)
			}
		}
	}()

	logger.Log.Infof("Scanning %s for license issues...", rpmDir)
	err = licenseChecker.CheckLicenses()
	if err != nil {
		return nil, nil, fmt.Errorf("failed to generate license scan:\n%w", err)
	}

	resultsString := licenseChecker.FormatResults(pedantic)
	logger.Log.Infof("Search results for %s:\n%s", rpmDir, resultsString)

	_, warningResults, failedResults = licenseChecker.GetAllResults(pedantic)

	return failedResults, warningResults, nil
}
