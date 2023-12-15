// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

func customizePartitionsUsingFileCopy(buildDir string, baseConfigPath string, config *imagecustomizerapi.Config,
	buildImageFile string, newBuildImageFile string,
) error {
	existingImageConnection, err := connectToExistingImage(buildImageFile, buildDir, "imageroot")
	if err != nil {
		return err
	}
	defer existingImageConnection.Close()

	diskConfig := (*config.Disks)[0]

	installOSFunc := func(imageChroot *safechroot.Chroot) error {
		return copyFilesIntoNewDisk(existingImageConnection.Chroot(), imageChroot)
	}

	newImageConnection, err := createNewImage(newBuildImageFile, diskConfig, config.SystemConfig.PartitionSettings,
		config.SystemConfig.BootType, config.SystemConfig.KernelCommandLine, buildDir, "newimageroot", installOSFunc)
	if err != nil {
		return err
	}
	defer newImageConnection.Close()

	err = newImageConnection.CleanClose()
	if err != nil {
		return err
	}

	err = existingImageConnection.CleanClose()
	if err != nil {
		return err
	}

	return nil
}

func copyFilesIntoNewDisk(existingImageChroot *safechroot.Chroot, newImageChroot *safechroot.Chroot) error {
	err := copyFilesIntoNewDiskHelper(existingImageChroot, newImageChroot)
	if err != nil {
		return fmt.Errorf("failed to copy files into new partition layout:\n%w", err)
	}
	return nil
}

func copyFilesIntoNewDiskHelper(existingImageChroot *safechroot.Chroot, newImageChroot *safechroot.Chroot) error {
	// Notes:
	// `-a` ensures unix permissions, extended attributes (including SELinux), and sub-directories (-r) are copied.
	// `--no-dereference` ensures that symlinks are copied as symlinks.
	copyArgs := []string{"--verbose", "--no-clobber", "-a", "--no-dereference", "--sparse", "always", "-t", newImageChroot.RootDir()}

	files, err := os.ReadDir(existingImageChroot.RootDir())
	if err != nil {
		return fmt.Errorf("failed to read base image root directory:\n%w", err)
	}

	for _, file := range files {
		switch file.Name() {
		case "dev", "proc", "sys", "run", "tmp":
			// Exclude special directories.
			//
			// Note: Under /var, there are symlinks to a couple of these special directories.
			// However, the `cp` command is called with `--no-dereference`. So, the symlinks will be copied as symlinks.
			continue
		}

		fullFileName := filepath.Join(existingImageChroot.RootDir(), file.Name())
		copyArgs = append(copyArgs, fullFileName)
	}

	err = shell.ExecuteLiveWithErr(1, "cp", copyArgs...)
	if err != nil {
		return fmt.Errorf("failed to copy files:\n%w", err)
	}

	return nil
}
