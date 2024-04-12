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
	ResetBootLoaderType ResetBootLoaderType `yaml:"resetBootLoaderType"`
	Hostname            string              `yaml:"hostname"`
	Packages            Packages            `yaml:"packages"`
	SELinux             SELinux             `yaml:"selinux"`
	KernelCommandLine   KernelCommandLine   `yaml:"kernelCommandLine"`
	AdditionalFiles     AdditionalFilesMap  `yaml:"additionalFiles"`
	Users               []User              `yaml:"users"`
	Services            Services            `yaml:"services"`
	Modules             []Module            `yaml:"modules"`
	Verity              *Verity             `yaml:"verity"`
	Overlays            *[]Overlay          `yaml:"overlays"`
}

func (s *OS) IsValid() error {
	var err error
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

	for i, user := range s.Users {
		err = user.IsValid()
		if err != nil {
			return fmt.Errorf("invalid users item at index %d: %w", i, err)
		}
	}

	if err := s.Services.IsValid(); err != nil {
		return err
	}

	moduleMap := make(map[string]int)
	for i, module := range s.Modules {
		// Check if module is duplicated to avoid conflicts with modules potentially having different LoadMode
		if _, exists := moduleMap[module.Name]; exists {
			return fmt.Errorf("duplicate module found: %s at index %d", module.Name, i)
		}
		moduleMap[module.Name] = i
		err = module.IsValid()
		if err != nil {
			return fmt.Errorf("invalid Modules item at index %d:\n%w", i, err)
		}
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
