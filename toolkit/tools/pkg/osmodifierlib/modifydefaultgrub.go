// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package osmodifierlib

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/imagecustomizerlib"
)

var grubArgs = []string{
	"rd.overlayfs",
	"root",
	"roothash",
	"selinux",
	"enforcing",
}

func modifyDefaultGrub() error {
	var dummyChroot safechroot.ChrootInterface = &safechroot.DummyChroot{}
	// Get verity, selinux, overlayfs, and root device values from /boot/grub2/grub.cfg
	values, rootDevice, err := extractValuesFromGrubConfig(dummyChroot)
	if err != nil {
		return fmt.Errorf("error getting verity, selinux and overlayfs values from grub.cfg:\n%w", err)
	}

	bootCustomizer, err := imagecustomizerlib.NewBootCustomizer(dummyChroot)
	if err != nil {
		return err
	}

	// Stamp verity, selinux and overlayfs values to /etc/default/grub
	err = bootCustomizer.UpdateKernelCommandLineArgs("GRUB_CMDLINE_LINUX", grubArgs, values)
	if err != nil {
		return err
	}

	// Stamp root device to /etc/default/grub
	err = bootCustomizer.SetRootDevice(rootDevice)
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

	lines, err := imagecustomizerlib.FindNonRecoveryLinuxLine(grubCfgContent)
	if err != nil {
		return nil, "", err
	}

	if len(lines) != 1 {
		return nil, "", fmt.Errorf("expected 1 non-recovery linux line, found %d", len(lines))
	}

	argTokens, err := imagecustomizerlib.ParseCommandLineArgs(lines[0].Tokens)
	if err != nil {
		return nil, "", err
	}

	var values []string
	var rootDevice string
	for _, arg := range argTokens {
		if sliceutils.ContainsValue(grubArgs, arg.Name) {
			if arg.Value != "" {
				if arg.Name == "root" {
					rootDevice = arg.Value
				} else {
					values = append(values, arg.Name+"="+arg.Value)
				}
			}
		}
	}
	return values, rootDevice, nil
}
