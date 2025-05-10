// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	//"bufio"
	"fmt"
	"os"
	//"path/filepath"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

func prepareUki(uki bool, imageChroot *safechroot.Chroot) error {
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

	// Carry over the os-subrelease file.
	err = imageChroot.UnsafeRun(func() error {
		return shell.ExecuteLiveWithErr(1, "sudo", "cp", "/etc/os-release", "/boot/os-release")
	})
	if err != nil {
		return fmt.Errorf("failed to create Ukify config:\n%w", err)
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

	// Parse kernel and initrd from GRUB config.
	kernel, initrd, err := extractKernelInitrdFromGrub(grubCfgOutput)
	if err != nil {
		return fmt.Errorf("failed to extract kernel, or initrd from GRUB configuration:\n%w", err)
	}

	logger.Log.Infof("Extracted Kernel: %s", kernel)
	logger.Log.Infof("Extracted Initrd: %s", initrd)

	// Write the Ukify config to /boot/ukify.conf
	err = imageChroot.UnsafeRun(func() error {
		configFilePath := "/boot/ukify.conf"
		configContent := fmt.Sprintf("[UKI]\nLinux=/boot%s\nInitrd=/boot%s", kernel, initrd)

		// Open file and write the content
		err := shell.ExecuteLiveWithErr(1, "sudo", "sh", "-c", fmt.Sprintf("echo '%s' > %s", configContent, configFilePath))
		if err != nil {
			logger.Log.Errorf("failed to write Ukify config to %s: %v", configFilePath, err)
			return err
		}
		logger.Log.Infof("Successfully wrote the Ukify config to %s", configFilePath)
		fmt.Println(configContent)
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

	err = imageChroot.UnsafeRun(func() error {
		return shell.ExecuteLiveWithErr(1, "sudo", "cp", "/usr/lib/systemd/boot/efi/linuxx64.efi.stub", "/boot")
	})
	if err != nil {
		return fmt.Errorf("failed to cp linuxx64.efi.stub:\n%w", err)
	}

	return nil
}

func extractKernelInitrdFromGrub(grubCfgContent string) (string, string, error) {
	var kernel, initrd string

	lines := strings.Split(grubCfgContent, "\n")
	for _, line := range lines {
		if strings.Contains(line, "linux") {
			parts := strings.Fields(line)
			for _, part := range parts {
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

		if kernel != "" && initrd != "" {
			return kernel, initrd, nil
		}
	}
	return "", "", fmt.Errorf("failed to extract kernel, initrd from GRUB config")
}

func retrieveLinuxFromUkifyConfig(ukifyConfigFullPath string) (string, error) {
	// Read the ukify.conf file
	ukifyConfigContent, err := os.ReadFile(ukifyConfigFullPath)
	if err != nil {
		return "", fmt.Errorf("failed to read ukify.conf file (%s):\n%w", ukifyConfigFullPath, err)
	}

	// Split the content into lines and search for the 'Linux=' line
	lines := strings.Split(string(ukifyConfigContent), "\n")
	var linuxLine string
	for _, line := range lines {
		if strings.HasPrefix(line, "Linux=") {
			linuxLine = strings.TrimPrefix(line, "Linux=")
			break
		}
	}

	if linuxLine == "" {
		return "", fmt.Errorf("failed to find 'Linux=' entry in ukify.conf (%s)", ukifyConfigFullPath)
	}

	// Remove the /boot prefix if present
	linuxValue := strings.TrimPrefix(linuxLine, "/boot")

	// Return the Linux value
	return linuxValue, nil
}

func retrieveInitrdFromUkifyConfig(ukifyConfigFullPath string) (string, error) {
	// Read the ukify.conf file
	ukifyConfigContent, err := os.ReadFile(ukifyConfigFullPath)
	if err != nil {
		return "", fmt.Errorf("failed to read ukify.conf file (%s):\n%w", ukifyConfigFullPath, err)
	}

	// Split the content into lines and search for the 'Linux=' line
	lines := strings.Split(string(ukifyConfigContent), "\n")
	var initrdLine string
	for _, line := range lines {
		if strings.HasPrefix(line, "Initrd=") {
			initrdLine = strings.TrimPrefix(line, "Initrd=")
			break
		}
	}

	if initrdLine == "" {
		return "", fmt.Errorf("failed to find 'Linux=' entry in ukify.conf (%s)", ukifyConfigFullPath)
	}

	// Remove the /boot prefix if present
	initrdValue := strings.TrimPrefix(initrdLine, "/boot")

	// Return the Linux value
	return initrdValue, nil
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
