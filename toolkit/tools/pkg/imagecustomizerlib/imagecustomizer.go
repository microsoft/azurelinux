// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safeloopback"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safemount"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

const (
	tmpParitionDirName = "tmppartition"
)

var (
	// Version specifies the version of the Mariner Image Customizer tool.
	// The value of this string is inserted during compilation via a linker flag.
	ToolVersion = ""

	bootPartitionRegex   = regexp.MustCompile(`(?m)^search -n -u ([a-zA-Z0-9\-]+) -s$`)
	rootfsPartitionRegex = regexp.MustCompile(`(?m)^set rootdevice=([A-Z]*)=([a-zA-Z0-9\-]+)$`)
)

func CustomizeImageWithConfigFile(buildDir string, configFile string, imageFile string,
	rpmsSources []string, outputImageFile string, outputImageFormat string,
	useBaseImageRpmRepos bool,
) error {
	var err error

	var config imagecustomizerapi.Config
	err = imagecustomizerapi.UnmarshalYamlFile(configFile, &config)
	if err != nil {
		return err
	}

	baseConfigPath, _ := filepath.Split(configFile)

	absBaseConfigPath, err := filepath.Abs(baseConfigPath)
	if err != nil {
		return fmt.Errorf("failed to get absolute path of config file directory:\n%w", err)
	}

	err = CustomizeImage(buildDir, absBaseConfigPath, &config, imageFile, rpmsSources, outputImageFile, outputImageFormat,
		useBaseImageRpmRepos)
	if err != nil {
		return err
	}

	return nil
}

func CustomizeImage(buildDir string, baseConfigPath string, config *imagecustomizerapi.Config, imageFile string,
	rpmsSources []string, outputImageFile string, outputImageFormat string, useBaseImageRpmRepos bool,
) error {
	var err error

	// Validate 'outputImageFormat' value.
	qemuOutputImageFormat, err := toQemuImageFormat(outputImageFormat)
	if err != nil {
		return err
	}

	// Validate config.
	err = validateConfig(baseConfigPath, config)
	if err != nil {
		return fmt.Errorf("invalid image config:\n%w", err)
	}

	// Normalize 'buildDir' path.
	buildDirAbs, err := filepath.Abs(buildDir)
	if err != nil {
		return err
	}

	// Create 'buildDir' directory.
	err = os.MkdirAll(buildDirAbs, os.ModePerm)
	if err != nil {
		return err
	}

	// Convert image file to raw format, so that a kernel loop device can be used to make changes to the image.
	buildImageFile := filepath.Join(buildDirAbs, "image.raw")

	_, _, err = shell.Execute("qemu-img", "convert", "-O", "raw", imageFile, buildImageFile)
	if err != nil {
		return fmt.Errorf("failed to convert image file to raw format:\n%w", err)
	}

	// Customize the raw image file.
	err = customizeImageHelper(buildDirAbs, baseConfigPath, config, buildImageFile, rpmsSources, useBaseImageRpmRepos)
	if err != nil {
		return err
	}

	// Create final output image file.
	outDir := filepath.Dir(outputImageFile)
	os.MkdirAll(outDir, os.ModePerm)

	_, _, err = shell.Execute("qemu-img", "convert", "-O", qemuOutputImageFormat, buildImageFile, outputImageFile)
	if err != nil {
		return fmt.Errorf("failed to convert image file to format: %s:\n%w", outputImageFormat, err)
	}

	return nil
}

func toQemuImageFormat(imageFormat string) (string, error) {
	switch imageFormat {
	case "vhd":
		return "vpc", nil

	case "vhdx", "raw", "qcow2":
		return imageFormat, nil

	default:
		return "", fmt.Errorf("unsupported image format (supported: vhd, vhdx, raw, qcow2): %s", imageFormat)
	}
}

func validateConfig(baseConfigPath string, config *imagecustomizerapi.Config) error {
	var err error

	err = validateSystemConfig(baseConfigPath, &config.SystemConfig)
	if err != nil {
		return err
	}

	return nil
}

func validateSystemConfig(baseConfigPath string, config *imagecustomizerapi.SystemConfig) error {
	var err error

	for sourceFile := range config.AdditionalFiles {
		sourceFileFullPath := filepath.Join(baseConfigPath, sourceFile)
		isFile, err := file.IsFile(sourceFileFullPath)
		if err != nil {
			return fmt.Errorf("invalid AdditionalFiles source file (%s):\n%w", sourceFile, err)
		}

		if !isFile {
			return fmt.Errorf("invalid AdditionalFiles source file (%s): not a file", sourceFile)
		}
	}

	for i, script := range config.PostInstallScripts {
		err = validateScript(baseConfigPath, &script)
		if err != nil {
			return fmt.Errorf("invalid PostInstallScripts item at index %d: %w", i, err)
		}
	}

	for i, script := range config.FinalizeImageScripts {
		err = validateScript(baseConfigPath, &script)
		if err != nil {
			return fmt.Errorf("invalid FinalizeImageScripts item at index %d: %w", i, err)
		}
	}

	return nil
}

func validateScript(baseConfigPath string, script *imagecustomizerapi.Script) error {
	// Ensure that install scripts sit under the config file's parent directory.
	// This allows the install script to be run in the chroot environment by bind mounting the config directory.
	if !filepath.IsLocal(script.Path) {
		return fmt.Errorf("install script (%s) is not under config directory (%s)", script.Path, baseConfigPath)
	}

	// Verify that the file exists.
	fullPath := filepath.Join(baseConfigPath, script.Path)

	scriptStat, err := os.Stat(fullPath)
	if err != nil {
		return fmt.Errorf("couldn't read install script (%s):\n%w", script.Path, err)
	}

	// Verify that the file has an executable bit set.
	if scriptStat.Mode()&0111 == 0 {
		return fmt.Errorf("install script (%s) does not have executable bit set", script.Path)
	}

	return nil
}

func customizeImageHelper(buildDir string, baseConfigPath string, config *imagecustomizerapi.Config,
	buildImageFile string, rpmsSources []string, useBaseImageRpmRepos bool,
) error {
	// Mount the raw disk image file.
	loopback, err := safeloopback.NewLoopback(buildImageFile)
	if err != nil {
		return fmt.Errorf("failed to mount raw disk (%s) as a loopback device:\n%w", buildImageFile, err)
	}
	defer loopback.Close()

	// Look for all the partitions on the image.
	newMountDirectories, mountPoints, err := findPartitions(buildDir, loopback.DevicePath())
	if err != nil {
		return fmt.Errorf("failed to find disk partitions:\n%w", err)
	}

	// Create chroot environment.
	imageChrootDir := filepath.Join(buildDir, "imageroot")

	chrootLeaveOnDisk := false
	imageChroot := safechroot.NewChroot(imageChrootDir, chrootLeaveOnDisk)
	err = imageChroot.Initialize("", newMountDirectories, mountPoints)
	if err != nil {
		return err
	}
	defer imageChroot.Close(chrootLeaveOnDisk)

	// Do the actual customizations.
	err = doCustomizations(buildDir, baseConfigPath, config, imageChroot, rpmsSources, useBaseImageRpmRepos)
	if err != nil {
		return err
	}

	// Close.
	err = imageChroot.Close(chrootLeaveOnDisk)
	if err != nil {
		return err
	}

	err = loopback.CleanClose()
	if err != nil {
		return err
	}

	return nil
}

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
	tmpDir := filepath.Join(buildDir, tmpParitionDirName)

	// Mount the EFI System Partition.
	efiSystemPartitionMount, err := safemount.NewMount(efiSystemPartition.Path, tmpDir, efiSystemPartition.FileSystemType, 0, "", true)
	if err != nil {
		return nil, fmt.Errorf("failed to mount EFI system partition:\n%w", err)
	}
	defer efiSystemPartitionMount.Close()

	// Read the grub.cfg file.
	grubConfigFilePath := filepath.Join(tmpDir, "boot/grub2/grub.cfg")
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

	rootfsPartition, err := tryFindRootfsPartitionFromBootPartition(bootPartition, diskPartitions, buildDir)
	if err != nil {
		return nil, err
	}

	if rootfsPartition == nil {
		return nil, fmt.Errorf("failed to find rootfs partition using boot partition (%s)", bootPartition.Name)
	}

	return rootfsPartition, nil
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
	rootfsPartitionMount, err := safemount.NewMount(rootfsPartition.Path, tmpDir, rootfsPartition.FileSystemType, 0, "", true)
	if err != nil {
		return nil, fmt.Errorf("failed to mount rootfs partition (%s):\n%w", rootfsPartition.Path, err)
	}
	defer rootfsPartitionMount.Close()

	// Read the fstab file.
	fstabPath := filepath.Join(tmpDir, "/etc/fstab")
	fstabEntries, err := diskutils.ReadFstabFile(fstabPath)
	if err != nil {
		return nil, err
	}

	// Close the rootfs partition mount.
	err = rootfsPartitionMount.CleanClose()
	if err != nil {
		return nil, fmt.Errorf("failed to close rootfs partition mount (%s):\n%w", rootfsPartition.Path, err)
	}

	mountPoints, err := fstabEntriesToMountPoints(fstabEntries, diskPartitions)
	if err != nil {
		return nil, err
	}

	return mountPoints, nil
}

func fstabEntriesToMountPoints(fstabEntries []diskutils.FstabEntry, diskPartitions []diskutils.PartitionInfo) ([]*safechroot.MountPoint, error) {
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
