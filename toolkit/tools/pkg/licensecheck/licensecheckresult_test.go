// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package licensecheck

import (
	"path/filepath"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/jsonutils"
	"github.com/stretchr/testify/assert"
)

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
			assert.Equal(t, tc.expectedBad, tc.result.HasErrorResult(LicenseCheckModeDefault))
			assert.Equal(t, tc.expectedWarning, tc.result.HasWarningResult(LicenseCheckModeDefault))
		})
	}
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

func TestSortAndFilter(t *testing.T) {
	r1 := LicenseCheckResult{
		RpmPath:        "/path/to/rpm1",
		BadDocs:        []string{"/docs/doc1", "/docs/doc2"},
		DuplicatedDocs: []string{"/docs/COPY"},
	}
	r2 := LicenseCheckResult{
		RpmPath:        "/path/to/rpm2",
		BadFiles:       []string{"/docs/doc1", "/docs/doc2"},
		DuplicatedDocs: []string{"/docs/COPY"},
	}
	r3 := LicenseCheckResult{
		RpmPath: "/path/to/rpm3",
		BadDocs: []string{"/docs/doc1", "/docs/doc2"},
	}
	r4 := LicenseCheckResult{
		RpmPath: "/path/to/rpm4",
	}
	r5 := LicenseCheckResult{
		RpmPath:        "/path/to/rpm5",
		DuplicatedDocs: []string{"/docs/COPY"},
	}

	unsortedList := []LicenseCheckResult{r5, r4, r2, r1, r3}
	sortedList := []LicenseCheckResult{r1, r2, r3, r4, r5}

	expectedAll := []LicenseCheckResult{r1, r2, r3, r5}
	expectedWarnings := []LicenseCheckResult{r1, r2, r5}
	expectedWarningsPedantic := []LicenseCheckResult{}
	expectedWarningsWarn := []LicenseCheckResult{r1, r2, r3, r5}
	expectedErrors := []LicenseCheckResult{r1, r2, r3}
	expectedErrorsPedantic := []LicenseCheckResult{r1, r2, r3, r5}
	expectedErrorsWarn := []LicenseCheckResult{}

	input := make([]LicenseCheckResult, len(unsortedList))
	copy(input, unsortedList)
	all, warnings, errors := SortAndFilterResults(input, LicenseCheckModeFatalOnly)
	assert.Equal(t, sortedList, input)
	assert.Equal(t, expectedAll, all)
	assert.Equal(t, expectedWarnings, warnings)
	assert.Equal(t, expectedErrors, errors)

	copy(input, unsortedList)
	all, warnings, errors = SortAndFilterResults(input, LicenseCheckModePedantic)
	assert.Equal(t, sortedList, input)
	assert.Equal(t, expectedAll, all)
	assert.Equal(t, expectedWarningsPedantic, warnings)
	assert.Equal(t, expectedErrorsPedantic, errors)

	copy(input, unsortedList)
	all, warnings, errors = SortAndFilterResults(input, LicenseCheckModeWarnOnly)
	assert.Equal(t, sortedList, input)
	assert.Equal(t, expectedAll, all)
	assert.Equal(t, expectedWarningsWarn, warnings)
	assert.Equal(t, expectedErrorsWarn, errors)

	copy(input, unsortedList)
	all, warnings, errors = SortAndFilterResults(input, LicenseCheckModeNone)
	assert.Equal(t, sortedList, input)
	assert.Equal(t, []LicenseCheckResult{}, all)
	assert.Equal(t, []LicenseCheckResult{}, warnings)
	assert.Equal(t, []LicenseCheckResult{}, errors)
}
