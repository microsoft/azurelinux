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
