// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A tool for validating %license entries in rpms

package licensecheck

import (
	"path/filepath"
	"strings"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/stretchr/testify/assert"
)

func generateTestVariantStrings(pkgName, base string) []string {
	upperCase := strings.ToUpper(base)
	lowerCase := strings.ToLower(base)
	randomizedCase := ""
	basePath := filepath.Join("/usr/share/licenses/", pkgName)
	for i, c := range base {
		if i%2 == 0 {
			randomizedCase += strings.ToLower(string(c))
		} else {
			randomizedCase += strings.ToUpper(string(c))
		}
	}
	fileNames := []string{
		lowerCase,
		upperCase,
		lowerCase + ".txt",
		upperCase + ".txt",
		lowerCase + ".mypkg.txt",
		randomizedCase,
		upperCase + "-mypkg",
		upperCase + "-mypkg-ver",
		"mypkg-" + upperCase,
		"mypkg-" + upperCase + ".txt",
		upperCase + ".MYPKG",
		upperCase + "_MYPKG",
	}
	for i := range fileNames {
		fileNames[i] = filepath.Join(basePath, fileNames[i])
	}
	return fileNames
}

// Test common variations on license file names
func TestIsALicenseFile_Common(t *testing.T) {
	const pkgName = "pkg"
	names := []string{
		"copying",
		"license",
		"licence", // British spelling is sometimes used
		"notice",
		"copyright",
		"artistic",
		"bsd",
		"gpl",
		"cc0",
		"mit.txt",
	}
	for _, name := range names {
		testCases := generateTestVariantStrings(pkgName, name)
		t.Run(name, func(t *testing.T) {
			for _, tc := range testCases {
				t.Run(tc, func(t *testing.T) {
					assert.True(t, IsALicenseFile(pkgName, tc))
					assert.False(t, IsASkippedLicenseFile(pkgName, tc))
				})
			}
		})
	}
}

func TestIsASkippedLicenseFile(t *testing.T) {
	const pkgName = "pkg"
	testCases := []string{
		"AUTHORS",
		"CONTRIBUTORS",
		"README",
		"CREDITS",
		"/usr/share/licenses/pkg/AUTHORS",
		"/usr/share/licenses/pkg/AUTHORS.txt",
		"/usr/share/licenses/pkg/docs/AUTHORS-1.0",
	}
	for _, tc := range testCases {
		t.Run(tc, func(t *testing.T) {
			assert.True(t, IsASkippedLicenseFile(pkgName, tc))
		})
	}
}

func TestIsALicenseFile_Specific(t *testing.T) {
	const pkgName = "pkg"
	testCases := []struct {
		file     string
		expected bool
	}{
		{"MIT", true},
		{"MIT_other", false},
		{"other_MIT", false},
	}
	for _, tc := range testCases {
		t.Run(tc.file, func(t *testing.T) {
			res := IsALicenseFile(pkgName, tc.file)
			assert.Equal(t, tc.expected, res)
		})
	}
}

func TestIsNotALicenseFile(t *testing.T) {
	const (
		pkgName  = "pkg"
		basePath = "/usr/share/licenses/"
	)
	testCases := []string{
		filepath.Join(basePath, pkgName, "file"),
		filepath.Join(basePath, pkgName, "README"),
		filepath.Join(basePath, pkgName, "MIT-file"),
		filepath.Join(basePath, pkgName, "AUTHORS.txt"),
		filepath.Join(basePath, pkgName),
		basePath,
		"/",
	}
	for _, tc := range testCases {
		t.Run(tc, func(t *testing.T) {
			assert.False(t, IsALicenseFile(pkgName, tc))
		})
	}
}

func TestSubDirsMatch(t *testing.T) {
	const pkgName = "pkg"
	testCases := []string{
		"/usr/share/licenses/pkg/COPYING",
		"/usr/share/licenses/pkg/subdir/COPYING",
		"/usr/share/licenses/pkg/LICENSES/random_file",
		"/usr/share/licenses/pkg/licenses/random_file",
		"/path/to/LICENSE",
	}
	for _, tc := range testCases {
		t.Run(tc, func(t *testing.T) {
			assert.True(t, IsALicenseFile(pkgName, tc))
			assert.False(t, IsASkippedLicenseFile(pkgName, tc))
		})
	}
}

// The license directory itself isn't a valid match.
func TestLicenseDirDoesNotMatch(t *testing.T) {
	const pkgName = "pkg"
	testCases := []string{
		"/usr/share/licenses/",
		"/usr/share/licenses/pkg",
		"/usr/share/licenses/pkg/",
	}
	for _, tc := range testCases {
		t.Run(tc, func(t *testing.T) {
			assert.False(t, IsALicenseFile(pkgName, tc))
		})
	}
}

func TestAgainstKnownLicenses(t *testing.T) {
	// We store all the %license files from the distro in ./testdata/all_licenses_<date>.txt
	// See ./testdata/README.md for more information on how to generate this file

	// This test will check that MOST of the known licenses are correctly identified as licenses. It is not
	// exhaustive, but it should catch most common cases. This value can be increased as the quality of the
	// packages improves.
	const acceptablePercentage = 0.8
	const delimiter = "`"

	// Find all data files in the testdata directory
	testDataFile := ""
	paths, err := filepath.Glob("./testdata/all_licenses_*.txt")
	if err != nil {
		t.Fatalf("Failed to find test data file: %v", err)
	}
	// Get the most recent file
	for _, path := range paths {
		if testDataFile < path {
			testDataFile = path
		}
	}
	if testDataFile == "" {
		t.Fatalf("Failed to find test data file")
	}

	test_data, err := file.ReadLines(testDataFile)

	if err != nil || len(test_data) == 0 {
		t.Fatalf("failed to read input file: %v", err)
	}

	invalid_entires := []string{}

	for _, line := range test_data {
		splitParts := strings.SplitN(line, delimiter, 2)
		if len(splitParts) != 2 {
			t.Fatalf("Invalid line (%s)", line)
		}
		pkgName, licensePath := splitParts[0], splitParts[1]
		if !IsALicenseFile(pkgName, licensePath) {
			invalid_entires = append(invalid_entires, line)
		}
	}

	invalidPercentage := float64(len(invalid_entires)) / float64(len(test_data))
	if invalidPercentage > 1.0-acceptablePercentage {
		t.Errorf("Failed to identify %d out of %d known licenses (%.2f%%)", len(invalid_entires), len(test_data), invalidPercentage*100)
	}
}

func TestAgainstKnownDocs(t *testing.T) {
	// We store all the %doc files from the distro in ./testdata/all_docs_<date>.txt
	// See ./testdata/README.md for more information on how to generate this file

	// This test will check that MOST of the known docs are correctly identified as not licenses. It is not
	// exhaustive, but it should catch most common cases.
	const acceptablePercentage = 0.95
	const delimiter = "`"

	// Find all data files in the testdata directory
	testDataFile := ""
	paths, err := filepath.Glob("./testdata/all_docs_*.txt")
	if err != nil {
		t.Fatalf("Failed to find test data file: %v", err)
	}
	// Get the most recent file
	for _, path := range paths {
		if testDataFile < path {
			testDataFile = path
		}
	}
	if testDataFile == "" {
		t.Fatalf("Failed to find test data file")
	}

	test_data, err := file.ReadLines(testDataFile)
	if err != nil || len(test_data) == 0 {
		t.Fatalf("failed to read input file: %v", err)
	}
	invalid_entires := []string{}

	for _, line := range test_data {
		splitParts := strings.SplitN(line, delimiter, 2)
		if len(splitParts) != 2 {
			t.Fatalf("Invalid line (%s)", line)
		}
		pkgName, licensePath := splitParts[0], splitParts[1]
		if IsALicenseFile(pkgName, licensePath) {
			invalid_entires = append(invalid_entires, line)
		}
	}

	invalidPercentage := float64(len(invalid_entires)) / float64(len(test_data))
	if invalidPercentage > 1.0-acceptablePercentage {
		t.Errorf("Failed to skip %d out of %d known docs (%.2f%%)", len(invalid_entires), len(test_data), invalidPercentage*100)
	}
}
