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
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

func enableVerityPartition(imageChroot *safechroot.Chroot) error {
	var err error

	// Integrate systemd veritysetup dracut module into initramfs img.
	systemdVerityDracutModule := "systemd-veritysetup"
	err = buildDracutModule(systemdVerityDracutModule, imageChroot)
	if err != nil {
		return err
	}

	// Update mariner config file with the new generated initramfs file.
	err = updateMarinerCfgWithInitramfs(imageChroot)
	if err != nil {
		return err
	}

	return nil
}

func buildDracutModule(dracutModuleName string, imageChroot *safechroot.Chroot) error {
	var err error

	// This function will be run inside the chroot to list kernel files in /boot
	listKernels := func() ([]string, error) {
		var kernels []string
		// Assuming the vmlinuz files are located in /boot
		files, err := filepath.Glob("/boot/vmlinuz-*")
		if err != nil {
			return nil, err
		}
		for _, file := range files {
			kernels = append(kernels, filepath.Base(file))
		}
		return kernels, nil
	}

	var kernelFiles []string
	err = imageChroot.Run(func() error {
		kernelFiles, err = listKernels()
		return err
	})
	if err != nil {
		return fmt.Errorf("failed to list kernels in chroot: %w", err)
	}

	if len(kernelFiles) == 0 {
		return fmt.Errorf("no kernels found in chroot environment")
	}

	// Extract the version from the kernel filename (e.g., vmlinuz-5.15.131.1-2.cm2 -> 5.15.131.1-2.cm2)
	kernelVersion := strings.TrimPrefix(kernelFiles[0], "vmlinuz-")

	err = imageChroot.Run(func() error {
		// TODO: Config Dracut module systemd-veritysetup.
		err = shell.ExecuteLiveWithErr(1, "dracut", "-f", "--kver", kernelVersion, "-a", dracutModuleName)
		return err
	})
	if err != nil {
		return fmt.Errorf("failed to build dracut module - (%s):\n%w", dracutModuleName, err)
	}

	return nil
}

func updateMarinerCfgWithInitramfs(imageChroot *safechroot.Chroot) error {
	var err error

	initramfsPath := filepath.Join(imageChroot.RootDir(), "boot/initramfs-*")
	// Fetch the initramfs file name.
	var initramfsFiles []string
	initramfsFiles, err = filepath.Glob(initramfsPath)
	if err != nil {
		return fmt.Errorf("failed to list initramfs file: %w", err)
	}

	// Ensure an initramfs file is found
	if len(initramfsFiles) != 1 {
		return fmt.Errorf("expected one initramfs file, but found %d", len(initramfsFiles))
	}

	newInitramfs := filepath.Base(initramfsFiles[0])

	cfgPath := filepath.Join(imageChroot.RootDir(), "boot/mariner.cfg")
	// Update mariner.cfg to reference the new initramfs
	input, err := os.ReadFile(cfgPath)
	if err != nil {
		return fmt.Errorf("failed to read mariner.cfg: %w", err)
	}

	lines := strings.Split(string(input), "\n")
	for i, line := range lines {
		if strings.HasPrefix(line, "mariner_initrd=") {
			lines[i] = "mariner_initrd=" + newInitramfs
		}
	}
	output := strings.Join(lines, "\n")
	os.WriteFile(cfgPath, []byte(output), 0644)

	return nil
}

func updateGrubConfig(dataPartitionIdType imagecustomizerapi.IdType, dataPartitionId string, hashPartitionIdType imagecustomizerapi.IdType, hashPartitionId string, rootHash string, grubCfgFullPath string) error {
	var err error

	const cmdlineTemplate = "rd.systemd.verity=1 roothash=%s systemd.verity_root_data=%s systemd.verity_root_hash=%s systemd.verity_root_options=panic-on-corruption"
	// Format the dataPartitionId and hashPartitionId using the helper function.
	formattedDataPartitionPlaceHolder, err := systemdFormatPartitionId(dataPartitionIdType, dataPartitionId)
	if err != nil {
		return err
	}
	formattedHashPartitionPlaceHolder, err := systemdFormatPartitionId(hashPartitionIdType, hashPartitionId)
	if err != nil {
		return err
	}

	newArgs := fmt.Sprintf(cmdlineTemplate, rootHash, formattedDataPartitionPlaceHolder, formattedHashPartitionPlaceHolder)

	content, err := os.ReadFile(grubCfgFullPath)
	if err != nil {
		return fmt.Errorf("failed to read grub config: %v", err)
	}

	// Split the content into lines for processing
	lines := strings.Split(string(content), "\n")
	var updatedLines []string

	for _, line := range lines {
		trimmedLine := strings.TrimSpace(line)
		if strings.HasPrefix(trimmedLine, "linux ") {
			// Append new arguments to the line that starts with "linux"
			line += " " + newArgs
		}
		if strings.HasPrefix(trimmedLine, "set rootdevice=PARTUUID=") {
			// Replace the root device line with the new root device. TODO: add supported type 'user'
			line = "set rootdevice=/dev/mapper/root"
		}
		updatedLines = append(updatedLines, line)
	}

	// Write the updated content back to grub.cfg
	err = os.WriteFile(grubCfgFullPath, []byte(strings.Join(updatedLines, "\n")), 0644)
	if err != nil {
		return fmt.Errorf("failed to write updated grub config: %v", err)
	}

	return nil
}

// idToPartitionBlockDevicePath returns the block device path for a given idType and id.
func idToPartitionBlockDevicePath(idType imagecustomizerapi.IdType, id string, nbdDevice string, diskPartitions []diskutils.PartitionInfo) (string, error) {
	imagerIdType, err := IdTypeToImager(idType)
	if err != nil {
		return "", err
	}

	// Create a regular expression to find the last number in the id string.
	partitionRegex := regexp.MustCompile(`\d+$`)

	// Iterate over each partition to find the matching id.
	for _, partition := range diskPartitions {
		switch imagerIdType {
		case "Partition":
			// Find the partition number in the provided id.
			partNum := partitionRegex.FindString(id)
			if partNum == "" {
				return "", fmt.Errorf("no partition number found in id: %s", id)
			}

			// Construct the expected partition name.
			expectedPartitionName := fmt.Sprintf("%sp%s", nbdDevice, partNum)

			// Check if the constructed name matches the partition name.
			if partition.Path == expectedPartitionName {
				return partition.Path, nil
			}
		case "PartLabel":
			if partition.PartLabel == id {
				return partition.Path, nil
			}
		case "Uuid":
			if partition.Uuid == id {
				return partition.Path, nil
			}
		case "PartUuid":
			if partition.PartUuid == id {
				return partition.Path, nil
			}
		default:
			return "", fmt.Errorf("invalid idType provided (%s)", imagerIdType)
		}
	}

	// If no partition is found with the given id.
	return "", fmt.Errorf("no partition found for %s: %s", idType, id)
}

// systemdFormatPartitionId formats the partition ID based on the ID type following systemd dm-verity style.
func systemdFormatPartitionId(idType imagecustomizerapi.IdType, id string) (string, error) {
	imagerIdType, err := IdTypeToImager(idType)
	if err != nil {
		return "", err
	}

	switch imagerIdType {
	case "Partition":
		return id, nil
	// case imagecustomizerapi.ID: // Ignored for now.
	case "PartLabel", "Uuid", "PartUuid":
		return fmt.Sprintf("%s=%s", strings.ToUpper(imagerIdType), id), nil
	default:
		return "", fmt.Errorf("invalid idType provided (%s)", imagerIdType)
	}
}

// findFreeNBDDevice finds the first available NBD device.
func findFreeNBDDevice() (string, error) {
	files, err := filepath.Glob("/sys/class/block/nbd*")
	if err != nil {
		return "", err
	}

	for _, file := range files {
		// Check if the pid file exists. If it does not exist, the device is likely free.
		pidFile := filepath.Join(file, "pid")
		if _, err := os.Stat(pidFile); os.IsNotExist(err) {
			return "/dev/" + filepath.Base(file), nil
		}
	}

	return "", fmt.Errorf("no free nbd devices available")
}
