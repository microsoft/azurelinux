// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Tool to validate test data for the licensecheck package unit tests.

package main

import (
	"os"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/exe"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/jsonutils"
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
	nameFile      = app.Flag("name-file", "Path to the file containing the list of license names to check for.").Required().ExistingFile()
	exceptionFile = app.Flag("exception-file", "Path to the file containing the list of exceptions to the license check.").Required().ExistingFile()
)

type testData struct {
	UniqueFiles     int
	UniquePackages  int
	TestDataEntries []testDataEntry
}

type testDataEntry struct {
	Pkg  string `json:"Pkg"`
	Path string `json:"Path"`
}

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitStderrLog()

	names, err := licensecheck.LoadLicenseNames(*nameFile)
	if err != nil {
		logger.Log.Fatalf("Failed to load license names: %v", err)
	}

	exceptions, err := licensecheck.LoadLicenseExceptions(*exceptionFile)
	if err != nil {
		logger.Log.Fatalf("Failed to load license exceptions: %v", err)
	}

	// Validate actual license files, checking for false negatives
	realLicenses := readTestData(*licenses)
	filesNotDetectedAsLicense := checkFalseNegatives(realLicenses, names, exceptions)
	writeTestData(filesNotDetectedAsLicense, *licensesOut)
	falseNegativeRatio := float64(len(filesNotDetectedAsLicense.TestDataEntries)) / float64(len(realLicenses.TestDataEntries))
	logger.Log.Infof("Wrote %d invalid entries to '%s' (%.2f%% false negative)", len(filesNotDetectedAsLicense.TestDataEntries), *licensesOut, falseNegativeRatio*100)

	// Validate doc files, checking for false positives
	docs := readTestData(*docs)
	invalidDocs := checkFalsePositives(docs, names, exceptions)
	writeTestData(invalidDocs, *docsOut)
	falsePositiveRatio := float64(len(invalidDocs.TestDataEntries)) / float64(len(docs.TestDataEntries))
	logger.Log.Infof("Wrote %d invalid docs to '%s' (%.2f%% false positive)", len(invalidDocs.TestDataEntries), *docsOut, falsePositiveRatio*100)

	// Validate other files, checking for false positives
	otherFiles := readTestData(*otherFiles)
	invalidOtherFiles := checkFalsePositives(otherFiles, names, exceptions)
	writeTestData(invalidOtherFiles, *otherFilesOut)
	falsePositiveRatio = float64(len(invalidOtherFiles.TestDataEntries)) / float64(len(otherFiles.TestDataEntries))
	logger.Log.Infof("Wrote %d invalid other files to '%s' (%.2f%% false positive)", len(invalidOtherFiles.TestDataEntries), *otherFilesOut, falsePositiveRatio*100)

}

func readTestData(filePath string) testData {
	var tests testData
	err := jsonutils.ReadJSONFile(filePath, &tests)
	if err != nil {
		logger.Log.Fatalf("failed to read input file: %v", err)
	}
	return tests
}

func writeTestData(tests testData, filePath string) {
	err := jsonutils.WriteJSONFile(filePath, tests)
	if err != nil {
		logger.Log.Fatalf("failed to write output file: %v", err)
	}
}

func checkFalseNegatives(tests testData, names licensecheck.LicenseNames, exceptions licensecheck.LicenseExceptions) (falseNegatives testData) {
	for _, test := range tests.TestDataEntries {
		if !names.IsALicenseFile(test.Pkg, test.Path) || exceptions.ShouldIgnoreFile(test.Pkg, test.Path) {
			falseNegatives.TestDataEntries = append(falseNegatives.TestDataEntries, test)
		}
	}
	falseNegatives.UniqueFiles = len(falseNegatives.TestDataEntries)
	falseNegatives.UniquePackages = len(falseNegatives.TestDataEntries)
	return falseNegatives
}

func checkFalsePositives(tests testData, names licensecheck.LicenseNames, exceptions licensecheck.LicenseExceptions) (falsePositives testData) {
	for _, test := range tests.TestDataEntries {
		if names.IsALicenseFile(test.Pkg, test.Path) && !exceptions.ShouldIgnoreFile(test.Pkg, test.Path) {
			falsePositives.TestDataEntries = append(falsePositives.TestDataEntries, test)
		}
	}
	falsePositives.UniqueFiles = len(falsePositives.TestDataEntries)
	falsePositives.UniquePackages = len(falsePositives.TestDataEntries)
	return falsePositives
}
