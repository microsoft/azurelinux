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
	Hostname                string                    `yaml:"Hostname"`
	UpdateBaseImagePackages bool                      `yaml:"UpdateBaseImagePackages"`
	PackageListsInstall     []string                  `yaml:"PackageListsInstall"`
	PackagesInstall         []string                  `yaml:"PackagesInstall"`
	PackageListsRemove      []string                  `yaml:"PackageListsRemove"`
	PackagesRemove          []string                  `yaml:"PackagesRemove"`
	PackageListsUpdate      []string                  `yaml:"PackageListsUpdate"`
	PackagesUpdate          []string                  `yaml:"PackagesUpdate"`
	AdditionalFiles         map[string]FileConfigList `yaml:"AdditionalFiles"`
	PostInstallScripts      []Script                  `yaml:"PostInstallScripts"`
	FinalizeImageScripts    []Script                  `yaml:"FinalizeImageScripts"`
	Users                   []User                    `yaml:"Users"`
	Services                Services                  `yaml:"Services"`
	Modules                 Modules                   `yaml:"Modules"`
	Verity                  Verity                    `yaml:"Verity"`
}

func (s *SystemConfig) IsValid() error {
	var err error

	if s.Hostname != "" {
		if !govalidator.IsDNSName(s.Hostname) || strings.Contains(s.Hostname, "_") {
			return fmt.Errorf("invalid hostname: %s", s.Hostname)
		}
	}

	for sourcePath, fileConfigList := range s.AdditionalFiles {
		err = fileConfigList.IsValid()
		if err != nil {
			return fmt.Errorf("invalid file configs for (%s):\n%w", sourcePath, err)
		}
	}

	for i, script := range s.PostInstallScripts {
		err = script.IsValid()
		if err != nil {
			return fmt.Errorf("invalid PostInstallScripts item at index %d: %w", i, err)
		}
	}

	for i, script := range s.FinalizeImageScripts {
		err = script.IsValid()
		if err != nil {
			return fmt.Errorf("invalid FinalizeImageScripts item at index %d: %w", i, err)
		}
	}

	for i, user := range s.Users {
		err = user.IsValid()
		if err != nil {
			return fmt.Errorf("invalid Users item at index %d: %w", i, err)
		}
	}

	if err := s.Services.IsValid(); err != nil {
		return err
	}

	if err := s.Modules.IsValid(); err != nil {
		return err
	}

	if err := s.Verity.IsValid(); err != nil {
		return err
	}

	return nil
}
