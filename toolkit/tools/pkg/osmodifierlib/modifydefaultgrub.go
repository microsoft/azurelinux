// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package osmodifierlib

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/imagecustomizerlib"
)

func modifyDefaultGrub() error {
	var dummyChroot safechroot.ChrootInterface = &safechroot.DummyChroot{}
	// Get verity, selinux, overlayfs, and root device values from /boot/grub2/grub.cfg
	values, rootDeviceValue, err := extractValuesFromGrubConfig(dummyChroot)
	if err != nil {
		return fmt.Errorf("error getting verity, selinux and overlayfs values from grub.cfg:\n%w", err)
	}

	bootCustomizer, err := imagecustomizerlib.NewBootCustomizer(dummyChroot)
	if err != nil {
		return err
	}

	// Stamp root device value to /etc/default/grub
	err = bootCustomizer.PrepareForVerity(rootDeviceValue)
	if err != nil {
		return fmt.Errorf("failed to prepare grub config files for verity:\n%w", err)
	}

	old := []string{"rd.overlayfs", "selinux", "enforcing", "rd.systemd.verity", "roothash",
		"systemd.verity_root_data", "systemd.verity_root_hash", "systemd.verity_root_options"}

	// Stamp verity, selinux and overlayfs values to /etc/default/grub
	err = bootCustomizer.UpdateKernelCommandLineArgs("GRUB_CMDLINE_LINUX", old, values)
	if err != nil {
		return err
	}

	err = bootCustomizer.WriteToFile(dummyChroot)
	if err != nil {
		return fmt.Errorf("error writing to default grub:\n%w", err)
	} else {
		logger.Log.Info("Successfully updated default grub")
	}

	return nil
}

func extractValuesFromGrubConfig(imageChroot safechroot.ChrootInterface) ([]string, string, error) {
	grubCfgContent, err := imagecustomizerlib.ReadGrub2ConfigFile(imageChroot)
	if err != nil {
		return nil, "", err
	}

	line, err := imagecustomizerlib.FindLinuxLine(grubCfgContent)
	if err != nil {
		return nil, "", err
	}

	argTokens, err := imagecustomizerlib.ParseCommandLineArgs(line.Tokens)
	if err != nil {
		return nil, "", err
	}

	var values []string
	var rootValue string
	for _, arg := range argTokens {
		if arg.Name == "rd.overlayfs" ||
			arg.Name == "roothash" ||
			arg.Name == "rd.systemd.verity" ||
			arg.Name == "systemd.verity_root_data" ||
			arg.Name == "systemd.verity_root_hash" ||
			arg.Name == "systemd.verity_root_options" ||
			arg.Name == "selinux" ||
			arg.Name == "enforcing" {
			if arg.Value != "" {
				values = append(values, arg.Name+"="+arg.Value)
			}
		}

		if arg.Name == "root" && arg.Value != "" {
			rootValue = arg.Value
		}
	}

	return values, rootValue, nil
}
