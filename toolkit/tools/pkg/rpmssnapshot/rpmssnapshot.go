// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A tool for generating snapshots of built RPMs from local specs.

package rpmssnapshot

import (
	"fmt"
	"path/filepath"
	"regexp"
	"runtime"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/jsonutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/packagerepo/repocloner"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/rpm"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/safechroot"
)

const (
	chrootOutputFilePath = "/snapshot.json"
	chrootSpecDirPath    = "/SPECS"
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
//	([^-]+-\d+)		<-- [index 2] package version and package release number connected by the last hyphen
//	\.				<-- second-to-last period separating the package release number from the distribution tag
//	([^.]+)			<-- [index 3] the distribution tag
//	\.				<-- last period separating the distribution tag from the architecture string
//	([^.]+)$		<-- [index 4] the architecture string
var rpmSpecBuiltRPMRegex = regexp.MustCompile(`^(.*)-([^-]+-\d+)\.([^.]+)\.([^.]+)$`)

const (
	rpmSpecBuiltRPMRegexNameIndex = iota + 1
	rpmSpecBuiltRPMRegexVersionIndex
	rpmSpecBuiltRPMRegexDistributionIndex
	rpmSpecBuiltRPMRegexArchitectureIndex
	rpmSpecBuiltRPMRegexMatchesCount
)

type SnapshotGenerator struct {
	chroot        *safechroot.Chroot
	buildDirPath  string
	workerTarPath string
}

// New creates an unitialized RPMs snapshot generator.
func New(buildDirPath, workerTarPath string) *SnapshotGenerator {
	return &SnapshotGenerator{
		buildDirPath:  buildDirPath,
		workerTarPath: workerTarPath,
	}
}

// GenerateSnapshot generates a snapshot of all packages built from the specs inside the input directory.
func (s *SnapshotGenerator) GenerateSnapshot(specsDirPath, outputFilePath, distTag string) (err error) {
	err = s.initializeChroot(specsDirPath)
	if err != nil {
		return
	}
	defer s.cleanUp()

	logger.Log.Infof("Generating RPMs snapshot from specs inside (%s).", specsDirPath)

	logger.Log.Debugf("Distribution tag: %s.", distTag)

	err = s.chroot.Run(func() error {
		return s.generateSnapshotInChroot(distTag)
	})
	if err != nil {
		return
	}

	chrootOutputFileFullPath := filepath.Join(s.chroot.RootDir(), chrootOutputFilePath)
	err = file.Move(chrootOutputFileFullPath, outputFilePath)
	if err != nil {
		logger.Log.Errorf("Failed to retrieve the snapshot from the chroot. Error: %v.", err)
	}

	return
}

func (s *SnapshotGenerator) buildAllSpecsList() (specPaths []string, err error) {
	specFilesGlob := filepath.Join(chrootSpecDirPath, "**", "*.spec")

	specPaths, err = filepath.Glob(specFilesGlob)
	if err != nil {
		logger.Log.Errorf("Failed while trying to enumerate all spec files with (%s). Error: %v.", specFilesGlob, err)
	}

	return
}

func (s *SnapshotGenerator) buildCompatibleSpecsList(defines map[string]string) (specPaths []string, err error) {
	var allSpecFilePaths []string

	allSpecFilePaths, err = s.buildAllSpecsList()
	if err != nil {
		return
	}

	return s.filterCompatibleSpecs(allSpecFilePaths, defines)
}

func (s *SnapshotGenerator) buildDefines(distTag string) map[string]string {
	const runCheck = true

	defines := rpm.DefaultDefines(runCheck)
	defines[rpm.DistTagDefine] = distTag

	return defines
}

func (s *SnapshotGenerator) cleanUp() {
	const leaveFilesOnDisk = false

	if s.chroot != nil {
		s.chroot.Close(leaveFilesOnDisk)
	}
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

func (s *SnapshotGenerator) filterCompatibleSpecs(allSpecFilePaths []string, defines map[string]string) (specPaths []string, err error) {
	var specCompatible bool

	buildArch, err := rpm.GetRpmArch(runtime.GOARCH)
	if err != nil {
		return
	}

	for _, specFilePath := range allSpecFilePaths {
		specDirPath := filepath.Dir(specFilePath)

		specCompatible, err = rpm.SpecArchIsCompatible(specFilePath, specDirPath, buildArch, defines)
		if err != nil {
			logger.Log.Errorf("Failed while querrying spec (%s). Error: %v.", specFilePath, err)
			return
		}

		if specCompatible {
			specPaths = append(specPaths, specFilePath)
		}
	}

	return
}

func (s *SnapshotGenerator) generateSnapshotInChroot(distTag string) (err error) {
	var (
		allBuiltRPMs []string
		repoContents repocloner.RepoContents
		specPaths    []string
	)

	defines := s.buildDefines(distTag)
	specPaths, err = s.buildCompatibleSpecsList(defines)
	if err != nil {
		logger.Log.Errorf("Failed to retrieve a list of specs inside (%s). Error: %v.", chrootSpecDirPath, err)
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

func (s *SnapshotGenerator) initializeChroot(specsDirPath string) (err error) {
	const (
		existingDir = false
		chrootName  = "rpmssnapshot_chroot"
	)

	chrootDirPath := filepath.Join(s.buildDirPath, chrootName)
	s.chroot = safechroot.NewChroot(chrootDirPath, existingDir)

	extraDirectories := []string{}
	extraMountPoints := []*safechroot.MountPoint{
		safechroot.NewMountPoint(specsDirPath, chrootSpecDirPath, "", safechroot.BindMountPointFlags, ""),
	}
	err = s.chroot.Initialize(s.workerTarPath, extraDirectories, extraMountPoints)
	if err != nil {
		logger.Log.Errorf("Failed to initialize chroot (%s) inside (%s). Error: %v.", s.workerTarPath, chrootDirPath, err)
	}

	return
}

func (s *SnapshotGenerator) readBuiltRPMs(specPaths []string, defines map[string]string) (allBuiltRPMs []string, err error) {
	var builtRPMs []string

	buildArch, err := rpm.GetRpmArch(runtime.GOARCH)
	if err != nil {
		return
	}

	for _, specPath := range specPaths {
		logger.Log.Debugf("Parsing spec (%s).", specPath)

		specDirPath := filepath.Dir(specPath)

		builtRPMs, err = rpm.QuerySPECForBuiltRPMs(specPath, specDirPath, buildArch, defines)
		if err != nil {
			logger.Log.Errorf("Failed to query built RPMs from (%s). Error: %v.", specPath, err)
			return
		}

		allBuiltRPMs = append(allBuiltRPMs, builtRPMs...)
	}

	return
}
