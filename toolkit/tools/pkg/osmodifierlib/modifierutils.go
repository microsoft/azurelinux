// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package osmodifierlib

import (
	"fmt"
	"regexp"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/imagecustomizerlib"
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

	if osConfig.Overlays != nil {
		_, err = imagecustomizerlib.EnableOverlays(osConfig.Overlays, dummyChroot)
		if err != nil {
			return err
		}
	}

	if osConfig.KernelCommandLine.ExtraCommandLine != "" || osConfig.SELinux.Mode != "" {
		bootCustomizer, err := imagecustomizerlib.NewBootCustomizer(dummyChroot)
		if err != nil {
			return err
		}

		err = handleSELinux(osConfig.SELinux.Mode, bootCustomizer, dummyChroot)
		if err != nil {
			return err
		}

		err = updateRootDevice(osConfig.KernelCommandLine.ExtraCommandLine, bootCustomizer)
		if err != nil {
			return err
		}

		err = bootCustomizer.WriteToFile(dummyChroot)
		if err != nil {
			return err
		}
	}

	return nil
}

func modifyDefaultGrub() error {
	var dummyChroot safechroot.ChrootInterface = &safechroot.DummyChroot{}
	// Get verity and overlayfs values in /boot/grub2/grub.cfg
	verityAndOverlayValues, rootDeviceValue, err := extractValuesFromGrubConfig(dummyChroot)
	if err != nil {
		return fmt.Errorf("error getting changes:\n%v", err)
	}

	bootCustomizer, err := imagecustomizerlib.NewBootCustomizer(dummyChroot)
	if err != nil {
		return err
	}

	// Stamp verity and overlayfs to /etc/default/grub
	err = bootCustomizer.ApplyChangesToGrub("GRUB_CMDLINE_LINUX", verityAndOverlayValues)
	if err != nil {
		return fmt.Errorf("error applying verity changes to default grub:\n%v", err)
	}

	// Stamp root device to /etc/default/grub
	err = bootCustomizer.ApplyChangesToGrub("GRUB_DEVICE", rootDeviceValue)
	if err != nil {
		return fmt.Errorf("error  to default grub:\n%v", err)
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

func updateRootDevice(kernelExtraArguments imagecustomizerapi.KernelExtraArguments, bootCustomizer *imagecustomizerlib.BootCustomizer) error {
	// Function to extract the root value from kernelCommandLine.extraCommandLine
	re := regexp.MustCompile(`root=([^\s]+)`)
	matches := re.FindStringSubmatch(string(kernelExtraArguments))
	if len(matches) < 2 {
		return fmt.Errorf("no root device found in extraCommandLine")
	}

	rootDeviceValue := matches[1]

	err := bootCustomizer.ApplyChangesToGrub("GRUB_DEVICE", rootDeviceValue)
	if err != nil {
		return fmt.Errorf("error writing root device to default grub:\n%v", err)
	}
	return nil
}
