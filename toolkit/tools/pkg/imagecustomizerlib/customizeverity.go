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

	buildDracutModuleArgs := []string{
		"dracut", "-f", "--kver", kernelVersion, "-a",
		// Placeholder for dracut module name.
		"",
	}

	buildDracutModuleArgs[len(buildDracutModuleArgs)-1] = dracutModuleName

	err = imageChroot.Run(func() error {
		_, _, err = shell.Execute("sudo", buildDracutModuleArgs...)
		return err
	})
	if err != nil {
		return fmt.Errorf("failed to build dracut module - (%s):\n%w", dracutModuleName, err)
	}

	return nil
}

func updateMarinerCfgWithInitramfs(imageChroot *safechroot.Chroot) error {
	initramfsPath := filepath.Join("boot", "initramfs-*")

	// Fetch the initramfs file name.
	var initramfsFiles []string
	err := imageChroot.Run(func() error {
		var innerErr error
		initramfsFiles, innerErr = filepath.Glob(initramfsPath)
		return innerErr
	})
	if err != nil {
		return fmt.Errorf("failed to list initramfs file: %w", err)
	}

	// Ensure an initramfs file is found
	if len(initramfsFiles) != 1 {
		return fmt.Errorf("expected one initramfs file, but found %d", len(initramfsFiles))
	}

	newInitramfs := filepath.Base(initramfsFiles[0])

	cfgPath := filepath.Join("boot", "mariner.cfg")

	// Update mariner.cfg to reference the new initramfs
	err = imageChroot.Run(func() error {
		input, innerErr := os.ReadFile(cfgPath)
		if innerErr != nil {
			return fmt.Errorf("failed to read mariner.cfg: %w", innerErr)
		}

		lines := strings.Split(string(input), "\n")
		for i, line := range lines {
			if strings.HasPrefix(line, "mariner_initrd=") {
				lines[i] = "mariner_initrd=" + newInitramfs
			}
		}
		output := strings.Join(lines, "\n")
		return os.WriteFile(cfgPath, []byte(output), 0644)
	})

	return nil
}

func updateGrubConfig(resolvedDataPartition string, resolvedHashPartition string, rootHash string, verityErrorBehavior imagecustomizerapi.VerityErrorBehavior, bootMountDir string) error {
	var err error

	const cmdlineTemplate = "rd.systemd.verity=1 roothash=%s systemd.verity_root_data=%s systemd.verity_root_hash=%s systemd.verity_root_options=%s"
	verityErrorBehaviorString, err := VerityErrorBehaviorToImager(verityErrorBehavior)
	if err != nil {
		return err
	}
	newArgs := fmt.Sprintf(cmdlineTemplate, rootHash, resolvedDataPartition, resolvedHashPartition, verityErrorBehaviorString)
	grubConfigPath := filepath.Join(bootMountDir, "grub2/grub.cfg")

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

// convertToDevicePath takes an NBD device path and a system config device path,
// and converts it to the corresponding NBD partition path.
func convertToNbdDevicePath(nbdDevice, systemDevice string) (string, error) {
	partitionRegex := regexp.MustCompile(`[0-9]+$`)
	partitionNumber := partitionRegex.FindString(systemDevice)

	if partitionNumber == "" {
		return "", fmt.Errorf("failed to extract partition number from %s", systemDevice)
	}

	return fmt.Sprintf("%sp%s", nbdDevice, partitionNumber), nil
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
