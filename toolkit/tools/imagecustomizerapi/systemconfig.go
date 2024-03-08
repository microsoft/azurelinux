// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
	"strings"

	"github.com/asaskevich/govalidator"
)

// SystemConfig defines how each system present on the image is supposed to be configured.
type SystemConfig struct {
	BootType                BootType           `yaml:"BootType"`
	Hostname                string             `yaml:"Hostname"`
	UpdateBaseImagePackages bool               `yaml:"UpdateBaseImagePackages"`
	PackageListsInstall     []string           `yaml:"PackageListsInstall"`
	PackagesInstall         []string           `yaml:"PackagesInstall"`
	PackageListsRemove      []string           `yaml:"PackageListsRemove"`
	PackagesRemove          []string           `yaml:"PackagesRemove"`
	PackageListsUpdate      []string           `yaml:"PackageListsUpdate"`
	PackagesUpdate          []string           `yaml:"PackagesUpdate"`
	KernelCommandLine       KernelCommandLine  `yaml:"KernelCommandLine"`
	AdditionalFiles         AdditionalFilesMap `yaml:"AdditionalFiles"`
	PartitionSettings       []PartitionSetting `yaml:"PartitionSettings"`
	PostInstallScripts      []Script           `yaml:"PostInstallScripts"`
	FinalizeImageScripts    []Script           `yaml:"FinalizeImageScripts"`
	Users                   []User             `yaml:"Users"`
	Services                Services           `yaml:"Services"`
	Modules                 Modules            `yaml:"Modules"`
	Verity                  *Verity            `yaml:"Verity"`
	Overlays                *[]Overlay         `yaml:"Overlays"`
}

func (s *SystemConfig) IsValid() error {
	var err error

	err = s.BootType.IsValid()
	if err != nil {
		return err
	}

	if s.Hostname != "" {
		if !govalidator.IsDNSName(s.Hostname) || strings.Contains(s.Hostname, "_") {
			return fmt.Errorf("invalid hostname: %s", s.Hostname)
		}
	}

	err = s.KernelCommandLine.IsValid()
	if err != nil {
		return fmt.Errorf("invalid KernelCommandLine: %w", err)
	}

	err = s.AdditionalFiles.IsValid()
	if err != nil {
		return fmt.Errorf("invalid AdditionalFiles: %w", err)
	}

	partitionIDSet := make(map[string]bool)
	for i, partition := range s.PartitionSettings {
		err = partition.IsValid()
		if err != nil {
			return fmt.Errorf("invalid PartitionSettings item at index (%d): %w", i, err)
		}

		if _, existingName := partitionIDSet[partition.ID]; existingName {
			return fmt.Errorf("duplicate PartitionSettings ID used (%s) at index (%d)", partition.ID, i)
		}

		partitionIDSet[partition.ID] = false // dummy value
	}

	for i, script := range s.PostInstallScripts {
		err = script.IsValid()
		if err != nil {
			return fmt.Errorf("invalid PostInstallScripts item at index (%d): %w", i, err)
		}
	}

	for i, script := range s.FinalizeImageScripts {
		err = script.IsValid()
		if err != nil {
			return fmt.Errorf("invalid FinalizeImageScripts item at index (%d): %w", i, err)
		}
	}

	for i, user := range s.Users {
		err = user.IsValid()
		if err != nil {
			return fmt.Errorf("invalid Users item at index (%d): %w", i, err)
		}
	}

	if err := s.Services.IsValid(); err != nil {
		return err
	}

	if err := s.Modules.IsValid(); err != nil {
		return err
	}

	if s.Verity != nil {
		err = s.Verity.IsValid()
		if err != nil {
			return fmt.Errorf("invalid Verity: %w", err)
		}
	}

	if s.Overlays != nil {
		upperDirs := make(map[string]bool)
		workDirs := make(map[string]bool)
		// Initialize a counter for overlays with a specified persistent partition
		persistentPartitionCount := 0

		for i, overlay := range *s.Overlays {
			// Validate the overlay itself
			err := overlay.IsValid()
			if err != nil {
				return fmt.Errorf("invalid Overlay (LowerDir: (%s)) at index (%d): %w", overlay.LowerDir, i, err)
			}

			// Check for unique UpperDir
			if _, exists := upperDirs[overlay.UpperDir]; exists {
				return fmt.Errorf("duplicate UpperDir (%s) found in Overlay (LowerDir: (%s)) at index (%d)", overlay.UpperDir, overlay.LowerDir, i)
			}
			upperDirs[overlay.UpperDir] = true

			// Check for unique WorkDir
			if _, exists := workDirs[overlay.WorkDir]; exists {
				return fmt.Errorf("duplicate WorkDir (%s) found in Overlay (LowerDir: (%s)) at index (%d)", overlay.WorkDir, overlay.LowerDir, i)
			}
			workDirs[overlay.WorkDir] = true

			// Check if the overlay has a specified persistent partition
			if overlay.Partition != nil {
				persistentPartitionCount++
			}
		}
		// Enforce that only one or zero persistent partitions to support
		// Overlays. Currently, the Overlayfs Dracut module from CBL-Mariner RPM
		// supports at most one persistent partition across all configured
		// overlays. While multiple overlays can be defined, only one of these
		// can be configured with a persistent storage option to ensure
		// compatibility with the underlying system architecture and to prevent
		// conflicts during the mount process. It's important to note that this
		// is a temporary limitation. Future optimizations are planned to
		// enhance the Overlayfs Dracut module's capabilities, allowing each
		// overlay to optionally have its own persistent partition. The
		// development team is actively working on these improvements to support
		// a more versatile and robust overlay filesystem configuration.
		if persistentPartitionCount > 1 {
			return fmt.Errorf("more than one overlay has a specified persistent partition, which is not supported")
		}
	}

	return nil
}
