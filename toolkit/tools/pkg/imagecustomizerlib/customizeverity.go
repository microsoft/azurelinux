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

	err = preparePkgDependenciesForVerity(imageChroot)
	if err != nil {
		return false, fmt.Errorf("failed to prepare package dependencies for verity:\n%w", err)
	}

	// Integrate systemd veritysetup dracut module into initramfs img.
	systemdVerityDracutModule := "systemd-veritysetup"
	dmVerityDracutDriver := "dm-verity"
	err = addDracutModule(systemdVerityDracutModule, dmVerityDracutDriver, imageChroot)
	if err != nil {
		return false, fmt.Errorf("failed to add dracut modules for verity:\n%w", err)
	}

	err = updateFstabForVerity(buildDir, imageChroot)
	if err != nil {
		return false, fmt.Errorf("failed to update fstab file for verity:\n%w", err)
	}

	err = prepareGrubConfigForVerity(imageChroot)
	if err != nil {
		return false, fmt.Errorf("failed to prepare grub config files for verity:\n%w", err)
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

func prepareGrubConfigForVerity(imageChroot *safechroot.Chroot) error {
	bootCustomizer, err := NewBootCustomizer(imageChroot)
	if err != nil {
		return err
	}

	err = bootCustomizer.PrepareForVerity()
	if err != nil {
		return err
	}

	err = bootCustomizer.WriteToFile(imageChroot)
	if err != nil {
		return err
	}

	return nil
}

func updateGrubConfigForVerity(dataPartitionIdType imagecustomizerapi.IdType, dataPartitionId string,
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

	newArgs := []string{
		"rd.systemd.verity=1",
		fmt.Sprintf("roothash=%s", rootHash),
		fmt.Sprintf("systemd.verity_root_data=%s", formattedDataPartition),
		fmt.Sprintf("systemd.verity_root_hash=%s", formattedHashPartition),
		fmt.Sprintf("systemd.verity_root_options=%s", formattedCorruptionOption),
	}

	grub2Config, err := file.Read(grubCfgFullPath)
	if err != nil {
		return fmt.Errorf("failed to read grub config:\n%w", err)
	}

	// Note: If grub-mkconfig is being used, then we can't add the verity command-line args to /etc/default/grub and
	// call grub-mkconfig, since this would create a catch-22 with the verity root partition hash.
	// So, instead we just modify the /boot/grub2/grub.cfg file directly.
	grubMkconfigEnabled := isGrubMkconfigConfig(grub2Config)

	grub2Config, err = updateKernelCommandLineArgs(grub2Config, []string{"rd.systemd.verity", "roothash",
		"systemd.verity_root_data", "systemd.verity_root_hash", "systemd.verity_root_options"}, newArgs)
	if err != nil {
		return fmt.Errorf("failed to set verity kernel command line args:\n%w", err)
	}

	if grubMkconfigEnabled {
		grub2Config, err = updateKernelCommandLineArgs(grub2Config, []string{"root"}, []string{"root=/dev/mapper/root"})
		if err != nil {
			return fmt.Errorf("failed to set verity root command-line arg:\n%w", err)
		}
	} else {
		grub2Config, err = replaceSetCommandValue(grub2Config, "rootdevice", "/dev/mapper/root")
		if err != nil {
			return fmt.Errorf("failed to set verity root device:\n%w", err)
		}
	}

	err = file.Write(grub2Config, grubCfgFullPath)
	if err != nil {
		return fmt.Errorf("failed to write updated grub config:\n%w", err)
	}

	return nil
}

// idToPartitionBlockDevicePath returns the block device path for a given idType and id.
func idToPartitionBlockDevicePath(partitionId imagecustomizerapi.IdentifiedPartition,
	diskPartitions []diskutils.PartitionInfo,
) (string, error) {
	// Iterate over each partition to find the matching id.
	for _, partition := range diskPartitions {
		matches, err := partitionMatchesId(partitionId, partition)
		if err != nil {
			return "", err
		}

		if matches {
			return partition.Path, nil
		}
	}

	// If no partition is found with the given id.
	return "", fmt.Errorf("no partition found for %s: %s", partitionId.IdType, partitionId.Id)
}

func partitionMatchesId(partitionId imagecustomizerapi.IdentifiedPartition, partition diskutils.PartitionInfo,
) (bool, error) {
	switch partitionId.IdType {
	case imagecustomizerapi.IdTypePartLabel:
		if partition.PartLabel == partitionId.Id {
			return true, nil
		}
	case imagecustomizerapi.IdTypeUuid:
		if partition.Uuid == partitionId.Id {
			return true, nil
		}
	case imagecustomizerapi.IdTypePartUuid:
		if partition.PartUuid == partitionId.Id {
			return true, nil
		}
	default:
		return true, fmt.Errorf("invalid idType provided (%s)", string(partitionId.IdType))
	}

	return false, nil
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

func preparePkgDependenciesForVerity(imageChroot *safechroot.Chroot) error {
	var err error
	requiredPkgs := []string{"lvm2"}
	var pkgsToInstall []string

	// Iterate over each required package and check if it's installed.
	for _, pkg := range requiredPkgs {
		installed := isPackageInstalled(imageChroot, pkg)
		if err != nil {
			return err
		}
		if !installed {
			// If the package is not installed, add it to the list of packages to install.
			pkgsToInstall = append(pkgsToInstall, pkg)
		}
	}

	// If there are any packages to install, install them.
	if len(pkgsToInstall) > 0 {
		logger.Log.Infof("Installing packages: %v", pkgsToInstall)
		err = installOrUpdatePackages("install", pkgsToInstall, imageChroot)
		if err != nil {
			return err
		}
	}

	return nil
}
