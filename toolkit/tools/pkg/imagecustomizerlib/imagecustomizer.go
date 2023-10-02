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
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safemount.go"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

var (
	rootfsPartitionRegex = regexp.MustCompile(`(?m)^search -n -u ([a-zA-Z0-9\-]+) -s$`)
)

func CustomizeImageWithConfigFile(buildDir string, configFile string, imageFile string,
	outputImageFile string, outputImageFormat string,
) error {
	var err error

	var config imagecustomizerapi.SystemConfig
	err = imagecustomizerapi.UnmarshalYamlFile(configFile, &config)
	if err != nil {
		return err
	}

	baseConfigPath, _ := filepath.Split(configFile)

	err = CustomizeImage(buildDir, baseConfigPath, &config, imageFile, outputImageFile, outputImageFormat)
	if err != nil {
		return err
	}

	return nil
}

func CustomizeImage(buildDir string, baseConfigPath string, config *imagecustomizerapi.SystemConfig, imageFile string,
	outputImageFile string, outputImageFormat string,
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
	err = customizeImageHelper(buildDirAbs, baseConfigPath, config, buildImageFile)
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

func validateConfig(baseConfigPath string, config *imagecustomizerapi.SystemConfig) error {
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

func customizeImageHelper(buildDir string, baseConfigPath string, config *imagecustomizerapi.SystemConfig,
	buildImageFile string,
) error {
	// Mount the raw disk image file.
	diskDevPath, err := diskutils.SetupLoopbackDevice(buildImageFile)
	if err != nil {
		return fmt.Errorf("failed to mount raw disk (%s) as a loopback device:\n%w", buildImageFile, err)
	}
	defer diskutils.DetachLoopbackDevice(diskDevPath)

	// Wait for the partitions to show up.
	err = diskutils.WaitForDevicesToSettle()
	if err != nil {
		return err
	}

	// Look for all the partitions on the image.
	newMountDirectories, mountPoints, err := findPartitions(buildDir, diskDevPath)
	if err != nil {
		return fmt.Errorf("failed to find disk partitions:\n%w", err)
	}

	// Create chroot environment.
	imageChrootDir := filepath.Join(buildDir, "imageroot")

	imageChroot := safechroot.NewChroot(imageChrootDir, false)
	err = imageChroot.Initialize("", newMountDirectories, mountPoints)
	if err != nil {
		return err
	}
	defer imageChroot.Close(false)

	// Do the actual customizations.
	err = doCustomizations(baseConfigPath, config, imageChroot)
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

	// Look for the boot partition (i.e. EFI system partition).
	var efiSystemPartition *diskutils.PartitionInfo
	for _, diskPartition := range diskPartitions {
		if diskPartition.PartitionTypeUuid == diskutils.EfiSystemPartitionUuid {
			efiSystemPartition = &diskPartition
			break
		}
	}

	if efiSystemPartition == nil {
		return nil, nil, fmt.Errorf("failed to find EFI system partition (%s)", diskDevice)
	}

	// Mount the boot partition.
	tmpDir := filepath.Join(buildDir, "tmppartition")

	efiSystemPartitionMount, err := safemount.NewMount(efiSystemPartition.Path, tmpDir, efiSystemPartition.FileSystemType, 0, "", true)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to mount EFI system partition:\n%w", err)
	}
	defer efiSystemPartitionMount.Close()

	// Read the grub.cfg file.
	grubConfigFilePath := filepath.Join(tmpDir, "boot/grub2/grub.cfg")
	grubConfigFile, err := os.ReadFile(grubConfigFilePath)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to read grub.cfg file:\n%w", err)
	}

	// Close the boot partition mount.
	err = efiSystemPartitionMount.Close()
	if err != nil {
		return nil, nil, fmt.Errorf("failed to close EFI system partition mount:\n%w", err)
	}

	// Look for the rootfs declaration line in the grub.cfg file.
	match := rootfsPartitionRegex.FindStringSubmatch(string(grubConfigFile))
	if match == nil {
		return nil, nil, fmt.Errorf("failed to find rootfs partition in grub.cfg file")
	}

	rootfsUuid := match[1]

	var rootfsPartition *diskutils.PartitionInfo
	for _, diskPartition := range diskPartitions {
		if diskPartition.Uuid == rootfsUuid {
			rootfsPartition = &diskPartition
			break
		}
	}

	// Temporarily mount the rootfs partition so that the fstab file can be read.
	rootfsPartitionMount, err := safemount.NewMount(rootfsPartition.Path, tmpDir, rootfsPartition.FileSystemType, 0, "", true)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to mount rootfs partition:\n%w", err)
	}
	defer rootfsPartitionMount.Close()

	// Read the fstab file.
	fstabPath := filepath.Join(tmpDir, "/etc/fstab")
	fstabEntries, err := diskutils.ReadFstabFile(fstabPath)
	if err != nil {
		return nil, nil, err
	}

	// Close the rootfs partition mount.
	err = rootfsPartitionMount.Close()
	if err != nil {
		return nil, nil, fmt.Errorf("failed to close rootfs partition mount:\n%w", err)
	}

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
			return nil, nil, err
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
		return nil, nil, fmt.Errorf("image has invalid fstab file: no root partition found")
	}

	return nil, mountPoints, nil
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
