// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A tool for validating %license entries in rpms

package licensecheck

import (
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

// licenseNamesFuzzy is a list of license names that should be matched in a case-insensitive sub-string search
var licenseNamesFuzzy = []*regexp.Regexp{
	regexp.MustCompile(`(?i).*copying.*`),
	regexp.MustCompile(`(?i).*license.*`),
	regexp.MustCompile(`(?i).*licence.*`), // British spelling
	regexp.MustCompile(`(?i).*licensing.*`),
	regexp.MustCompile(`(?i).*notice.*`),
	regexp.MustCompile(`(?i).*copyright.*`),
	regexp.MustCompile(`(?i).*artistic.*`),
	regexp.MustCompile(`(?i).*bsd.*`),
	regexp.MustCompile(`(?i).*gpl.*`),
	regexp.MustCompile(`(?i).*cc0.*`),
	regexp.MustCompile(`(?i).*mit\.txt.*`),
}

// licenseNamesVerbatim is a list of license names that should be matched exactly
var licenseNamesVerbatim = []*regexp.Regexp{
	regexp.MustCompile(`^MIT$`),
}

// licenseNamesSkip is a list of files that may appear as a license file but generally aren't really licenses
var licenseNamesSkip = []*regexp.Regexp{
	regexp.MustCompile(`(?i).*AUTHORS.*`),
	regexp.MustCompile(`(?i).*CONTRIBUTORS.*`),
	regexp.MustCompile(`(?i).*README.*`),
	regexp.MustCompile(`(?i).*CREDITS.*`),
}

// IsALicenseFile makes a best effort guess if a file is a license file or not. This is a heuristic  and is NOT foolproof however.
// Some examples of files that may be incorrectly identified as licenses:
// - /path/to/code/gpl/README.md ("gpl")
// - /path/to/a/hash/CC05f4dcc3b5aa765d61d8327deb882cf ("cc0")
// - /path/to/freebsd-parts/file.ext ("bds")
func IsALicenseFile(pkgName, licenseFilePath string) bool {
	// Check if the file is in the list of explicit known license files
	for _, name := range licenseNamesVerbatim {
		baseName := filepath.Base(licenseFilePath)
		if name.MatchString(baseName) {
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
