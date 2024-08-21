// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"path/filepath"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/installutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
)

func handleSELinux(selinuxMode imagecustomizerapi.SELinuxMode, resetBootLoaderType imagecustomizerapi.ResetBootLoaderType,
	imageChroot *safechroot.Chroot,
) (imagecustomizerapi.SELinuxMode, error) {
	var err error

	bootCustomizer, err := NewBootCustomizer(imageChroot)
	if err != nil {
		return imagecustomizerapi.SELinuxModeDefault, err
	}

	if selinuxMode == imagecustomizerapi.SELinuxModeDefault {
		// No changes to the SELinux have been requested.
		// So, return the current SELinux mode.
		currentSELinuxMode, err := bootCustomizer.GetSELinuxMode(imageChroot)
		if err != nil {
			return imagecustomizerapi.SELinuxModeDefault, fmt.Errorf("failed to get current SELinux mode:\n%w", err)
		}

		return currentSELinuxMode, nil
	}

	logger.Log.Infof("Configuring SELinux mode")

	switch resetBootLoaderType {
	case imagecustomizerapi.ResetBootLoaderTypeHard:
		// The grub.cfg file has been recreated from scratch and therefore the SELinux args will already be correct and
		// don't need to be updated.

	default:
		// Update the SELinux kernel command-line args.
		err := bootCustomizer.UpdateSELinuxCommandLine(selinuxMode)
		if err != nil {
			return imagecustomizerapi.SELinuxModeDefault, err
		}

		err = bootCustomizer.WriteToFile(imageChroot)
		if err != nil {
			return imagecustomizerapi.SELinuxModeDefault, err
		}
	}

	err = updateSELinuxModeInConfigFile(selinuxMode, imageChroot)
	if err != nil {
		return imagecustomizerapi.SELinuxModeDefault, err
	}

	return selinuxMode, nil
}

func updateSELinuxModeInConfigFile(selinuxMode imagecustomizerapi.SELinuxMode, imageChroot *safechroot.Chroot) error {
	imagerSELinuxMode, err := selinuxModeToImager(selinuxMode)
	if err != nil {
		return err
	}

	selinuxConfigFileFullPath := filepath.Join(imageChroot.RootDir(), installutils.SELinuxConfigFile)
	selinuxConfigFileExists, err := file.PathExists(selinuxConfigFileFullPath)
	if err != nil {
		return fmt.Errorf("failed to check if (%s) file exists:\n%w", installutils.SELinuxConfigFile, err)
	}

	// Ensure an SELinux policy has been installed.
	// Typically, this is provided by the 'selinux-policy' package.
	if selinuxMode != imagecustomizerapi.SELinuxModeDisabled && !selinuxConfigFileExists {
		return fmt.Errorf("SELinux is enabled but the (%s) file is missing:\n"+
			"please ensure an SELinux policy is installed:\n"+
			"the '%s' package provides the default policy",
			installutils.SELinuxConfigFile, configuration.SELinuxPolicyDefault)
	}

	if selinuxConfigFileExists {
		err = installutils.SELinuxUpdateConfig(imagerSELinuxMode, imageChroot)
		if err != nil {
			return fmt.Errorf("failed to set SELinux mode in config file:\n%w", err)
		}
	}

	return nil
}

func selinuxSetFiles(selinuxMode imagecustomizerapi.SELinuxMode, imageChroot *safechroot.Chroot) error {
	if selinuxMode == imagecustomizerapi.SELinuxModeDisabled {
		// SELinux is disabled in the kernel command line.
		// So, no need to call setfiles.
		return nil
	}

	logger.Log.Infof("Setting file SELinux labels")

	// Get the list of mount points.
	mountPointToFsTypeMap := make(map[string]string, 0)
	for _, mountPoint := range getNonSpecialChrootMountPoints(imageChroot) {
		mountPointToFsTypeMap[mountPoint.GetTarget()] = mountPoint.GetFSType()
	}

	// Set the SELinux config file and relabel all the files.
	err := installutils.SELinuxRelabelFiles(imageChroot, mountPointToFsTypeMap, false)
	if err != nil {
		return fmt.Errorf("failed to set SELinux file labels:\n%w", err)
	}

	return nil
}
