// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package osmodifierlib

import (
	"fmt"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/osmodifierapi"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/imagecustomizerlib"
)

func doModifications(baseConfigPath string, osConfig *osmodifierapi.OS) error {
	var dummyChroot safechroot.ChrootInterface = &safechroot.DummyChroot{}

	err := imagecustomizerlib.AddOrUpdateUsers(osConfig.Users, baseConfigPath, dummyChroot)
	if err != nil {
		return err
	}

	err = imagecustomizerlib.UpdateHostname(osConfig.Hostname, dummyChroot)
	if err != nil {
		return err
	}

	if osConfig.Overlays != nil {
		bootCustomizer, err := imagecustomizerlib.NewBootCustomizer(dummyChroot)
		if err != nil {
			return err
		}

		err = updateGrubConfigForOverlay(*osConfig.Overlays, bootCustomizer)
		if err != nil {
			return err
		}

		err = bootCustomizer.WriteToFile(dummyChroot)
		if err != nil {
			return err
		}
	}

	if osConfig.SELinux.Mode != "" {
		bootCustomizer, err := imagecustomizerlib.NewBootCustomizer(dummyChroot)
		if err != nil {
			return err
		}

		err = handleSELinux(osConfig.SELinux.Mode, bootCustomizer, dummyChroot)
		if err != nil {
			return err
		}

		err = bootCustomizer.WriteToFile(dummyChroot)
		if err != nil {
			return err
		}
	}

	err = imagecustomizerlib.AddKernelCommandLine(osConfig.KernelCommandLine.ExtraCommandLine, dummyChroot)
	if err != nil {
		return fmt.Errorf("failed to add extra kernel command line:\n%w", err)
	}

	return nil
}

func updateGrubConfigForOverlay(overlays []osmodifierapi.Overlay, bootCustomizer *imagecustomizerlib.BootCustomizer) error {
	var err error
	var overlayConfigs []string

	// Iterate over each Overlay configuration
	for _, overlay := range overlays {
		// Construct the argument for each Overlay
		overlayConfig := fmt.Sprintf(
			"%s,%s,%s,%s",
			overlay.LowerDir, overlay.UpperDir, overlay.WorkDir, overlay.Partition.Id,
		)
		overlayConfigs = append(overlayConfigs, overlayConfig)
	}

	// Concatenate all overlay configurations with spaces
	concatenatedOverlays := strings.Join(overlayConfigs, " ")

	// Construct the final cmdline argument
	newArgs := []string{
		fmt.Sprintf("rd.overlayfs=%s", concatenatedOverlays),
	}

	err = bootCustomizer.UpdateKernelCommandLineArgs("GRUB_CMDLINE_LINUX", []string{"rd.overlayfs"},
		newArgs)
	if err != nil {
		return err
	}

	return nil
}

func handleSELinux(selinuxMode imagecustomizerapi.SELinuxMode, bootCustomizer *imagecustomizerlib.BootCustomizer, dummyChroot safechroot.ChrootInterface) error {
	var err error
	currentSELinuxMode, err := bootCustomizer.GetSELinuxMode(dummyChroot)
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

	err = imagecustomizerlib.UpdateSELinuxModeInConfigFile(selinuxMode, dummyChroot)
	if err != nil {
		return err
	}

	// No need to set SELinux labels here as in trident there is reset labels at the end
	return nil
}
