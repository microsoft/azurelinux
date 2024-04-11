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
	expectedFilePath := filepath.Join(tempDir, "/usr/lib/rpm/macros.d", macroFileName)
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
	expectedFilePath := filepath.Join(tempDir, "/usr/lib/rpm/macros.d", macroFileName)
	_, err = os.Stat(expectedFilePath)
	assert.True(t, os.IsNotExist(err))
}

func TestAddMacroFileComments(t *testing.T) {
	// Define the test cases
	testCases := []struct {
		name           string
		macros         map[string]string
		customComments []string
		expectError    bool
	}{
		{
			name: "WithCustomComments",
			macros: map[string]string{
				"MACRO1": "VALUE1",
				"MACRO2": "VALUE2",
			},
			customComments: []string{
				"# Custom comment 1",
				"# Custom comment 2",
			},
			expectError: false,
		},
		{
			name: "WithBadComment",
			macros: map[string]string{
				"MACRO1": "VALUE1",
				"MACRO2": "VALUE2",
			},
			customComments: []string{
				"# Custom comment 1",
				"Custom comment 2",
			},
			expectError: true,
		},
		{
			name: "WithEmptyCustomComments",
			macros: map[string]string{
				"MACRO1": "VALUE1",
				"MACRO2": "VALUE2",
			},
			customComments: []string{},
			expectError:    false,
		},
		{
			name: "WithNilCustomComments",
			macros: map[string]string{
				"MACRO1": "VALUE1",
				"MACRO2": "VALUE2",
			},
			customComments: nil,
			expectError:    false,
		},
		{
			name: "With whitespace in custom comments",
			macros: map[string]string{
				"MACRO1": "VALUE1",
				"MACRO2": "VALUE2",
			},
			customComments: []string{
				"  # Custom comment 1",
				"  # Custom comment 2",
			},
			expectError: false,
		},
		{
			name: "With empty custom comments",
			macros: map[string]string{
				"MACRO1": "VALUE1",
				"MACRO2": "VALUE2",
			},
			customComments: []string{""},
			expectError:    false,
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
				expectedFilePath := filepath.Join(tempDir, "/usr/lib/rpm/macros.d", macroFileName)
				actualContents, err := file.ReadLines(expectedFilePath)
				assert.NoError(t, err)

				expectedContents := append(customizationMacroHeaderComments, tc.customComments...)
				if len(tc.customComments) > 0 {
					expectedContents = append(expectedContents, "")
				}
				expectedContents = append(expectedContents, []string{
					"%MACRO1 VALUE1",
					"%MACRO2 VALUE2",
				}...)
				assert.Equal(t, expectedContents, actualContents)

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
	testCases := []struct {
		name           string
		disableDocs    bool
		disableLocales bool
		expectError    bool
	}{
		{
			name:           "DisableDocs",
			disableDocs:    true,
			disableLocales: false,
			expectError:    false,
		},
		{
			name:           "DisableLocales",
			disableDocs:    false,
			disableLocales: true,
			expectError:    false,
		},
		{
			name:           "DisableDocsAndLocales",
			disableDocs:    true,
			disableLocales: true,
			expectError:    false,
		},
		{
			name:           "EnableDocsAndLocales",
			disableDocs:    false,
			disableLocales: false,
			expectError:    false,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			tempDir := t.TempDir()
			err := AddCustomizationMacros(tempDir, tc.disableDocs, tc.disableLocales)

			if tc.expectError {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)

				// If neither are enabled, ensure no file
				if !tc.disableDocs && !tc.disableLocales {
					_, err := os.Stat(filepath.Join(tempDir, "/usr/lib/rpm/macros.d"))
					assert.True(t, os.IsNotExist(err))
				}

				// Verify the existence and contents of the macro files
				if tc.disableDocs {
					expectedDocFilePath := filepath.Join(tempDir, "/usr/lib/rpm/macros.d", disableDocsMacroFile)
					docContents, err := file.ReadLines(expectedDocFilePath)
					assert.NoError(t, err)
					// check we set the macro we wanted
					foundMacro := false
					for _, line := range docContents {
						if line == "%_excludedocs 1" {
							foundMacro = true
							break
						}
					}
					assert.True(t, foundMacro)
				}

				if tc.disableLocales {
					expectedLocaleFilePath := filepath.Join(tempDir, "/usr/lib/rpm/macros.d", disableLocalesMacroFile)
					localeContents, err := file.ReadLines(expectedLocaleFilePath)
					assert.NoError(t, err)
					// check we set the macro we wanted
					foundMacro := false
					for _, line := range localeContents {
						if line == "%_install_langs POSIX" {
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
