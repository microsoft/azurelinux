// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package osmodifierlib

import (
	"fmt"
	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/imagecustomizerlib"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
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

	err = handleSELinux(osConfig.SELinux.Mode, dummyChroot)
	if err != nil {
		return err
	}

	return nil
}

func handleSELinux(selinuxMode imagecustomizerapi.SELinuxMode, imageChroot safechroot.ChrootInterface) error {
	var err error

	bootCustomizer, err := imagecustomizerlib.NewBootCustomizer(imageChroot)
	if err != nil {
		return err
	}

	currentSELinuxMode, err := bootCustomizer.GetSELinuxMode(imageChroot)
	if err != nil {
		return fmt.Errorf("failed to get current SELinux mode:\n%w", err)
	}

	if selinuxMode == imagecustomizerapi.SELinuxModeDefault || selinuxMode == currentSELinuxMode {
		// Don't need to change the configured SELinux mode.
		return nil
	}

	logger.Log.Infof("Configuring SELinux mode")

	err = bootCustomizer.UpdateSELinuxCommandLine(selinuxMode)
	if err != nil {
		return err
	}

	err = imagecustomizerapi.WriteGrub2ConfigFile(bootCustomizer.grubCfgContent, imageChroot)
	if err != nil {
		return err
	}

	return nil
}
