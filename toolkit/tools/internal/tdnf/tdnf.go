// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Package tdnf provides utility functions for interfacing with the TDNF package manager.
package tdnf

import (
	"fmt"
	"regexp"
	"strconv"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/exe"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

var (
	// Every valid line will be of the form: <package_name> <architecture> <version>.<dist> <repo_id>
	// For:
	//     X aarch64	5:1.1b.8_X-22~rc1.azl3		fetcher-cloned-repo
	//
	// We'd get:
	//   - package_name:    X
	//   - architecture:    aarch64
	//   - version:         5:1.1b.8_X-22~rc1
	//   - dist:            azl3
	InstallPackageRegex = regexp.MustCompile(`^\s*([[:alnum:]_.+-]+)\s+([[:alnum:]_+-]+)\s+((?:[[:digit:]]:)?[[:alnum:]._+~-]+)\.([[:alpha:]]+[[:digit:]]+)`)

	// Every valid line pair will be of the form:
	//		<package>-<version>.<arch> : <Description>
	//		Repo	: [repo_name]
	//
	// NOTE: we ignore packages installed in the build environment denoted by "Repo	: @System".
	PackageProvidesRegex = regexp.MustCompile(`(\S+)\s+:[^\n]*\nRepo\s+:\s+[^@]`)

	// Tdnf may opt to ignore case when doing a provides lookup. While this is useful for a user, it will give
	// bad results when we're trying to match a package name to a package in the repo. This regex will match the
	// message that indicates that case-insensitive matching is enabled.
	DidCaseInsensitiveMatchRegex = regexp.MustCompile(`\[ignoring case for '.*'\]`)

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
	InstallPackageMatchSubString = iota
	InstallPackageName           = iota
	InstallPackageArch           = iota
	InstallPackageVersion        = iota
	InstallPackageDist           = iota
	InstallPackageMaxMatchLen    = iota
)

const (
	PackageProvidesMatchSubString = iota
	PackageProvidesNameIndex      = iota
	PackageProvidesMaxMatchLen    = iota
)

const (
	ListedPackageMatchSubString = iota
	ListedPackageName           = iota
	ListedPackageArch           = iota
	ListedPackageVersion        = iota
	ListedPackageDist           = iota
	ListedPackageMaxMatchLen    = iota
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
	// of Azure Linux and its repositories.
	//
	// Examples: "1.0", "2.0", "3.0"
	majorVersionRegex = regexp.MustCompile(`^(\d+\.\d+)(\..+)?$`)

	// Cache the populated releasever argument
	// so we don't have to run the same regex/string formatting thousands of times
	releaseverArgumentPopulatedCache = ""
)

// GetReleaseverCliArg returns a TDNF CLI argument suitable for resolving the `$releasever` variable in
// Azure Linux's RPM repo files to the major version of the toolkit. This argument allows TDNF to resolve
// without the presence of the `azurelinux-release` package.
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
		err = fmt.Errorf("failed to get Azure Linux major version- toolkit version not set in exe package at link-time")
		return
	}
	arg, err = getMajorVersionFromString(exe.ToolkitVersion)
	return
}

// getMajorVersionFromString returns the major version of a given string.
// Specifically, we look for the first submatch in the input string using `majorVersionRegex`.
func getMajorVersionFromString(version string) (majorVersion string, err error) {
	const (
		errorFormatString = "failed to extract major Azure Linux version from the following string: %s"
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

func GetRepoSnapshotCliArg(posixTime string) (repoSnapshot string, err error) {
	const (
		errorFormatString = "cannot generate snapshot cli arg for: %s"
	)
	if posixTime == "" {
		err = fmt.Errorf(errorFormatString, posixTime)
		return "", err
	}

	_, err = strconv.Atoi(posixTime)
	if err != nil {
		err = fmt.Errorf(errorFormatString, posixTime)
		return "", err
	}

	repoSnapshot = fmt.Sprintf("--snapshottime=%s", posixTime)

	return repoSnapshot, nil
}

func GetRepoSnapshotExcludeCliArg(excludeRepos []string) (excludeArg string, err error) {
	if excludeRepos == nil {
		err = fmt.Errorf("exclude repos cannot be empty")
		return "", err
	}

	repos := ""
	for _, repo := range excludeRepos {
		if repo == "" {
			err = fmt.Errorf("exclude repo member cannot be empty")
			return "", err
		}

		if repos == "" {
			repos = repo
		} else {
			repos = fmt.Sprintf("%s,%s", repos, repo)
		}
	}
	excludeArg = fmt.Sprintf("--snapshotexcluderepos=%s", repos)

	return excludeArg, nil
}

func AddSnapshotToConfig(configFilePath, posixTime string) (err error) {
	if configFilePath == "" {
		err = fmt.Errorf("config file path cannot be empty")
		return err
	}

	if posixTime == "" {
		err = fmt.Errorf("posix time cannot be empty")
		return err
	}
	exists, err := file.PathExists(configFilePath)
	if err != nil {
		return err
	}
	if !exists {
		// print warning
		logger.Log.Warnf("config file path does not exist, nothing to append")
		return nil
	}

	// create config entry, and add to config file
	snapshotConfigEntry := fmt.Sprintf("snapshottime=%s\n", posixTime)
	err = file.Append(snapshotConfigEntry, configFilePath)
	if err != nil {
		return err
	}
	return nil
}
