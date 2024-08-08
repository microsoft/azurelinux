// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package osmodifierlib

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/imagecustomizerlib"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/installutils"
)

func doModifications(baseConfigPath string, osConfig *imagecustomizerapi.OS) error {
	var dummyChroot safechroot.ChrootInterface = &safechroot.DummyChroot{}
	err := imagecustomizerlib.AddOrUpdateUsers(osConfig.Users, baseConfigPath, dummyChroot)
	if err != nil {
		return err
	}

	err = imagecustomizerlib.UpdateHostname(osConfig.Hostname, dummyChroot)
	if err != nil {
		return err
	}

	selinuxMode, err := handleSELinux(osConfig.SELinux.Mode, dummyChroot)
	if err != nil {
		return err
	}

	if selinuxMode == imagecustomizerapi.SELinuxModeDisabled {
		// SELinux is disabled in the kernel command line.
		// So, no need to call setfiles.
		return nil
	}

	logger.Log.Infof("Setting file SELinux labels")

	// Set the SELinux config file and relabel all the files.
	err = installutils.SELinuxRelabelFiles(dummyChroot, make(map[string]string, 0), true)
	if err != nil {
		return fmt.Errorf("failed to set SELinux file labels:\n%w", err)
	}

	return nil
}

func handleSELinux(selinuxMode imagecustomizerapi.SELinuxMode, imageChroot safechroot.ChrootInterface,
) (imagecustomizerapi.SELinuxMode, error) {
	var err error

	bootCustomizer, err := imagecustomizerlib.NewBootCustomizer(imageChroot)
	if err != nil {
		return imagecustomizerapi.SELinuxModeDefault, err
	}

	currentSELinuxMode, err := bootCustomizer.GetSELinuxMode(imageChroot)
	if err != nil {
		return imagecustomizerapi.SELinuxModeDefault, fmt.Errorf("failed to get current SELinux mode:\n%w", err)
	}

	if selinuxMode == imagecustomizerapi.SELinuxModeDefault || selinuxMode == currentSELinuxMode {
		// Don't need to change the configured SELinux mode.
		return imagecustomizerapi.SELinuxModeDefault, nil
	}

	logger.Log.Infof("Configuring SELinux mode")

	err = bootCustomizer.UpdateSELinuxCommandLine(selinuxMode)
	if err != nil {
		return imagecustomizerapi.SELinuxModeDefault, err
	}

	err = bootCustomizer.WriteToFile(imageChroot)
	if err != nil {
		return imagecustomizerapi.SELinuxModeDefault, err
	}

	err = imagecustomizerlib.UpdateSELinuxModeInConfigFile(selinuxMode, imageChroot)
	if err != nil {
		return imagecustomizerapi.SELinuxModeDefault, err
	}

	return selinuxMode, nil
}
