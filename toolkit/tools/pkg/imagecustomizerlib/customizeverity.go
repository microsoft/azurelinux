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
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

func enableVerityPartition(verity *imagecustomizerapi.Verity, imageChroot *safechroot.Chroot) error {
	var err error

	if verity == nil {
		return nil
	}

	// Integrate systemd veritysetup dracut module into initramfs img.
	systemdVerityDracutModule := "systemd-veritysetup"
	dmVerityDracutDriver := "dm-verity"
	err = buildDracutModule(systemdVerityDracutModule, dmVerityDracutDriver, imageChroot)
	if err != nil {
		return err
	}

	return nil
}

func buildDracutModule(dracutModuleName string, dracutDriverName string, imageChroot *safechroot.Chroot) error {
	var err error

	listKernels := func() ([]string, error) {
		var kernels []string
		// Use RootDir to get the path on the host OS
		bootDir := filepath.Join(imageChroot.RootDir(), "boot")
		files, err := filepath.Glob(filepath.Join(bootDir, "vmlinuz-*"))
		if err != nil {
			return nil, err
		}
		for _, file := range files {
			kernels = append(kernels, filepath.Base(file))
		}
		return kernels, nil
	}

	kernelFiles, err := listKernels()
	if err != nil {
		return fmt.Errorf("failed to list kernels: %w", err)
	}

	if len(kernelFiles) != 1 {
		return fmt.Errorf("expected one kernel file, but found %d", len(kernelFiles))
	}

	// Extract the version from the kernel filename (e.g., vmlinuz-5.15.131.1-2.cm2 -> 5.15.131.1-2.cm2)
	kernelVersion := strings.TrimPrefix(kernelFiles[0], "vmlinuz-")

	dracutConfigFile := filepath.Join(imageChroot.RootDir(), "etc", "dracut.conf.d", dracutModuleName+".conf")

	// Check if the dracut module configuration file already exists.
	if _, err := os.Stat(dracutConfigFile); os.IsNotExist(err) {
		lines := []string{
			"add_dracutmodules+=\" " + dracutModuleName + " \"",
			"add_drivers+=\" " + dracutDriverName + " \"",
		}
		err = file.WriteLines(lines, dracutConfigFile)
		if err != nil {
			return fmt.Errorf("failed to write to dracut module config file (%s): %w", dracutConfigFile, err)
		}
	}

	err = imageChroot.Run(func() error {
		initrdImagePath := "/boot/initrd.img-" + kernelVersion
		err = shell.ExecuteLiveWithErr(1, "mkinitrd", "-f", initrdImagePath, kernelVersion)
		return err
	})
	if err != nil {
		return fmt.Errorf("failed to build initrd img for kernel - (%s):\n%w", kernelVersion, err)
	}

	return nil
}

func updateGrubConfig(dataPartitionIdType imagecustomizerapi.IdType, dataPartitionId string,
	hashPartitionIdType imagecustomizerapi.IdType, hashPartitionId string, rootHash string, grubCfgFullPath string,
) error {
	var err error

	// Format the dataPartitionId and hashPartitionId using the helper function.
	formattedDataPartition, err := systemdFormatPartitionId(dataPartitionIdType, dataPartitionId)
	if err != nil {
		return err
	}
	formattedHashPartition, err := systemdFormatPartitionId(hashPartitionIdType, hashPartitionId)
	if err != nil {
		return err
	}

	newArgs := fmt.Sprintf(
		"rd.systemd.verity=1 roothash=%s systemd.verity_root_data=%s systemd.verity_root_hash=%s systemd.verity_root_options=panic-on-corruption",
		rootHash, formattedDataPartition, formattedHashPartition,
	)

	// Read grub.cfg using the internal method
	lines, err := file.ReadLines(grubCfgFullPath)
	if err != nil {
		return fmt.Errorf("failed to read grub config: %v", err)
	}

	var updatedLines []string
	linuxLineRegex := regexp.MustCompile(`^linux .*rd.systemd.verity=(1|0).*`)
	for _, line := range lines {
		trimmedLine := strings.TrimSpace(line)
		if linuxLineRegex.MatchString(trimmedLine) {
			// Replace existing arguments
			verityRegexPattern := `rd.systemd.verity=(1|0)` +
				`( roothash=[^ ]*)?` +
				`( systemd.verity_root_data=[^ ]*)?` +
				`( systemd.verity_root_hash=[^ ]*)?` +
				`( systemd.verity_root_options=[^ ]*)?`
			verityRegex := regexp.MustCompile(verityRegexPattern)
			newLinuxLine := verityRegex.ReplaceAllString(trimmedLine, newArgs)
			updatedLines = append(updatedLines, newLinuxLine)
		} else if strings.HasPrefix(trimmedLine, "linux ") {
			// Append new arguments
			updatedLines = append(updatedLines, line+" "+newArgs)
		} else if strings.HasPrefix(trimmedLine, "set rootdevice=PARTUUID=") {
			line = "set rootdevice=/dev/mapper/root"
			updatedLines = append(updatedLines, line)
		} else {
			// Add other lines unchanged
			updatedLines = append(updatedLines, line)
		}
	}

	err = file.WriteLines(updatedLines, grubCfgFullPath)
	if err != nil {
		return fmt.Errorf("failed to write updated grub config: %v", err)
	}

	return nil
}

// idToPartitionBlockDevicePath returns the block device path for a given idType and id.
func idToPartitionBlockDevicePath(idType imagecustomizerapi.IdType, id string, nbdDevice string, diskPartitions []diskutils.PartitionInfo) (string, error) {
	// Iterate over each partition to find the matching id.
	for _, partition := range diskPartitions {
		switch idType {
		case imagecustomizerapi.IdTypePartLabel:
			if partition.PartLabel == id {
				return partition.Path, nil
			}
		case imagecustomizerapi.IdTypeUuid:
			if partition.Uuid == id {
				return partition.Path, nil
			}
		case imagecustomizerapi.IdTypePartUuid:
			if partition.PartUuid == id {
				return partition.Path, nil
			}
		default:
			return "", fmt.Errorf("invalid idType provided (%s)", string(idType))
		}
	}

	// If no partition is found with the given id.
	return "", fmt.Errorf("no partition found for %s: %s", idType, id)
}

// systemdFormatPartitionId formats the partition ID based on the ID type following systemd dm-verity style.
func systemdFormatPartitionId(idType imagecustomizerapi.IdType, id string) (string, error) {
	switch idType {
	case imagecustomizerapi.IdTypePartLabel, imagecustomizerapi.IdTypeUuid, imagecustomizerapi.IdTypePartUuid:
		return fmt.Sprintf("%s=%s", strings.ToUpper(string(idType)), id), nil
	default:
		return "", fmt.Errorf("invalid idType provided (%s)", string(idType))
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
