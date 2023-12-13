// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
)

var (
	linuxCommandLineRegex = regexp.MustCompile(`\tlinux .* (\$kernelopts)`)
)

func handleKernelCommandLine(extraCommandLine string, imageChroot *safechroot.Chroot, partitionsCustomized bool) error {
	var err error

	if partitionsCustomized {
		// ExtraCommandLine was handled when the new image was created and the grub.cfg file was regenerated from
		// scatch.
		return nil
	}

	if extraCommandLine == "" {
		// Nothing to do.
		return nil
	}

	logger.Log.Infof("Setting KernelCommandLine.ExtraCommandLine")

	grub2ConfigFilePath := filepath.Join(imageChroot.RootDir(), "/boot/grub2/grub.cfg")

	// Read the existing grub.cfg file.
	grub2ConfigFileBytes, err := os.ReadFile(grub2ConfigFilePath)
	if err != nil {
		return fmt.Errorf("failed to read existing grub2 config file: %w", err)
	}

	grub2ConfigFile := string(grub2ConfigFileBytes)

	// Find the point where the new command line arguments should be added.
	match := linuxCommandLineRegex.FindStringSubmatchIndex(grub2ConfigFile)
	if match == nil {
		return fmt.Errorf("failed to find Linux kernel command line params in grub2 config file")
	}

	// Get the location of "$kernelopts".
	// Note: regexp returns index pairs. So, [2] is the start index of the 1st group.
	insertIndex := match[2]

	// Insert new command line arguments.
	newGrub2ConfigFile := grub2ConfigFile[:insertIndex] + extraCommandLine + " " + grub2ConfigFile[insertIndex:]

	// Update grub.cfg file.
	err = os.WriteFile(grub2ConfigFilePath, []byte(newGrub2ConfigFile), 0)
	if err != nil {
		return fmt.Errorf("failed to write new grub2 config file: %w", err)
	}

	return nil
}
