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
	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"
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
	mountPoints, err := findPartitions(buildDir, imageConnection.Loopback().DevicePath())
	if err != nil {
		return fmt.Errorf("failed to find disk partitions:\n%w", err)
	}

	// Create chroot environment.
	imageChrootDir := filepath.Join(buildDir, chrootDirName)

	err = imageConnection.ConnectChroot(imageChrootDir, false, []string(nil), mountPoints, includeDefaultMounts)
	if err != nil {
		return err
	}

	return nil
}

func createNewImage(filename string, diskConfig imagecustomizerapi.Disk,
	fileSystems []imagecustomizerapi.FileSystem, buildDir string, chrootDirName string,
	installOS installOSFunc,
) (map[string]string, error) {
	imageConnection := NewImageConnection()
	defer imageConnection.Close()

	partIdToPartUuid, err := createNewImageHelper(imageConnection, filename, diskConfig, fileSystems, buildDir, chrootDirName,
		installOS)
	if err != nil {
		return nil, fmt.Errorf("failed to create new image:\n%w", err)
	}

	// Close image.
	err = imageConnection.CleanClose()
	if err != nil {
		return nil, err
	}

	return partIdToPartUuid, nil
}

func createNewImageHelper(imageConnection *ImageConnection, filename string, diskConfig imagecustomizerapi.Disk,
	fileSystems []imagecustomizerapi.FileSystem, buildDir string, chrootDirName string,
	installOS installOSFunc,
) (map[string]string, error) {

	// Convert config to image config types, so that the imager's utils can be used.
	imagerDiskConfig, err := diskConfigToImager(diskConfig, fileSystems)
	if err != nil {
		return nil, err
	}

	imagerPartitionSettings, err := partitionSettingsToImager(fileSystems)
	if err != nil {
		return nil, err
	}

	// Create imager boilerplate.
	partIdToPartUuid, tmpFstabFile, err := createImageBoilerplate(imageConnection, filename, buildDir, chrootDirName,
		imagerDiskConfig, imagerPartitionSettings)
	if err != nil {
		return nil, err
	}

	// Install the OS.
	err = installOS(imageConnection.Chroot())
	if err != nil {
		return nil, err
	}

	// Move the fstab file into the image.
	imageFstabFilePath := filepath.Join(imageConnection.Chroot().RootDir(), "etc/fstab")

	err = file.Move(tmpFstabFile, imageFstabFilePath)
	if err != nil {
		return nil, fmt.Errorf("failed to move fstab into new image:\n%w", err)
	}

	return partIdToPartUuid, nil
}

func configureDiskBootLoader(imageConnection *ImageConnection, rootMountIdType imagecustomizerapi.MountIdentifierType,
	bootType imagecustomizerapi.BootType, selinuxConfig imagecustomizerapi.SELinux,
	kernelCommandLine imagecustomizerapi.KernelCommandLine, currentSELinuxMode imagecustomizerapi.SELinuxMode,
) error {
	imagerBootType, err := bootTypeToImager(bootType)
	if err != nil {
		return err
	}

	imagerKernelCommandLine, err := kernelCommandLineToImager(kernelCommandLine, selinuxConfig, currentSELinuxMode)
	if err != nil {
		return err
	}

	imagerRootMountIdType, err := mountIdentifierTypeToImager(rootMountIdType)
	if err != nil {
		return err
	}

	grubMkconfigEnabled, err := isGrubMkconfigEnabled(imageConnection.Chroot())
	if err != nil {
		return err
	}

	mountPointMap := make(map[string]string)
	for _, mountPoint := range imageConnection.Chroot().GetMountPoints() {
		mountPointMap[mountPoint.GetTarget()] = mountPoint.GetSource()
	}

	// Configure the boot loader.
	err = installutils.ConfigureDiskBootloaderWithRootMountIdType(imagerBootType, false, imagerRootMountIdType,
		imagerKernelCommandLine, imageConnection.Chroot(), imageConnection.Loopback().DevicePath(),
		mountPointMap, diskutils.EncryptedRootDevice{}, grubMkconfigEnabled,
		!grubMkconfigEnabled)
	if err != nil {
		return fmt.Errorf("failed to install bootloader:\n%w", err)
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
	partIDToDevPathMap, partIDToFsTypeMap, _, err := diskutils.CreatePartitions(
		imageConnection.Loopback().DevicePath(), imagerDiskConfig, configuration.RootEncryption{},
		true /*diskKnownToBeEmpty*/)
	if err != nil {
		return nil, "", fmt.Errorf("failed to create partitions on disk (%s):\n%w", imageConnection.Loopback().DevicePath(), err)
	}

	// Refresh partition entries under /dev.
	err = refreshPartitions(imageConnection.Loopback().DevicePath())
	if err != nil {
		return nil, "", err
	}

	// Read the disk partitions.
	diskPartitions, err := diskutils.GetDiskPartitions(imageConnection.Loopback().DevicePath())
	if err != nil {
		return nil, "", err
	}

	// Create mapping from partition ID to partition UUID.
	partIdToPartUuid, err := createPartIdToPartUuidMap(partIDToDevPathMap, diskPartitions)
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

	mountList := sliceutils.MapToSlice(mountPointMap)

	// Sort the mounts so that they are mounted in the correct oder.
	sort.Slice(mountList, func(i, j int) bool {
		return mountList[i] < mountList[j]
	})

	err = installutils.UpdateFstabFile(tmpFstabFile, imagerPartitionSettings, mountList, mountPointMap,
		mountPointToFsTypeMap, mountPointToMountArgsMap, partIDToDevPathMap, partIDToFsTypeMap,
		false, /*hidepidEnabled*/
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

	return partIdToPartUuid, tmpFstabFile, nil
}

func createPartIdToPartUuidMap(partIDToDevPathMap map[string]string, diskPartitions []diskutils.PartitionInfo,
) (map[string]string, error) {
	partIdToPartUuid := make(map[string]string)
	for partId, devPath := range partIDToDevPathMap {
		partition, found := sliceutils.FindValueFunc(diskPartitions, func(partition diskutils.PartitionInfo) bool {
			return devPath == partition.Path
		})
		if !found {
			return nil, fmt.Errorf("failed to find partition for device path (%s)", devPath)
		}

		partIdToPartUuid[partId] = partition.PartUuid
	}

	return partIdToPartUuid, nil
}
