// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package osmodifierlib

import (
	"fmt"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/imagecustomizerlib"
)

func modifyDefaultGrub() error {
	var dummyChroot safechroot.ChrootInterface = &safechroot.DummyChroot{}
	// Get verity, selinux and overlayfs values in /boot/grub2/grub.cfg
	verityAndOverlayValues, rootDeviceValue, err := extractValuesFromGrubConfig(dummyChroot)
	if err != nil {
		return fmt.Errorf("error getting changes:\n%v", err)
	}

	bootCustomizer, err := imagecustomizerlib.NewBootCustomizer(dummyChroot)
	if err != nil {
		return err
	}

	// Stamp root device to /etc/default/grub
	err = bootCustomizer.PrepareForVerity(rootDeviceValue)
	if err != nil {
		return fmt.Errorf("failed to prepare grub config files for verity:\n%v", err)
	}

	// Merge existing grub cmdline values with new values
	updatedCmdline, err := bootCustomizer.UpdateCmdlineValues(verityAndOverlayValues)
	if err != nil {
		return err
	}

	// Stamp verity, selinux and overlayfs to /etc/default/grub
	err = bootCustomizer.ApplyChangesToGrub("GRUB_CMDLINE_LINUX", updatedCmdline)
	if err != nil {
		return fmt.Errorf("error applying verity changes to default grub:\n%v", err)
	}

	err = bootCustomizer.WriteToFile(dummyChroot)
	if err != nil {
		return fmt.Errorf("error writing to default grub:\n%v", err)
	} else {
		logger.Log.Info("Successfully updated default grub")
	}

	return nil
}

func extractValuesFromGrubConfig(imageChroot safechroot.ChrootInterface) (string, string, error) {
	grubCfgContent, err := imagecustomizerlib.ReadGrub2ConfigFile(imageChroot)
	if err != nil {
		return "", "", err
	}

	line, err := imagecustomizerlib.FindLinuxLine(grubCfgContent)
	if err != nil {
		return "", "", err
	}

	argTokens, err := imagecustomizerlib.ParseCommandLineArgs(line.Tokens)
	if err != nil {
		return "", "", err
	}

	var verityAndOverlayValues []string
	var rootValue string
	for _, arg := range argTokens {
		if strings.Contains(arg.Name, "overlayfs") ||
			strings.Contains(arg.Name, "verity") ||
			strings.Contains(arg.Name, "roothash") ||
			strings.Contains(arg.Name, "verity_root_data") ||
			strings.Contains(arg.Name, "verity_root_hash") ||
			strings.Contains(arg.Name, "verity_root_options") ||
			strings.Contains(arg.Name, "selinux") ||
			strings.Contains(arg.Name, "enforcing") {
			if arg.Value != "" {
				verityAndOverlayValues = append(verityAndOverlayValues, arg.Name+"="+arg.Value)
			}
		}

		if strings.HasPrefix(arg.Name, "root") && !strings.HasPrefix(arg.Name, "roothash") {
			if arg.Value != "" {
				rootValue = arg.Value
			}
		}

	}

	return strings.Join(verityAndOverlayValues, " "), rootValue, nil
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

	if selinuxMode == imagecustomizerapi.SELinuxModeDisabled {
		// SELinux is disabled in the kernel command line.
		// So, no need to call setfiles.
		return nil
	}

	// No need to set SELinux labels here as in trident there is reset labels at the end
	return nil
}
