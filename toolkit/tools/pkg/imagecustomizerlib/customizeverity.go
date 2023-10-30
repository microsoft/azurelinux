// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Final logic in this module

package imagecustomizerlib

import (
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerapi"
)

const cmdlineTemplate = "rd.systemd.verity=1 roothash=%s systemd.verity_root_data=/dev/sda3 systemd.verity_root_hash=/dev/sda6 systemd.verity_root_options=restart-on-corruption rootflags=noload"

func enableVerityPartition(baseConfigPath string, VerityPartition string, imageChroot *safechroot.Chroot) error {
	var err error

	if VerityPartition != "root" && VerityPartition != "user" {
		return fmt.Errorf("invalid VerityPartition: %s. It should be either 'root' or 'user'", VerityPartition)
	}

	// Upgrade systemd to version 254-3
	// This can be done through system config yaml, however, we can give a check here.
	minRequiredVersion := "254.3" // Extracted from "254-3" to make comparison easier.
	err := validateSystemdVersion(imageChroot, minRequiredVersion)
	if err != nil {
		return err
	}

	// Install rpm dependency for veritysetup
	// This can also be done through system config
	// Check if veritysetup rpm is installed
	if !isRpmInstalled(imageChroot, "veritysetup") {
		return fmt.Errorf("veritysetup rpm is not installed")
	}

	// Integrate systemd veritysetup dracut module into initramfs
	if err := runDracutInChroot(imageChroot); err != nil {
		return err
	}

	// Modify mariner.cfg to reference the newly generated initramfs
	newInitramfs, err := findNewInitramfs(imageChroot)
	if err != nil {
		return err
	}

	if err := updateMarinerCfg(imageChroot, newInitramfs); err != nil {
		return err
	}

	// Obtain the UUID for the root or user partitions using MIC

	// Extract the UUID of the hash device

	// Acquire the root hash in veritysetup format from the nbd mount status

	// chroot into the boot partition to modify or add kernel cmdline arguments
	// Assuming the grub config file is located at /boot/grub2/grub.cfg inside the chroot environment.
    grubConfigPath := filepath.Join(imageChroot.Dir(), "boot", "grub2", "grub.cfg")

    err = modifyGrubConfig(grubConfigPath, rootHash) // replace rootHash with the variable holding the root hash value
    if err != nil {
        return fmt.Errorf("failed to modify grub config: %w", err)
    }

	// Return nil
	return nil
}

func getSystemdVersion(imageChroot *safechroot.Chroot) (string, error) {
	// Run the command to get systemd version inside chroot.
	cmd := exec.Command("chroot", imageChroot.Dir(), "systemctl", "--version")
	output, err := cmd.CombinedOutput()
	if err != nil {
		return "", fmt.Errorf("failed to get systemd version: %v", err)
	}

	// Extract the version from the command output.
	versionLine := strings.SplitN(string(output), "\n", 2)[0]
	versionParts := strings.Split(versionLine, " ")
	if len(versionParts) < 2 {
		return "", fmt.Errorf("unexpected format for systemd version output: %s", versionLine)
	}
	return versionParts[1], nil
}

func validateSystemdVersion(imageChroot *safechroot.Chroot, minVersion string) error {
	installedVersion, err := getSystemdVersion(imageChroot)
	if err != nil {
		return err
	}

	// Split and compare version numbers.
	installedParts := strings.Split(installedVersion, ".")
	minParts := strings.Split(minVersion, ".")

	for i, part := range minParts {
		// Check the main version if minor version is missing.
		if i >= len(installedParts) {
			return fmt.Errorf("installed systemd version (%s) is lower than the minimum required version (%s)", installedVersion, minVersion)
		}

		if installedParts[i] > part {
			// Installed version part is greater than the required version part.
			return nil
		} else if installedParts[i] < part {
			// Installed version part is less than the required version part.
			return fmt.Errorf("installed systemd version (%s) is lower than the minimum required version (%s)", installedVersion, minVersion)
		}
		// If versions are equal, continue checking the next parts.
	}

	return nil
}

func isRpmInstalled(imageChroot *safechroot.Chroot, rpmName string) bool {
	cmd := exec.Command("chroot", imageChroot.Dir(), "rpm", "-q", rpmName)
	err := cmd.Run() // this will return an error if the rpm command does not find the package
	return err == nil
}

func runDracutInChroot(imageChroot *safechroot.Chroot) error {
	cmd := exec.Command("chroot", imageChroot.Dir(), "dracut", "-a", "systemd-veritysetup", "-f")
	return cmd.Run()
}

func findNewInitramfs(imageChroot *safechroot.Chroot) (string, error) {
	initramfsFiles, err := filepath.Glob(filepath.Join(imageChroot.Dir(), "boot", "initramfs-*"))
	if err != nil {
		return "", fmt.Errorf("failed to list initramfs files: %w", err)
	}
	if len(initramfsFiles) == 0 {
		return "", fmt.Errorf("no initramfs file found")
	}
	return filepath.Base(initramfsFiles[len(initramfsFiles)-1]), nil
}

func updateMarinerCfg(imageChroot *safechroot.Chroot, newInitramfs string) error {
	cfgPath := filepath.Join(imageChroot.Dir(), "boot", "mariner.cfg")
	input, err := ioutil.ReadFile(cfgPath)
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
	return ioutil.WriteFile(cfgPath, []byte(output), 0644)
}

func modifyGrubConfig(grubConfigPath, rootHash string) error {
    content, err := ioutil.ReadFile(grubConfigPath)
    if err != nil {
        return err
    }

    lines := strings.Split(string(content), "\n")
    insideMenuEntry := false
    for i, line := range lines {
        if strings.Contains(line, "menuentry \"CBL-Mariner\"") {
            insideMenuEntry = true
        }
        
        if insideMenuEntry && strings.HasPrefix(strings.TrimSpace(line), "linux") {
            // Assuming the cmdline arguments don't already exist. If they might exist and need to be replaced, a more refined approach will be required.
            lines[i] = fmt.Sprintf("%s %s", line, fmt.Sprintf(cmdlineTemplate, rootHash))
            break
        }

        if insideMenuEntry && strings.Contains(line, "}") {
            insideMenuEntry = false
        }
    }

    err = ioutil.WriteFile(grubConfigPath, []byte(strings.Join(lines, "\n")), 0644)
    if err != nil {
        return err
    }

    return nil
}
