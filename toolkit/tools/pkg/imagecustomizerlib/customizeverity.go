// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
)

func enableVerityPartition(buildDir string, verity *imagecustomizerapi.Verity, imageChroot *safechroot.Chroot,
) (bool, error) {
	var err error

	if verity == nil {
		return false, nil
	}

	logger.Log.Infof("Enable verity")

	// Integrate systemd veritysetup dracut module into initramfs img.
	systemdVerityDracutModule := "systemd-veritysetup"
	dmVerityDracutDriver := "dm-verity"
	err = addDracutModule(systemdVerityDracutModule, dmVerityDracutDriver, imageChroot)
	if err != nil {
		return false, err
	}

	err = updateFstabForVerity(buildDir, imageChroot)
	if err != nil {
		return false, err
	}

	return true, nil
}

func addDracutModule(dracutModuleName string, dracutDriverName string, imageChroot *safechroot.Chroot) error {
	dracutConfigFile := filepath.Join(imageChroot.RootDir(), "etc", "dracut.conf.d", dracutModuleName+".conf")

	// Check if the dracut module configuration file already exists.
	if _, err := os.Stat(dracutConfigFile); os.IsNotExist(err) {
		lines := []string{
			// Add white spaces on both sides for dracut config syntax.
			"add_dracutmodules+=\" " + dracutModuleName + " \"",
			"add_drivers+=\" " + dracutDriverName + " \"",
		}
		err = file.WriteLines(lines, dracutConfigFile)
		if err != nil {
			return fmt.Errorf("failed to write to dracut module config file (%s): %w", dracutConfigFile, err)
		}
	}

	return nil
}

func updateFstabForVerity(buildDir string, imageChroot *safechroot.Chroot) error {
	var err error

	fstabFile := filepath.Join(imageChroot.RootDir(), "etc", "fstab")
	fstabEntries, err := diskutils.ReadFstabFile(fstabFile)
	if err != nil {
		return fmt.Errorf("failed to read fstab file: %v", err)
	}

	var updatedEntries []diskutils.FstabEntry
	for _, entry := range fstabEntries {
		if entry.Target == "/" {
			// Replace existing root partition line with the Verity target.
			entry.Source = "/dev/mapper/root"
			entry.Options = "ro," + entry.Options
		}
		updatedEntries = append(updatedEntries, entry)
	}

	// Write the updated fstab entries back to the fstab file
	err = diskutils.WriteFstabFile(updatedEntries, fstabFile)
	if err != nil {
		return err
	}

	return nil
}

func updateGrubConfig(dataPartitionIdType imagecustomizerapi.IdType, dataPartitionId string,
	hashPartitionIdType imagecustomizerapi.IdType, hashPartitionId string,
	corruptionOption imagecustomizerapi.CorruptionOption, rootHash string, grubCfgFullPath string,
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

	formattedCorruptionOption, err := systemdFormatCorruptionOption(corruptionOption)
	if err != nil {
		return err
	}

	newArgs := fmt.Sprintf(
		"rd.systemd.verity=1 roothash=%s systemd.verity_root_data=%s systemd.verity_root_hash=%s systemd.verity_root_options=%s",
		rootHash, formattedDataPartition, formattedHashPartition, formattedCorruptionOption,
	)

	grub2Config, err := file.Read(grubCfgFullPath)
	if err != nil {
		return fmt.Errorf("failed to read grub config:\n%w", err)
	}

	grub2Config, err = updateKernelCommandLineArguments(grub2Config, []string{"rd.systemd.verity", "roothash",
		"systemd.verity_root_data", "systemd.verity_root_hash", "systemd.verity_root_options"}, newArgs)
	if err != nil {
		return fmt.Errorf("failed to set verity kernel command line args:\n%w", err)
	}

	grub2Config, err = replaceSetCommandValue(grub2Config, "rootdevice", "/dev/mapper/root")
	if err != nil {
		return fmt.Errorf("failed to set verity root device:\n%w", err)
	}

	err = file.Write(grub2Config, grubCfgFullPath)
	if err != nil {
		return fmt.Errorf("failed to write updated grub config:\n%w", err)
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
	case imagecustomizerapi.IdTypePartLabel:
		return fmt.Sprintf("%s=%s", "PARTLABEL", id), nil
	case imagecustomizerapi.IdTypeUuid:
		return fmt.Sprintf("%s=%s", "UUID", id), nil
	case imagecustomizerapi.IdTypePartUuid:
		return fmt.Sprintf("%s=%s", "PARTUUID", id), nil
	default:
		return "", fmt.Errorf("invalid idType provided (%s)", string(idType))
	}
}

func systemdFormatCorruptionOption(corruptionOption imagecustomizerapi.CorruptionOption) (string, error) {
	switch corruptionOption {
	case imagecustomizerapi.CorruptionOptionDefault, imagecustomizerapi.CorruptionOptionIoError:
		return "", nil
	case imagecustomizerapi.CorruptionOptionIgnore:
		return "ignore-corruption", nil
	case imagecustomizerapi.CorruptionOptionPanic:
		return "panic-on-corruption", nil
	case imagecustomizerapi.CorruptionOptionRestart:
		return "restart-on-corruption", nil
	default:
		return "", fmt.Errorf("invalid corruptionOption provided (%s)", string(corruptionOption))
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
