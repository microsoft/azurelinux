// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/sirupsen/logrus"
)

func customizePartitionsUsingFileCopy(buildDir string, baseConfigPath string, config *imagecustomizerapi.Config,
	buildImageFile string, newBuildImageFile string,
) error {
	existingImageConnection, err := connectToExistingImage(buildImageFile, buildDir, "imageroot", false)
	if err != nil {
		return err
	}
	defer existingImageConnection.Close()

	diskConfig := config.Storage.Disks[0]

	installOSFunc := func(imageChroot *safechroot.Chroot) error {
		return copyFilesIntoNewDisk(existingImageConnection.Chroot(), imageChroot)
	}

	err = createNewImage(newBuildImageFile, diskConfig, config.Storage.FileSystems,
		buildDir, "newimageroot", installOSFunc)
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

	err := shell.NewExecBuilder("cp", copyArgs...).
		LogLevel(logrus.TraceLevel, logrus.DebugLevel).
		ErrorStderrLines(1).
		Execute()
	if err != nil {
		return fmt.Errorf("failed to copy files:\n%w", err)
	}

	return nil
}
