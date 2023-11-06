// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"strings"
	"path/filepath"
	"io/ioutil"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

func enableVerityPartition(Verity imagecustomizerapi.Verity, imageChroot *safechroot.Chroot) error {
	var err error

	// Ensure the VerityPartition value is one of the supported types: 'root' or 'user'.
	if Verity.VerityTab != "root" && Verity.VerityTab != "user" {
		return fmt.Errorf("invalid VerityPartition: %s. It should be either 'root' or 'user'", Verity.VerityTab)
	}

	// Integrate systemd veritysetup dracut module into initramfs img.
	systemdVerityDracutModule := "systemd-veritysetup"
	err = buildDracutModule(systemdVerityDracutModule, imageChroot) 
	if err != nil {
		return fmt.Errorf("failed to integrate systemd veritysetup dracut module: %w", err)
	}

	// Update mariner config file with the new generated initramfs file.
	err = updateMarinerCfgWithInitramfs(imageChroot)
	if err != nil {
		return fmt.Errorf("failed to update mariner config file: %w", err)
	}

	// Calculate the root hash using veritysetup
	rootHash, err := calculateRootHash(Verity, imageChroot)
	if err != nil {
		return fmt.Errorf("failed to calculate the root hash: %w", err)
	}

	// Update grub.cfg with the new kernel command-line arguments.
	err = updateGrubConfigWithVerityArgs(rootHash, Verity, imageChroot)
	if err != nil {
		return fmt.Errorf("failed to update grub.cfg with verity arguments: %w", err)
	}

	return nil
}

func buildDracutModule(dracutModuleName string, imageChroot *safechroot.Chroot) error {
	var err error

	buildDracutModuleArgs := []string{
		"dracut", "-f", "-a",
		// Placeholder for dracut module name.
		"",
	}

	buildDracutModuleArgs[len(buildDracutModuleArgs)-1] = dracutModuleName

	err = imageChroot.Run(func() error {
		stdout, stderr, err := shell.Execute("sudo", buildDracutModuleArgs...)
		return err
	})
	if err != nil {
		return fmt.Errorf("failed to build dracut module - (%s):\n%w", dracutModuleName, err)
	}

	return nil
}

func updateMarinerCfgWithInitramfs(imageChroot *safechroot.Chroot) error {
	var err error

	// Construct path for the initramfs file inside the chroot environment.
	initramfsPath := filepath.Join("boot", "initramfs-*")

	// Fetch the initramfs file name.
	var initramfsFiles []string
	err = imageChroot.Run(func() error {
		var innerErr error
		initramfsFiles, innerErr = filepath.Glob(initramfsPath)
		return innerErr
	})
	if err != nil {
		return fmt.Errorf("failed to list initramfs file: %w", err)
	}

	// Ensure an initramfs file is found.
	if len(initramfsFiles) != 1 {
		return fmt.Errorf("expected one initramfs file, but found %d", len(initramfsFiles))
	}

	newInitramfs := filepath.Base(initramfsFiles[0])

	// Construct path for mariner.cfg inside the chroot environment.
	cfgPath := filepath.Join("boot", "mariner.cfg")

	// Update mariner.cfg to reference the new initramfs.
	err = imageChroot.Run(func() error {
		input, innerErr := ioutil.ReadFile(cfgPath)
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
		return ioutil.WriteFile(cfgPath, []byte(output), 0644)
	})

	return nil
}

func calculateRootHash(Verity imagecustomizerapi.Verity, imageChroot *safechroot.Chroot) (string, error) {
	var err error
	var rootHash string
	cmd := fmt.Sprintf("veritysetup -v --debug format %s %s | grep 'Root hash: ' | awk '{print $3}'", Verity.VerityDevice, Verity.HashDevice)

	rootHashOutput, stderr, err := shell.Execute("sh", "-c", cmd)
	if err != nil {
		return "", fmt.Errorf("failed to calculate root hash: %w", err)
	}
	rootHash = strings.TrimSpace(rootHashOutput)

	if rootHash == "" {
		return "", fmt.Errorf("failed to extract root hash from veritysetup output")
	}

	return rootHash, nil
}

func updateGrubConfigWithVerityArgs(rootHash string, Verity imagecustomizerapi.Verity, imageChroot *safechroot.Chroot) error {
	var err error
	const grubCfgPath = "/boot/grub2/grub.cfg"
	const cmdlineTemplate = "rd.systemd.verity=1 roothash=%s systemd.verity_root_data=%s systemd.verity_root_hash=%s systemd.verity_root_options=restart-on-corruption rootflags=noload"
	const rootDevicePattern = "set rootdevice=PARTUUID="
    const replacement = "set rootdevice=/dev/mapper/root"

	newArgs := fmt.Sprintf(cmdlineTemplate, rootHash, Verity.VerityDevice, Verity.HashDevice)

	var updatedLines []string

	err := imageChroot.Run(func() error {
		lines, err := ioutil.ReadFile(grubCfgPath)
		if err != nil {
			return err
		}

		for _, line := range strings.Split(string(lines), "\n") {
			trimmedLine := strings.TrimSpace(line)
			if strings.HasPrefix(trimmedLine, "linux ") {
				line += " " + newArgs
			}
			if strings.HasPrefix(trimmedLine, rootDevicePattern) {
				line = replacement
			}
			updatedLines = append(updatedLines, line)
		}

		// Write the updated content back to grub.cfg
		err = ioutil.WriteFile(grubCfgPath, []byte(strings.Join(updatedLines, "\n")), 0644)
		if err != nil {
			return err
		}

		return nil
	})

	if err != nil {
		return fmt.Errorf("failed to update grub.cfg: %w", err)
	}

	return nil
}
