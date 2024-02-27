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

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
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

func TestDistroDefines(t *testing.T) {
	distName := "myDistro"
	distVersion := "1234"
	distTag := fmt.Sprintf(".%s%s", distName, distVersion)

	// Save the original values and restore them after the test
	originalDistroName := distNameAbreviation
	originalDistroVersion := distMajorVersion
	t.Cleanup(func() {
		distNameAbreviation = originalDistroName
		distMajorVersion = originalDistroVersion
	})

	SetDistroMacros(distName, distVersion)

	defines, err := DefaultDistroDefines(true, distTag)
	assert.NoError(t, err)

	assert.Equal(t, "1", defines[definesWithCheckKey])
	assert.Equal(t, distTag, defines[DistTagDefine])

	defines, err = DefaultDistroDefines(false, distTag)
	assert.NoError(t, err)
	assert.Equal(t, "0", defines[definesWithCheckKey])

	// Check for distro name and version
	assert.Equal(t, distTag, defines["dist"])
	assert.Equal(t, fmt.Sprint(distVersion), defines[distName])

	// Check that an empty distro tag is ok
	defines, err = DefaultDistroDefines(false, "")
	assert.NoError(t, err)
	assert.Equal(t, "", defines["dist"])
	assert.Equal(t, fmt.Sprint(distVersion), defines[distName])

	// Handle errors when distro name and version are not set
	SetDistroMacros("", distVersion)
	defines, err = DefaultDistroDefines(false, distTag)
	assert.Error(t, err)
	assert.Nil(t, defines)

	SetDistroMacros("", distVersion)
	defines, err = DefaultDistroDefines(false, distTag)
	assert.Error(t, err)
	assert.Nil(t, defines)

	// Handle errors when version is negative
	SetDistroMacros(distName, "-1")

	defines, err = DefaultDistroDefines(false, distTag)
	assert.Error(t, err)
	assert.Nil(t, defines)
}

func TestDefaultDefines(t *testing.T) {
	if exe.DistroMajorVersion == "" && exe.DistroNameAbreviation == "" {
		t.Skip("Skipping test because distro name and version are not set")
	}
	distTag := "testDistroTag"
	defines, err := DefaultDistroDefines(true, distTag)
	assert.NoError(t, err)
	assert.Equal(t, "3", defines["azl"])
}
