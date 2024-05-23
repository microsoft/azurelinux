// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A tool for validating %license entries in rpms

package licensecheck

import (
	"path/filepath"
	"regexp"
	"strings"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/jsonutils"
	"github.com/stretchr/testify/assert"
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

func TestLoadLicenseNames(t *testing.T) {
	file := "testdata/test_license_names.json"
	expectedNames := LicenseNames{
		FuzzyLicenseNamesRegexList: []string{
			"(?i).*fuzzy.*",
		},
		compiledFuzzyLicenseNamesList: []*regexp.Regexp{
			regexp.MustCompile("(?i).*fuzzy.*"),
		},
		VerbatimLicenseNamesRegexList: []string{
			"^vErBaTiM$",
		},
		compiledVerbatimLicenseNamesList: []*regexp.Regexp{
			regexp.MustCompile("^vErBaTiM$"),
		},
		SkipLicenseNamesRegexList: []string{
			"(?i).*skip.*",
		},
		compiledSkipLicenseNamesList: []*regexp.Regexp{
			regexp.MustCompile("(?i).*skip.*"),
		},
	}

	names, err := LoadLicenseNames(file)

	// Check if there was an error loading the license exceptions
	if err != nil {
		t.Errorf("Failed to load license names: %v", err)
	}

	// Check if the loaded exceptions match the expected exceptions
	assert.Equal(t, expectedNames, names)
}

func TestNotPanicMissingNameFile(t *testing.T) {
	tempPath := t.TempDir()
	file := filepath.Join(tempPath, "missing_file.json")
	assert.NotPanics(t, func() {
		_, err := LoadLicenseNames(file)
		assert.EqualError(t, err, "failed to read license names file:\nopen "+file+": no such file or directory")
	})
}

func TestInvalidNameRegex(t *testing.T) {
	const invalidRegex = `.*[`
	testCases := []struct {
		name        string
		json        string
		expectedErr string
	}{
		{
			name:        "Invalid fuzzy regex",
			json:        `{"FuzzyLicenseNamesRegexList": ["` + invalidRegex + `"], "VerbatimLicenseNamesRegexList": [], "SkipLicenseNamesRegexList": []}`,
			expectedErr: "failed to compile regex for license names (.*[):\nerror parsing regexp: missing closing ]: `[`",
		},
		{
			name:        "Invalid verbatim regex",
			json:        `{"FuzzyLicenseNamesRegexList": [], "VerbatimLicenseNamesRegexList": ["` + invalidRegex + `"], "SkipLicenseNamesRegexList": []}`,
			expectedErr: "failed to compile regex for license names (.*[):\nerror parsing regexp: missing closing ]: `[`",
		},
		{
			name:        "Invalid skip regex",
			json:        `{"FuzzyLicenseNamesRegexList": [], "VerbatimLicenseNamesRegexList": [], "SkipLicenseNamesRegexList": ["` + invalidRegex + `"]}`,
			expectedErr: "failed to compile regex for license names (.*[):\nerror parsing regexp: missing closing ]: `[`",
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			tempPath := t.TempDir()
			jsonFilePath := filepath.Join(tempPath, "invalid_regex.json")
			err := file.Write(tc.json, jsonFilePath)
			assert.NoError(t, err)
			names, err := LoadLicenseNames(jsonFilePath)
			assert.Error(t, err)
			assert.EqualError(t, err, tc.expectedErr)
			assert.Equal(t, LicenseNames{}, names)
		})
	}
}

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
	n := loadDefaultLicenseNames(t)

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
					assert.True(t, n.IsALicenseFile(pkgName, tc))
					assert.False(t, n.IsASkippedLicenseFile(pkgName, tc))
				})
			}
		})
	}
}

func TestIsASkippedLicenseFile(t *testing.T) {
	const pkgName = "pkg"
	n := loadDefaultLicenseNames(t)

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
			assert.True(t, n.IsASkippedLicenseFile(pkgName, tc))
		})
	}
}

func TestIsALicenseFile_Specific(t *testing.T) {
	const pkgName = "pkg"
	n := loadDefaultLicenseNames(t)

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
			res := n.IsALicenseFile(pkgName, tc.file)
			assert.Equal(t, tc.expected, res)
		})
	}
}

func TestIsNotALicenseFile(t *testing.T) {
	const (
		pkgName  = "pkg"
		basePath = "/usr/share/licenses/"
	)
	n := loadDefaultLicenseNames(t)

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
			assert.False(t, n.IsALicenseFile(pkgName, tc))
		})
	}
}

func TestSubDirsMatch(t *testing.T) {
	const pkgName = "pkg"
	n := loadDefaultLicenseNames(t)

	testCases := []string{
		"/usr/share/licenses/pkg/COPYING",
		"/usr/share/licenses/pkg/subdir/COPYING",
		"/usr/share/licenses/pkg/LICENSES/random_file",
		"/usr/share/licenses/pkg/licenses/random_file",
		"/path/to/LICENSE",
	}
	for _, tc := range testCases {
		t.Run(tc, func(t *testing.T) {
			assert.True(t, n.IsALicenseFile(pkgName, tc))
			assert.False(t, n.IsASkippedLicenseFile(pkgName, tc))
		})
	}
}

// The license directory itself isn't a valid match.
func TestLicenseDirDoesNotMatch(t *testing.T) {
	const pkgName = "pkg"
	n := loadDefaultLicenseNames(t)

	testCases := []string{
		"/usr/share/licenses/",
		"/usr/share/licenses/pkg",
		"/usr/share/licenses/pkg/",
	}
	for _, tc := range testCases {
		t.Run(tc, func(t *testing.T) {
			assert.False(t, n.IsALicenseFile(pkgName, tc))
		})
	}
}

func TestAgainstKnownLicenses(t *testing.T) {
	// We store all the %license files from the distro in ./testdata/all_licenses_<date>.json
	// See ./testdata/README.md for more information on how to generate this file

	// This test will check that MOST of the known licenses are correctly identified as licenses. It is not
	// exhaustive, but it should catch most common cases. This value can be increased as the quality of the
	// packages improves.
	const acceptablePercentage = 0.98
	n := loadDefaultLicenseNames(t)

	// Find all data files in the testdata directory
	testDataFile := ""
	paths, err := filepath.Glob("./testdata/all_licenses_*.json")
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

	test_data := testData{}
	err = jsonutils.ReadJSONFile(testDataFile, &test_data)
	if err != nil || test_data.UniqueFiles == 0 {
		t.Fatalf("failed to read input file: %v", err)
	}

	invalid_entires := 0
	for _, test := range test_data.TestDataEntries {
		if !n.IsALicenseFile(test.Pkg, test.Path) {
			invalid_entires++
		}
	}

	invalidPercentage := float64(invalid_entires) / float64(test_data.UniqueFiles)
	if invalidPercentage > 1.0-acceptablePercentage {
		t.Errorf("Failed to identify %d out of %d known licenses (%.2f%%)", invalid_entires, test_data.UniqueFiles, invalidPercentage*100)
	}
}

func TestAgainstKnownDocs(t *testing.T) {
	// We store all the %doc files from the distro in ./testdata/all_docs_<date>.json
	// See ./testdata/README.md for more information on how to generate this file

	// This test will check that MOST of the known docs are correctly identified as not licenses. It is not
	// exhaustive, but it should catch most common cases.
	const acceptablePercentage = 0.99
	n := loadDefaultLicenseNames(t)

	// Find all data files in the testdata directory
	testDataFile := ""
	paths, err := filepath.Glob("./testdata/all_docs_*.json")
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

	test_data := testData{}
	err = jsonutils.ReadJSONFile(testDataFile, &test_data)
	if err != nil || test_data.UniqueFiles == 0 {
		t.Fatalf("failed to read input file: %v", err)
	}

	invalid_entires := 0
	for _, test := range test_data.TestDataEntries {
		if n.IsALicenseFile(test.Pkg, test.Path) {
			invalid_entires++
		}
	}

	invalidPercentage := float64(invalid_entires) / float64(test_data.UniqueFiles)
	if invalidPercentage > 1.0-acceptablePercentage {
		t.Errorf("Failed to skip %d out of %d known docs (%.2f%%)", invalid_entires, test_data.UniqueFiles, invalidPercentage*100)
	}
}
