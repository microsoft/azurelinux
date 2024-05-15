// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A tool for validating %license entries in rpms

package licensecheck

import (
	"path/filepath"
	"regexp"
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
