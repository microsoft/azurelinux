// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
	"strings"

	"github.com/asaskevich/govalidator"
)

// OS defines how each system present on the image is supposed to be configured.
type OS struct {
	BootType             BootType            `yaml:"bootType"`
	ResetBootLoaderType  ResetBootLoaderType `yaml:"resetBootLoaderType"`
	Hostname             string              `yaml:"hostname"`
	Packages             Packages            `yaml:"packages"`
	SELinux              SELinux             `yaml:"selinux"`
	KernelCommandLine    KernelCommandLine   `yaml:"kernelCommandLine"`
	AdditionalFiles      AdditionalFilesMap  `yaml:"additionalFiles"`
	PartitionSettings    []PartitionSetting  `yaml:"partitionSettings"`
	PostInstallScripts   []Script            `yaml:"postInstallScripts"`
	FinalizeImageScripts []Script            `yaml:"finalizeImageScripts"`
	Users                []User              `yaml:"users"`
	Services             Services            `yaml:"services"`
	Modules              Modules             `yaml:"modules"`
	Verity               *Verity             `yaml:"verity"`
	Overlays             *[]Overlay          `yaml:"overlays"`
}

func (s *OS) IsValid() error {
	var err error

	err = s.BootType.IsValid()
	if err != nil {
		return err
	}

	err = s.ResetBootLoaderType.IsValid()
	if err != nil {
		return err
	}

	if s.Hostname != "" {
		if !govalidator.IsDNSName(s.Hostname) || strings.Contains(s.Hostname, "_") {
			return fmt.Errorf("invalid hostname: %s", s.Hostname)
		}
	}

	err = s.SELinux.IsValid()
	if err != nil {
		return fmt.Errorf("invalid selinux:\n%w", err)
	}

	err = s.KernelCommandLine.IsValid()
	if err != nil {
		return fmt.Errorf("invalid kernelCommandLine: %w", err)
	}

	err = s.AdditionalFiles.IsValid()
	if err != nil {
		return fmt.Errorf("invalid additionalFiles: %w", err)
	}

	partitionIDSet := make(map[string]bool)
	for i, partition := range s.PartitionSettings {
		err = partition.IsValid()
		if err != nil {
			return fmt.Errorf("invalid partitionSettings item at index %d: %w", i, err)
		}

		if _, existingName := partitionIDSet[partition.ID]; existingName {
			return fmt.Errorf("duplicate partitionSettings ID used (%s) at index %d", partition.ID, i)
		}

		partitionIDSet[partition.ID] = false // dummy value
	}

	for i, script := range s.PostInstallScripts {
		err = script.IsValid()
		if err != nil {
			return fmt.Errorf("invalid postInstallScripts item at index %d: %w", i, err)
		}
	}

	for i, script := range s.FinalizeImageScripts {
		err = script.IsValid()
		if err != nil {
			return fmt.Errorf("invalid finalizeImageScripts item at index %d: %w", i, err)
		}
	}

	for i, user := range s.Users {
		err = user.IsValid()
		if err != nil {
			return fmt.Errorf("invalid users item at index %d: %w", i, err)
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
			return fmt.Errorf("invalid verity: %w", err)
		}
	}

	if s.Overlays != nil {
		upperDirs := make(map[string]bool)
		workDirs := make(map[string]bool)

		for i, overlay := range *s.Overlays {
			// Validate the overlay itself
			err := overlay.IsValid()
			if err != nil {
				return fmt.Errorf("invalid overlay (lowerDir: '%s') at index %d: %w", overlay.LowerDir, i, err)
			}

			// Check for unique UpperDir
			if _, exists := upperDirs[overlay.UpperDir]; exists {
				return fmt.Errorf("duplicate upperDir '%s' found in overlay (lowerDir: '%s') at index %d", overlay.UpperDir, overlay.LowerDir, i)
			}
			upperDirs[overlay.UpperDir] = true

			// Check for unique WorkDir
			if _, exists := workDirs[overlay.WorkDir]; exists {
				return fmt.Errorf("duplicate workDir '%s' found in overlay (lowerDir: '%s') at index %d", overlay.WorkDir, overlay.LowerDir, i)
			}
			workDirs[overlay.WorkDir] = true
		}
	}

	return nil
}
