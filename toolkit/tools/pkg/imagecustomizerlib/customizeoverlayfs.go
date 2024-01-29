// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
)

func enableOverlayFS(overlays *[]imagecustomizerapi.OverlayFS, imageChroot *safechroot.Chroot) error {
	var err error

	if overlays == nil {
		return nil
	}

	// Integrate overlayfs dracut module and overlay driver into initramfs img.
	// Integrate systemd veritysetup dracut module into initramfs img.
	overlayfsDracutModule := "overlayfs"
	overlayDracutDriver := "overlay"
	err = buildDracutModule(overlayfsDracutModule, overlayDracutDriver, imageChroot)
	if err != nil {
		return err
	}

	err = updateGrubConfigForOverlayFS(imageChroot, overlays)
	if err != nil {
		return err
	}

	return nil
}

func updateGrubConfigForOverlayFS(imageChroot *safechroot.Chroot, overlays *[]imagecustomizerapi.OverlayFS) error {
	var err error
	var newArgsParts []string

	// Dereference the pointer to get the slice
	overlayFSConfigs := *overlays

	// Iterate over each OverlayFS configuration
	for _, overlay := range overlayFSConfigs {
		formattedPersistentPartition, err := systemdFormatPartitionId(overlay.PersistentPartition.IdType, overlay.PersistentPartition.Id)
		if err != nil {
			return err
		}

		// Construct cmdline arguments for each OverlayFS
		newArg := fmt.Sprintf(
			"rd.overlays=%s,%s,%s rd.overlayfs_persistent_volume=%s",
			overlay.LowerDir, overlay.UpperDir, overlay.WorkDir, formattedPersistentPartition,
		)
		newArgsParts = append(newArgsParts, newArg)
	}

	// Concatenate all cmdline arguments
	newArgs := strings.Join(newArgsParts, " ")

	grubCfgPath := filepath.Join(imageChroot.RootDir(), "boot/grub2/grub.cfg")
	lines, err := file.ReadLines(grubCfgPath)
	if err != nil {
		return fmt.Errorf("failed to read grub config: %v", err)
	}

	var updatedLines []string
	linuxLineRegex := regexp.MustCompile(`^linux .*rd.overlays=.*`)
	for _, line := range lines {
		trimmedLine := strings.TrimSpace(line)
		if linuxLineRegex.MatchString(trimmedLine) {
			// Replace existing arguments for overlays.
			overlayRegexPattern := `rd.overlays=[^ ]*` +
				`( rd.overlayfs_persistent_volume=[^ ]*)?`
			overlayRegex := regexp.MustCompile(overlayRegexPattern)
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
		return fmt.Errorf("failed to write updated grub config: %v", err)
	}

	return nil
}
