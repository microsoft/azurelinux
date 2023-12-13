// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

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

func updateGrubConfig(resolvedDataPartition string, resolvedHashPartition string, rootHash string, imageChroot *safechroot.Chroot) error {
	var err error

	const cmdlineTemplate = "rd.systemd.verity=1 roothash=%s systemd.verity_root_data=%s systemd.verity_root_hash=%s systemd.verity_root_options=ignore-corruption"
	newArgs := fmt.Sprintf(cmdlineTemplate, rootHash, resolvedDataPartition, resolvedHashPartition)
	grubConfigPath := filepath.Join(imageChroot.RootDir(), "boot/grub2/grub.cfg")

	content, err := os.ReadFile(grubConfigPath)
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
	err = os.WriteFile(grubConfigPath, []byte(strings.Join(updatedLines, "\n")), 0644)
	if err != nil {
		return fmt.Errorf("failed to write updated grub config: %v", err)
	}

	return nil
}

// findDeviceByUUIDOrLabel attempts to resolve a PARTUUID, PARTLABEL, UUID, or LABEL to a device file.
func findDeviceByUUIDOrLabel(uuidOrLabel string) (string, error) {
	// Error if the input is already a device path
	if strings.HasPrefix(uuidOrLabel, "/dev/") {
		return uuidOrLabel, nil
	}

	// Resolve UUIDs and LABELs
	for _, dir := range []string{"by-partuuid", "by-partlabel", "by-uuid", "by-label"} {
		devicePath, err := filepath.EvalSymlinks(filepath.Join("/dev/disk", dir, uuidOrLabel))
		if err == nil {
			return devicePath, nil
		}
	}
	return "", fmt.Errorf("device with UUID, LABEL, PARTUUID, or PARTLABEL '%s' not found", uuidOrLabel)
}
