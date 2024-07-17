// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package osmodifierlib

import (
	"fmt"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/imagecustomizerlib"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/grub"
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

	return nil
}

func doModificationsWithoutConfig() error {
	var dummyChroot safechroot.ChrootInterface = &safechroot.DummyChroot{}
	verityParams, err := getVerityChanges(dummyChroot)
	if err != nil {
		fmt.Printf("Error getting verity changes: %v\n", err)
		return err
	}

	bootCustomizer, err := imagecustomizerlib.NewBootCustomizer(dummyChroot)
	if err != nil {
		return err
	}

	// Apply the verity changes to /etc/default/grub
	err = bootCustomizer.ApplyChangesToGrub("GRUB_CMDLINE_LINUX", verityParams)
	if err != nil {
		fmt.Printf("Error applying verity changes to default grub: %v\n", err)
	} else {
		fmt.Println("Successfully applied verity changes to default grub")
	}

	// Update /boot/grub2/grub.cfg file.
	err = installutils.CallGrubMkconfig(dummyChroot)
	if err != nil {
		return fmt.Errorf("failed to generate grub.cfg via grub2-mkconfig:\n%w", err)
	}

	return nil
}

func getVerityChanges(imageChroot safechroot.ChrootInterface) (string, error) {
	grubCfgContent, err := imagecustomizerlib.ReadGrub2ConfigFile(imageChroot)
	if err != nil {
		return "", err
	}

    newLine, err := imagecustomizerlib.FindLinuxLine(grubCfgContent)
    if err != nil {
        return "", err
    }

    verityParams := parseVerityParams(newLine)
    return verityParams, nil
}

func parseVerityParams(line grub.Line) string {
    var params []string
    for _, token := range line.Tokens {
        // Look for tokens that contain relevant substrings for verity
        if strings.Contains(token.RawContent, "verity") ||
           strings.Contains(token.RawContent, "roothash") ||
           strings.Contains(token.RawContent, "verity_root_data") ||
           strings.Contains(token.RawContent, "verity_root_hash") ||
           strings.Contains(token.RawContent, "verity_root_options") {
            params = append(params, token.RawContent)
        }
    }
    return strings.Join(params, " ")
}
