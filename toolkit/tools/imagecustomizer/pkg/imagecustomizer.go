// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizer

import (
	"fmt"
	"io/ioutil"
	"os"
	"path"
	"path/filepath"
	"regexp"

	icapi "github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizer/api"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"gopkg.in/yaml.v3"
)

func CustomizeImageWithConfigFile(buildDir string, configFile string, imageFile string) error {
	yamlFile, err := ioutil.ReadFile(configFile)
	if err != nil {
		return err
	}

	var config icapi.SystemConfig
	err = yaml.Unmarshal(yamlFile, &config)
	if err != nil {
		return err
	}

	err = CustomizeImage(buildDir, &config, imageFile)
	if err != nil {
		return err
	}

	return nil
}

func CustomizeImage(buildDir string, config *icapi.SystemConfig, imageFile string) error {
	var err error

	err = loadNbdKernelModule()
	if err != nil {
		return err
	}

	nbdDevicePath, err := connectToQcow2File(imageFile)
	if err != nil {
		return err
	}
	defer disconnectFromQcow2File(nbdDevicePath)

	newMountDirectories, mountPoints, err := findPartitions(nbdDevicePath)
	if err != nil {
		return err
	}

	imageChrootDir := filepath.Join(buildDir, "imageroot")

	err = os.MkdirAll(buildDir, os.ModePerm)
	if err != nil {
		return err
	}

	imageChroot := safechroot.NewChroot(imageChrootDir, false)
	err = imageChroot.Initialize("", newMountDirectories, mountPoints)
	if err != nil {
		return err
	}
	defer imageChroot.Close(false)

	return nil
}

// Loads the NBD (Network Block Device) kernel module.
func loadNbdKernelModule() error {
	var err error

	_, _, err = shell.Execute("modprobe", "nbd")
	if err != nil {
		return fmt.Errorf("failed to load nbd kernel module: %w", err)
	}

	return nil
}

// Connect to a QCOW2 disk file using qemu-nbd.
func connectToQcow2File(imageFile string) (string, error) {
	var err error

	nbdDevicePath, err := findUnusedNbdSlot()
	if err != nil {
		return "", nil
	}

	// Connect to QCOW2 file.
	_, _, err = shell.Execute("qemu-nbd", "--connect", nbdDevicePath, imageFile)
	if err != nil {
		return "", fmt.Errorf("failed to connect to QCOW2 file: %w", err)
	}

	// Wait for the partitions to show up.
	_, _, err = shell.Execute("udevadm", "settle")
	if err != nil {
		return "", fmt.Errorf("failed to wait for partitions to be detected: %w", err)
	}

	return nbdDevicePath, nil
}

func disconnectFromQcow2File(nbdDevicePath string) error {
	var err error

	_, _, err = shell.Execute("qemu-nbd", "--disconnect", nbdDevicePath)
	if err != nil {
		return fmt.Errorf("failed to disconnect from QCOW2 file: %w", err)
	}

	return nil
}

// Look for an NBD slot that isn't being used.
func findUnusedNbdSlot() (string, error) {
	var err error

	// For whatever reason, Go's ioutil.ReadDir() won't list block devices under /dev.
	// But we can grab the list from /sys/block instead.
	files, err := ioutil.ReadDir("/sys/block")
	if err != nil {
		return "", fmt.Errorf("can't list NBD device slots: %w", err)
	}

	nbdRegex, err := regexp.Compile("^nbd[0-9]*$")
	if err != nil {
		return "", err
	}

	var nbdDevicePath string
	for _, file := range files {
		// Check if file is a NBD device slot.
		if !nbdRegex.MatchString(file.Name()) {
			continue
		}

		nbdDevicePath = path.Join("/dev", file.Name())

		// Check if the NBD slot is already being used by trying to open an exclusive lock.
		// Pre-checking this avoids masking other errors encountered by qemu-nbd.
		// https://unix.stackexchange.com/a/312273
		var nbdDevice *os.File
		nbdDevice, err = os.OpenFile(nbdDevicePath, os.O_RDONLY|os.O_EXCL, 0)
		if err != nil {
			continue
		}
		nbdDevice.Close()

		break
	}

	if nbdDevicePath == "" {
		return "", fmt.Errorf("no NBD device slots found")
	}

	if err != nil {
		return "", fmt.Errorf("all NBD device slots are unavailable (or there is a permission problem): %w", err)
	}

	return nbdDevicePath, nil
}

func findPartitions(diskDevice string) ([]string, []*safechroot.MountPoint, error) {
	newMountDirectories := []string{}

	// TODO: Dynamically find partitions instead of hardcoding the mappings.
	mountPoints := []*safechroot.MountPoint{
		safechroot.NewPreDefaultsMountPoint(fmt.Sprintf("%sp2", diskDevice), "/", "ext4", 0, ""),
		safechroot.NewMountPoint(fmt.Sprintf("%sp1", diskDevice), "/boot", "vfat", 0, ""),
	}

	return newMountDirectories, mountPoints, nil
}
