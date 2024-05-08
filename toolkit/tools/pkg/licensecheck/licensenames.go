// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A tool for validating %license entries in rpms

package licensecheck

// licenseNamesFuzzy is a list of license names that should be matched in a case-insensitive sub-string search
var licenseNamesFuzzy = []string{
	"copying",
	"license",
	"licence", // British spelling
	"licensing",
	"notice",
	"copyright",
	"artistic",
	"bsd",
	"gpl",
	"cc0",
	"mit.txt",
}

// licenseNamesVerbatim is a list of license names that should be matched exactly
var licenseNamesVerbatim = []string{
	"MIT",
}

// licenseNamesSkip is a list of files that may appear as a license file but generally aren't really licenses
var licenseNamesSkip = []string{
	"AUTHORS",
	"CONTRIBUTORS",
	"README",
	"CREDITS",
}
