// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"os"
	"path"
	"path/filepath"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"
)

func enableOverlays(overlays *[]imagecustomizerapi.Overlay, selinuxMode imagecustomizerapi.SELinuxMode,
	imageChroot safechroot.ChrootInterface,
) (bool, error) {
	var err error

	if overlays == nil {
		return false, nil
	}

	logger.Log.Infof("Enable filesystem overlays")

	// Integrate the overlay driver into the initrd image. Including the overlay
	// driver in initrd is essential for enabling the system to recognize and
	// mount overlay filesystems during the initrd phase of the boot process.
	overlayDriver := "overlay"
	err = addDracutDriver(overlayDriver, imageChroot)
	if err != nil {
		return false, err
	}

	// Dereference the pointer to get the slice
	overlaysDereference := *overlays
	err = updateFstabForOverlays(overlaysDereference, imageChroot)
	if err != nil {
		return false, fmt.Errorf("failed to update fstab file for overlays:\n%w", err)
	}

	// Create necessary directories for overlays
	err = createOverlayDirectories(overlaysDereference, imageChroot)
	if err != nil {
		return false, fmt.Errorf("failed to create overlay directories:\n%w", err)
	}

	// Add equivalency rules for each overlay
	err = addEquivalencyRules(selinuxMode, overlaysDereference, imageChroot)
	if err != nil {
		return false, fmt.Errorf("failed to add equivalency rules for overlays:\n%w", err)
	}

	return true, nil
}

func updateFstabForOverlays(overlays []imagecustomizerapi.Overlay, imageChroot safechroot.ChrootInterface,
) error {
	var err error

	fstabFile := filepath.Join(imageChroot.RootDir(), "etc/fstab")
	fstabEntries, err := diskutils.ReadFstabFile(fstabFile)
	if err != nil {
		return fmt.Errorf("failed to read fstab file: %v", err)
	}

	var updatedEntries []diskutils.FstabEntry
	updatedEntries = append(updatedEntries, fstabEntries...)

	for _, overlay := range overlays {
		lowerDirs := overlay.LowerDirs
		upperDir := overlay.UpperDir
		workDir := overlay.WorkDir
		mountDependencies := overlay.MountDependencies

		if overlay.IsRootfsOverlay {
			// Validate that each mountDependency has the x-initrd.mount option in
			// the corresponding fstab entry.
			for i, dep := range mountDependencies {
				entry, found := sliceutils.FindValueFunc(fstabEntries, func(entry diskutils.FstabEntry) bool {
					return entry.Target == dep
				})
				if !found {
					return fmt.Errorf("mountDependency %s not found in fstab", dep)
				}

				optionFound := sliceutils.ContainsValue(strings.Split(entry.Options, ","), "x-initrd.mount")
				if !optionFound {
					return fmt.Errorf("mountDependency %s requires x-initrd.mount option in fstab", dep)
				}

				mountDependencies[i] = path.Join("/sysroot", dep)
			}

			for i, dir := range lowerDirs {
				lowerDirs[i] = path.Join("/sysroot", dir)
			}
			upperDir = path.Join("/sysroot", overlay.UpperDir)
			workDir = path.Join("/sysroot", overlay.WorkDir)
		}

		// Multiple lower layers can be specified by joining directory names
		// with a colon (":") as a separator, which is supported by the overlay
		// filesystem in the mount command.
		lowerDirOption := strings.Join(lowerDirs, ":")

		options := fmt.Sprintf("lowerdir=%s,upperdir=%s,workdir=%s", lowerDirOption, upperDir, workDir)

		// Add any additional options if needed (e.g., x-initrd.mount,
		// x-systemd.requires)
		for _, dep := range mountDependencies {
			options = fmt.Sprintf("%s,x-systemd.requires=%s", options, dep)
		}
		if overlay.IsRootfsOverlay {
			options = fmt.Sprintf("%s,x-initrd.mount,x-systemd.wanted-by=initrd-fs.target", options)
		}
		if overlay.MountOptions != "" {
			options = fmt.Sprintf("%s,%s", options, overlay.MountOptions)
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

func createOverlayDirectories(overlays []imagecustomizerapi.Overlay, imageChroot safechroot.ChrootInterface) error {
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

func addEquivalencyRules(selinuxMode imagecustomizerapi.SELinuxMode,
	overlays []imagecustomizerapi.Overlay, imageChroot safechroot.ChrootInterface,
) error {
	var err error

	if selinuxMode == imagecustomizerapi.SELinuxModeDisabled {
		// No need to add equivalency rules if SELinux is disabled.
		return nil
	}

	for _, overlay := range overlays {
		err = imageChroot.UnsafeRun(func() error {
			return shell.ExecuteLiveWithErr(1, "sudo", "semanage", "fcontext", "-a", "-e", overlay.MountPoint, overlay.UpperDir)
		})
		if err != nil {
			return fmt.Errorf("failed to add equivalency rule between %s and %s:\n%w", overlay.MountPoint, overlay.UpperDir, err)
		}
	}

	return nil
}
