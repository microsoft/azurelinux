// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safeloopback"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

const (
	tmpParitionDirName = "tmppartition"
)

var (
	// Version specifies the version of the Mariner Image Customizer tool.
	// The value of this string is inserted during compilation via a linker flag.
	ToolVersion = ""
)

func CustomizeImageWithConfigFile(buildDir string, configFile string, imageFile string,
	rpmsSources []string, outputImageFile string, outputImageFormat string,
	useBaseImageRpmRepos bool,
) error {
	var err error

	var config imagecustomizerapi.Config
	err = imagecustomizerapi.UnmarshalYamlFile(configFile, &config)
	if err != nil {
		return err
	}

	baseConfigPath, _ := filepath.Split(configFile)

	absBaseConfigPath, err := filepath.Abs(baseConfigPath)
	if err != nil {
		return fmt.Errorf("failed to get absolute path of config file directory:\n%w", err)
	}

	err = CustomizeImage(buildDir, absBaseConfigPath, &config, imageFile, rpmsSources, outputImageFile, outputImageFormat,
		useBaseImageRpmRepos)
	if err != nil {
		return err
	}

	return nil
}

func CustomizeImage(buildDir string, baseConfigPath string, config *imagecustomizerapi.Config, imageFile string,
	rpmsSources []string, outputImageFile string, outputImageFormat string, useBaseImageRpmRepos bool,
) error {
	var err error

	// Validate 'outputImageFormat' value.
	qemuOutputImageFormat, err := toQemuImageFormat(outputImageFormat)
	if err != nil {
		return err
	}

	// Validate config.
	err = validateConfig(baseConfigPath, config)
	if err != nil {
		return fmt.Errorf("invalid image config:\n%w", err)
	}

	// Normalize 'buildDir' path.
	buildDirAbs, err := filepath.Abs(buildDir)
	if err != nil {
		return err
	}

	// Create 'buildDir' directory.
	err = os.MkdirAll(buildDirAbs, os.ModePerm)
	if err != nil {
		return err
	}

	// Convert image file to raw format, so that a kernel loop device can be used to make changes to the image.
	buildImageFile := filepath.Join(buildDirAbs, "image.raw")

	_, _, err = shell.Execute("qemu-img", "convert", "-O", "raw", imageFile, buildImageFile)
	if err != nil {
		return fmt.Errorf("failed to convert image file to raw format:\n%w", err)
	}

	// Customize the raw image file.
	err = customizeImageHelper(buildDirAbs, baseConfigPath, config, buildImageFile, rpmsSources, useBaseImageRpmRepos)
	if err != nil {
		return err
	}

	// Create final output image file.
	outDir := filepath.Dir(outputImageFile)
	os.MkdirAll(outDir, os.ModePerm)

	_, _, err = shell.Execute("qemu-img", "convert", "-O", qemuOutputImageFormat, buildImageFile, outputImageFile)
	if err != nil {
		return fmt.Errorf("failed to convert image file to format: %s:\n%w", outputImageFormat, err)
	}

	// Customize the nbd image file.
	err = customizeImageHelperNbd(buildDirAbs, baseConfigPath, config, outputImageFile, rpmsSources, useBaseImageRpmRepos)
	if err != nil {
		return err
	}

	return nil
}

func toQemuImageFormat(imageFormat string) (string, error) {
	switch imageFormat {
	case "vhd":
		return "vpc", nil

	case "vhdx", "raw", "qcow2":
		return imageFormat, nil

	default:
		return "", fmt.Errorf("unsupported image format (supported: vhd, vhdx, raw, qcow2): %s", imageFormat)
	}
}

func validateConfig(baseConfigPath string, config *imagecustomizerapi.Config) error {
	var err error

	err = validateSystemConfig(baseConfigPath, &config.SystemConfig)
	if err != nil {
		return err
	}

	return nil
}

func validateSystemConfig(baseConfigPath string, config *imagecustomizerapi.SystemConfig) error {
	var err error

	for sourceFile := range config.AdditionalFiles {
		sourceFileFullPath := filepath.Join(baseConfigPath, sourceFile)
		isFile, err := file.IsFile(sourceFileFullPath)
		if err != nil {
			return fmt.Errorf("invalid AdditionalFiles source file (%s):\n%w", sourceFile, err)
		}

		if !isFile {
			return fmt.Errorf("invalid AdditionalFiles source file (%s): not a file", sourceFile)
		}
	}

	for i, script := range config.PostInstallScripts {
		err = validateScript(baseConfigPath, &script)
		if err != nil {
			return fmt.Errorf("invalid PostInstallScripts item at index %d: %w", i, err)
		}
	}

	for i, script := range config.FinalizeImageScripts {
		err = validateScript(baseConfigPath, &script)
		if err != nil {
			return fmt.Errorf("invalid FinalizeImageScripts item at index %d: %w", i, err)
		}
	}

	return nil
}

func validateScript(baseConfigPath string, script *imagecustomizerapi.Script) error {
	// Ensure that install scripts sit under the config file's parent directory.
	// This allows the install script to be run in the chroot environment by bind mounting the config directory.
	if !filepath.IsLocal(script.Path) {
		return fmt.Errorf("install script (%s) is not under config directory (%s)", script.Path, baseConfigPath)
	}

	// Verify that the file exists.
	fullPath := filepath.Join(baseConfigPath, script.Path)

	scriptStat, err := os.Stat(fullPath)
	if err != nil {
		return fmt.Errorf("couldn't read install script (%s):\n%w", script.Path, err)
	}

	// Verify that the file has an executable bit set.
	if scriptStat.Mode()&0111 == 0 {
		return fmt.Errorf("install script (%s) does not have executable bit set", script.Path)
	}

	return nil
}

func customizeImageHelper(buildDir string, baseConfigPath string, config *imagecustomizerapi.Config,
	buildImageFile string, rpmsSources []string, useBaseImageRpmRepos bool,
) error {
	// Mount the raw disk image file.
	loopback, err := safeloopback.NewLoopback(buildImageFile)
	if err != nil {
		return fmt.Errorf("failed to mount raw disk (%s) as a loopback device:\n%w", buildImageFile, err)
	}
	defer loopback.Close()

	// Look for all the partitions on the image.
	newMountDirectories, mountPoints, err := findPartitions(buildDir, loopback.DevicePath())
	if err != nil {
		return fmt.Errorf("failed to find disk partitions:\n%w", err)
	}

	// Create chroot environment.
	imageChrootDir := filepath.Join(buildDir, "imageroot")

	chrootLeaveOnDisk := false
	imageChroot := safechroot.NewChroot(imageChrootDir, chrootLeaveOnDisk)
	err = imageChroot.Initialize("", newMountDirectories, mountPoints)
	if err != nil {
		return err
	}
	defer imageChroot.Close(chrootLeaveOnDisk)

	// Do the actual customizations.
	err = doCustomizations(buildDir, baseConfigPath, config, imageChroot, rpmsSources, useBaseImageRpmRepos)
	if err != nil {
		return err
	}

	// Close.
	err = imageChroot.Close(chrootLeaveOnDisk)
	if err != nil {
		return err
	}

	err = loopback.CleanClose()
	if err != nil {
		return err
	}

	return nil
}

func customizeImageHelperNbd(buildDir string, baseConfigPath string, config *imagecustomizerapi.Config,
	buildImageFile string, rpmsSources []string, useBaseImageRpmRepos bool,
) error {
	var err error

	// Connect the disk image to an NBD device using qemu-nbd
	nbdDevice := "/dev/nbd0" // You may want to dynamically find a free nbd device
	_, _, err = shell.Execute("sudo", "qemu-nbd", "-c", nbdDevice, buildImageFile)
	if err != nil {
		return fmt.Errorf("failed to connect nbd %s to image %s", nbdDevice, buildImageFile)
	}
	defer func() {
		// Disconnect the NBD device when the function returns
		_, _, err = shell.Execute("sudo", "qemu-nbd", "-d", nbdDevice)
		if err != nil {
			return
		}
	}()

	// Check if the NBD device is connected using lsblk
	var out bytes.Buffer
	lsblkCmd := exec.Command("lsblk")
	lsblkCmd.Stdout = &out // Redirects output to buffer
	if err := lsblkCmd.Run(); err != nil {
		return fmt.Errorf("failed to execute lsblk:\n%w", err)
	}

	// Print the output of lsblk
	fmt.Println("Output of lsblk:")
	fmt.Println(out.String())

	// Extract salt and root hash using regular expressions
	verityOutput, _, err := shell.Execute("sudo", "veritysetup", "format", "/dev/nbd0p3", "/dev/nbd0p6")
	if err != nil {
		return fmt.Errorf("failed to calculate root hash:\n%w", err)
	}

	var salt, rootHash string
	saltRegex := regexp.MustCompile(`Salt:\s+([0-9a-fA-F]+)`)
	rootHashRegex := regexp.MustCompile(`Root hash:\s+([0-9a-fA-F]+)`)

	saltMatches := saltRegex.FindStringSubmatch(verityOutput)
	if len(saltMatches) > 1 {
		salt = saltMatches[1]
	}

	rootHashMatches := rootHashRegex.FindStringSubmatch(verityOutput)
	if len(rootHashMatches) > 1 {
		rootHash = rootHashMatches[1]
	}

	if salt == "" || rootHash == "" {
		return fmt.Errorf("failed to parse salt or root hash from veritysetup output")
	}

	// Print salt and root hash
	fmt.Printf("Salt: %s\n", salt)
	fmt.Printf("Root hash: %s\n", rootHash)

	// Mount the boot partition
	mountOutput, _, err := shell.Execute("sudo", "mount", "/dev/nbd0p2", "/mnt/boot_partition")
	if err != nil {
		return err
	}

	// Assuming mountOutput contains relevant information, you might want to log it
	fmt.Println("Mount output:", mountOutput)

	// Check if the NBD device is connected using lsblk
	lsblkCmd = exec.Command("lsblk")
	lsblkCmd.Stdout = &out // Redirects output to buffer
	if err = lsblkCmd.Run(); err != nil {
		return fmt.Errorf("failed to execute lsblk:\n%w", err)
	}

	// Print the output of lsblk
	fmt.Println("Output of lsblk:")
	fmt.Println(out.String())

	// Update grub configuration
    err = updateGrubConfig(salt, rootHash)
    if err != nil {
        return err
    }

    // Unmount the boot partition after the update
    _, _, err = shell.Execute("sudo", "umount", "/mnt/boot_partition")
    if err != nil {
        return fmt.Errorf("failed to unmount boot partition: %v", err)
    }

	return nil
}

func updateGrubConfig(salt string, rootHash string) error {
	const cmdlineTemplate = "rd.systemd.verity=1 roothash=%s systemd.verity_root_data=/dev/sda3 systemd.verity_root_hash=/dev/sda6 systemd.verity_root_options=panic-on-corruption,salt=%s"
	newArgs := fmt.Sprintf(cmdlineTemplate, rootHash, salt)
	// Define the relative path to grub.cfg from the mount point
    grubConfigPath := "/mnt/boot_partition/grub2/grub.cfg"

    // Read the content of the grub configuration file
    content, err := ioutil.ReadFile(grubConfigPath)
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
            // Replace the root device line with the new root device
            line = "set rootdevice=/dev/mapper/root"
        }
        updatedLines = append(updatedLines, line)
    }

    // Write the updated content back to grub.cfg
    err = ioutil.WriteFile(grubConfigPath, []byte(strings.Join(updatedLines, "\n")), 0644)
    if err != nil {
        return fmt.Errorf("failed to write updated grub config: %v", err)
    }

	// Read and print the updated grub configuration file
    updatedContent, err := ioutil.ReadFile(grubConfigPath)
    if err != nil {
        return err
    }
    fmt.Println("Updated grub.cfg content:")
    fmt.Print(string(updatedContent))

    return nil
}
