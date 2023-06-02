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

// SimpleChrootTool is a tool for creating a basic spec/rpm parsing environment inside a chroot. When creating a new instance, the
// following fields must be set:
//   - BuildDirPath: The path to the directory where the chroot will be created and run from.
//   - WorkerTarPath: The path to the tarball containing the chroot environment.
// The following fields will be set by InitializeChroot():
//   - chroot: The chroot environment we are working in, call Chroot.Run() to execute commands inside the chroot.
//   - chrootSpecDir: The path to the SPECS directory inside the chroot "/SPECS."

type SimpleChrootTool struct {
	BuildDirPath  string
	WorkerTarPath string
	chroot        *safechroot.Chroot
	chrootSpecDir string
}

// Chroot returns the chroot environment we are working in, call Chroot().Run() to execute commands inside the chroot. Call
// InitializeChroot() before calling this function.
func (s *SimpleChrootTool) Chroot() *safechroot.Chroot {
	return s.chroot
}

// ChrootSpecDir returns the directory inside the choot where the specs dir is mounted. Call InitializeChroot() before calling this function.
func (s *SimpleChrootTool) ChrootSpecDir() string {
	return s.chrootSpecDir
}

// InitializeChroot initializes the chroot environment so .Run() can be used to execute commands inside the chroot. This function
// should be called before any other functions in this package.
//   - chrootName: The name of the chroot directory to use
//   - specsDirPath: The path to the directory containing the spec files
func (s *SimpleChrootTool) InitializeChroot(chrootName, specsDirPath string) (err error) {
	const (
		existingDir = false
	)

	chrootDirPath := filepath.Join(s.BuildDirPath, chrootName)
	s.chroot = safechroot.NewChroot(chrootDirPath, existingDir)
	s.chrootSpecDir = chrootSpecDirPath

	extraDirectories := []string{}
	extraMountPoints := []*safechroot.MountPoint{
		safechroot.NewMountPoint(specsDirPath, s.chrootSpecDir, "", safechroot.BindMountPointFlags, ""),
	}
	err = s.chroot.Initialize(s.WorkerTarPath, extraDirectories, extraMountPoints)
	if err != nil {
		logger.Log.Errorf("Failed to initialize chroot (%s) inside (%s). Error: %v.", s.WorkerTarPath, chrootDirPath, err)
	}

	return
}

// CleanUp cleans up the chroot environment. This function should be called after all other functions in this package have been
// called (likely in a defer statement)
func (s *SimpleChrootTool) CleanUp() {
	const leaveFilesOnDisk = false

	if s.chroot != nil {
		s.chroot.Close(leaveFilesOnDisk)
	}
}

// BuildDefines creates a map of RPM build defines for the crhoot. This function should be called after InitializeChroot()
// and from a context inside a call to the chroot's .Run() function.
func (s *SimpleChrootTool) BuildDefines(distTag string) map[string]string {
	const runCheck = true

	defines := rpm.DefaultDefines(runCheck)
	defines[rpm.DistTagDefine] = distTag

	return defines
}

// BuildCompatibleSpecsList builds a list of spec files in the chroot's SPECs directory that are compatible with the build arch. Paths
// are relative to the chroot's base directory. This function should be called after InitializeChroot() and from a context inside a call
// to the chroot's .Run() function.
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
	specFilesGlob := filepath.Join(s.chrootSpecDir, "**", "*.spec")

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
