// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

func enableUki(uki bool, imageChroot *safechroot.Chroot) error {
	var err error
	var grubCfgOutput string

	if !uki {
		return nil
	}

	logger.Log.Infof("Enable uki")

	// Check UKI dependency packages.
	err = validateUkiDependencies(imageChroot)
	if err != nil {
		return fmt.Errorf("failed to validate package dependencies for uki:\n%w", err)
	}

	// Create the EFI directory.
	err = imageChroot.UnsafeRun(func() error {
		return shell.ExecuteLiveWithErr(1, "sudo", "mkdir", "-p", "/boot/efi/EFI/Linux")
	})
	if err != nil {
		return fmt.Errorf("failed to create EFI directory:\n%w", err)
	}

	// Create the Ukify config.
	err = imageChroot.UnsafeRun(func() error {
		return shell.ExecuteLiveWithErr(1, "sudo", "touch", "/boot/ukify.conf")
	})
	if err != nil {
		return fmt.Errorf("failed to create Ukify config:\n%w", err)
	}

	// Extract /boot/grub2/grub.cfg
	err = imageChroot.UnsafeRun(func() error {
		// Store the output of the cat command
		stdout, stderr, err := shell.Execute("cat", "/boot/grub2/grub.cfg")
		if err != nil {
			logger.Log.Errorf("failed to read GRUB configuration: %v", stderr)
			return err
		}
		grubCfgOutput = stdout
		return nil
	})
	if err != nil {
		return fmt.Errorf("failed to read GRUB configuration:\n%w", err)
	}

	// Parse UUID from GRUB config
	uuid, kernel, initrd, err := extractRootUUIDKernelInitrdFromGrub(grubCfgOutput)
	if err != nil {
		return fmt.Errorf("failed to extract UUID, kernel, or initrd from GRUB configuration:\n%w", err)
	}

	if strings.HasPrefix(uuid, "/dev/mapper/root") {
		uuid = "/dev/mapper/root"
	} else {
		uuid = fmt.Sprintf("UUID=%s", uuid)
	}

	logger.Log.Infof("Extracted UUID: %s", uuid)
	logger.Log.Infof("Extracted Kernel: %s", kernel)
	logger.Log.Infof("Extracted Initrd: %s", initrd)

	// Write the Ukify config to /boot/ukify.conf
	err = imageChroot.UnsafeRun(func() error {
		configFilePath := "/boot/ukify.conf"
		configContent := fmt.Sprintf("[UKI]\nLinux=/boot%s\nInitrd=/boot%s\nCmdline=BOOT_IMAGE=%s root=%s ro selinux=0 rd.auto=1 net.ifnames=0 lockdown=integrity console=tty0 console=ttyS0 rd.debug\n", kernel, initrd, kernel, uuid)

		// Open file and write the content
		err := shell.ExecuteLiveWithErr(1, "sudo", "sh", "-c", fmt.Sprintf("echo '%s' > %s", configContent, configFilePath))
		if err != nil {
			logger.Log.Errorf("failed to write Ukify config to %s: %v", configFilePath, err)
			return err
		}
		logger.Log.Infof("Successfully wrote the Ukify config to %s", configFilePath)
		return nil
	})
	if err != nil {
		return fmt.Errorf("failed to write Ukify config file:\n%w", err)
	}

	// Install systemd-boot.
	err = imageChroot.UnsafeRun(func() error {
		return shell.ExecuteLiveWithErr(1, "sudo", "bootctl", "install", "--no-variables")
	})
	if err != nil {
		return fmt.Errorf("failed to install systemd-boot:\n%w", err)
	}

	// Run ukify to build UKI using the helper function inside the imageChroot
	err = runUkifyBuild(imageChroot)
	if err != nil {
		return fmt.Errorf("failed to build UKI:\n%w", err)
	}

	return nil
}

func extractRootUUIDKernelInitrdFromGrub(grubCfgContent string) (string, string, string, error) {
	var uuid, kernel, initrd string

	lines := strings.Split(grubCfgContent, "\n")
	for _, line := range lines {
		if strings.Contains(line, "linux") {
			parts := strings.Fields(line)
			for _, part := range parts {
				if strings.HasPrefix(part, "root=UUID=") {
					uuid = strings.TrimPrefix(part, "root=UUID=")
				} else if part == "root=/dev/mapper/root" {
					uuid = "/dev/mapper/root"
				}
				if strings.HasPrefix(part, "/vmlinuz") {
					kernel = part
				}
			}
		}

		if strings.Contains(line, "initrd") {
			parts := strings.Fields(line)
			for _, part := range parts {
				if strings.HasPrefix(part, "/initramfs") {
					initrd = part
				}
			}
		}

		if uuid != "" && kernel != "" && initrd != "" {
			return uuid, kernel, initrd, nil
		}
	}
	return "", "", "", fmt.Errorf("failed to extract UUID, kernel, initrd from GRUB config")
}

func runUkifyBuild(imageChroot *safechroot.Chroot) error {
	err := imageChroot.UnsafeRun(func() error {
		configFilePath := "/boot/ukify.conf"

		// Read the ukify config file to extract the kernel from the "Linux=" line
		var kernel string
		file, err := os.Open(configFilePath)
		if err != nil {
			return fmt.Errorf("failed to open ukify config file: %w", err)
		}
		defer file.Close()

		// Scan through the config file to find the "Linux=" line
		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			line := scanner.Text()
			if strings.HasPrefix(line, "Linux=") {
				kernel = strings.TrimPrefix(line, "Linux=")
				break
			}
		}

		if kernel == "" {
			return fmt.Errorf("failed to find Linux= entry in %s", configFilePath)
		}

		// Strip the /boot prefix from the kernel path if present
		kernelFileName := filepath.Base(kernel)

		// Prepare the ukify command
		ukifyCmd := []string{
			"ukify", "-c", "/boot/ukify.conf", "build",
			fmt.Sprintf("--output=/boot/efi/EFI/Linux/%s.unsigned.efi", kernelFileName),
		}

		return shell.ExecuteLiveWithErr(1, "sudo", ukifyCmd...)
	})
	if err != nil {
		return fmt.Errorf("failed to build UKI:\n%w", err)
	}

	return nil
}

func validateUkiDependencies(imageChroot *safechroot.Chroot) error {
	requiredRpms := []string{"systemd-ukify", "systemd-boot", "efibootmgr"}

	// Iterate over each required package and check if it's installed.
	for _, pkg := range requiredRpms {
		logger.Log.Debugf("Checking if package (%s) is installed", pkg)
		if !isPackageInstalled(imageChroot, pkg) {
			return fmt.Errorf("package (%s) is not installed:\nthe following packages must be installed to use Uki: %v", pkg, requiredRpms)
		}
	}

	return nil
}
