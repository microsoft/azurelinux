// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package rpm

import (
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/exe"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/stretchr/testify/assert"
)

const (
	definesDistKey      = "dist"
	definesWithCheckKey = "with_check"
	specsDir            = "testdata"

	// Distro macro intpus
	distName    = "myDistro"
	distVersion = 1234
	distTag     = ".myDistro1234"
)

var buildArch = goArchToRpmArch[runtime.GOARCH]

var defines = map[string]string{
	definesDistKey:      ".cmX",
	definesWithCheckKey: "1",
}

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	os.Exit(m.Run())
}

func TestExclusiveArchCheckShouldSucceedForSupportedArchitectures(t *testing.T) {
	specFilePath := filepath.Join(specsDir, "supported_unsupported_architectures.spec")

	matches, err := SpecExclusiveArchIsCompatible(specFilePath, specsDir, buildArch, defines)
	assert.NoError(t, err)
	assert.True(t, matches)
}

func TestExclusiveArchCheckShouldSucceedForNoExclusiveArch(t *testing.T) {
	specFilePath := filepath.Join(specsDir, "no_exclusive_architecture.spec")

	matches, err := SpecExclusiveArchIsCompatible(specFilePath, specsDir, buildArch, defines)
	assert.NoError(t, err)
	assert.True(t, matches)
}

func TestExclusiveArchCheckShouldFailForUnsupportedArchitectures(t *testing.T) {
	specFilePath := filepath.Join(specsDir, "unsupported_architectures.spec")

	matches, err := SpecExclusiveArchIsCompatible(specFilePath, specsDir, buildArch, defines)
	assert.NoError(t, err)
	assert.False(t, matches)
}

func TestExcludedArchCheckShouldSucceedForSupportedArchitectures(t *testing.T) {
	specFilePath := filepath.Join(specsDir, "supported_unsupported_architectures.spec")

	matches, err := SpecExcludeArchIsCompatible(specFilePath, specsDir, buildArch, defines)
	assert.NoError(t, err)
	assert.True(t, matches)
}

func TestExcludedArchShouldSucceedForNoExcludedArch(t *testing.T) {
	specFilePath := filepath.Join(specsDir, "no_exclusive_architecture.spec")

	matches, err := SpecExcludeArchIsCompatible(specFilePath, specsDir, buildArch, defines)
	assert.NoError(t, err)
	assert.True(t, matches)
}

func TestExcludedArchShouldFailForExcludedArchitectures(t *testing.T) {
	specFilePath := filepath.Join(specsDir, "unsupported_architectures.spec")

	matches, err := SpecExcludeArchIsCompatible(specFilePath, specsDir, buildArch, defines)
	assert.NoError(t, err)
	assert.False(t, matches)
}

func TestArchCheckShouldSucceedForSupportedArchitectures(t *testing.T) {
	specFilePath := filepath.Join(specsDir, "supported_unsupported_architectures.spec")

	matches, err := SpecArchIsCompatible(specFilePath, specsDir, buildArch, defines)
	assert.NoError(t, err)
	assert.True(t, matches)
}

func TestArchShouldSucceedForNoExcludedArch(t *testing.T) {
	specFilePath := filepath.Join(specsDir, "no_exclusive_architecture.spec")

	matches, err := SpecArchIsCompatible(specFilePath, specsDir, buildArch, defines)
	assert.NoError(t, err)
	assert.True(t, matches)
}

func TestArchShouldFailForExcludedArchitectures(t *testing.T) {
	specFilePath := filepath.Join(specsDir, "unsupported_architectures.spec")

	matches, err := SpecArchIsCompatible(specFilePath, specsDir, buildArch, defines)
	assert.NoError(t, err)
	assert.False(t, matches)
}

func TestShouldListOnlySubpackageWithArchitectureInRPMsList(t *testing.T) {
	expectedArchSuffix := fmt.Sprintf(".%s", buildArch)
	specFilePath := filepath.Join(specsDir, "no_default_package_or_check.spec")

	builtRPMs, err := QuerySPECForBuiltRPMs(specFilePath, specsDir, buildArch, defines)
	assert.NoError(t, err)
	assert.Len(t, builtRPMs, 1)
	assert.True(t, strings.HasSuffix(builtRPMs[0], expectedArchSuffix))
}

func TestShouldNotListPackageEpochForEpochZero(t *testing.T) {
	expectedNameWithVersion := fmt.Sprintf("subpackage_name-1.0.0-1%s", defines[definesDistKey])
	specFilePath := filepath.Join(specsDir, "no_default_package_or_check.spec")

	builtRPMs, err := QuerySPECForBuiltRPMs(specFilePath, specsDir, buildArch, defines)
	assert.NoError(t, err)
	assert.Len(t, builtRPMs, 1)
	assert.True(t, strings.HasPrefix(builtRPMs[0], expectedNameWithVersion))
}

func TestShouldListPackageEpochForEpochOne(t *testing.T) {
	expectedRPMs := []string{
		fmt.Sprintf("with_epoch_and_check-1:1.0.0-1%s.%s", defines[definesDistKey], buildArch),
	}
	specFilePath := filepath.Join(specsDir, "with_epoch_and_check.spec")

	builtRPMs, err := QuerySPECForBuiltRPMs(specFilePath, specsDir, buildArch, defines)
	assert.NoError(t, err)
	assert.EqualValues(t, expectedRPMs, builtRPMs)
}

func TestShouldFindCheckSectionInSpecWithCheckSection(t *testing.T) {
	specFilePath := filepath.Join(specsDir, "with_epoch_and_check.spec")

	hasCheckSection, err := SpecHasCheckSection(specFilePath, specsDir, buildArch, defines)
	assert.NoError(t, err)
	assert.True(t, hasCheckSection)
}

func TestShouldNotFindCheckSectionInSpecWithoutCheckSection(t *testing.T) {
	specFilePath := filepath.Join(specsDir, "no_default_package_or_check.spec")

	hasCheckSection, err := SpecHasCheckSection(specFilePath, specsDir, buildArch, defines)
	assert.NoError(t, err)
	assert.False(t, hasCheckSection)
}

func TestExtractNameFromRPMPath(t *testing.T) {
	tests := []struct {
		name     string
		rpmFile  string
		expected string
		err      error
	}{
		{
			name:     "valid rpm file",
			rpmFile:  "/path/to/pkg-1.0.0-1.noarch.rpm",
			expected: "pkg",
			err:      nil,
		},
		{
			name:     "valid rpm file with complex name",
			rpmFile:  "/path/to/pkg-name-1.0.0-1.noarch.rpm",
			expected: "pkg-name",
			err:      nil,
		},
		{
			name:     "invalid rpm file",
			rpmFile:  "/path/to/garbage.rpm",
			expected: "",
			err:      fmt.Errorf("invalid RPM file path (%s), can't extract name", "/path/to/garbage.rpm"),
		},
		{
			name:     "empty rpm file",
			rpmFile:  "",
			expected: "",
			err:      fmt.Errorf("invalid RPM file path (%s), can't extract name", ""),
		},
		{
			name:     "just a hyphen",
			rpmFile:  "-",
			expected: "",
			err:      fmt.Errorf("invalid RPM file path (%s), can't extract name", "-"),
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			actual, err := ExtractNameFromRPMPath(tt.rpmFile)
			assert.Equal(t, tt.err, err)
			assert.Equal(t, tt.expected, actual)
		})
	}
}

func configureTestDistroMacros(nameAbreviation string, majorVersion int) error {
	err := checkDistroMacros(nameAbreviation, majorVersion)
	if err != nil {
		err = fmt.Errorf("failed to set distro macros:\n%w", err)
		return err
	}
	distNameAbreviation, distMajorVersion = nameAbreviation, majorVersion
	return nil
}

func TestDistroDefines(t *testing.T) {
	tests := []struct {
		name          string
		distroTag     string
		distroName    string
		distroVersion int
		check         bool
		expected      map[string]string
		errorExpected bool
	}{
		{
			name:          "valid distro name and version w/ check",
			distroTag:     distTag,
			distroName:    distName,
			distroVersion: distVersion,
			check:         true,
			expected: map[string]string{
				"dist":       distTag,
				distName:     fmt.Sprint(distVersion),
				"with_check": "1",
			},
			errorExpected: false,
		},
		{
			name:          "valid distro name and version w/o check",
			distroTag:     distTag,
			distroName:    distName,
			distroVersion: distVersion,
			check:         false,
			expected: map[string]string{
				"dist":       distTag,
				distName:     fmt.Sprint(distVersion),
				"with_check": "0",
			},
			errorExpected: false,
		},
		{
			name:          "empty distro tag",
			distroTag:     "",
			distroName:    distName,
			distroVersion: distVersion,
			check:         true,
			expected: map[string]string{
				"dist":       "",
				distName:     fmt.Sprint(distVersion),
				"with_check": "1",
			},
			errorExpected: false,
		},
		{
			name:          "empty distro name",
			distroTag:     distTag,
			distroName:    "",
			distroVersion: distVersion,
			check:         true,
			expected:      nil,
			errorExpected: true,
		},
		{
			name:       "empty distro version",
			distroTag:  distTag,
			distroName: distName,
			// distroVersion is unset
			check:         true,
			expected:      nil,
			errorExpected: true,
		},
		{
			name:          "negative distro version",
			distroTag:     distTag,
			distroName:    distName,
			distroVersion: -1,
			check:         true,
			expected:      nil,
			errorExpected: true,
		},
		{
			name:          "zero distro version",
			distroTag:     distTag,
			distroName:    distName,
			distroVersion: 0,
			check:         true,
			expected:      nil,
			errorExpected: true,
		},
		{
			name:          "one distro version",
			distroTag:     distTag,
			distroName:    distName,
			distroVersion: 1,
			check:         true,
			expected: map[string]string{
				"dist":       distTag,
				distName:     "1",
				"with_check": "1",
			},
			errorExpected: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Save the original values and restore them after the test
			originalDistroName := distNameAbreviation
			originalDistroVersion := distMajorVersion
			t.Cleanup(func() {
				distNameAbreviation = originalDistroName
				distMajorVersion = originalDistroVersion
			})

			err := configureTestDistroMacros(tt.distroName, tt.distroVersion)
			if tt.errorExpected {
				assert.Error(t, err)
				return
			} else {
				assert.NoError(t, err)
			}
			defines := DefaultDistroDefines(tt.check, tt.distroTag)
			assert.Equal(t, tt.expected, defines)
		})
	}
}

func TestDefaultDefines(t *testing.T) {
	// Check that we parse the distro name and version as expected
	expectedName := exe.DistroNameAbbreviation
	expectedVersion, err := strconv.Atoi(exe.DistroMajorVersion)
	assert.NoError(t, err)
	assert.Equal(t, expectedName, distNameAbreviation)
	assert.Equal(t, expectedVersion, distMajorVersion)
}

func TestDistroMacrosLdLoad(t *testing.T) {
	tests := []struct {
		name          string
		distroName    string
		distroVersion string
		panicExpected bool
	}{
		{
			name:          "valid distro name and version",
			distroName:    distName,
			distroVersion: fmt.Sprint(distVersion),
			panicExpected: false,
		},
		{
			name:          "empty distro name",
			distroName:    "",
			distroVersion: fmt.Sprint(distVersion),
			panicExpected: true,
		},
		{
			name:          "empty distro version",
			distroName:    distName,
			distroVersion: "",
			panicExpected: true,
		},
		{
			name:          "negative distro version",
			distroName:    distName,
			distroVersion: "-1",
			panicExpected: true,
		},
		{
			name:          "garbage distro version",
			distroName:    distName,
			distroVersion: "garbage",
			panicExpected: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Save the original values and restore them after the test
			originalDistroName := exe.DistroNameAbbreviation
			originalDistroVersion := exe.DistroMajorVersion
			t.Cleanup(func() {
				exe.DistroNameAbbreviation = originalDistroName
				exe.DistroMajorVersion = originalDistroVersion
			})

			exe.DistroMajorVersion = tt.distroVersion
			exe.DistroNameAbbreviation = tt.distroName
			var (
				ldDistroName    string
				ldDistroVersion int
			)
			if tt.panicExpected {
				assert.Panics(t, func() {
					ldDistroName, ldDistroVersion = loadLdDistroFlags()
				})
			} else {
				assert.NotPanics(t, func() {
					ldDistroName, ldDistroVersion = loadLdDistroFlags()
				})
				assert.Equal(t, tt.distroName, ldDistroName)
				assert.Equal(t, tt.distroVersion, fmt.Sprint(ldDistroVersion))
			}
		})
	}
}

func TestDisableDocumentationDefines(t *testing.T) {
	expectedDefines := map[string]string{
		"_excludedocs": "1",
	}
	result := DisableDocumentationDefines()
	assert.Equal(t, expectedDefines, result)
}

func TestOverrideLocaleDefines(t *testing.T) {
	expectedDefines := map[string]string{
		"_install_langs": "ab:cd:ef",
	}
	result := OverrideLocaleDefines("ab:cd:ef")
	assert.Equal(t, expectedDefines, result)
}

func TestGetMacroDir(t *testing.T) {
	const expectedMacroDir = "/usr/lib/rpm/macros.d"
	macroDir, err := getMacroDirWithFallback(true)
	assert.NoError(t, err)
	assert.Equal(t, expectedMacroDir, macroDir)
}

func TestGetMacroDirWithRpmAvailable(t *testing.T) {
	const expectedMacroDir = "/usr/lib/rpm/macros.d"

	rpmFound, execErr := file.CommandExists(rpmProgram)
	if execErr != nil {
		t.Fatalf("failed to check if rpm is available: %v", execErr)
	}
	if !rpmFound {
		t.Skip("rpm is not available")
	}

	macroDir, err := GetMacroDir()
	assert.NoError(t, err)
	assert.Equal(t, expectedMacroDir, macroDir)
}

func TestConflictingPackageRegex(t *testing.T) {
	tests := []struct {
		name           string
		inputLine      string
		expectedMatch  bool
		expectedOutput string
	}{
		{
			name:           "perl with epoch",
			inputLine:      "D: ========== +++ perl-4:5.34.1-489.cm2 x86_64-linux 0x0",
			expectedMatch:  true,
			expectedOutput: "perl-4:5.34.1-489.cm2.x86_64",
		},
		{
			name:           "systemd no epoch",
			inputLine:      "D: ========== +++ systemd-devel-239-42.cm2 x86_64-linux 0x0",
			expectedMatch:  true,
			expectedOutput: "systemd-devel-239-42.cm2.x86_64",
		},
		{
			name:           "non-matching line",
			inputLine:      "D: ========== tsorting packages (order, #predecessors, #succesors, depth)",
			expectedMatch:  false,
			expectedOutput: "",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			match, actualOut := extractCompetingPackageInfoFromLine(tt.inputLine)
			assert.Equal(t, tt.expectedMatch, match)
			assert.Equal(t, tt.expectedOutput, actualOut)
		})
	}
}

func TestPackageFQNRegexWithValidInput(t *testing.T) {
	tests := []struct {
		name           string
		input          string
		expectedGroups []string
	}{
		{
			name:           "package with epoch and architecture",
			input:          "pkg-name-0:1.2.3-4.azl3.x86_64.rpm",
			expectedGroups: []string{"pkg-name", "0", "1.2.3", "4.azl3", "x86_64", "rpm"},
		},
		{
			name:           "package with epoch and architecture but no '.rpm' suffix",
			input:          "pkg-name-0:1.2.3-4.azl3.x86_64",
			expectedGroups: []string{"pkg-name", "0", "1.2.3", "4.azl3", "x86_64", ""},
		},
		{
			name:           "package without epoch, and architecture",
			input:          "pkg-name-1.2.3-4.azl3.rpm",
			expectedGroups: []string{"pkg-name", "", "1.2.3", "4.azl3", "", "rpm"},
		},
		{
			name:           "package with architecture but no epoch",
			input:          "pkg-name-1.2.3-4.azl3.aarch64",
			expectedGroups: []string{"pkg-name", "", "1.2.3", "4.azl3", "aarch64", ""},
		},
		{
			name:           "package with epoch but no architecture",
			input:          "pkg-name-0:1.2.3-4.azl3",
			expectedGroups: []string{"pkg-name", "0", "1.2.3", "4.azl3", "", ""},
		},
		{
			name:           "package without '.rpm' suffix",
			input:          "pkg-name-1.2.3-4.azl3.x86_64",
			expectedGroups: []string{"pkg-name", "", "1.2.3", "4.azl3", "x86_64", ""},
		},
		{
			name:           "package with version containing the '+' character",
			input:          "pkg-name-1.2.3+4-4.azl3.x86_64.rpm",
			expectedGroups: []string{"pkg-name", "", "1.2.3+4", "4.azl3", "x86_64", "rpm"},
		},
		{
			name:           "package with version containing the '~' character",
			input:          "pkg-name-1.2.3~4-4.azl3.x86_64.rpm",
			expectedGroups: []string{"pkg-name", "", "1.2.3~4", "4.azl3", "x86_64", "rpm"},
		},
		{
			name:           "package with release containing two '.' characters",
			input:          "pkg-name-1.2.3-4.5.azl3.x86_64.rpm",
			expectedGroups: []string{"pkg-name", "", "1.2.3", "4.5.azl3", "x86_64", "rpm"},
		},
		{
			name:           "package with release containing the '_' character",
			input:          "pkg-name-1.2.3-45.az_l3.x86_64.rpm",
			expectedGroups: []string{"pkg-name", "", "1.2.3", "45.az_l3", "x86_64", "rpm"},
		},
		{
			name:           "package with release containing the `~` character",
			input:          "pkg-name-1.2.3-45.azl3~2.x86_64.rpm",
			expectedGroups: []string{"pkg-name", "", "1.2.3", "45.azl3~2", "x86_64", "rpm"},
		},
		{
			name:           "package with double dash in name",
			input:          "nvidia-container-toolkit-1.15.0-1.azl3.x86_64.rpm",
			expectedGroups: []string{"nvidia-container-toolkit", "", "1.15.0", "1.azl3", "x86_64", "rpm"},
		},
		{
			name:           "package with underscore in release",
			input:          "nvidia-container-toolkit-550.54.15-2_5.15.162.2.1.azl3.x86_64.rpm",
			expectedGroups: []string{"nvidia-container-toolkit", "", "550.54.15", "2_5.15.162.2.1.azl3", "x86_64", "rpm"},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			matches := packageFQNRegex.FindStringSubmatch(tt.input)
			assert.NotNil(t, matches)
			assert.Equal(t, tt.expectedGroups, matches[1:])
		})
	}
}

func TestPackageFQNRegexWithInvalidInput(t *testing.T) {
	tests := []struct {
		name  string
		input string
	}{
		{
			name:  "package with missing version",
			input: "pkg-name--4.azl3.x86_64.rpm",
		},
		{
			name:  "package with missing release",
			input: "pkg-name-1.2.3-.azl3.x86_64.rpm",
		},
		{
			name:  "package with missing name",
			input: "-1.2.3-4.azl3.x86_64.rpm",
		},
		{
			name:  "package with only hyphen",
			input: "-",
		},
		{
			name:  "package with version not beginning with a digit",
			input: "pkg-name-0:a1.2.3-4.azl3.x86_64.rpm",
		},
		{
			name:  "package with release not beginning with a digit",
			input: "pkg-name-0:1.2.3-D4.azl3.x86_64.rpm",
		},
		{
			name:  "package with epoch not beginning with a digit",
			input: "pkg-name-0:1.2.3-D4.azl3.x86_64.rpm",
		},
		{
			name:  "package with epoch unsupported architecture",
			input: "pkg-name-0:1.2.3-D4.azl3.other_arch.rpm",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			matches := packageFQNRegex.FindStringSubmatch(tt.input)
			assert.Nil(t, matches)
		})
	}
}

func TestStripEpochFromPackageFullQualifiedNameWithValidInput(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{
			name:     "package with epoch and architecture",
			input:    "pkg-name-0:1.2.3-4.azl3.x86_64.rpm",
			expected: "pkg-name-1.2.3-4.azl3.x86_64.rpm",
		},
		{
			name:     "package with epoch and architecture but no '.rpm' suffix",
			input:    "pkg-name-0:1.2.3-4.azl3.x86_64",
			expected: "pkg-name-1.2.3-4.azl3.x86_64",
		},
		{
			name:     "package with epoch but no architecture",
			input:    "pkg-name-0:1.2.3-4.azl3",
			expected: "pkg-name-1.2.3-4.azl3",
		},
		{
			name:     "package with architecture but no epoch",
			input:    "pkg-name-1.2.3-4.azl3.aarch64",
			expected: "pkg-name-1.2.3-4.azl3.aarch64",
		},
		{
			name:     "package without epoch, and architecture",
			input:    "pkg-name-1.2.3-4.azl3.rpm",
			expected: "pkg-name-1.2.3-4.azl3.rpm",
		},
		{
			name:     "package with version containing the '+' character",
			input:    "pkg-name-1.2.3+4-4.azl3.x86_64.rpm",
			expected: "pkg-name-1.2.3+4-4.azl3.x86_64.rpm",
		},
		{
			name:     "package with version containing the '~' character",
			input:    "pkg-name-1.2.3~4-4.azl3.x86_64.rpm",
			expected: "pkg-name-1.2.3~4-4.azl3.x86_64.rpm",
		},
		{
			name:     "package with release containing two '.' characters",
			input:    "pkg-name-1.2.3-4.5.azl3.x86_64.rpm",
			expected: "pkg-name-1.2.3-4.5.azl3.x86_64.rpm",
		},
		{
			name:     "package with release containing the '_' character",
			input:    "pkg-name-1.2.3-4_5.azl3.x86_64.rpm",
			expected: "pkg-name-1.2.3-4_5.azl3.x86_64.rpm",
		},
		{
			name:     "package with release containing the `~` character",
			input:    "pkg-name-1.2.3-4~5.azl3.x86_64.rpm",
			expected: "pkg-name-1.2.3-4~5.azl3.x86_64.rpm",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			actual := StripEpochFromPackageFullQualifiedName(tt.input)
			assert.Equal(t, tt.expected, actual)
		})
	}
}

func TestStripEpochFromPackageFullQualifiedNameWithInvalidInput(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{
			name:     "invalid package name",
			input:    "invalid-package-name",
			expected: "invalid-package-name",
		},
		{
			name:     "empty package name",
			input:    "",
			expected: "",
		},
		{
			name:     "package name with only hyphens",
			input:    "----",
			expected: "----",
		},
		{
			name:     "package name with spaces",
			input:    "pkg name-1.2.3-4.azl3.x86_64.rpm",
			expected: "pkg name-1.2.3-4.azl3.x86_64.rpm",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			actual := StripEpochFromPackageFullQualifiedName(tt.input)
			assert.Equal(t, tt.expected, actual)
		})
	}
}
