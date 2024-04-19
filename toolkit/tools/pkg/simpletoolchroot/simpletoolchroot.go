// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A common interface for creating a basic spec/rpm parsing environment inside a chroot.

package simpletoolchroot

import (
	"fmt"
	"path/filepath"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
)

const (
	chrootMountDirPath = "/chroot_mnt"
)

// SimpleToolChroot is a tool for creating an environment inside a chroot suitable for basic tasks like parsing RPMs.
// The following fields will be set by InitializeChroot():
//   - chroot: The chroot environment we are working in, call SimpleToolChroot.RunInChroot() to execute commands inside the chroot.
//   - chrootSpecDir: The relative path to the SPECS directory inside the chroot: "/SPECS."
//   - runChecks: Whether or not to parse with check sections enabled.
//   - distTag: The distribution tag to use when parsing RPMs.
type SimpleToolChroot struct {
	chroot *safechroot.Chroot
}

// ChrootRootDir returns the root directory where the chroot was created. Call InitializeChroot() before calling this function.
func (s *SimpleToolChroot) ChrootRootDir() string {
	if s.chroot == nil {
		return ""
	}
	return s.chroot.RootDir()
}

// ChrootRelativeMountDir returns the directory inside the chroot where the specs dir is mounted. Call InitializeChroot() before calling this function.
func (s *SimpleToolChroot) ChrootRelativeMountDir() string {
	return chrootMountDirPath
}

// InitializeChroot initializes the chroot environment so .RunInChroot() can be used to execute commands inside the chroot. This function
// should be called before any other functions in this package. CleanUp() must be called (likely via defer) after InitializeChroot() is used.
//   - buildDir: The path to the directory where the chroot will be created
//   - chrootName: The name of the chroot to create
//   - workerTarPath: The path to the tar file containing the worker files
//   - mountDirPath: The path to the directory to mount, will be mounted to s.ChrootRelativeMountDir() inside the chroot
func (s *SimpleToolChroot) InitializeChroot(buildDir, chrootName, workerTarPath, mountDirPath string) (err error) {
	const (
		existingDir = false
	)

	chrootDirPath := filepath.Join(buildDir, chrootName)
	s.chroot = safechroot.NewChroot(chrootDirPath, existingDir)

	extraDirectories := []string{}
	extraMountPoints := []*safechroot.MountPoint{
		safechroot.NewMountPoint(mountDirPath, chrootMountDirPath, "", safechroot.BindMountPointFlags, ""),
	}
	err = s.chroot.Initialize(workerTarPath, extraDirectories, extraMountPoints, true)
	if err != nil {
		err = fmt.Errorf("failed to initialize chroot (%s) inside (%s):\n%w", workerTarPath, chrootDirPath, err)
		return
	}

	return
}

// EnableNetwork enables network access inside the chroot environment. This function should be called after InitializeChroot() has been called.
func (s *SimpleToolChroot) EnableNetwork() (err error) {
	if s.chroot == nil {
		return fmt.Errorf("chroot has not been initialized")
	}
	files := []safechroot.FileToCopy{
		{Src: "/etc/resolv.conf", Dest: "/etc/resolv.conf"},
	}
	err = s.chroot.AddFiles(files...)
	if err != nil {
		err = fmt.Errorf("failed to add files to chroot:\n%w", err)
	}
	return
}

// CleanUp cleans up the chroot environment. This function should be called after all other functions in this package have been
// called (likely in a defer statement)
func (s *SimpleToolChroot) CleanUp() (err error) {
	const leaveFilesOnDisk = false

	if s.chroot != nil {
		err = s.chroot.Close(leaveFilesOnDisk)
	}
	return
}

// RunInChroot executes a given function inside the tool's chroot environment.
func (s *SimpleToolChroot) RunInChroot(toRun func() error) (err error) {
	if s.chroot == nil {
		return fmt.Errorf("chroot has not been initialized")
	}
	return s.chroot.Run(toRun)
}
