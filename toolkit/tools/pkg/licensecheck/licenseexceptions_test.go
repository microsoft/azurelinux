// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package licensecheck

import (
	"path/filepath"
	"regexp"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/stretchr/testify/assert"
)

func TestLoadLicenseExceptions(t *testing.T) {
	file := "testdata/test_license_exceptions.json"
	expectedExceptions := LicenseExceptions{
		PkgExceptions: []PkgExceptions{
			{
				PackageName: "TestPackage1",
				IgnoredFilesRegexList: []string{
					"/usr/share/doc/LICENSE",
					"/usr/share/doc/README.GPL",
					".*GLOB1",
				},
				compiledIgnoreRegexList: []*regexp.Regexp{
					regexp.MustCompile("/usr/share/doc/LICENSE"),
					regexp.MustCompile("/usr/share/doc/README.GPL"),
					regexp.MustCompile(".*GLOB1"),
				},
			},
			{
				PackageName: "TestPackage2",
				IgnoredFilesRegexList: []string{
					"/usr/share/doc/LICENSE",
					"/usr/share/doc/README.GPL",
					".*GLOB2",
				},
				compiledIgnoreRegexList: []*regexp.Regexp{
					regexp.MustCompile("/usr/share/doc/LICENSE"),
					regexp.MustCompile("/usr/share/doc/README.GPL"),
					regexp.MustCompile(".*GLOB2"),
				},
			},
		},
		GlobalExceptionsRegexList: []string{
			".*GLOB3",
		},
		compiledGlobalIgnoreRegexList: []*regexp.Regexp{
			regexp.MustCompile(".*GLOB3"),
		},
	}

	exceptions, err := LoadLicenseExceptions(file)

	// Check if there was an error loading the license exceptions
	if err != nil {
		t.Errorf("Failed to load license exceptions: %v", err)
	}

	// Check if the loaded exceptions match the expected exceptions
	assert.Equal(t, expectedExceptions, exceptions)
}

func TestShouldIgnoreFile(t *testing.T) {
	exceptions := LicenseExceptions{
		PkgExceptions: []PkgExceptions{
			{
				PackageName: "TestPackage1",
				IgnoredFilesRegexList: []string{
					"/usr/share/doc/LICENSE",
					"/usr/share/doc/README.GPL",
					".*GLOB1",
				},
				compiledIgnoreRegexList: []*regexp.Regexp{
					regexp.MustCompile("/usr/share/doc/LICENSE"),
					regexp.MustCompile("/usr/share/doc/README.GPL"),
					regexp.MustCompile(".*GLOB1"),
				},
			},
			{
				PackageName: "TestPackage2",
				IgnoredFilesRegexList: []string{
					"/usr/share/doc/LICENSE",
					"/usr/share/doc/README.GPL",
					".*GLOB2",
				},
				compiledIgnoreRegexList: []*regexp.Regexp{
					regexp.MustCompile("/usr/share/doc/LICENSE"),
					regexp.MustCompile("/usr/share/doc/README.GPL"),
					regexp.MustCompile(".*GLOB2"),
				},
			},
		},
		GlobalExceptionsRegexList: []string{
			".*GLOB3",
		},
		compiledGlobalIgnoreRegexList: []*regexp.Regexp{
			regexp.MustCompile(".*GLOB3"),
		},
	}

	testCases := []struct {
		name             string
		packageName      string
		filePath         string
		expectedResponse bool
	}{
		{
			name:             "File should be ignored",
			packageName:      "TestPackage1",
			filePath:         "/usr/share/doc/LICENSE",
			expectedResponse: true,
		},
		{
			name:             "2nd File should be ignored",
			packageName:      "TestPackage1",
			filePath:         "/usr/share/doc/README.GPL",
			expectedResponse: true,
		},
		{
			name:             "File should be ignored in other package",
			packageName:      "TestPackage2",
			filePath:         "/usr/share/doc/LICENSE",
			expectedResponse: true,
		},
		{
			name:             "File should not be ignored in listed package",
			packageName:      "TestPackage1",
			filePath:         "/usr/share/doc/other_file",
			expectedResponse: false,
		},
		{
			name:             "File should not be ignored in other package",
			packageName:      "TestPackage3",
			filePath:         "/usr/share/doc/LICENSE",
			expectedResponse: false,
		},
		{
			name:             "File should match package glob",
			packageName:      "TestPackage1",
			filePath:         "/usr/share/doc/GLOB1",
			expectedResponse: true,
		},
		{
			name:             "File should not match package glob",
			packageName:      "TestPackage1",
			filePath:         "/usr/share/doc/GLOB2",
			expectedResponse: false,
		},
		{
			name:             "File should match global glob",
			packageName:      "TestPackage1",
			filePath:         "/usr/share/doc/GLOB3",
			expectedResponse: true,
		},
		{
			name:             "File should match unkown package with global glob",
			packageName:      "NOT_A_PACKAGE",
			filePath:         "/usr/share/doc/GLOB3",
			expectedResponse: true,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			assert.Equal(t, tc.expectedResponse, exceptions.ShouldIgnoreFile(tc.packageName, tc.filePath))
		})
	}
}

func TestNotPanicMissingFile(t *testing.T) {
	tempPath := t.TempDir()
	file := filepath.Join(tempPath, "missing_file.json")
	assert.NotPanics(t, func() {
		_, err := LoadLicenseExceptions(file)
		assert.EqualError(t, err, "failed to read license exceptions file:\nopen "+file+": no such file or directory")
	})
}

func TestInvalidRegex(t *testing.T) {
	const invalidRegex = `.*[`
	testCases := []struct {
		name        string
		json        string
		expectedErr string
	}{
		{
			name:        "Invalid regex",
			json:        `{"PkgExceptions": [{"PackageName": "TestPackage1", "IgnoredFilesRegexList": ["` + invalidRegex + `"]}], "GlobalExceptionsRegexList": []}`,
			expectedErr: "failed to compile regex for ignored files (.*[):\nerror parsing regexp: missing closing ]: `[`",
		},
		{
			name:        "Invalid global regex",
			json:        `{"PkgExceptions": [], "GlobalExceptionsRegexList": ["` + invalidRegex + `"]}`,
			expectedErr: "failed to compile regex for global ignored files (.*[):\nerror parsing regexp: missing closing ]: `[`",
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			tempPath := t.TempDir()
			jsonFilePath := filepath.Join(tempPath, "invalid_regex.json")
			err := file.Write(tc.json, jsonFilePath)
			assert.NoError(t, err)
			exceptions, err := LoadLicenseExceptions(jsonFilePath)
			assert.Error(t, err)
			assert.EqualError(t, err, tc.expectedErr)
			assert.Equal(t, LicenseExceptions{}, exceptions)
		})
	}
}
