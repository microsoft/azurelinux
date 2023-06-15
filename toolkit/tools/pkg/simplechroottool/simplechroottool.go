// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A common interface for creating a basic spec/rpm parsing environment inside a chroot.

package simplechroottool

import (
	"fmt"
	"path/filepath"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/rpm"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
)

const (
	chrootSpecDirPath = "/SPECS"
)

// SimpleChrootTool is a tool for creating an environment inside a chroot suitable for basic tasks like parsing RPMs.
// The following fields will be set by InitializeChroot():
//   - chroot: The chroot environment we are working in, call SimpleChrootTool.RunInChroot() to execute commands inside the chroot.
//   - chrootSpecDir: The relative path to the SPECS directory inside the chroot: "/SPECS."
//   - runChecks: Whether or not to parse with check sections enabled.
//   - distTag: The distribution tag to use when parsing RPMs.
type SimpleChrootTool struct {
	chroot        *safechroot.Chroot
	chrootSpecDir string
	runChecks     bool
	distTag       string
}

// ChrootRootDir returns the root directory where the chroot was created. Call InitializeChroot() before calling this function.
func (s *SimpleChrootTool) ChrootRootDir() string {
	if s.chroot == nil {
		return ""
	}
	return s.chroot.RootDir()
}

// ChrootSpecDir returns the directory inside the chroot where the specs dir is mounted. Call InitializeChroot() before calling this function.
func (s *SimpleChrootTool) ChrootRelativeSpecDir() string {
	return s.chrootSpecDir
}

// InitializeChroot initializes the chroot environment so .RunInChroot() can be used to execute commands inside the chroot. This function
// should be called before any other functions in this package. CleanUp() must be called (likely via defer) after InitializeChroot() is used.
//   - buildDir: The path to the directory where the chroot will be created
//   - chrootName: The name of the chroot to create
//   - workerTarPath: The path to the tar file containing the worker files
//   - specsDirPath: The path to the directory containing the spec files
//   - distTag: The distribution tag to use when parsing RPMs
//   - runChecks: Whether or not to parse with check sections enabled
func (s *SimpleChrootTool) InitializeChroot(buildDir, chrootName, workerTarPath, specsDirPath, distTag string, runChecks bool) (err error) {
	const (
		existingDir = false
	)

	chrootDirPath := filepath.Join(buildDir, chrootName)
	s.chroot = safechroot.NewChroot(chrootDirPath, existingDir)
	s.chrootSpecDir = chrootSpecDirPath
	s.runChecks = runChecks
	s.distTag = distTag

	extraDirectories := []string{}
	extraMountPoints := []*safechroot.MountPoint{
		safechroot.NewMountPoint(specsDirPath, s.chrootSpecDir, "", safechroot.BindMountPointFlags, ""),
	}
	err = s.chroot.Initialize(workerTarPath, extraDirectories, extraMountPoints)
	if err != nil {
		logger.Log.Errorf("Failed to initialize chroot (%s) inside (%s). Error: %v.", workerTarPath, chrootDirPath, err)
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

// Run executes a given function inside the tool's chroot environment.
func (s *SimpleChrootTool) RunInChroot(toRun func() error) (err error) {
	if s.chroot == nil {
		return fmt.Errorf("chroot has not been initialized")
	}
	return s.chroot.Run(toRun)
}

// DefaultDefines creates a map of RPM build defines for the chroot. This function should be called after InitializeChroot()
// and from a context inside a call to the chroot's .Run() function.
func (s *SimpleChrootTool) DefaultDefines() map[string]string {
	defines := rpm.DefaultDefines(s.runChecks)
	defines[rpm.DistTagDefine] = s.distTag

	return defines
}
