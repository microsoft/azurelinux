// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

func customizePartitionsUsingFileCopy(buildDir string, baseConfigPath string, config *imagecustomizerapi.Config,
	buildImageFile string, newBuildImageFile string,
) error {
	existingImageConnection, err := connectToExistingImage(buildImageFile, buildDir, "imageroot", false)
	if err != nil {
		return err
	}
	defer existingImageConnection.Close()

	currentSELinuxMode, err := getCurrentSELinuxMode(existingImageConnection.Chroot())
	if err != nil {
		return err
	}

	diskConfig := (*config.Disks)[0]

	installOSFunc := func(imageChroot *safechroot.Chroot) error {
		return copyFilesIntoNewDisk(existingImageConnection.Chroot(), imageChroot)
	}

	err = createNewImage(newBuildImageFile, diskConfig, config.SystemConfig.PartitionSettings,
		config.SystemConfig.BootType, config.SystemConfig.KernelCommandLine, buildDir, "newimageroot",
		currentSELinuxMode, installOSFunc)
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
	err := copyPartitionFiles(existingImageChroot.RootDir()+"/.", newImageChroot.RootDir())
	if err != nil {
		return fmt.Errorf("failed to copy files into new partition layout:\n%w", err)
	}
	return nil
}

func copyPartitionFiles(sourceRoot, targetRoot string) error {
	// Notes:
	// `-a` ensures unix permissions, extended attributes (including SELinux), and sub-directories (-r) are copied.
	// `--no-dereference` ensures that symlinks are copied as symlinks.
	copyArgs := []string{"--verbose", "--no-clobber", "-a", "--no-dereference", "--sparse", "always",
		sourceRoot, targetRoot}

	err := shell.ExecuteLiveWithErrAndCallbacks(1, func(...interface{}) {}, logger.Log.Debug, "cp", copyArgs...)
	if err != nil {
		return fmt.Errorf("failed to copy files:\n%w", err)
	}

	return nil
}
