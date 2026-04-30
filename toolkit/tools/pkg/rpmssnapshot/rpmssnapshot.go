// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A tool for generating snapshots of built RPMs from local specs.

package rpmssnapshot

import (
	"fmt"
	"path/filepath"
	"runtime"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/packagerepo/repocloner"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/rpm"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/simpletoolchroot"
)

const (
	chrootOutputFilePath = "/snapshot.json"
)

type SnapshotGenerator struct {
	simpleToolChroot simpletoolchroot.SimpleToolChroot
}

// New creates a new snapshot generator. If the chroot is created successfully, the caller is responsible for calling CleanUp().
func New(buildDirPath, workerTarPath, specsDirPath, releaseVersionMacrosFile string) (newSnapshotGenerator *SnapshotGenerator, err error) {
	const chrootName = "rpmssnapshot_chroot"
	newSnapshotGenerator = &SnapshotGenerator{}
	err = newSnapshotGenerator.simpleToolChroot.InitializeChroot(buildDirPath, chrootName, workerTarPath, specsDirPath, releaseVersionMacrosFile)

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
		return fmt.Errorf("failed to retrieve snapshot from chroot:\n%w", err)
	}

	return
}

func (s *SnapshotGenerator) convertResultsToRepoContents(allBuiltRPMs []string) (repoContents repocloner.RepoContents, err error) {
	repoContents = repocloner.RepoContents{
		Repo: []*repocloner.RepoPackage{},
	}

	for _, builtRPM := range allBuiltRPMs {
		matches := rpm.RpmSpecBuiltRPMRegex.FindStringSubmatch(builtRPM)
		if len(matches) != rpm.RpmSpecBuiltRPMRegexMatchesCount {
			return repoContents, fmt.Errorf("RPM package name (%s) doesn't match the regular expression (%s)", builtRPM, rpm.RpmSpecBuiltRPMRegex.String())
		}

		// Reattach a non-zero epoch to the version (`epoch:version-release`) so the resulting
		// 'Version' field keeps the same shape it had before epoch was split out into its own
		// capture group.
		version := fmt.Sprintf("%s-%s", matches[rpm.RpmSpecBuiltRPMRegexVersionIndex], matches[rpm.RpmSpecBuiltRPMRegexReleaseIndex])
		if epoch := matches[rpm.RpmSpecBuiltRPMRegexEpochIndex]; epoch != "" {
			version = fmt.Sprintf("%s:%s", epoch, version)
		}

		repoContents.Repo = append(repoContents.Repo, &repocloner.RepoPackage{
			Name:         matches[rpm.RpmSpecBuiltRPMRegexNameIndex],
			Version:      version,
			Distribution: matches[rpm.RpmSpecBuiltRPMRegexDistributionIndex],
			Architecture: matches[rpm.RpmSpecBuiltRPMRegexArchitectureIndex],
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

	defines := rpm.DefaultDistroDefines(runChecks, distTag)
	specPaths, err = rpm.BuildCompatibleSpecsList(s.simpleToolChroot.ChrootRelativeMountDir(), []string{}, defines)
	if err != nil {
		err = fmt.Errorf("failed to retrieve a list of specs inside (%s):\n%w", s.simpleToolChroot.ChrootRelativeMountDir(), err)
		return
	}

	logger.Log.Infof("Found %d compatible specs.", len(specPaths))

	allBuiltRPMs, err = s.readBuiltRPMs(specPaths, defines)
	if err != nil {
		err = fmt.Errorf("failed to extract built RPMs from specs:\n%w", err)
		return
	}

	logger.Log.Infof("The specs build %d packages in total.", len(allBuiltRPMs))

	repoContents, err = s.convertResultsToRepoContents(allBuiltRPMs)
	if err != nil {
		err = fmt.Errorf("failed to convert RPMs list to a packages summary file:\n%w", err)
		return
	}

	err = jsonutils.WriteJSONFile(chrootOutputFilePath, repoContents)
	if err != nil {
		err = fmt.Errorf("Failed to save results into (%s):\n%w", chrootOutputFilePath, err)
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
			builtRPMs, queryErr := rpm.QuerySPECForBuiltRPMs(pathIter, specDirPath, buildArch, defines)
			if queryErr != nil {
				queryErr = fmt.Errorf("failed to query built RPMs from (%s):\n%w", pathIter, queryErr)
			}

			resultsChannel <- SnapshotResult{
				rpms: builtRPMs,
				err:  queryErr,
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
