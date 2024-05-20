// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Tool to validate test data for the licensecheck package unit tests.

package main

import (
	"os"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/exe"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/licensecheck"

	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app           = kingpin.New("licensetestchecker", "Checks test data for licenses.")
	licenses      = app.Flag("licenses", "Path to the input file of license file paths to check for false negatives.").Required().ExistingFile()
	licensesOut   = app.Flag("licenses-output", "Path to the output file to list all false negatives.").Required().String()
	docs          = app.Flag("docs", "Path to the input file of doc file paths to check for false positives.").Required().ExistingFile()
	docsOut       = app.Flag("docs-output", "Path to the output file to list all false positives.").Required().String()
	otherFiles    = app.Flag("other-files", "Path to the input file of other file paths to check for false positives.").Required().ExistingFile()
	otherFilesOut = app.Flag("other-files-output", "Path to the output file to list all false positives.").Required().String()
	exceptionFile = app.Flag("exception-file", "Path to the file containing the list of exceptions to the license check.").Required().ExistingFile()
)

func main() {
	const delimiter = "`"

	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitStderrLog()

	exceptions, err := licensecheck.LoadLicenseExceptions(*exceptionFile)
	// Check if there was an error loading the license exceptions
	if err != nil {
		logger.Log.Fatalf("Failed to load license exceptions: %v", err)
	}

	realLicenseLines, err := file.ReadLines(*licenses)
	if err != nil {
		logger.Log.Fatalf("failed to read input file: %v", err)
	}

	// Each line will be of the form <pkg>`/usr/share/licenses/<pkg>/<subpath>
	filesNotDetectedAsLicense := []string{}
	for _, line := range realLicenseLines {
		splitParts := strings.SplitN(line, delimiter, 2)
		if len(splitParts) != 2 {
			logger.Log.Fatalf("invalid line format: %s", line)
		}
		pkgName, licensePath := splitParts[0], splitParts[1]
		// Check if we consider any of the test data to not be a license file
		if !licensecheck.IsALicenseFile(pkgName, licensePath) || exceptions.ShouldIgnoreFile(pkgName, licensePath) {
			formattedLine := pkgName + delimiter + licensePath
			filesNotDetectedAsLicense = append(filesNotDetectedAsLicense, formattedLine)
		}
	}

	falseNegativeRatio := float64(len(filesNotDetectedAsLicense)) / float64(len(realLicenseLines))
	err = file.WriteLines(filesNotDetectedAsLicense, *licensesOut)
	if err != nil {
		logger.Log.Fatalf("failed to write output file: %v", err)
	}
	logger.Log.Infof("Wrote %d invalid entries to '%s' (%.2f%% false negative)", len(filesNotDetectedAsLicense), *licensesOut, falseNegativeRatio*100)

	// Validate false positives with docs
	invalidDocs := []string{}
	docLines, err := file.ReadLines(*docs)
	if err != nil {
		logger.Log.Fatalf("failed to read docs file: %v", err)
	}

	for _, line := range docLines {
		splitParts := strings.SplitN(line, delimiter, 2)
		if len(splitParts) != 2 {
			logger.Log.Fatalf("invalid line format: %s", line)
		}
		pkgName, docPath := splitParts[0], splitParts[1]

		if licensecheck.IsALicenseFile(pkgName, docPath) && !exceptions.ShouldIgnoreFile(pkgName, docPath) {
			formattedLine := pkgName + delimiter + docPath
			invalidDocs = append(invalidDocs, formattedLine)
		}
	}

	err = file.WriteLines(invalidDocs, *docsOut)
	if err != nil {
		logger.Log.Fatalf("failed to write docs output file: %v", err)
	}

	falsePositiveRatio := float64(len(invalidDocs)) / float64(len(docLines))
	logger.Log.Infof("Wrote %d invalid docs to '%s' (%.2f%% false positive)", len(invalidDocs), *docsOut, falsePositiveRatio*100)

	// Validate false positives with other files
	invalidOtherFiles := []string{}
	otherFilesLines, err := file.ReadLines(*otherFiles)
	if err != nil {
		logger.Log.Fatalf("failed to read docs file: %v", err)
	}

	for _, line := range otherFilesLines {
		splitParts := strings.SplitN(line, delimiter, 2)
		if len(splitParts) != 2 {
			logger.Log.Fatalf("invalid line format: %s", line)
		}
		pkgName, docPath := splitParts[0], splitParts[1]

		if licensecheck.IsALicenseFile(pkgName, docPath) && !exceptions.ShouldIgnoreFile(pkgName, docPath) {
			formattedLine := pkgName + delimiter + docPath
			invalidOtherFiles = append(invalidOtherFiles, formattedLine)
		}
	}

	err = file.WriteLines(invalidOtherFiles, *otherFilesOut)
	if err != nil {
		logger.Log.Fatalf("failed to write docs output file: %v", err)
	}

	falsePositiveRatio = float64(len(invalidOtherFiles)) / float64(len(otherFilesLines))
	logger.Log.Infof("Wrote %d invalid other files to '%s' (%.2f%% false positive)", len(invalidOtherFiles), *otherFilesOut, falsePositiveRatio*100)
}
