// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
)

func enableOverlays(overlays *[]imagecustomizerapi.Overlay, imageChroot *safechroot.Chroot) error {
	var err error

	if overlays == nil {
		return nil
	}

	// Integrate overlay dracut module and overlay driver into initramfs img.
	overlayDracutModule := "overlayfs"
	overlayDracutDriver := "overlay"
	err = buildDracutModule(overlayDracutModule, overlayDracutDriver, imageChroot)
	if err != nil {
		return err
	}

	// Dereference the pointer to get the slice
	overlaysDereference := *overlays
	err = updateGrubConfigForOverlay(imageChroot, overlaysDereference)
	if err != nil {
		return err
	}

	return nil
}

func updateGrubConfigForOverlay(imageChroot *safechroot.Chroot, overlays []imagecustomizerapi.Overlay) error {
	var err error
	var overlayConfigs []string
	var formattedPartition string

	// Iterate over each Overlay configuration
	for _, overlay := range overlays {
		formattedPartition = ""
		if overlay.Partition != nil {
			formattedPartition, err = systemdFormatPartitionId(overlay.Partition.IdType, overlay.Partition.Id)
			if err != nil {
				return err
			}
		}
		// Construct the argument for each Overlay
		overlayConfig := fmt.Sprintf(
			"%s,%s,%s,%s",
			overlay.LowerDir, overlay.UpperDir, overlay.WorkDir, formattedPartition,
		)
		overlayConfigs = append(overlayConfigs, overlayConfig)
	}

	// Concatenate all overlay configurations with spaces
	concatenatedOverlays := strings.Join(overlayConfigs, " ")

	// Construct the final cmdline argument
	newArgs := fmt.Sprintf("rd.overlayfs=\"%s\"", concatenatedOverlays)

	grubCfgPath := filepath.Join(imageChroot.RootDir(), "boot/grub2/grub.cfg")
	lines, err := file.ReadLines(grubCfgPath)
	if err != nil {
		return fmt.Errorf("failed to read grub config: %w", err)
	}

	var updatedLines []string
	linuxLineRegex, err := regexp.Compile(`^linux .*rd.overlayfs=.*`)
	if err != nil {
		return fmt.Errorf("failed to compile regex: %w", err)
	}
	for _, line := range lines {
		trimmedLine := strings.TrimSpace(line)
		if linuxLineRegex.MatchString(trimmedLine) {
			// Replace existing arguments for overlays.
			overlayRegexPattern := `rd.overlayfs=[^ ]*`
			overlayRegex, err := regexp.Compile(overlayRegexPattern)
			if err != nil {
				return fmt.Errorf("failed to compile overlay regex: %w", err)
			}
			newLinuxLine := overlayRegex.ReplaceAllString(trimmedLine, newArgs)
			updatedLines = append(updatedLines, newLinuxLine)
		} else if strings.HasPrefix(trimmedLine, "linux ") {
			// Append new overlay arguments if no existing overlay arguments are found.
			updatedLines = append(updatedLines, line+" "+newArgs)
		} else {
			// Add other lines unchanged.
			updatedLines = append(updatedLines, line)
		}
	}

	// Write the updated lines back to grub.cfg
	err = file.WriteLines(updatedLines, grubCfgPath)
	if err != nil {
		return fmt.Errorf("failed to write updated grub config: %w", err)
	}

	return nil
}
