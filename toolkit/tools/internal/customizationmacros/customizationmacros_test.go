// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package customizationmacros

import (
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	os.Exit(m.Run())
}

func TestAddMacroFile(t *testing.T) {
	// Create a temporary directory for testing
	tempDir := t.TempDir()

	// Define the test data
	macros := map[string]string{
		"MACRO1": "VALUE1",
		"MACRO2": "VALUE2",
	}
	macroFileName := "test_macros"

	err := AddMacroFile(tempDir, macros, macroFileName, nil)
	assert.NoError(t, err)

	// Verify the existence and contents of the macro file
	expectedFilePath := filepath.Join(tempDir, macroFileName)
	actualContents, err := file.ReadLines(expectedFilePath)
	assert.NoError(t, err)

	expectedContents := append(customizationMacroHeaderComments, []string{
		"%MACRO1 VALUE1",
		"%MACRO2 VALUE2",
	}...)
	assert.Equal(t, expectedContents, actualContents)
}

func TestAddMacroFileWithEmptyMacros(t *testing.T) {
	// Create a temporary directory for testing
	tempDir := t.TempDir()

	// Define the test data
	macros := map[string]string{}
	macroFileName := "test_macros"

	err := AddMacroFile(tempDir, macros, macroFileName, nil)
	assert.NoError(t, err)

	// Ensure the file is not created
	expectedFilePath := filepath.Join(tempDir, macroFileName)
	_, err = os.Stat(expectedFilePath)
	assert.True(t, os.IsNotExist(err))
}

func TestAddMacroFileComments(t *testing.T) {
	// Define the test cases
	defaultMacrosInput := map[string]string{
		"MACRO1": "VALUE1",
		"MACRO2": "VALUE2",
	}
	defaultExpectedContents := []string{
		"%MACRO1 VALUE1",
		"%MACRO2 VALUE2",
	}
	testCases := []struct {
		name             string
		macros           map[string]string
		customComments   []string
		expectError      bool
		expectedContents []string
	}{
		{
			name:   "WithCustomComments",
			macros: defaultMacrosInput,
			customComments: []string{
				"# Custom comment 1",
				"# Custom comment 2",
			},
			expectError: false,
			expectedContents: append(append(customizationMacroHeaderComments, []string{
				"# Custom comment 1",
				"# Custom comment 2",
				"",
			}...), defaultExpectedContents...),
		},
		{
			name:   "WithBadComment",
			macros: defaultMacrosInput,
			customComments: []string{
				"# Custom comment 1",
				"Custom comment 2",
			},
			expectError: true,
		},
		{
			name:             "WithEmptyCustomComments",
			macros:           defaultMacrosInput,
			customComments:   []string{},
			expectError:      false,
			expectedContents: append(customizationMacroHeaderComments, defaultExpectedContents...),
		},
		{
			name:             "WithNilCustomComments",
			macros:           defaultMacrosInput,
			customComments:   nil,
			expectError:      false,
			expectedContents: append(customizationMacroHeaderComments, defaultExpectedContents...),
		},
		{
			name:   "WithWhitespaceInCustomComments",
			macros: defaultMacrosInput,
			customComments: []string{
				"  # Custom comment 1",
				"  # Custom comment 2",
			},
			expectError: false,
			expectedContents: append(append(customizationMacroHeaderComments, []string{
				"  # Custom comment 1",
				"  # Custom comment 2",
				"",
			}...), defaultExpectedContents...),
		},
		{
			name:             "WithEmptyStringCustomComments",
			macros:           defaultMacrosInput,
			customComments:   []string{""},
			expectError:      false,
			expectedContents: append(append(customizationMacroHeaderComments, []string{"", ""}...), defaultExpectedContents...),
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Create a temporary directory for testing
			tempDir := t.TempDir()

			// Define the test data
			macroFileName := "test_macros"

			err := AddMacroFile(tempDir, tc.macros, macroFileName, tc.customComments)

			if tc.expectError {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)

				// Verify the existence and contents of the macro file
				expectedFilePath := filepath.Join(tempDir, macroFileName)
				actualContents, err := file.ReadLines(expectedFilePath)
				assert.NoError(t, err)

				assert.Equal(t, tc.expectedContents, actualContents)

				// Ensure all lines are either empty, one of the macros, or have a "#" prefix
				for _, line := range actualContents {
					trimedLine := strings.TrimSpace(line)
					if trimedLine == "" {
						continue
					}
					if trimedLine[0] == '#' {
						continue
					}
					if line[0] == '%' {
						continue
					}
					assert.Fail(t, "unexpected line in macro file: "+line)
				}
			}
		})
	}
}

func TestAddCustomizationMacros(t *testing.T) {
	// Define the test cases
	const (
		docFile    = "/usr/lib/rpm/macros.d/macros.installercustomizations_disable_docs"
		localeFile = "/usr/lib/rpm/macros.d/macros.installercustomizations_customize_locales"
	)
	testCases := []struct {
		name                string
		disableDocs         bool
		DisableRpmLocales   bool
		OverrideRpmLocales  string
		expectError         bool
		expectedDocMacro    string
		expectedLocaleMacro string
		expectedDocFile     string
		expectedLocaleFile  string
	}{
		{
			name:              "DisableDocs",
			disableDocs:       true,
			DisableRpmLocales: false,
			expectError:       false,
			expectedDocMacro:  "%_excludedocs 1",
			expectedDocFile:   docFile,
		},
		{
			name:                "DisableRpmLocales",
			disableDocs:         false,
			DisableRpmLocales:   true,
			expectError:         false,
			expectedLocaleMacro: "%_install_langs NONE",
			expectedLocaleFile:  localeFile,
		},
		{
			name:                "DisableDocsAndLocales",
			disableDocs:         true,
			DisableRpmLocales:   true,
			expectError:         false,
			expectedDocMacro:    "%_excludedocs 1",
			expectedLocaleMacro: "%_install_langs NONE",
			expectedDocFile:     docFile,
			expectedLocaleFile:  localeFile,
		},
		{
			name:              "EnableDocsAndLocales",
			disableDocs:       false,
			DisableRpmLocales: false,
			expectError:       false,
		},
		{
			name:                "OverrideRpmLocales",
			disableDocs:         false,
			DisableRpmLocales:   false,
			OverrideRpmLocales:  "en:de:fr",
			expectError:         false,
			expectedLocaleMacro: "%_install_langs en:de:fr",
			expectedLocaleFile:  localeFile,
		},
		{
			name:               "DisableRpmLocalesAndOverrideRpmLocales",
			disableDocs:        false,
			DisableRpmLocales:  true,
			OverrideRpmLocales: "en_US",
			expectError:        true,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			tempDir := t.TempDir()
			err := AddCustomizationMacros(tempDir, tc.disableDocs, tc.DisableRpmLocales, tc.OverrideRpmLocales)

			if tc.expectError {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)

				// If a macro file is not expected, ensure it does not exist
				if tc.expectedDocFile == "" {
					_, err := os.Stat(filepath.Join(tempDir, docFile))
					assert.True(t, os.IsNotExist(err))
				}
				if tc.expectedLocaleFile == "" {
					_, err := os.Stat(filepath.Join(tempDir, localeFile))
					assert.True(t, os.IsNotExist(err))
				}

				// If neither are enabled, ensure no directory is created
				if tc.expectedDocFile == "" && tc.expectedLocaleFile == "" {
					_, err := os.Stat(filepath.Join(tempDir, "/usr/lib/rpm/macros.d"))
					assert.True(t, os.IsNotExist(err))
				}

				// Verify the existence and contents of the macro files
				if tc.expectedDocFile != "" {
					expectedDocFilePath := filepath.Join(tempDir, tc.expectedDocFile)
					docContents, err := file.ReadLines(expectedDocFilePath)
					assert.NoError(t, err)
					// check we set the macro we wanted
					foundMacro := false
					for _, line := range docContents {
						if line == tc.expectedDocMacro {
							foundMacro = true
							break
						}
					}
					assert.True(t, foundMacro)
				}

				if tc.expectedLocaleFile != "" {
					expectedLocaleFilePath := filepath.Join(tempDir, tc.expectedLocaleFile)
					localeContents, err := file.ReadLines(expectedLocaleFilePath)
					assert.NoError(t, err)
					// check we set the macro we wanted
					foundMacro := false
					for _, line := range localeContents {
						if line == tc.expectedLocaleMacro {
							foundMacro = true
							break
						}
					}
					assert.True(t, foundMacro)
				}
			}
		})
	}
}
