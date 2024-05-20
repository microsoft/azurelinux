// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package licensecheck

import (
	"fmt"
	"os"
	"path/filepath"
	"testing"

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
