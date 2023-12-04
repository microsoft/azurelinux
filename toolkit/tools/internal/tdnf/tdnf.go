// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Package tdnf provides utility functions for interfacing with the TDNF package manager.
package tdnf

import (
	"fmt"
	"regexp"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
)

var (
	// Every valid line will be of the form: <package_name> <architecture> <version>.<dist> <repo_id>
	// For:
	//     X aarch64	1.1b.8_X-22~rc1.azl3		fetcher-cloned-repo
	//
	// We'd get:
	//   - package_name:    X
	//   - architecture:    aarch64
	//   - version:         1.1b.8_X-22~rc1
	//   - dist:            azl3
	InstallPackageRegex = regexp.MustCompile(`^\s*([[:alnum:]_.+-]+)\s+([[:alnum:]_+-]+)\s+([[:alnum:]._+~-]+)\.([[:alpha:]]+[[:digit:]]+)`)

	// Every valid line pair will be of the form:
	//		<package>-<version>.<arch> : <Description>
	//		Repo	: [repo_name]
	//
	// NOTE: we ignore packages installed in the build environment denoted by "Repo	: @System".
	PackageLookupNameMatchRegex = regexp.MustCompile(`([^:\s]+(x86_64|aarch64|noarch))\s*:[^\n]*\nRepo\s+:\s+[^@]`)
	PackageNameIndex            = 1

	// Every line containing a repo ID will be of the form:
	//		[<repo_name>]
	// For:
	//
	//		[fetcher-cloned-repo]
	//
	// We'd get:
	//   - repo_name:    fetcher-cloned-repo
	//
	// The non-capturing groups are used to ignore the brackets.
	RepoIDRegex = regexp.MustCompile(`(?:\[)([^]]+)(?:\])`)
	RepoIDIndex = 1

	// Every valid line will be of the form: <package_name>.<architecture> <version>.<dist> <repo_id>
	// For:
	//
	//		COOL_package2-extended++.aarch64	1.1b.8_X-22~rc1.azl3		fetcher-cloned-repo
	//
	// We'd get:
	//   - package_name:    COOL_package2-extended++
	//   - architecture:    aarch64
	//   - version:         1.1b.8_X-22~rc1
	//   - dist:            azl3
	ListedPackageRegex = regexp.MustCompile(`^\s*([[:alnum:]_.+-]+)\.([[:alnum:]_+-]+)\s+([[:alnum:]._+~-]+)\.([[:alpha:]]+[[:digit:]]+)`)
)

const (
	InstallMatchSubString = iota
	InstallPackageName    = iota
	InstallPackageArch    = iota
	InstallPackageVersion = iota
	InstallPackageDist    = iota
	InstallMaxMatchLen    = iota
)

const (
	ListMatchSubString = iota
	ListPackageName    = iota
	ListPackageArch    = iota
	ListPackageVersion = iota
	ListPackageDist    = iota
	ListMaxMatchLen    = iota
)

const (
	// ReleaseverArgument specifies the release version argument to be used with tdnf
	releaseverArgument = "--releasever"
)

var (
	// We consider the major version to be the first two numbers in the version string
	// separated by a dot.
	//
	// Limiting this to digits only is a normative limitation based on past versioning
	// of Mariner and its repositories.
	//
	// Examples: "1.0", "2.0", "3.0"
	majorVersionRegex = regexp.MustCompile(`^(\d+\.\d+)(\..+)?$`)

	// Cache the populated releasever argument
	// so we don't have to run the same regex/string formatting thousands of times
	releaseverArgumentPopulatedCache = ""
)

// GetReleaseverCliArg returns a TDNF CLI argument suitable for resolving the `$releasever` variable in
// Mariner's RPM repo files to the major version of the toolkit. This argument allows TDNF to resolve
// without the presence of the `mariner-release` package.
func GetReleaseverCliArg() (arg string, err error) {
	if releaseverArgumentPopulatedCache == "" {
		var majorVersion string
		majorVersion, err = getMajorVersionFromToolkitVersion()
		if err != nil {
			return
		}
		arg = fmt.Sprintf("%s=%s", releaseverArgument, majorVersion)
		releaseverArgumentPopulatedCache = arg
	} else {
		arg = releaseverArgumentPopulatedCache
	}
	return

}

// getMajorVersionFromToolkitVersion returns the major version taken from the `exe` package's
// `ToolkitVersion` string.
func getMajorVersionFromToolkitVersion() (arg string, err error) {
	if exe.ToolkitVersion == "" {
		err = fmt.Errorf("failed to get Mariner major version- toolkit version not set in exe package at link-time")
		return
	}
	arg, err = getMajorVersionFromString(exe.ToolkitVersion)
	return
}

// getMajorVersionFromString returns the major version of a given string.
// Specifically, we look for the first submatch in the input string using `majorVersionRegex`.
func getMajorVersionFromString(version string) (majorVersion string, err error) {
	const (
		errorFormatString = "failed to extract major Mariner version from the following string: %s"
	)

	matches := majorVersionRegex.FindStringSubmatch(version)

	if len(matches) < 2 {
		err = fmt.Errorf(errorFormatString, version)
		return
	}

	majorVersion = matches[1]

	if majorVersion == "" {
		err = fmt.Errorf(errorFormatString, version)
		return
	}
	return
}
