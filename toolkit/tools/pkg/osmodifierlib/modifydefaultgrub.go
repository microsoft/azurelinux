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
	"roothash",
	"rd.systemd.verity",
	"systemd.verity_root_data",
	"systemd.verity_root_hash",
	"systemd.verity_root_options",
	"selinux",
	"enforcing",
}

func modifyDefaultGrub() error {
	var dummyChroot safechroot.ChrootInterface = &safechroot.DummyChroot{}
	// Get verity, selinux, overlayfs, and root device values from /boot/grub2/grub.cfg
	values, err := extractValuesFromGrubConfig(dummyChroot)
	if err != nil {
		return fmt.Errorf("error getting verity, selinux and overlayfs values from grub.cfg:\n%w", err)
	}

	bootCustomizer, err := imagecustomizerlib.NewBootCustomizer(dummyChroot)
	if err != nil {
		return err
	}

	// Stamp root device value to /etc/default/grub
	err = bootCustomizer.PrepareForVerity()
	if err != nil {
		return fmt.Errorf("failed to prepare grub config files for verity:\n%w", err)
	}

	// Stamp verity, selinux and overlayfs values to /etc/default/grub
	err = bootCustomizer.UpdateKernelCommandLineArgs("GRUB_CMDLINE_LINUX", grubArgs, values)
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

func extractValuesFromGrubConfig(imageChroot safechroot.ChrootInterface) ([]string, error) {
	grubCfgContent, err := imagecustomizerlib.ReadGrub2ConfigFile(imageChroot)
	if err != nil {
		return nil, err
	}

	line, err := imagecustomizerlib.FindLinuxLine(grubCfgContent)
	if err != nil {
		return nil, err
	}

	argTokens, err := imagecustomizerlib.ParseCommandLineArgs(line.Tokens)
	if err != nil {
		return nil, err
	}

	var values []string
	for _, arg := range argTokens {
		if sliceutils.ContainsValue(grubArgs, arg.Name) {
			if arg.Value != "" {
				values = append(values, arg.Name+"="+arg.Value)
			}
		}
	}

	return values, nil
}
