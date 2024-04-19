// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/installutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safemount"
)

var (
	bootPartitionRegex = regexp.MustCompile(`(?m)^search -n -u ([a-zA-Z0-9\-]+) -s$`)
)

func findPartitions(buildDir string, diskDevice string) ([]*safechroot.MountPoint, error) {
	var err error

	diskPartitions, err := diskutils.GetDiskPartitions(diskDevice)
	if err != nil {
		return nil, err
	}

	rootfsPartition, err := findRootfsPartition(diskPartitions, buildDir)
	if err != nil {
		return nil, err
	}

	mountPoints, err := findMountsFromRootfs(rootfsPartition, diskPartitions, buildDir)
	if err != nil {
		return nil, err
	}

	return mountPoints, nil
}

func findSystemBootPartition(diskPartitions []diskutils.PartitionInfo) (*diskutils.PartitionInfo, error) {
	// Look for all system boot partitions, including both EFI System Paritions (ESP) and BIOS boot partitions.
	var bootPartitions []*diskutils.PartitionInfo
	for i := range diskPartitions {
		diskPartition := diskPartitions[i]

		switch diskPartition.PartitionTypeUuid {
		case diskutils.EfiSystemPartitionTypeUuid, diskutils.BiosBootPartitionTypeUuid:
			bootPartitions = append(bootPartitions, &diskPartition)
		}
	}

	if len(bootPartitions) > 1 {
		return nil, fmt.Errorf("found more than one boot partition (ESP or BIOS boot parititon)")
	} else if len(bootPartitions) < 1 {
		return nil, fmt.Errorf("failed to find boot partition (ESP or BIOS boot parititon)")
	}

	bootPartition := bootPartitions[0]
	return bootPartition, nil
}

func findBootPartitionFromEsp(efiSystemPartition *diskutils.PartitionInfo, diskPartitions []diskutils.PartitionInfo, buildDir string) (*diskutils.PartitionInfo, error) {
	tmpDir := filepath.Join(buildDir, tmpParitionDirName)

	// Mount the EFI System Partition.
	efiSystemPartitionMount, err := safemount.NewMount(efiSystemPartition.Path, tmpDir, efiSystemPartition.FileSystemType, 0, "", true)
	if err != nil {
		return nil, fmt.Errorf("failed to mount EFI system partition:\n%w", err)
	}
	defer efiSystemPartitionMount.Close()

	// Read the grub.cfg file.
	grubConfigFilePath := filepath.Join(tmpDir, installutils.GrubCfgFile)
	grubConfigFile, err := os.ReadFile(grubConfigFilePath)
	if err != nil {
		return nil, fmt.Errorf("failed to read EFI system partition's grub.cfg file:\n%w", err)
	}

	// Close the EFI System Partition mount.
	err = efiSystemPartitionMount.CleanClose()
	if err != nil {
		return nil, fmt.Errorf("failed to close EFI system partition mount:\n%w", err)
	}

	// Look for the bootloader partition declaration line in the grub.cfg file.
	match := bootPartitionRegex.FindStringSubmatch(string(grubConfigFile))
	if match == nil {
		return nil, fmt.Errorf("failed to find boot partition in grub.cfg file")
	}

	bootPartitionUuid := match[1]

	var bootPartition *diskutils.PartitionInfo
	for i := range diskPartitions {
		diskPartition := diskPartitions[i]

		if diskPartition.Uuid == bootPartitionUuid {
			bootPartition = &diskPartition
			break
		}
	}

	if bootPartition == nil {
		return nil, fmt.Errorf("failed to find boot partition with UUID (%s)", bootPartitionUuid)
	}

	return bootPartition, nil
}

// Searches for the partition that contains the /etc/fstab file.
// While technically it is possible to place /etc on a different partition, doing so is fairly difficult and requires
// a custom initramfs module.
func findRootfsPartition(diskPartitions []diskutils.PartitionInfo, buildDir string) (*diskutils.PartitionInfo, error) {
	tmpDir := filepath.Join(buildDir, tmpParitionDirName)

	var rootfsPartitions []*diskutils.PartitionInfo
	for i := range diskPartitions {
		diskPartition := diskPartitions[i]

		if diskPartition.Type != "part" {
			continue
		}

		// Check if the partition is using DM_verity_hash file system type.
		if diskPartition.FileSystemType == "DM_verity_hash" {
			return nil, fmt.Errorf("this image has dm-verity pre-enabled, stop the customized build process")
		}

		// Temporarily mount the partition.
		partitionMount, err := safemount.NewMount(diskPartition.Path, tmpDir, diskPartition.FileSystemType, 0,
			"", true)
		if err != nil {
			return nil, fmt.Errorf("failed to mount partition (%s):\n%w", diskPartition.Path, err)
		}
		defer partitionMount.Close()

		// Check if the /etc/fstab file exists.
		fstabPath := filepath.Join(tmpDir, "/etc/fstab")
		exists, err := file.PathExists(fstabPath)
		if err != nil {
			return nil, fmt.Errorf("failed to check if /etc/fstab file exists (%s):\n%w", diskPartition.Path, err)
		}

		if exists {
			rootfsPartitions = append(rootfsPartitions, &diskPartition)
		}

		// Close the rootfs partition mount.
		err = partitionMount.CleanClose()
		if err != nil {
			return nil, fmt.Errorf("failed to close partition mount (%s):\n%w", diskPartition.Path, err)
		}
	}

	if len(rootfsPartitions) > 1 {
		return nil, fmt.Errorf("found too many rootfs partition candidates (%d)", len(rootfsPartitions))
	} else if len(rootfsPartitions) < 1 {
		return nil, fmt.Errorf("failed to find rootfs partition")
	}

	rootfsPartition := rootfsPartitions[0]
	return rootfsPartition, nil
}

func findMountsFromRootfs(rootfsPartition *diskutils.PartitionInfo, diskPartitions []diskutils.PartitionInfo,
	buildDir string,
) ([]*safechroot.MountPoint, error) {
	tmpDir := filepath.Join(buildDir, tmpParitionDirName)

	// Temporarily mount the rootfs partition so that the fstab file can be read.
	rootfsPartitionMount, err := safemount.NewMount(rootfsPartition.Path, tmpDir, rootfsPartition.FileSystemType, 0, "",
		true)
	if err != nil {
		return nil, fmt.Errorf("failed to mount rootfs partition (%s):\n%w", rootfsPartition.Path, err)
	}
	defer rootfsPartitionMount.Close()

	// Read the fstab file.
	fstabPath := filepath.Join(tmpDir, "/etc/fstab")

	mountPoints, err := findMountsFromFstabFile(fstabPath, diskPartitions)
	if err != nil {
		return nil, err
	}

	// Close the rootfs partition mount.
	err = rootfsPartitionMount.CleanClose()
	if err != nil {
		return nil, fmt.Errorf("failed to close rootfs partition mount (%s):\n%w", rootfsPartition.Path, err)
	}

	return mountPoints, nil
}

func findMountsFromFstabFile(fstabPath string, diskPartitions []diskutils.PartitionInfo,
) ([]*safechroot.MountPoint, error) {
	// Read the fstab file.
	fstabEntries, err := diskutils.ReadFstabFile(fstabPath)
	if err != nil {
		return nil, err
	}

	mountPoints, err := fstabEntriesToMountPoints(fstabEntries, diskPartitions)
	if err != nil {
		return nil, err
	}

	return mountPoints, nil
}

func fstabEntriesToMountPoints(fstabEntries []diskutils.FstabEntry, diskPartitions []diskutils.PartitionInfo,
) ([]*safechroot.MountPoint, error) {
	// Convert fstab entries into mount points.
	var mountPoints []*safechroot.MountPoint
	var foundRoot bool
	for _, fstabEntry := range fstabEntries {
		// Ignore special partitions.
		switch fstabEntry.FsType {
		case "devtmpfs", "proc", "sysfs", "devpts", "tmpfs":
			continue
		}

		source, err := findSourcePartition(fstabEntry.Source, diskPartitions)
		if err != nil {
			return nil, err
		}

		var mountPoint *safechroot.MountPoint
		if fstabEntry.Target == "/" {
			mountPoint = safechroot.NewPreDefaultsMountPoint(
				source, fstabEntry.Target, fstabEntry.FsType,
				uintptr(fstabEntry.VfsOptions), fstabEntry.FsOptions)

			foundRoot = true
		} else {
			mountPoint = safechroot.NewMountPoint(
				source, fstabEntry.Target, fstabEntry.FsType,
				uintptr(fstabEntry.VfsOptions), fstabEntry.FsOptions)
		}

		mountPoints = append(mountPoints, mountPoint)
	}

	if !foundRoot {
		return nil, fmt.Errorf("image has invalid fstab file: no root partition found")
	}

	return mountPoints, nil
}

func findSourcePartition(source string, partitions []diskutils.PartitionInfo) (string, error) {
	partUuid, isPartUuid := strings.CutPrefix(source, "PARTUUID=")
	if isPartUuid {
		for _, partition := range partitions {
			if partition.PartUuid == partUuid {
				return partition.Path, nil
			}
		}

		return "", fmt.Errorf("partition not found: %s", source)
	}

	return "", fmt.Errorf("unknown fstab source type: %s", source)
}
