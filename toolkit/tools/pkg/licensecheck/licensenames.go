// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A tool for validating %license entries in rpms

package licensecheck

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/jsonutils"
)

type LicenseNames struct {
	FuzzyLicenseNamesRegexList       []string `json:"FuzzyLicenseNamesRegexList"`
	compiledFuzzyLicenseNamesList    []*regexp.Regexp
	VerbatimLicenseNamesRegexList    []string `json:"VerbatimLicenseNamesRegexList"`
	compiledVerbatimLicenseNamesList []*regexp.Regexp
	SkipLicenseNamesRegexList        []string `json:"SkipLicenseNamesRegexList"`
	compiledSkipLicenseNamesList     []*regexp.Regexp
}

// IsALicenseFile makes a best effort guess if a file is a license file or not. This is a heuristic  and is NOT foolproof however.
// Some examples of files that may be incorrectly identified as licenses:
// - /path/to/code/gpl/README.md ("gpl")
// - /path/to/a/hash/CC05f4dcc3b5aa765d61d8327deb882cf ("cc0")
// - /path/to/freebsd-parts/file.ext ("bds")
func (l *LicenseNames) IsALicenseFile(pkgName, licenseFilePath string) bool {
	// Check if the file is in the list of explicit known license files
	for _, name := range l.compiledVerbatimLicenseNamesList {
		baseName := filepath.Base(licenseFilePath)
		if name.MatchString(baseName) {
			return true
		}
	}

	return checkFilePath(pkgName, licenseFilePath, l.compiledFuzzyLicenseNamesList) && !l.IsASkippedLicenseFile(pkgName, licenseFilePath)
}

// IsASkippedLicenseFile checks if a file is a known non-license file.
func (l *LicenseNames) IsASkippedLicenseFile(pkgName, licenseFilePath string) bool {
	return checkFilePath(pkgName, licenseFilePath, l.compiledSkipLicenseNamesList)
}

// checkFilePath checks if a file path matches any of the given names. Any leading common path is stripped before
// matching (i.e. "/usr/share/licenses/<pkg>/file/path" -> "file/path"). The matching is a case-insensitive sub-string
// search.
func checkFilePath(pkgName, licenseFilePath string, licenseFilesMatches []*regexp.Regexp) bool {
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
		if name.MatchString(strippedPath) {
			return true
		}
	}
	return false
}

// LoadLicenseNames loads the license name regexes from the given .json file into a LicenseNames struct
func LoadLicenseNames(file string) (LicenseNames, error) {
	config := LicenseNames{}
	err := jsonutils.ReadJSONFile(file, &config)
	if err != nil {
		return LicenseNames{}, fmt.Errorf("failed to read license names file (%s):\n%w", file, err)
	}

	for i := range config.FuzzyLicenseNamesRegexList {
		regex, err := regexp.Compile(config.FuzzyLicenseNamesRegexList[i])
		if err != nil {
			return LicenseNames{}, fmt.Errorf("failed to compile regex for license names (%s):\n%w", config.FuzzyLicenseNamesRegexList[i], err)
		}
		config.compiledFuzzyLicenseNamesList = append(config.compiledFuzzyLicenseNamesList, regex)
	}

	for i := range config.VerbatimLicenseNamesRegexList {
		regex, err := regexp.Compile(config.VerbatimLicenseNamesRegexList[i])
		if err != nil {
			return LicenseNames{}, fmt.Errorf("failed to compile regex for license names (%s):\n%w", config.VerbatimLicenseNamesRegexList[i], err)
		}
		config.compiledVerbatimLicenseNamesList = append(config.compiledVerbatimLicenseNamesList, regex)
	}

	for i := range config.SkipLicenseNamesRegexList {
		regex, err := regexp.Compile(config.SkipLicenseNamesRegexList[i])
		if err != nil {
			return LicenseNames{}, fmt.Errorf("failed to compile regex for license names (%s):\n%w", config.SkipLicenseNamesRegexList[i], err)
		}
		config.compiledSkipLicenseNamesList = append(config.compiledSkipLicenseNamesList, regex)
	}

	return config, nil
}
