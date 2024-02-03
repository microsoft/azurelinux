// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/installutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safemount"
)

var (
	bootPartitionRegex   = regexp.MustCompile(`(?m)^search -n -u ([a-zA-Z0-9\-]+) -s$`)
	rootfsPartitionRegex = regexp.MustCompile(`(?m)^set rootdevice=([A-Z]*)=([a-zA-Z0-9\-]+)$`)
)

func findPartitions(buildDir string, diskDevice string) ([]string, []*safechroot.MountPoint, error) {
	var err error

	diskPartitions, err := diskutils.GetDiskPartitions(diskDevice)
	if err != nil {
		return nil, nil, err
	}

	systemBootPartition, err := findSystemBootPartition(diskPartitions)
	if err != nil {
		return nil, nil, err
	}

	var rootfsPartition *diskutils.PartitionInfo

	switch systemBootPartition.PartitionTypeUuid {
	case diskutils.EfiSystemPartitionTypeUuid:
		rootfsPartition, err = findRootfsPartitionFromEsp(systemBootPartition, diskPartitions, buildDir)
		if err != nil {
			return nil, nil, err
		}

	case diskutils.BiosBootPartitionTypeUuid:
		rootfsPartition, err = findRootfsPartitionFromBiosBootPartition(systemBootPartition, diskPartitions, buildDir)
		if err != nil {
			return nil, nil, err
		}
	}

	mountPoints, err := findMountsFromRootfs(rootfsPartition, diskPartitions, buildDir)
	if err != nil {
		return nil, nil, err
	}

	return nil, mountPoints, nil
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

func findRootfsPartitionFromEsp(efiSystemPartition *diskutils.PartitionInfo, diskPartitions []diskutils.PartitionInfo, buildDir string) (*diskutils.PartitionInfo, error) {
	var bootPartition *diskutils.PartitionInfo
	bootPartition, err := findBootPartitionFromEsp(efiSystemPartition, diskPartitions, buildDir)

	rootfsPartition, err := tryFindRootfsPartitionFromBootPartition(bootPartition, diskPartitions, buildDir)
	if err != nil {
		return nil, err
	}

	if rootfsPartition == nil {
		return nil, fmt.Errorf("failed to find rootfs partition using boot partition (%s)", bootPartition.Name)
	}

	return rootfsPartition, nil
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
		return nil, fmt.Errorf("failed to read grub.cfg file:\n%w", err)
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

func findRootfsPartitionFromBiosBootPartition(biosBootLoaderPartition *diskutils.PartitionInfo,
	diskPartitions []diskutils.PartitionInfo, buildDir string,
) (*diskutils.PartitionInfo, error) {

	// The BIOS boot parition is just an executable blob that is uniquely built for each system/disk.
	// So, there is not much that can be done to reliably extract the boot loader partition from it.
	// So, instead, find the boot partition through brute force.

	var rootfsPartitions []*diskutils.PartitionInfo
	for i := range diskPartitions {
		diskPartition := diskPartitions[i]

		switch diskPartition.FileSystemType {
		case "ext4", "vfat", "xfs":

		default:
			// Skips file system types that aren't known to support the boot loader partition.
			// (This list may be incomplete.)
			continue
		}

		rootfsPartition, err := tryFindRootfsPartitionFromBootPartition(&diskPartition, diskPartitions, buildDir)
		if err != nil {
			return nil, err
		}

		if rootfsPartition != nil {
			rootfsPartitions = append(rootfsPartitions, rootfsPartition)
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

func tryFindRootfsPartitionFromBootPartition(bootPartition *diskutils.PartitionInfo,
	diskPartitions []diskutils.PartitionInfo, buildDir string,
) (*diskutils.PartitionInfo, error) {
	tmpDir := filepath.Join(buildDir, tmpParitionDirName)

	// Temporarily mount the partition.
	partitionMount, err := safemount.NewMount(bootPartition.Path, tmpDir, bootPartition.FileSystemType, 0, "", true)
	if err != nil {
		return nil, fmt.Errorf("failed to mount partition (%s):\n%w", bootPartition.Path, err)
	}
	defer partitionMount.Close()

	// Check if grub exists on the file system.
	var rootfsPartition *diskutils.PartitionInfo
	for _, grubCfgPath := range []string{"boot/grub2/grub.cfg", "grub2/grub.cfg"} {
		grubCfgFullPath := filepath.Join(tmpDir, grubCfgPath)

		grubCfgExists, err := file.PathExists(grubCfgFullPath)
		if err != nil {
			return nil, fmt.Errorf("failed to stat file (%s):\n%w", grubCfgFullPath, err)
		}

		if grubCfgExists {
			rootfsPartition, err = findRootfsPartitionFromGrubCfgFile(grubCfgFullPath, diskPartitions)
			if err != nil {
				return nil, err
			}

			break
		}
	}

	err = partitionMount.CleanClose()
	if err != nil {
		return nil, fmt.Errorf("failed to unmount partition (%s):\n%w", bootPartition.Path, err)
	}

	return rootfsPartition, nil
}

func findRootfsPartitionFromGrubCfgFile(grubCfgFilePath string, diskPartitions []diskutils.PartitionInfo) (*diskutils.PartitionInfo, error) {
	// Read the grub.cfg file.
	grubConfigFile, err := os.ReadFile(grubCfgFilePath)
	if err != nil {
		return nil, fmt.Errorf("failed to read grub.cfg file:\n%w", err)
	}

	// Look for the root partition declaration line in the grub.cfg file.
	match := rootfsPartitionRegex.FindStringSubmatch(string(grubConfigFile))
	if match == nil {
		return nil, fmt.Errorf("failed to find rootfs partition in grub.cfg file")
	}

	rootfsType := match[1]
	rootfsId := match[2]

	// Search for the partition in the list of partitions.
	var rootfsPartition *diskutils.PartitionInfo
	for i := range diskPartitions {
		diskPartition := diskPartitions[i]

		var found bool
		switch rootfsType {
		case "UUID":
			found = diskPartition.Uuid == rootfsId

		case "PARTUUID":
			found = diskPartition.PartUuid == rootfsId

		case "PARTLABEL":
			found = diskPartition.PartLabel == rootfsId

		default:
			return nil, fmt.Errorf("unknown rootdevice target type (%s) in grub.cfg (%s)", rootfsType, grubConfigFile)
		}

		if found {
			rootfsPartition = &diskPartition
			break
		}
	}

	if rootfsPartition == nil {
		return nil, fmt.Errorf("failed to find rootfs partition (%s=%s)", rootfsType, rootfsId)
	}

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
				uintptr(fstabEntry.Options), fstabEntry.FsOptions)

			foundRoot = true
		} else {
			mountPoint = safechroot.NewMountPoint(
				source, fstabEntry.Target, fstabEntry.FsType,
				uintptr(fstabEntry.Options), fstabEntry.FsOptions)
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
