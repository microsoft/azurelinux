// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
)

func enableOverlays(overlays *[]imagecustomizerapi.Overlay, imageChroot *safechroot.Chroot) (bool, error) {
	var err error

	if overlays == nil {
		return false, nil
	}

	logger.Log.Infof("Enable filesystem overlays")

	// Integrate overlay dracut module and overlay driver into initramfs img.
	overlayDracutModule := "overlayfs"
	overlayDracutDriver := "overlay"
	err = addDracutModule(overlayDracutModule, overlayDracutDriver, imageChroot)
	if err != nil {
		return false, err
	}

	// Dereference the pointer to get the slice
	overlaysDereference := *overlays
	err = updateGrubConfigForOverlay(imageChroot, overlaysDereference)
	if err != nil {
		return false, fmt.Errorf("failed to update grub config for filesystem overlays:\n%w", err)
	}

	return true, nil
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
	newArgs := []string{
		fmt.Sprintf("rd.overlayfs=%s", concatenatedOverlays),
	}

	bootCustomizer, err := NewBootCustomizer(imageChroot)
	if err != nil {
		return err
	}

	err = bootCustomizer.UpdateKernelCommandLineArgs(defaultGrubFileVarNameCmdlineLinux, []string{"rd.overlayfs"},
		newArgs)
	if err != nil {
		return err
	}

	err = bootCustomizer.WriteToFile(imageChroot)
	if err != nil {
		return err
	}

	return nil
}
