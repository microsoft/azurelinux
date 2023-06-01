// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A common interface for creating a basic spec/rpm parsing environment inside a chroot.

package simplechroottool

import (
	"path/filepath"
	"runtime"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/rpm"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
)

const (
	chrootSpecDirPath = "/SPECS"
)

type SimpleChrootTool struct {
	Chroot        *safechroot.Chroot
	ChrootSpecDir string
	BuildDirPath  string
	WorkerTarPath string
}

// BuildDefines creates a map of RPM build defines for the crhoot.
func (s *SimpleChrootTool) BuildDefines(distTag string) map[string]string {
	const runCheck = true

	defines := rpm.DefaultDefines(runCheck)
	defines[rpm.DistTagDefine] = distTag

	return defines
}

// InitializeChroot initializes the chroot environment.
//   - chrootName: The name of the chroot directory to use
//   - specsDirPath: The path to the directory containing the spec files
func (s *SimpleChrootTool) InitializeChroot(chrootName, specsDirPath string) (err error) {
	const (
		existingDir = false
	)

	chrootDirPath := filepath.Join(s.BuildDirPath, chrootName)
	s.Chroot = safechroot.NewChroot(chrootDirPath, existingDir)
	s.ChrootSpecDir = chrootSpecDirPath

	extraDirectories := []string{}
	extraMountPoints := []*safechroot.MountPoint{
		safechroot.NewMountPoint(specsDirPath, s.ChrootSpecDir, "", safechroot.BindMountPointFlags, ""),
	}
	err = s.Chroot.Initialize(s.WorkerTarPath, extraDirectories, extraMountPoints)
	if err != nil {
		logger.Log.Errorf("Failed to initialize chroot (%s) inside (%s). Error: %v.", s.WorkerTarPath, chrootDirPath, err)
	}

	return
}

// CleanUp cleans up the chroot environment.
func (s *SimpleChrootTool) CleanUp() {
	const leaveFilesOnDisk = false

	if s.Chroot != nil {
		s.Chroot.Close(leaveFilesOnDisk)
	}
}

// BuildCompatibleSpecsList builds a list of spec files in the chroot's SPECs directory that are compatible with the build arch. Paths
// are relative to the chroot's base directory.
func (s *SimpleChrootTool) BuildCompatibleSpecsList(inputSpecPaths []string, defines map[string]string) (filteredSpecPaths []string, err error) {
	var specPaths []string
	if len(inputSpecPaths) > 0 {
		specPaths = inputSpecPaths
	} else {
		specPaths, err = s.buildAllSpecsList()
		if err != nil {
			return
		}
	}

	return s.filterCompatibleSpecs(specPaths, defines)
}

// buildAllSpecsList builds a list of all spec files in the chroot's SPECs directory. Paths are relative to the chroot's base directory.
func (s *SimpleChrootTool) buildAllSpecsList() (specPaths []string, err error) {
	specFilesGlob := filepath.Join(s.ChrootSpecDir, "**", "*.spec")

	specPaths, err = filepath.Glob(specFilesGlob)
	if err != nil {
		logger.Log.Errorf("Failed while trying to enumerate all spec files with (%s). Error: %v.", specFilesGlob, err)
	}

	return
}

// filterCompatibleSpecs filters a list of spec files in the chroot's SPECs directory that are compatible with the build arch. Paths
func (s *SimpleChrootTool) filterCompatibleSpecs(inputSpecPaths []string, defines map[string]string) (filteredSpecPaths []string, err error) {
	var specCompatible bool

	buildArch, err := rpm.GetRpmArch(runtime.GOARCH)
	if err != nil {
		return
	}

	for _, specFilePath := range inputSpecPaths {
		specDirPath := filepath.Dir(specFilePath)

		specCompatible, err = rpm.SpecArchIsCompatible(specFilePath, specDirPath, buildArch, defines)
		if err != nil {
			logger.Log.Errorf("Failed while querrying spec (%s). Error: %v.", specFilePath, err)
			return
		}

		if specCompatible {
			filteredSpecPaths = append(filteredSpecPaths, specFilePath)
		}
	}

	return
}
