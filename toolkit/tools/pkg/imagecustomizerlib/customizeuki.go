// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

func enableUki(uki bool, imageChroot *safechroot.Chroot) error {
	var err error
	var grubCfgOutput string

	if uki == false {
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

	logger.Log.Infof("Extracted UUID: %s", uuid)
	logger.Log.Infof("Extracted Kernel: %s", kernel)
	logger.Log.Infof("Extracted Initrd: %s", initrd)

	// Run ukify to build UKI.
	err = imageChroot.UnsafeRun(func() error {
		ukifyCmd := []string{
			"ukify", "build",
			fmt.Sprintf("--linux=/boot%s", kernel),
			fmt.Sprintf("--initrd=/boot%s", initrd), 
			fmt.Sprintf("--cmdline=BOOT_IMAGE=%s root=UUID=%s ro selinux=0 rd.auto=1 net.ifnames=0 lockdown=integrity console=tty0 console=ttyS0 rd.debug", kernel, uuid),
			fmt.Sprintf("--output=/boot/efi/EFI/Linux%s.unsigned.efi", kernel),
		}
		return shell.ExecuteLiveWithErr(1, "sudo", ukifyCmd...)
	})
	if err != nil {
		return fmt.Errorf("failed to build UKI:\n%w", err)
	}

	// Install systemd-boot.
	err = imageChroot.UnsafeRun(func() error {
		return shell.ExecuteLiveWithErr(1, "sudo", "bootctl", "install", "--no-variables")
	})
	if err != nil {
		return fmt.Errorf("failed to install systemd-boot:\n%w", err)
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
