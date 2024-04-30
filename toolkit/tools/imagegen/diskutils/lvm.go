// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Utility for logical volume management

package diskutils

import (
	"fmt"
	"path/filepath"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

const (
	encryptGroupName = "cryptVG"
	encryptVolName   = "root"
)

// GetEncryptedRootVolPath returns the device path of the root volume
func GetEncryptedRootVolPath() string {
	return fmt.Sprintf("%v/%v", encryptGroupName, encryptVolName)
}

// GetEncryptedRootVolMapping returns the device mapping path of the root volume
func GetEncryptedRootVolMapping() string {
	return filepath.Join(mappingFilePath, GetEncryptedRootVol())
}

// GetEncryptedRootVol returns the full root volume name
func GetEncryptedRootVol() string {
	return fmt.Sprintf("%s-%s", encryptGroupName, encryptVolName)
}

func enableLVMForEncryptedRoot(devicePath string) (volumePath string, err error) {
	const (
		fullPhysicalVolume = "100%PVS"
	)

	err = createPhysicalVolume(devicePath)
	if err != nil {
		return
	}

	err = createVolumeGroup(encryptGroupName, devicePath)
	if err != nil {
		return
	}

	err = createLogicalVolume(fullPhysicalVolume, encryptGroupName, encryptVolName)
	if err != nil {
		return
	}

	logger.Log.Infof("Created logical volume on device %v", devicePath)

	volumePath = GetEncryptedRootVolMapping()

	return
}

func createPhysicalVolume(devicePath string) (err error) {
	_, stderr, err := shell.Execute("pvcreate", "-qy", devicePath)
	if err != nil {
		logger.Log.Warnf("Unable to create physical volume on %v: %v", devicePath, stderr)
		return
	}

	return
}

func createVolumeGroup(groupName, devicePath string) (err error) {
	_, stderr, err := shell.Execute("vgcreate", "-qy", groupName, devicePath)
	if err != nil {
		logger.Log.Warnf("Unable to create volume group %v: %v", groupName, stderr)
		return
	}

	return
}

func createLogicalVolume(extents, groupName, volumeName string) (err error) {
	lvCreateArgs := []string{
		"--extents",
		extents,
		groupName,
		"-n",
		volumeName,
	}
	_, stderr, err := shell.Execute("lvcreate", lvCreateArgs...)
	if err != nil {
		logger.Log.Warnf("Unable to create logical volume %v: %v", volumeName, stderr)
		return
	}

	return
}

func deactivateLVM() (err error) {
	_, stderr, err := shell.Execute("vgchange", "-a", "n", encryptGroupName)
	if err != nil {
		logger.Log.Warnf("Unable to deactivate volume group: %v", stderr)
		return
	}

	return
}

func restartLVMetadataService() (err error) {
	_, stderr, err := shell.Execute("systemctl", "restart", "lvm2-lvmetad.service")
	if err != nil {
		logger.Log.Warnf("Unable to restart lvm2-lvmetad.service: %v", stderr)
		return
	}

	return
}
