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
			assert.Equal(t, tc.expectedBad, tc.result.HasBadResult())
			assert.Equal(t, tc.expectedWarning, tc.result.HasWarningResult())
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
