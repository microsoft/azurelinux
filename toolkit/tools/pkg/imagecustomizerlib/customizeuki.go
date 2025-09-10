// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

func prepareUki(uki *imagecustomizerapi.Uki, imageChroot *safechroot.Chroot) error {
	var err error

	if uki == nil {
		return nil
	}

	logger.Log.Infof("Enable uki")

	// Check UKI dependency packages.
	err = validateUkiDependencies(imageChroot)
	if err != nil {
		return fmt.Errorf("failed to validate package dependencies for uki:\n%w", err)
	}

	// Create necessary directories for UKI.
	err = createUkiDirectories(imageChroot)
	if err != nil {
		return fmt.Errorf("failed to create UKI directories:\n%w", err)
	}

	// Install systemd-boot.
	err = imageChroot.UnsafeRun(func() error {
		return shell.ExecuteLiveWithErr(1, "sudo", "bootctl", "install", "--no-variables")
	})
	if err != nil {
		return fmt.Errorf("failed to install systemd-boot:\n%w", err)
	}

	// Copy UKI specific files.
	err = copyUkiFiles(imageChroot)
	if err != nil {
		return fmt.Errorf("failed to copy UKI files:\n%w", err)
	}

	// Prepare ukify config files.
	bootDir := filepath.Join(imageChroot.RootDir(), "/boot")

	kernels, err := findKernelImages(bootDir)
	if err != nil {
		return err
	}

	err = ensureInitramfsForKernels(bootDir, kernels)
	if err != nil {
		return err
	}

	for _, kernel := range kernels {
		err = createUkifyConfig(bootDir, kernel)
		if err != nil {
			return fmt.Errorf("failed to create ukify config: %w", err)
		}
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

func createUkiDirectories(imageChroot *safechroot.Chroot) error {
	// Default directories required for the UKI setup. This list may expand as additional directories are needed.
	dirsToCreate := []string{
		filepath.Join(imageChroot.RootDir(), "/boot/efi/EFI/Linux"),
	}

	// Iterate over each directory and create it if it doesn't exist.
	for _, dir := range dirsToCreate {
		err := os.MkdirAll(dir, os.ModePerm)
		if err != nil {
			return fmt.Errorf("failed to create directory (%s): %w", dir, err)
		}
	}

	return nil
}

func copyUkiFiles(imageChroot *safechroot.Chroot) error {
	// Define the files to copy with their source and destination paths.
	filesToCopy := map[string]string{
		"/etc/os-release": "/boot/os-release",
		"/usr/lib/systemd/boot/efi/linuxx64.efi.stub": "/boot/linuxx64.efi.stub",
	}

	for src, dest := range filesToCopy {
		err := imageChroot.UnsafeRun(func() error {
			return shell.ExecuteLiveWithErr(1, "sudo", "cp", src, dest)
		})
		if err != nil {
			return fmt.Errorf("failed to copy file from %s to %s: %w", src, dest, err)
		}
	}

	return nil
}

func findKernelImages(bootDir string) ([]string, error) {
	var kernelImages []string

	// Walk through the aimed directory to find matching kernel images.
	err := filepath.Walk(bootDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return fmt.Errorf("error accessing path %s: %w", path, err)
		}

		// Check if the file name matches the kernel image pattern.
		if !info.IsDir() && strings.HasPrefix(info.Name(), "vmlinuz-") && strings.HasSuffix(info.Name(), ".azl3") {
			kernelImages = append(kernelImages, filepath.Base(path))
		}

		return nil
	})
	if err != nil {
		return nil, err
	}

	return kernelImages, nil
}

func ensureInitramfsForKernels(bootDir string, kernels []string) error {
	// Prepare a map to store required initramfs paths for the given kernels.
	requiredInitramfs := make(map[string]string)
	for _, kernel := range kernels {
		if strings.HasPrefix(kernel, "vmlinuz-") {
			kernelVersion := strings.TrimPrefix(kernel, "vmlinuz-")
			initramfsFile := fmt.Sprintf("initramfs-%s.img", kernelVersion)
			requiredInitramfs[kernelVersion] = filepath.Join(bootDir, initramfsFile)
		}
	}

	// Keep track of found initramfs files.
	foundInitramfs := make(map[string]bool)

	// Walk through the boot directory to find initramfs files.
	err := filepath.Walk(bootDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return fmt.Errorf("error accessing path %s: %w", path, err)
		}

		// Check if the file matches the required initramfs paths.
		for _, initramfsPath := range requiredInitramfs {
			if path == initramfsPath {
				foundInitramfs[initramfsPath] = true
			}
		}

		return nil
	})
	if err != nil {
		return err
	}

	// Check if all required initramfs files were found.
	for kernelVersion, initramfsPath := range requiredInitramfs {
		if !foundInitramfs[initramfsPath] {
			return fmt.Errorf("missing initramfs for kernel: vmlinuz-%s (expected at %s)", kernelVersion, initramfsPath)
		}
	}

	return nil
}

func createUkifyConfig(bootDir string, kernel string) error {
	// Extract kernel version from the kernel file name.
	kernelVersion := strings.TrimPrefix(kernel, "vmlinuz-")

	// Derive initramfs and config file paths.
	initramfs := fmt.Sprintf("/initramfs-%s.img", kernelVersion)
	configFilePath := filepath.Join(bootDir, fmt.Sprintf("ukify_%s.conf", kernelVersion))

	configContent := fmt.Sprintf("[UKI]\nLinux=%s\nInitrd=%s\n", kernel, initramfs)

	// Write the config content to the file.
	err := os.WriteFile(configFilePath, []byte(configContent), 0644)
	if err != nil {
		return fmt.Errorf("failed to write ukify config file for kernel (%s): %w", kernelVersion, err)
	}

	// Log the updated config content.
	logger.Log.Infof("Created ukify config file at: %s\nContent:\n%s", configFilePath, configContent)

	return nil
}

func retrieveLinuxFromUkifyConf(ukifyConfigFullPath string) (string, error) {
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

func retrieveInitramfsFromUkifyConf(ukifyConfigFullPath string) (string, error) {
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
