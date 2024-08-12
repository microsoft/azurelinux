// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"os"
	"os/exec"
	"path"
	"path/filepath"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
)

func enableOverlays(overlays *[]imagecustomizerapi.Overlay, imageChroot *safechroot.Chroot) (bool, error) {
	var err error

	if overlays == nil {
		return false, nil
	}

	logger.Log.Infof("Enable filesystem overlays")

	// Integrate overlay driver into the initramfs img.
	overlayDriver := "overlay"
	err = addDracutDriver(overlayDriver, imageChroot)
	if err != nil {
		return false, err
	}

	// Dereference the pointer to get the slice
	overlaysDereference := *overlays
	err = updateFstabForOverlays(imageChroot, overlaysDereference)
	if err != nil {
		return false, fmt.Errorf("failed to update fstab file for overlays:\n%w", err)
	}

	// Create necessary directories for overlays
	err = createOverlayDirectories(imageChroot, overlaysDereference)
	if err != nil {
		return false, fmt.Errorf("failed to create overlay directories:\n%w", err)
	}

	// Add equivalency rules for each overlay
	for _, overlay := range overlaysDereference {
		err = addEquivalencyRule(filepath.Join(imageChroot.RootDir(), overlay.UpperDir), filepath.Join(imageChroot.RootDir(), overlay.LowerDir))
		if err != nil {
			return false, fmt.Errorf("failed to add equivalency rule for overlay:\n%w", err)
		}
	}

	return true, nil
}

func updateFstabForOverlays(imageChroot *safechroot.Chroot, overlays []imagecustomizerapi.Overlay) error {
	var err error

	fstabFile := filepath.Join(imageChroot.RootDir(), "etc", "fstab")
	fstabEntries, err := diskutils.ReadFstabFile(fstabFile)
	if err != nil {
		return fmt.Errorf("failed to read fstab file: %v", err)
	}

	var updatedEntries []diskutils.FstabEntry
	for _, entry := range fstabEntries {
		updatedEntries = append(updatedEntries, entry)
	}

	for _, overlay := range overlays {
		lowerDir := overlay.LowerDir
		upperDir := overlay.UpperDir
		workDir := overlay.WorkDir
		mountDependency := overlay.MountDependency

		if overlay.IsRootfsOverlay {
			lowerDir = path.Join("/sysroot", overlay.LowerDir)
			upperDir = path.Join("/sysroot", overlay.UpperDir)
			workDir = path.Join("/sysroot", overlay.WorkDir)
			if mountDependency != nil {
				dep := path.Join("/sysroot", *mountDependency)
				mountDependency = &dep
			}
		}

		options := fmt.Sprintf("lowerdir=%s,upperdir=%s,workdir=%s", lowerDir, upperDir, workDir)

		// Add any additional options if needed (e.g., x-initrd.mount, x-systemd.requires)
		if mountDependency != nil {
			options = fmt.Sprintf("%s,x-systemd.requires=%s", options, *mountDependency)
		}
		if overlay.IsRootfsOverlay {
			options = fmt.Sprintf("%s,x-initrd.mount", options)
		}
		if overlay.MountOptions != nil && *overlay.MountOptions != "" {
			options = fmt.Sprintf("%s,%s", options, *overlay.MountOptions)
		}

		// Create the FstabEntry based on the overlay.
		newEntry := diskutils.FstabEntry{
			Source:  "overlay",
			Target:  overlay.MountPoint,
			FsType:  "overlay",
			Options: options,
			Freq:    0,
			PassNo:  0,
		}

		updatedEntries = append(updatedEntries, newEntry)
	}

	err = diskutils.WriteFstabFile(updatedEntries, fstabFile)
	if err != nil {
		return err
	}

	return nil
}

func createOverlayDirectories(imageChroot *safechroot.Chroot, overlays []imagecustomizerapi.Overlay) error {
	for _, overlay := range overlays {
		dirsToCreate := []string{
			filepath.Join(imageChroot.RootDir(), overlay.MountPoint),
			filepath.Join(imageChroot.RootDir(), overlay.UpperDir),
			filepath.Join(imageChroot.RootDir(), overlay.WorkDir),
		}

		// Iterate over each directory and create it if it doesn't exist.
		for _, dir := range dirsToCreate {
			if err := os.MkdirAll(dir, os.ModePerm); err != nil {
				return fmt.Errorf("failed to create directory (%s): %w", dir, err)
			}
		}
	}

	return nil
}

func addEquivalencyRule(upperDir string, lowerDir string) error {
	// Construct the semanage command
	cmd := exec.Command("semanage", "fcontext", "-a", "-e", upperDir, lowerDir)

	// Execute the command
	output, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Errorf("failed to add equivalency rule between %s and %s: %v\nOutput: %s", upperDir, lowerDir, err, string(output))
	}

	return nil
}
