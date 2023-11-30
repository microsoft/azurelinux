// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package rpm

import (
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/stretchr/testify/assert"
)

const (
	definesDistKey      = "dist"
	definesWithCheckKey = "with_check"
	specsDir            = "testdata"
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
			err:      fmt.Errorf("invalid RPM file path '%s', can't extract name", "/path/to/garbage.rpm"),
		},
		{
			name:     "empty rpm file",
			rpmFile:  "",
			expected: "",
			err:      fmt.Errorf("invalid RPM file path '%s', can't extract name", ""),
		},
		{
			name:     "just a hyphen",
			rpmFile:  "-",
			expected: "",
			err:      fmt.Errorf("invalid RPM file path '%s', can't extract name", "-"),
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
func TestExtractArchFromRPMPath(t *testing.T) {
	tests := []struct {
		name          string
		rpmFilePath   string
		expectedArch  string
		expectedError error
	}{
		{
			name:          "valid RPM file path",
			rpmFilePath:   "/path/to/pkg-1.0.0-1.x86_64.rpm",
			expectedArch:  "x86_64",
			expectedError: nil,
		},
		{
			name:          "valid RPM file path with complex name",
			rpmFilePath:   "/path/to/pkg-name-1.0.0-1.aarch64.rpm",
			expectedArch:  "aarch64",
			expectedError: nil,
		},
		{
			name:          "invalid RPM file path",
			rpmFilePath:   "/path/to/garbage.rpm",
			expectedArch:  "",
			expectedError: fmt.Errorf("invalid RPM file path '/path/to/garbage.rpm', can't extract arch"),
		},
		{
			name:          "empty RPM file path",
			rpmFilePath:   "",
			expectedArch:  "",
			expectedError: fmt.Errorf("invalid RPM file path '', can't extract arch"),
		},
		{
			name:          "RPM file path without arch",
			rpmFilePath:   "/path/to/pkg-foo-bar..rpm",
			expectedArch:  "",
			expectedError: fmt.Errorf("invalid RPM file path '/path/to/pkg-foo-bar..rpm', can't extract arch"),
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			actualArch, actualError := ExtractArchFromRPMPath(tt.rpmFilePath)
			assert.Equal(t, tt.expectedArch, actualArch)
			assert.Equal(t, tt.expectedError, actualError)
		})
	}
}

// func TestExistingSpecsJsonInput(t *testing.T) {
// 	specsJsonPath := filepath.Join(specsDir, "specs.json")

// 	localPackages := pkgjson.PackageRepo{}
// 	err := localPackages.ParsePackageJSON(specsJsonPath)
// 	assert.NoError(t, err)

// 	for _, pkg := range localPackages.Repo {
// 		rpmPath := pkg.RpmPath
// 		arch := pkg.Architecture

// 		actualArch, actualError := ExtractArchFromRPMPath(rpmPath)
// 		assert.Equal(t, arch, actualArch)
// 		assert.Equal(t, nil, actualError)
// 	}
// }
