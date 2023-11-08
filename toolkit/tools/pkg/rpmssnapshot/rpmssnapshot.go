// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A tool for generating snapshots of built RPMs from local specs.

package rpmssnapshot

import (
	"fmt"
	"path/filepath"
	"regexp"
	"runtime"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repocloner"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/rpm"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/simpletoolchroot"
)

const (
	chrootOutputFilePath = "/snapshot.json"
)

// Regular expression to extract package name, version, distribution, and architecture from values returned by 'rpmspec --builtrpms'.
// Examples:
//
//	kernel-5.15.63.1-1.cm2.x86_64		->	Name: kernel, Version: 5.15.63.1-1, Distribution: cm2, Architecture: x86_64
//	python3-perf-5.15.63.1-1.cm2.x86_64	->	Name: python3-perf, Version: 5.15.63.1-1, Distribution: cm2, Architecture: x86_64
//
// NOTE: regular expression based on following assumptions:
//   - Package version and release values are not allowed to contain a hyphen character.
//   - Our tooling prevents the 'Release' tag from having any other form than '[[:digit:]]+%{?dist}'
//   - The distribution tag is not allowed to contain a period or a hyphen.
//   - The architecture is not allowed to contain a period or a hyphen.
//
// Regex breakdown:
//
//	^(.*)			<-- [index 1] package name
//	-				<-- second-to-last hyphen separating the package name from its version
//	([^-]+-[^-]+)		<-- [index 2] package version and package release number connected by the last hyphen
//	\.				<-- second-to-last period separating the package release number from the distribution tag
//	([^.]+)			<-- [index 3] the distribution tag
//	\.				<-- last period separating the distribution tag from the architecture string
//	([^.]+)$		<-- [index 4] the architecture string
var rpmSpecBuiltRPMRegex = regexp.MustCompile(`^(.*)-([^-]+-[^-]+)\.([^.]+)\.([^.]+)$`)

const (
	rpmSpecBuiltRPMRegexNameIndex = iota + 1
	rpmSpecBuiltRPMRegexVersionIndex
	rpmSpecBuiltRPMRegexDistributionIndex
	rpmSpecBuiltRPMRegexArchitectureIndex
	rpmSpecBuiltRPMRegexMatchesCount
)

type SnapshotGenerator struct {
	simpleToolChroot simpletoolchroot.SimpleToolChroot
}

// New creates a new snapshot generator. If the chroot is created successfully, the caller is responsible for calling CleanUp().
func New(buildDirPath, workerTarPath, specsDirPath string) (newSnapshotGenerator *SnapshotGenerator, err error) {
	const chrootName = "rpmssnapshot_chroot"
	newSnapshotGenerator = &SnapshotGenerator{}
	err = newSnapshotGenerator.simpleToolChroot.InitializeChroot(buildDirPath, chrootName, workerTarPath, specsDirPath)

	return newSnapshotGenerator, err
}

// CleanUp tears down the chroot
func (s *SnapshotGenerator) CleanUp() error {
	return s.simpleToolChroot.CleanUp()
}

// GenerateSnapshot generates a snapshot of all packages built from the specs inside the input directory.
func (s *SnapshotGenerator) GenerateSnapshot(outputFilePath, distTag string) (err error) {
	err = s.simpleToolChroot.RunInChroot(func() error {
		return s.generateSnapshotInChroot(distTag)
	})
	if err != nil {
		return
	}

	chrootOutputFileFullPath := filepath.Join(s.simpleToolChroot.ChrootRootDir(), chrootOutputFilePath)
	err = file.Move(chrootOutputFileFullPath, outputFilePath)
	if err != nil {
		logger.Log.Errorf("Failed to retrieve the snapshot from the chroot. Error: %v.", err)
	}

	return
}

func (s *SnapshotGenerator) convertResultsToRepoContents(allBuiltRPMs []string) (repoContents repocloner.RepoContents, err error) {
	repoContents = repocloner.RepoContents{
		Repo: []*repocloner.RepoPackage{},
	}

	for _, builtRPM := range allBuiltRPMs {
		matches := rpmSpecBuiltRPMRegex.FindStringSubmatch(builtRPM)
		if len(matches) != rpmSpecBuiltRPMRegexMatchesCount {
			return repoContents, fmt.Errorf("RPM package name (%s) doesn't match the regular expression (%s)", builtRPM, rpmSpecBuiltRPMRegex.String())
		}

		repoContents.Repo = append(repoContents.Repo, &repocloner.RepoPackage{
			Name:         matches[rpmSpecBuiltRPMRegexNameIndex],
			Version:      matches[rpmSpecBuiltRPMRegexVersionIndex],
			Distribution: matches[rpmSpecBuiltRPMRegexDistributionIndex],
			Architecture: matches[rpmSpecBuiltRPMRegexArchitectureIndex],
		})
	}

	return
}

func (s *SnapshotGenerator) generateSnapshotInChroot(distTag string) (err error) {
	const runChecks = false
	var (
		allBuiltRPMs []string
		repoContents repocloner.RepoContents
		specPaths    []string
	)

	defines := rpm.DefaultDefinesWithDist(runChecks, distTag)
	specPaths, err = rpm.BuildCompatibleSpecsList(s.simpleToolChroot.ChrootRelativeSpecDir(), []string{}, defines)
	if err != nil {
		logger.Log.Errorf("Failed to retrieve a list of specs inside (%s). Error: %v.", s.simpleToolChroot.ChrootRelativeSpecDir(), err)
		return
	}

	logger.Log.Infof("Found %d compatible specs.", len(specPaths))

	allBuiltRPMs, err = s.readBuiltRPMs(specPaths, defines)
	if err != nil {
		logger.Log.Errorf("Failed to extract built RPMs from specs. Error: %v.", err)
		return
	}

	logger.Log.Infof("The specs build %d packages in total.", len(allBuiltRPMs))

	repoContents, err = s.convertResultsToRepoContents(allBuiltRPMs)
	if err != nil {
		logger.Log.Errorf("Failed to convert RPMs list to a packages summary file. Error: %v.", err)
		return
	}

	err = jsonutils.WriteJSONFile(chrootOutputFilePath, repoContents)
	if err != nil {
		logger.Log.Errorf("Failed to save results into (%s). Error: %v.", chrootOutputFilePath, err)
	}

	return
}

func (s *SnapshotGenerator) readBuiltRPMs(specPaths []string, defines map[string]string) (allBuiltRPMs []string, err error) {
	buildArch, err := rpm.GetRpmArch(runtime.GOARCH)
	if err != nil {
		return
	}

	type SnapshotResult struct {
		rpms []string
		err  error
	}
	resultsChannel := make(chan SnapshotResult, len(specPaths))

	for _, specPath := range specPaths {
		logger.Log.Debugf("Parsing spec (%s).", specPath)

		specDirPath := filepath.Dir(specPath)

		go func(pathIter string) {
			builtRPMs, err := rpm.QuerySPECForBuiltRPMs(pathIter, specDirPath, buildArch, defines)
			if err != nil {
				err = fmt.Errorf("failed to query built RPMs from (%s):\n%w", pathIter, err)
			}

			resultsChannel <- SnapshotResult{
				rpms: builtRPMs,
				err:  err,
			}
		}(specPath)
	}

	for i := 0; i < len(specPaths); i++ {
		result := <-resultsChannel
		if result.err != nil {
			err = result.err
			return
		}
		allBuiltRPMs = append(allBuiltRPMs, result.rpms...)
	}

	return
}
