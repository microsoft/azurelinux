// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package tdnf

import (
	"os"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	os.Exit(m.Run())
}

func TestGetMajorVersionFromString_AcceptEmptyMinorVersion(t *testing.T) {
	fullVersion := "2.0"
	expectedMajorVersion := "2.0"
	majorVersion, err := getMajorVersionFromString(fullVersion)

	assert.NoError(t, err)
	assert.Equal(t, expectedMajorVersion, majorVersion)
}

func TestGetMajorVersionFromString_AcceptPopulatedMinorVersionTimestamp(t *testing.T) {
	fullVersion := "2.0.20220519.1844"
	expectedMajorVersion := "2.0"
	majorVersion, err := getMajorVersionFromString(fullVersion)

	assert.NoError(t, err)
	assert.Equal(t, expectedMajorVersion, majorVersion)
}

func TestGetMajorVersionFromString_AcceptAlphabeticalMinorVersion(t *testing.T) {
	fullVersion := "2.0.reallycoolteststring"
	expectedMajorVersion := "2.0"
	majorVersion, err := getMajorVersionFromString(fullVersion)

	assert.NoError(t, err)
	assert.Equal(t, expectedMajorVersion, majorVersion)
}

func TestGetMajorVersionFromString_RejectAlphabeticalInMajor(t *testing.T) {
	fullVersion := "2.A"
	_, err := getMajorVersionFromString(fullVersion)
	assert.Error(t, err)
}

func TestGetMajorVersionFromString_RejectEmpty(t *testing.T) {
	fullVersion := ""
	_, err := getMajorVersionFromString(fullVersion)
	assert.Error(t, err)
}

func TestGetMajorVersionFromString_RejectWithNoDot(t *testing.T) {
	fullVersion := "2"
	_, err := getMajorVersionFromString(fullVersion)
	assert.Error(t, err)
}

func TestGetMajorVersionFromString_RejectNoSecondComponentWithDot(t *testing.T) {
	fullVersion := "2."
	_, err := getMajorVersionFromString(fullVersion)
	assert.Error(t, err)
}

func TestGetMajorVersionFromString_RejectTrailingDot(t *testing.T) {
	fullVersion := "2.0."
	_, err := getMajorVersionFromString(fullVersion)
	assert.Error(t, err)
}

func TestInstallPackageRegex_MatchesPackageName(t *testing.T) {
	const line = "X aarch64 1.1b.8_X-22~rc1.azl3 fetcher-cloned-repo"

	matches := InstallPackageRegex.FindStringSubmatch(line)

	assert.Len(t, matches, InstallPackageMaxMatchLen)
	assert.Equal(t, "X", matches[InstallPackageName])
}

func TestInstallPackageRegex_FailsForMissingPackageName(t *testing.T) {
	const line = " aarch64 1.1b.8_X-22~rc1.azl3 fetcher-cloned-repo"

	assert.False(t, InstallPackageRegex.MatchString(line))
}

func TestInstallPackageRegex_MatchesPackageArch(t *testing.T) {
	const line = "X aarch64 1.1b.8_X-22~rc1.azl3 fetcher-cloned-repo"

	matches := InstallPackageRegex.FindStringSubmatch(line)

	assert.Len(t, matches, InstallPackageMaxMatchLen)
	assert.Equal(t, "aarch64", matches[InstallPackageArch])
}

func TestInstallPackageRegex_FailsForMissingArch(t *testing.T) {
	const line = "X  1.1b.8_X-22~rc1.azl3 fetcher-cloned-repo"

	assert.False(t, InstallPackageRegex.MatchString(line))
}

func TestInstallPackageRegex_MatchesPackageVersionNoEpoch(t *testing.T) {
	const line = "X aarch64 1.1b.8_X-22~rc1.azl3 fetcher-cloned-repo"

	matches := InstallPackageRegex.FindStringSubmatch(line)

	assert.Len(t, matches, InstallPackageMaxMatchLen)
	assert.Equal(t, "1.1b.8_X-22~rc1", matches[InstallPackageVersion])
}

func TestInstallPackageRegex_MatchesPackageVersionWithEpoch(t *testing.T) {
	const line = "X aarch64 5:1.1b.8_X-22~rc1.azl3 fetcher-cloned-repo"

	matches := InstallPackageRegex.FindStringSubmatch(line)

	assert.Len(t, matches, InstallPackageMaxMatchLen)
	assert.Equal(t, "5:1.1b.8_X-22~rc1", matches[InstallPackageVersion])
}

func TestInstallPackageRegex_FailsForMissingVersion(t *testing.T) {
	const line = "X aarch64 .azl3 fetcher-cloned-repo"

	assert.False(t, InstallPackageRegex.MatchString(line))
}

func TestInstallPackageRegex_MatchesPackageDist(t *testing.T) {
	const line = "X aarch64 1.1b.8_X-22~rc1.azl3 fetcher-cloned-repo"

	matches := InstallPackageRegex.FindStringSubmatch(line)

	assert.Len(t, matches, InstallPackageMaxMatchLen)
	assert.Equal(t, "azl3", matches[InstallPackageDist])
}

func TestInstallPackageRegex_FailsForMissingDist(t *testing.T) {
	const line = "X aarch64 1.1b.8_X-22~rc1 fetcher-cloned-repo"

	assert.False(t, InstallPackageRegex.MatchString(line))
}

func TestInstallPackageRegex_MatchesRandomWhiteSpaces(t *testing.T) {
	const line = "X   aarch64  1.1b.8_X-22~rc1.azl3          	fetcher-cloned-repo"

	assert.True(t, InstallPackageRegex.MatchString(line))
}

func TestInstallPackageRegex_DoesNotMatchInvalidLine(t *testing.T) {
	const line = "Invalid line"

	assert.False(t, InstallPackageRegex.MatchString(line))
}
func TestPackageLookupNameMatchRegex_MatchesExternalRepo(t *testing.T) {
	const line = "xz-devel-5.4.4-1.azl3.x86_64 : Header and development files for xz\nRepo : toolchain-repo"

	matches := PackageProvidesRegex.FindStringSubmatch(line)

	assert.Len(t, matches, PackageProvidesMaxMatchLen)
	assert.Equal(t, "xz-devel-5.4.4-1.azl3.x86_64", matches[PackageProvidesNameIndex])
}

func TestPackageLookupNameMatchRegex_MatchesPackageWithEpoch(t *testing.T) {
	const line = "xz-devel-2:5.4.4-1.azl3.x86_64 : Header and development files for xz\nRepo : toolchain-repo"

	matches := PackageProvidesRegex.FindStringSubmatch(line)

	assert.Len(t, matches, PackageProvidesMaxMatchLen)
	assert.Equal(t, "xz-devel-2:5.4.4-1.azl3.x86_64", matches[PackageProvidesNameIndex])
}

func TestPackageLookupNameMatchRegex_FailsForOutputWithoutRepo(t *testing.T) {
	const line = "xz-devel-5.4.4-1.azl3.x86_64 : Header and development files for xz"

	assert.False(t, PackageProvidesRegex.MatchString(line))
}

func TestPackageLookupNameMatchRegex_FailsForOutputWithSystemRepo(t *testing.T) {
	const line = "xz-devel-5.4.4-1.azl3.x86_64 : Header and development files for xz\nRepo : @System"

	assert.False(t, PackageProvidesRegex.MatchString(line))
}

func TestPackageLookupNameMatchRegex_FailsForEmptyOutput(t *testing.T) {
	const line = ""

	assert.False(t, PackageProvidesRegex.MatchString(line))
}

func TestPackageLookupNameMatchRegex_FailsForInvalidOutput(t *testing.T) {
	const line = "Invalid output line"

	assert.False(t, PackageProvidesRegex.MatchString(line))
}

func TestPackageLookupNameMatchRegex_MatchesOutputWithCapabilityMatch(t *testing.T) {
	const line = "[using capability match for 'pkgconfig(liblzma)'] xz-devel-5.4.4-1.azl3.x86_64 : Header and development files for xz\nRepo : toolchain-repo"

	matches := PackageProvidesRegex.FindStringSubmatch(line)

	assert.Len(t, matches, PackageProvidesMaxMatchLen)
	assert.Equal(t, "xz-devel-5.4.4-1.azl3.x86_64", matches[PackageProvidesNameIndex])
}

func TestPackageLookupNameMatchRegex_MatchesOutputWithMultiplePackages(t *testing.T) {
	const line = "xz-devel-5.4.4-1.azl3.x86_64 : ABC\nRepo : toolchain-repo\nother-package-4.4.4-1.azl3.x86_64 : ABC2\nRepo : other-repo\n"

	allMatches := PackageProvidesRegex.FindAllStringSubmatch(line, -1)

	assert.Len(t, allMatches, 2)
	assert.Len(t, allMatches[0], PackageProvidesMaxMatchLen)
	assert.Equal(t, "xz-devel-5.4.4-1.azl3.x86_64", allMatches[0][PackageProvidesNameIndex])

	assert.Len(t, allMatches[1], PackageProvidesMaxMatchLen)
	assert.Equal(t, "other-package-4.4.4-1.azl3.x86_64", allMatches[1][PackageProvidesNameIndex])
}

func TestPackageLookupNameMatchRegex_MatchesOutputWithExternalAndSystemMix(t *testing.T) {
	const line = "xz-devel-5.4.4-1.azl3.x86_64 : ABC\nRepo : toolchain-repo\nother-package-4.4.4-1.azl3.x86_64 : ABC2\nRepo : @System\n"

	allMatches := PackageProvidesRegex.FindAllStringSubmatch(line, -1)

	assert.Len(t, allMatches, 1)
	assert.Len(t, allMatches[0], PackageProvidesMaxMatchLen)
	assert.Equal(t, "xz-devel-5.4.4-1.azl3.x86_64", allMatches[0][PackageProvidesNameIndex])
}

func TestPackageLookupNameMatchRegex_MatchesOutputWithSystemFirstExternalSecond(t *testing.T) {
	const line = "other-package-4.4.4-1.azl3.x86_64 : ABC2\nRepo : @System\nxz-devel-5.4.4-1.azl3.x86_64 : ABC\nRepo : toolchain-repo"

	allMatches := PackageProvidesRegex.FindAllStringSubmatch(line, -1)

	assert.Len(t, allMatches, 1)
	assert.Len(t, allMatches[0], PackageProvidesMaxMatchLen)
	assert.Equal(t, "xz-devel-5.4.4-1.azl3.x86_64", allMatches[0][PackageProvidesNameIndex])
}

func TestPackageLookupNameMatchRegex_FailsForOutputWithOnlyPluginLoaded(t *testing.T) {
	const line = "Loaded plugin: tdnfrepogpgcheck"

	assert.False(t, PackageProvidesRegex.MatchString(line))
}
