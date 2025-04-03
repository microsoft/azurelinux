// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package licensecheckformat

import (
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/pkg/licensecheck"
	"github.com/stretchr/testify/assert"
)

func TestFormatResultsNonPedantic(t *testing.T) {
	testCases := []struct {
		name     string
		results  []licensecheck.LicenseCheckResult
		expected string
	}{
		{
			name:     "No results",
			results:  []licensecheck.LicenseCheckResult{},
			expected: "No license issues found\n",
		},
		{
			name: "Single result",
			results: []licensecheck.LicenseCheckResult{
				{
					RpmPath: "/path/to/package.rpm",
					BadDocs: []string{"doc1"},
				},
			},
			expected: "ERROR: (package.rpm) has license errors:\n" +
				"\tbad %doc files:\n" +
				"\t\tdoc1\n",
		},
		{
			name: "Multiple results",
			results: []licensecheck.LicenseCheckResult{
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
			expected: "WARN: (another-package.rpm) has license warnings:\n" +
				"\tduplicated license files:\n" +
				"\t\tdupe3\n" +
				"\t\tdupe4\n" +
				"ERROR: (package.rpm) has license errors:\n" +
				"\tbad %doc files:\n" +
				"\t\tdoc1\n" +
				"\t\tdoc2\n" +
				"\tbad general file:\n" +
				"\t\tfile1\n" +
				"\t\tfile2\n" +
				"WARN: (package.rpm) has license warnings:\n" +
				"\tduplicated license files:\n" +
				"\t\tdupe1\n" +
				"\t\tdupe2\n",
		},
		{
			name: "Duplicated docs only",
			results: []licensecheck.LicenseCheckResult{
				{
					RpmPath:        "/path/to/package.rpm",
					DuplicatedDocs: []string{"dupe1", "dupe2"},
				},
			},
			expected: "WARN: (package.rpm) has license warnings:\n" +
				"\tduplicated license files:\n" +
				"\t\tdupe1\n" +
				"\t\tdupe2\n",
		},
	}
	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			actual := FormatResults(tc.results, licensecheck.LicenseCheckModeDefault)
			assert.Equal(t, tc.expected, actual)
		})
	}
}

func TestFormatResultsPedantic(t *testing.T) {
	testCases := []struct {
		name     string
		results  []licensecheck.LicenseCheckResult
		expected string
	}{
		{
			name:     "No results",
			results:  []licensecheck.LicenseCheckResult{},
			expected: "No license issues found\n",
		},
		{
			name: "Single result",
			results: []licensecheck.LicenseCheckResult{
				{
					RpmPath: "/path/to/package.rpm",
					BadDocs: []string{"doc1"},
				},
			},
			expected: "ERROR: (package.rpm) has license errors:\n" +
				"\tbad %doc files:\n" +
				"\t\tdoc1\n",
		},
		{
			name: "Multiple results",
			results: []licensecheck.LicenseCheckResult{
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
			expected: "ERROR: (another-package.rpm) has license errors:\n" +
				"\tduplicated license files:\n" +
				"\t\tdupe3\n" +
				"\t\tdupe4\n" +
				"ERROR: (package.rpm) has license errors:\n" +
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
			results: []licensecheck.LicenseCheckResult{
				{
					RpmPath:        "/path/to/package.rpm",
					DuplicatedDocs: []string{"dupe1", "dupe2"},
				},
			},
			expected: "ERROR: (package.rpm) has license errors:\n" +
				"\tduplicated license files:\n" +
				"\t\tdupe1\n" +
				"\t\tdupe2\n",
		},
	}
	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			actual := FormatResults(tc.results, licensecheck.LicenseCheckModePedantic)
			assert.Equal(t, tc.expected, actual)
		})
	}
}

func TestFormatResultsWarnOnly(t *testing.T) {
	testCases := []struct {
		name     string
		results  []licensecheck.LicenseCheckResult
		expected string
	}{
		{
			name:     "No results",
			results:  []licensecheck.LicenseCheckResult{},
			expected: "No license issues found\n",
		},
		{
			name: "Single result",
			results: []licensecheck.LicenseCheckResult{
				{
					RpmPath: "/path/to/package.rpm",
					BadDocs: []string{"doc1"},
				},
			},
			expected: "WARN: (package.rpm) has license warnings:\n" +
				"\tbad %doc files:\n" +
				"\t\tdoc1\n",
		},
		{
			name: "Multiple results",
			results: []licensecheck.LicenseCheckResult{
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
			expected: "WARN: (another-package.rpm) has license warnings:\n" +
				"\tduplicated license files:\n" +
				"\t\tdupe3\n" +
				"\t\tdupe4\n" +
				"WARN: (package.rpm) has license warnings:\n" +
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
			results: []licensecheck.LicenseCheckResult{
				{
					RpmPath:        "/path/to/package.rpm",
					DuplicatedDocs: []string{"dupe1", "dupe2"},
				},
			},
			expected: "WARN: (package.rpm) has license warnings:\n" +
				"\tduplicated license files:\n" +
				"\t\tdupe1\n" +
				"\t\tdupe2\n",
		},
	}
	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			actual := FormatResults(tc.results, licensecheck.LicenseCheckModeWarnOnly)
			assert.Equal(t, tc.expected, actual)
		})
	}
}

func TestFormatResultsEmpty(t *testing.T) {
	actual := FormatResults([]licensecheck.LicenseCheckResult{}, licensecheck.LicenseCheckModeDefault)
	assert.Equal(t, "No license issues found\n", actual)

	actual = FormatResults([]licensecheck.LicenseCheckResult{{RpmPath: "/path/to/package.rpm", PackageName: "pkg1"}}, licensecheck.LicenseCheckModeDefault)
	assert.Equal(t, "No license issues found\n", actual)
}
