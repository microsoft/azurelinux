// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Utility to encrypt disks and partitions

package diskutils

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

const (
	// DefaultKeyFilePath points to the initramfs keyfile for the install chroot
	DefaultKeyFilePath = "/etc/default.keyfile"
)

const (
	mappingEncryptedPrefix = "luks-"
	defaultKeyFileName     = "default.keyfile"
)

// EncryptedRootDevice holds settings for an encrypted root partition or disk
type EncryptedRootDevice struct {
	Device      string
	LuksUUID    string
	HostKeyFile string
}

// AddDefaultKeyfile adds a LUKS keyfile for initramfs unlock
// - keyFileDir is the directory to make the keyfile in
// - devPath is the path of the encrypted LUKS device
// - encrypt is the encryption settings
func AddDefaultKeyfile(keyFileDir, devPath string, encrypt configuration.RootEncryption) (fullKeyPath string, err error) {
	fullKeyPath, err = createDefaultKeyFile(keyFileDir)
	if err != nil {
		err = fmt.Errorf("failed to create default keyfile:\n%w", err)
		return
	}

	_, stderr, err := shell.ExecuteWithStdin(encrypt.Password, "cryptsetup", "luksAddKey", devPath, fullKeyPath)
	if err != nil {
		err = fmt.Errorf("failed to add keyfile to encrypted devce:\n%v\n%w", stderr, err)
		return
	}

	err = os.Chmod(fullKeyPath, 000)
	if err != nil {
		err = fmt.Errorf("failed to change permissions on keyfile:\n%v\n%w", stderr, err)
		return
	}

	return
}

// CleanupEncryptedDisks performs cleanup work
func CleanupEncryptedDisks(encryptedRoot EncryptedRootDevice, isOfflineInstall bool) (err error) {
	err = deleteDefaultKeyFile(encryptedRoot.HostKeyFile)
	if err != nil {
		logger.Log.Warnf("Unable to delete default keyfile: %v", err)
	}

	// Order matters for below functions
	err = deactivateLVM()
	if err != nil {
		err = fmt.Errorf("failed to deactive LVM:\n%w", err)
		return
	}

	err = closeEncryptedDisks()
	if err != nil {
		err = fmt.Errorf("failed to close encrypted disks:\n%w", err)
		return
	}

	if isOfflineInstall {
		err = restartLVMetadataService()
		if err != nil {
			err = fmt.Errorf("failed to restart lvm metadata service:\n%w", err)
			return
		}
	}

	return
}

// IsEncryptedDevice checks if a given device is a luks or LVM encrypted device
// - devicePath is the device to check
func IsEncryptedDevice(devicePath string) (result bool) {
	luksPrefix := filepath.Join(mappingFilePath, mappingEncryptedPrefix)
	if strings.HasPrefix(devicePath, luksPrefix) {
		result = true
		return
	}

	lvmRootPath := GetEncryptedRootVolMapping()
	if strings.HasPrefix(devicePath, lvmRootPath) {
		result = true
		return
	}

	return
}

// GetLuksMappingName returns the device name under /dev/mapepr
func GetLuksMappingName(uuid string) (mappingName string) {
	mappingName = fmt.Sprintf("%v%v", mappingEncryptedPrefix, uuid)
	return
}

// encryptRootPartition encrypts the root partition
// - partDevPath is the path of the root partition
// - partition is the configuration
// - encrypt is the root encryption settings
func encryptRootPartition(partDevPath string, partition configuration.Partition, encrypt configuration.RootEncryption) (encryptedRoot EncryptedRootDevice, err error) {
	const (
		defaultCipher  = "aes-xts-plain64"
		defaultKeySize = "256"
		defaultHash    = "sha512"
		defaultLuks    = "luks1"
	)
	if encrypt.Enable == false {
		err = fmt.Errorf("encryption not enabled for partition %v", partition.ID)
		return
	}

	encryptedRoot.Device = partDevPath

	// Encrypt the partition
	cryptsetupArgs := []string{
		"--cipher", defaultCipher,
		"--key-size", defaultKeySize,
		"--hash", defaultHash,
		"--type", defaultLuks,
		"luksFormat", partDevPath,
	}
	_, stderr, err := shell.ExecuteWithStdin(encrypt.Password, "cryptsetup", cryptsetupArgs...)

	if err != nil {
		err = fmt.Errorf("failed to encrypt partition (%v):\n%v\n%w", partDevPath, stderr, err)
		return
	}

	logger.Log.Infof("Encrypted partition %v", partition.ID)

	// Open the partition
	uuid, err := getPartUUID(partDevPath)
	if err != nil || uuid == "" {
		err = fmt.Errorf("failed to get UUID for partition (%v):\n%w", partDevPath, err)
		return
	}

	encryptedRoot.LuksUUID = uuid

	blockDevice := fmt.Sprintf("%v%v", mappingEncryptedPrefix, uuid)

	_, stderr, err = shell.ExecuteWithStdin(encrypt.Password, "cryptsetup", "-q", "open", partDevPath, blockDevice)
	if err != nil {
		err = fmt.Errorf("failed to open encrypted partition (%v):\n%v\n%w", partDevPath, stderr, err)
		return
	}

	// Add the LVM
	fullMappedPath, err := enableLVMForEncryptedRoot(filepath.Join(mappingFilePath, blockDevice))
	if err != nil {
		err = fmt.Errorf("failed to enable LVM for encrypted root:\n%w", err)
		return
	}

	// Create the file system
	_, stderr, err = shell.Execute("mkfs", "-t", partition.FsType, fullMappedPath)
	if err != nil {
		err = fmt.Errorf("failed to mkfs for partition (%v):\n%v\n%w", partDevPath, stderr, err)
	}

	return
}

func createDefaultKeyFile(keyFileDir string) (fullPath string, err error) {
	const (
		defaultBs     = "bs=512"
		defaultCount  = "count=4"
		defaultIf     = "if=/dev/urandom"
		outFilePrefix = "of="
		defaultConv   = "conv=excl"
		defaultIflag  = "iflag=fullblock"
	)
	fullPath = filepath.Join(keyFileDir, defaultKeyFileName)
	outFile := fmt.Sprintf("%v%v", outFilePrefix, fullPath)

	// Create keyfile filled with random bytes
	ddArgs := []string{
		defaultBs,
		defaultCount,
		defaultIf,
		outFile,
		defaultConv,
		defaultIflag,
	}
	_, stderr, err := shell.Execute("dd", ddArgs...)
	if err != nil {
		logger.Log.Warnf("Unable to create default keyfile: %v", stderr)
		return
	}

	return
}

func deleteDefaultKeyFile(hostKeyFile string) (err error) {
	_, stderr, err := shell.Execute("rm", hostKeyFile)
	if err != nil {
		err = fmt.Errorf("failed to delete default keyfile:\n%v\n%w", stderr, err)
		return
	}

	return
}

func closeEncryptedDisks() (err error) {
	stdout, stderr, err := shell.Execute("dmsetup", "info", "-c", "-o", "Name", "--noheadings")
	if err != nil {
		err = fmt.Errorf("failed to run dmsetup:\n%v\n%w", stderr, err)
		return
	}

	mappedDevices := strings.Split(stdout, "\n")

	for _, device := range mappedDevices {
		if strings.HasPrefix(device, mappingEncryptedPrefix) {
			logger.Log.Infof("Closing Encrypted Device: %v", device)
			_, stderr, err := shell.Execute("cryptsetup", "close", device)
			if err != nil {
				err = fmt.Errorf("failed to close encrypted disk:\n%v\n%w", stderr, err)
				return err
			}
		}
	}

	return
}
