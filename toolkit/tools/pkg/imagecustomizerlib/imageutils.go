// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"path/filepath"
	"sort"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/installutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
)

type installOSFunc func(imageChroot *safechroot.Chroot) error

func connectToExistingImage(imageFilePath string, buildDir string, chrootDirName string, includeDefaultMounts bool,
) (*ImageConnection, error) {
	imageConnection := NewImageConnection()

	err := connectToExistingImageHelper(imageConnection, imageFilePath, buildDir, chrootDirName, includeDefaultMounts)
	if err != nil {
		imageConnection.Close()
		return nil, err
	}
	return imageConnection, nil
}

func connectToExistingImageHelper(imageConnection *ImageConnection, imageFilePath string,
	buildDir string, chrootDirName string, includeDefaultMounts bool,
) error {
	// Connect to image file using loopback device.
	err := imageConnection.ConnectLoopback(imageFilePath)
	if err != nil {
		return err
	}

	// Look for all the partitions on the image.
	newMountDirectories, mountPoints, err := findPartitions(buildDir, imageConnection.Loopback().DevicePath())
	if err != nil {
		return fmt.Errorf("failed to find disk partitions:\n%w", err)
	}

	// Create chroot environment.
	imageChrootDir := filepath.Join(buildDir, chrootDirName)

	err = imageConnection.ConnectChroot(imageChrootDir, false, newMountDirectories, mountPoints, includeDefaultMounts)
	if err != nil {
		return err
	}

	return nil
}

func createNewImage(filename string, diskConfig imagecustomizerapi.Disk,
	partitionSettings []imagecustomizerapi.PartitionSetting, bootType imagecustomizerapi.BootType,
	kernelCommandLine imagecustomizerapi.KernelCommandLine, buildDir string, chrootDirName string,
	currentSELinuxMode imagecustomizerapi.SELinux, installOS installOSFunc,
) error {
	err := createNewImageHelper(filename, diskConfig, partitionSettings, bootType, kernelCommandLine,
		buildDir, chrootDirName, currentSELinuxMode, installOS,
	)
	if err != nil {
		return fmt.Errorf("failed to create new image:\n%w", err)
	}

	return nil
}

func createNewImageHelper(filename string, diskConfig imagecustomizerapi.Disk,
	partitionSettings []imagecustomizerapi.PartitionSetting, bootType imagecustomizerapi.BootType,
	kernelCommandLine imagecustomizerapi.KernelCommandLine, buildDir string, chrootDirName string,
	currentSELinuxMode imagecustomizerapi.SELinux, installOS installOSFunc,
) error {
	imageConnection := NewImageConnection()
	defer imageConnection.Close()

	// Convert config to image config types, so that the imager's utils can be used.
	imagerBootType, err := bootTypeToImager(bootType)
	if err != nil {
		return err
	}

	imagerDiskConfig, err := diskConfigToImager(diskConfig)
	if err != nil {
		return err
	}

	imagerPartitionSettings, err := partitionSettingsToImager(partitionSettings)
	if err != nil {
		return err
	}

	imagerKernelCommandLine, err := kernelCommandLineToImager(kernelCommandLine, currentSELinuxMode)
	if err != nil {
		return err
	}

	// Sort the partitions so that they are mounted in the correct oder.
	sort.Slice(imagerPartitionSettings, func(i, j int) bool {
		return imagerPartitionSettings[i].MountPoint < imagerPartitionSettings[j].MountPoint
	})

	// Create imager boilerplate.
	mountPointMap, tmpFstabFile, err := createImageBoilerplate(imageConnection, filename, buildDir, chrootDirName, imagerDiskConfig,
		imagerPartitionSettings)
	if err != nil {
		return err
	}

	// Install the OS.
	err = installOS(imageConnection.Chroot())
	if err != nil {
		return err
	}

	// Move the fstab file into the image.
	imageFstabFilePath := filepath.Join(imageConnection.Chroot().RootDir(), "etc/fstab")

	err = file.Move(tmpFstabFile, imageFstabFilePath)
	if err != nil {
		return fmt.Errorf("failed to move fstab into new image:\n%w", err)
	}

	// Configure the boot loader.
	err = installutils.ConfigureDiskBootloader(imagerBootType, false, false, imagerPartitionSettings,
		imagerKernelCommandLine, imageConnection.Chroot(), imageConnection.Loopback().DevicePath(),
		mountPointMap, diskutils.EncryptedRootDevice{}, diskutils.VerityDevice{}, false /*enableGrubMkconfig*/)
	if err != nil {
		return fmt.Errorf("failed to install bootloader:\n%w", err)
	}

	// Close image.
	err = imageConnection.CleanClose()
	if err != nil {
		return err
	}

	return nil
}

func createImageBoilerplate(imageConnection *ImageConnection, filename string, buildDir string, chrootDirName string,
	imagerDiskConfig configuration.Disk, imagerPartitionSettings []configuration.PartitionSetting,
) (map[string]string, string, error) {
	// Create raw disk image file.
	err := diskutils.CreateSparseDisk(filename, imagerDiskConfig.MaxSize, 0o644)
	if err != nil {
		return nil, "", fmt.Errorf("failed to create empty disk file (%s):\n%w", filename, err)
	}

	// Connect raw disk image file.
	err = imageConnection.ConnectLoopback(filename)
	if err != nil {
		return nil, "", err
	}

	// Set up partitions.
	partIDToDevPathMap, partIDToFsTypeMap, _, _, err := diskutils.CreatePartitions(
		imageConnection.Loopback().DevicePath(), imagerDiskConfig, configuration.RootEncryption{},
		configuration.ReadOnlyVerityRoot{})
	if err != nil {
		return nil, "", fmt.Errorf("failed to create partitions on disk (%s):\n%w", imageConnection.Loopback().DevicePath(), err)
	}

	// Read the disk partitions.
	diskPartitions, err := diskutils.GetDiskPartitions(imageConnection.Loopback().DevicePath())
	if err != nil {
		return nil, "", err
	}

	// Create the fstab file.
	// This is done so that we can read back the file using findmnt, which conveniently splits the vfs and fs mount
	// options for us. If we wanted to handle this more directly, we could create a golang wrapper around libmount
	// (which is what findmnt uses). But we are already using the findmnt in other places.
	tmpFstabFile := filepath.Join(buildDir, chrootDirName+"_fstab")
	err = file.RemoveFileIfExists(tmpFstabFile)
	if err != nil {
		return nil, "", err
	}

	mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap, _ := installutils.CreateMountPointPartitionMap(
		partIDToDevPathMap, partIDToFsTypeMap, imagerPartitionSettings,
	)

	err = installutils.UpdateFstabFile(tmpFstabFile, imagerPartitionSettings, mountPointMap, mountPointToFsTypeMap,
		mountPointToMountArgsMap, partIDToDevPathMap, partIDToFsTypeMap, false, /*hidepidEnabled*/
	)
	if err != nil {
		return nil, "", fmt.Errorf("failed to write temp fstab file:\n%w", err)
	}

	// Read back the fstab file.
	mountPoints, err := findMountsFromFstabFile(tmpFstabFile, diskPartitions)
	if err != nil {
		return nil, "", err
	}

	// Create chroot environment.
	imageChrootDir := filepath.Join(buildDir, chrootDirName)

	err = imageConnection.ConnectChroot(imageChrootDir, false, nil, mountPoints, false)
	if err != nil {
		return nil, "", err
	}

	return mountPointMap, tmpFstabFile, nil
}
