// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package osmodifierlib

import (
	"fmt"
	"strings"

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

	// Merge existing grub cmdline values with new values
	updatedCmdline, err := bootCustomizer.UpdateCmdlineValues(values)
	if err != nil {
		return err
	}

	// Stamp verity, selinux and overlayfs values to /etc/default/grub
	err = bootCustomizer.ApplyChangesToGrub("GRUB_CMDLINE_LINUX", updatedCmdline)
	if err != nil {
		return fmt.Errorf("error applying verity changes to default grub:\n%w", err)
	}

	err = bootCustomizer.WriteToFile(dummyChroot)
	if err != nil {
		return fmt.Errorf("error writing to default grub:\n%w", err)
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

	var values []string
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
				values = append(values, arg.Name+"="+arg.Value)
			}
		}

		if arg.Name == "root" && arg.Value != "" {
			rootValue = arg.Value
		}
	}

	return imagecustomizerlib.GrubArgsToString(values), rootValue, nil
}
