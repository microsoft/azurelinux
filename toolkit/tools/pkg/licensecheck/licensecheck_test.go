// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package licensecheck

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"
	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	os.Exit(m.Run())
}

func TestCategorizeResults(t *testing.T) {
	testCases := []struct {
		name            string
		result          LicenseCheckResult
		expectedBad     bool
		expectedWarning bool
	}{
		{
			name: "All results",
			result: LicenseCheckResult{
				BadDocs:        []string{"doc"},
				BadFiles:       []string{"file"},
				DuplicatedDocs: []string{"dupe"},
			},
			expectedBad:     true,
			expectedWarning: true,
		},
		{
			name: "BadDocs",
			result: LicenseCheckResult{
				BadDocs: []string{"doc"},
			},
			expectedBad:     true,
			expectedWarning: false,
		},
		{
			name: "BadFiles",
			result: LicenseCheckResult{
				BadFiles: []string{"file"},
			},
			expectedBad:     true,
			expectedWarning: false,
		},
		{
			name: "DuplicatedDocs",
			result: LicenseCheckResult{
				DuplicatedDocs: []string{"dupe"},
			},
			expectedBad:     false,
			expectedWarning: true,
		},
		{
			name: "BadDocsAndBadFiles",
			result: LicenseCheckResult{
				BadDocs:  []string{"doc"},
				BadFiles: []string{"file"},
			},
			expectedBad:     true,
			expectedWarning: false,
		},
		{
			name: "Dupes with bad doc",
			result: LicenseCheckResult{
				BadDocs:        []string{"doc"},
				DuplicatedDocs: []string{"dupe"},
			},
			expectedBad:     true,
			expectedWarning: true,
		},
		{
			name: "Dupes with bad file",
			result: LicenseCheckResult{
				BadFiles:       []string{"file"},
				DuplicatedDocs: []string{"dupe"},
			},
			expectedBad:     true,
			expectedWarning: true,
		},
		{
			name:            "No results",
			result:          LicenseCheckResult{},
			expectedBad:     false,
			expectedWarning: false,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			assert.Equal(t, tc.expectedBad, tc.result.HasBadResult())
			assert.Equal(t, tc.expectedWarning, tc.result.HasWarningResult())
		})
	}
}

func TestSearchLicenseFilesForMatch(t *testing.T) {
	defaultLicenseFiles := []string{"/usr/share/licenses/pkg/COPYING", "/usr/share/licenses/pkg/COPYING.LIB"}
	testCases := []struct {
		name             string
		documentFile     string
		licenseFiles     []string
		expectedResponse bool
	}{
		{
			name:             "Not a license file",
			documentFile:     "file1",
			licenseFiles:     defaultLicenseFiles,
			expectedResponse: false,
		},
		{
			name:             "License file different dir",
			documentFile:     "/usr/share/docs/pkg/COPYING",
			licenseFiles:     defaultLicenseFiles,
			expectedResponse: true,
		},
		{
			name:             "License file found exact match",
			documentFile:     "/usr/share/licenses/pkg/COPYING",
			licenseFiles:     defaultLicenseFiles,
			expectedResponse: true,
		},
		{
			name:             "License file case mismatch",
			documentFile:     "/usr/share/licenses/pkg/copying",
			licenseFiles:     defaultLicenseFiles,
			expectedResponse: false,
		},
		{
			name:             "License file found with extension",
			documentFile:     "/usr/share/licenses/pkg/COPYING.LIB",
			licenseFiles:     defaultLicenseFiles,
			expectedResponse: true,
		},
		{
			name:             "License file extension mismatch",
			documentFile:     "/usr/share/licenses/pkg/COPYING.wrong_ext",
			licenseFiles:     defaultLicenseFiles,
			expectedResponse: false,
		},
		{
			name:             "License file found with extra bits",
			documentFile:     "/usr/share/licenses/pkg/mypkg-COPYING",
			licenseFiles:     []string{"/usr/share/licenses/pkg/mypkg-COPYING"},
			expectedResponse: true,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			actualResponse := isDocumentInLicenseFiles(tc.documentFile, tc.licenseFiles)
			if actualResponse != tc.expectedResponse {
				t.Errorf("Expected %v, got %v", tc.expectedResponse, actualResponse)
			}
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

func TestIsFileMisplacedInLicensesFolder(t *testing.T) {
	licenseFiles := []string{"/usr/share/licenses/pkg/COPYING", "/usr/share/licenses/pkg/COPYING.LIB"}
	licenseFileSet := sliceutils.SliceToSet(licenseFiles)
	assert.False(t, isFileMisplacedInLicensesFolder("/usr/share/licenses/pkg/COPYING", licenseFileSet))
	assert.False(t, isFileMisplacedInLicensesFolder("/usr/share/not/in/licenses.txt", licenseFileSet))
	assert.True(t, isFileMisplacedInLicensesFolder("/usr/share/licenses/pkg/NOTICE", licenseFileSet))
}

func TestIsFileMisplacedInLicensesFolderDetectPackageFolder(t *testing.T) {
	emptyLicenseFiles := make(map[string]bool)
	assert.True(t, isFileMisplacedInLicensesFolder("/usr/share/licenses/OTHER_PKG/", emptyLicenseFiles))
	assert.True(t, isFileMisplacedInLicensesFolder("/usr/share/licenses/OTHER_PKG", emptyLicenseFiles))
}

func TestSaveResultsToFile(t *testing.T) {
	results := []LicenseCheckResult{
		{
			RpmPath:        "/path/to/rpm",
			BadDocs:        []string{"/docs/doc1", "/docs/doc2"},
			DuplicatedDocs: []string{"/docs/COPY"},
		},
	}
	tempFile := filepath.Join(t.TempDir(), "missing_dir", "results.json")
	err := SaveLicenseCheckResults(tempFile, results)
	assert.Nil(t, err)

	// Load it back and see if it matches.
	resultsCheck := []LicenseCheckResult{}
	err = jsonutils.ReadJSONFile(tempFile, &resultsCheck)
	assert.Nil(t, err)

	assert.Equal(t, results, resultsCheck)
}

func TestFormatResultsNonPedantic(t *testing.T) {
	const notPedantic = false
	testCases := []struct {
		name     string
		results  []LicenseCheckResult
		expected string
	}{
		{
			name:     "No results",
			results:  []LicenseCheckResult{},
			expected: "",
		},
		{
			name: "Single result",
			results: []LicenseCheckResult{
				{
					RpmPath: "/path/to/package.rpm",
					BadDocs: []string{"doc1"},
				},
			},
			expected: "ERROR: 'package.rpm' has license errors:\n" +
				"\tbad %doc files:\n" +
				"\t\tdoc1\n",
		},
		{
			name: "Multiple results",
			results: []LicenseCheckResult{
				{
					RpmPath:        "/path/to/package.rpm",
					BadDocs:        []string{"doc1", "doc2"},
					BadFiles:       []string{"file1", "file2"},
					DuplicatedDocs: []string{"dupe1", "dupe2"},
				},
				{
					RpmPath:        "/path/to/another-package.rpm",
					DuplicatedDocs: []string{"dupe3", "dupe4"},
				},
			},
			expected: "WARN: 'another-package.rpm' has license warnings:\n" +
				"\tduplicated license files:\n" +
				"\t\tdupe3\n" +
				"\t\tdupe4\n" +
				"ERROR: 'package.rpm' has license errors:\n" +
				"\tbad %doc files:\n" +
				"\t\tdoc1\n" +
				"\t\tdoc2\n" +
				"\tbad general file:\n" +
				"\t\tfile1\n" +
				"\t\tfile2\n" +
				"WARN: 'package.rpm' has license warnings:\n" +
				"\tduplicated license files:\n" +
				"\t\tdupe1\n" +
				"\t\tdupe2\n",
		},
		{
			name: "Duplicated docs only",
			results: []LicenseCheckResult{
				{
					RpmPath:        "/path/to/package.rpm",
					DuplicatedDocs: []string{"dupe1", "dupe2"},
				},
			},
			expected: "WARN: 'package.rpm' has license warnings:\n" +
				"\tduplicated license files:\n" +
				"\t\tdupe1\n" +
				"\t\tdupe2\n",
		},
	}
	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			checker := LicenseChecker{
				results: tc.results,
			}
			actual := checker.FormatResults(notPedantic)
			assert.Equal(t, tc.expected, actual)
		})
	}
}

func TestFormatResultsPedantic(t *testing.T) {
	const pedantic = true
	testCases := []struct {
		name     string
		results  []LicenseCheckResult
		expected string
	}{
		{
			name:     "No results",
			results:  []LicenseCheckResult{},
			expected: "",
		},
		{
			name: "Single result",
			results: []LicenseCheckResult{
				{
					RpmPath: "/path/to/package.rpm",
					BadDocs: []string{"doc1"},
				},
			},
			expected: "ERROR: 'package.rpm' has license errors:\n" +
				"\tbad %doc files:\n" +
				"\t\tdoc1\n",
		},
		{
			name: "Multiple results",
			results: []LicenseCheckResult{
				{
					RpmPath:        "/path/to/package.rpm",
					BadDocs:        []string{"doc1", "doc2"},
					BadFiles:       []string{"file1", "file2"},
					DuplicatedDocs: []string{"dupe1", "dupe2"},
				},
				{
					RpmPath:        "/path/to/another-package.rpm",
					DuplicatedDocs: []string{"dupe3", "dupe4"},
				},
			},
			expected: "ERROR: 'another-package.rpm' has license errors:\n" +
				"\tduplicated license files:\n" +
				"\t\tdupe3\n" +
				"\t\tdupe4\n" +
				"ERROR: 'package.rpm' has license errors:\n" +
				"\tbad %doc files:\n" +
				"\t\tdoc1\n" +
				"\t\tdoc2\n" +
				"\tbad general file:\n" +
				"\t\tfile1\n" +
				"\t\tfile2\n" +
				"\tduplicated license files:\n" +
				"\t\tdupe1\n" +
				"\t\tdupe2\n",
		},
		{
			name: "Duplicated docs only",
			results: []LicenseCheckResult{
				{
					RpmPath:        "/path/to/package.rpm",
					DuplicatedDocs: []string{"dupe1", "dupe2"},
				},
			},
			expected: "ERROR: 'package.rpm' has license errors:\n" +
				"\tduplicated license files:\n" +
				"\t\tdupe1\n" +
				"\t\tdupe2\n",
		},
	}
	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			checker := LicenseChecker{
				results: tc.results,
			}
			actual := checker.FormatResults(pedantic)
			assert.Equal(t, tc.expected, actual)
		})
	}
}

func makeResult(name string, numBadDocs, numBadFiles, numDupes int) LicenseCheckResult {
	badDocs := make([]string, numBadDocs)
	for i := 0; i < numBadDocs; i++ {
		badDocs[i] = fmt.Sprintf("doc%d", i)
	}
	badFiles := make([]string, numBadFiles)
	for i := 0; i < numBadFiles; i++ {
		badFiles[i] = fmt.Sprintf("file%d", i)
	}
	dupes := make([]string, numDupes)
	for i := 0; i < numDupes; i++ {
		dupes[i] = fmt.Sprintf("dupe%d", i)
	}
	return LicenseCheckResult{
		RpmPath:        name,
		BadDocs:        badDocs,
		BadFiles:       badFiles,
		DuplicatedDocs: dupes,
	}
}

func TestGetResults(t *testing.T) {
	type expected struct {
		all  []LicenseCheckResult
		warn []LicenseCheckResult
		fail []LicenseCheckResult
	}

	testCases := []struct {
		name     string
		results  []LicenseCheckResult
		expected expected
	}{
		{
			name:    "No results",
			results: []LicenseCheckResult{},
			expected: expected{
				all:  []LicenseCheckResult{},
				warn: []LicenseCheckResult{},
				fail: []LicenseCheckResult{},
			},
		},
		{
			name: "No issues",
			results: []LicenseCheckResult{
				makeResult("pkg1", 0, 0, 0),
			},
			expected: expected{
				all: []LicenseCheckResult{
					makeResult("pkg1", 0, 0, 0),
				},
				warn: []LicenseCheckResult{},
				fail: []LicenseCheckResult{},
			},
		},
		{
			name: "Single error",
			results: []LicenseCheckResult{
				makeResult("pkg1", 1, 1, 1),
			},
			expected: expected{
				all: []LicenseCheckResult{
					makeResult("pkg1", 1, 1, 1),
				},
				warn: []LicenseCheckResult{
					makeResult("pkg1", 1, 1, 1)},
				fail: []LicenseCheckResult{
					makeResult("pkg1", 1, 1, 1),
				},
			},
		},
		{
			name: "Single warn",
			results: []LicenseCheckResult{
				makeResult("pkg1", 0, 0, 1),
			},
			expected: expected{
				all: []LicenseCheckResult{
					makeResult("pkg1", 0, 0, 1),
				},
				warn: []LicenseCheckResult{
					makeResult("pkg1", 0, 0, 1),
				},
				fail: []LicenseCheckResult{},
			},
		},
		{
			name: "Double error",
			results: []LicenseCheckResult{
				makeResult("pkg1", 1, 0, 0),
				makeResult("pkg2", 1, 0, 0),
			},
			expected: expected{
				all: []LicenseCheckResult{
					makeResult("pkg1", 1, 0, 0),
					makeResult("pkg2", 1, 0, 0),
				},
				warn: []LicenseCheckResult{},
				fail: []LicenseCheckResult{
					makeResult("pkg1", 1, 0, 0),
					makeResult("pkg2", 1, 0, 0),
				},
			},
		},
		{
			name: "Multiple results with warn",
			results: []LicenseCheckResult{
				makeResult("pkg1", 1, 1, 1),
				makeResult("pkg2", 0, 0, 2),
			},
			expected: expected{
				all: []LicenseCheckResult{
					makeResult("pkg1", 1, 1, 1),
					makeResult("pkg2", 0, 0, 2),
				},
				warn: []LicenseCheckResult{
					makeResult("pkg1", 1, 1, 1),
					makeResult("pkg2", 0, 0, 2),
				},
				fail: []LicenseCheckResult{
					makeResult("pkg1", 1, 1, 1),
				},
			},
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			checker := LicenseChecker{
				results: tc.results,
			}
			all, warn, fail := checker.GetAllResults(false)
			assert.Equal(t, tc.expected.all, all)
			assert.Equal(t, tc.expected.warn, warn)
			assert.Equal(t, tc.expected.fail, fail)
		})
	}
}

func TestParseCheckResults(t *testing.T) {
	pkgName := "testpkg"
	files := []string{
		"/some/random/file",
		"/usr/share/docs/testpkg/doc.txt",
		"/usr/share/docs/testpkg/COPYING",
		"/usr/share/licenses/testpkg/other_misplaced_2",
		"/usr/share/licenses/testpkg/misplaced",
		"/usr/share/docs/testpkg/licenses/duplicated",
	}
	documentFiles := []string{
		"/usr/share/docs/testpkg/doc.txt",
		"/usr/share/docs/testpkg/COPYING",
		"/usr/share/licenses/testpkg/other_misplaced_2",
		"/usr/share/licenses/testpkg/other_misplaced",
		"/usr/share/docs/testpkg/licenses/duplicated",
	}
	licenseFiles := []string{
		"/usr/share/licenses/testpkg/duplicated",
	}
	exceptions := LicenseExceptions{}

	expectedBadDocFiles := []string{
		"/usr/share/docs/testpkg/COPYING",
	}
	expectedBadOtherFiles := []string{
		"/usr/share/licenses/testpkg/misplaced",
		"/usr/share/licenses/testpkg/other_misplaced_2",
	}
	expectedDuplicatedDocs := []string{
		"/usr/share/docs/testpkg/licenses/duplicated",
	}

	badDocFiles, badOtherFiles, duplicatedDocs := interpretResults(pkgName, files, documentFiles, licenseFiles, exceptions)

	assert.Equal(t, expectedBadDocFiles, badDocFiles)
	assert.Equal(t, expectedBadOtherFiles, badOtherFiles)
	assert.Equal(t, expectedDuplicatedDocs, duplicatedDocs)
}
