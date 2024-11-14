// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package osmodifierapi

import (
	"fmt"
	"strings"

	"github.com/asaskevich/govalidator"
	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
)

// OS defines how each system present on the image is supposed to be configured.
type OS struct {
	Hostname          string                               `yaml:"hostname"`
	SELinux           imagecustomizerapi.SELinux           `yaml:"selinux"`
	Users             []imagecustomizerapi.User            `yaml:"users"`
	Overlays          *[]Overlay                           `yaml:"overlays"`
	Services          imagecustomizerapi.Services          `yaml:"services"`
	Modules           []imagecustomizerapi.Module          `yaml:"modules"`
	KernelCommandLine imagecustomizerapi.KernelCommandLine `yaml:"kernelCommandLine"`
}

func (s *OS) IsValid() error {
	var err error

	if s.Hostname != "" {
		if !govalidator.IsDNSName(s.Hostname) || strings.Contains(s.Hostname, "_") {
			return fmt.Errorf("invalid hostname (%s)", s.Hostname)
		}
	}

	err = s.SELinux.IsValid()
	if err != nil {
		return fmt.Errorf("invalid selinux:\n%w", err)
	}

	for i, user := range s.Users {
		err = user.IsValid()
		if err != nil {
			return fmt.Errorf("invalid users item at index %d:\n%w", i, err)
		}
	}

	if s.Overlays != nil {
		upperDirs := make(map[string]bool)
		workDirs := make(map[string]bool)

		for i, overlay := range *s.Overlays {
			// Validate the overlay itself
			err := overlay.IsValid()
			if err != nil {
				return fmt.Errorf("invalid overlay at index %d:\n%w", i, err)
			}

			// Check for unique UpperDir
			if _, exists := upperDirs[overlay.UpperDir]; exists {
				return fmt.Errorf("duplicate upperDir (%s) found in overlay at index %d", overlay.UpperDir, i)
			}
			upperDirs[overlay.UpperDir] = true

			// Check for unique WorkDir
			if _, exists := workDirs[overlay.WorkDir]; exists {
				return fmt.Errorf("duplicate workDir (%s) found in overlay at index %d", overlay.WorkDir, i)
			}
			workDirs[overlay.WorkDir] = true
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
			return fmt.Errorf("invalid modules item at index %d:\n%w", i, err)
		}
	}

	return nil
}
