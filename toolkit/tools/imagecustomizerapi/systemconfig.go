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
	BootType                BootType                  `yaml:"bootType"`
	Hostname                string                    `yaml:"hostname"`
	UpdateBaseImagePackages bool                      `yaml:"updateBaseImagePackages"`
	PackageListsInstall     []string                  `yaml:"packageListsInstall"`
	PackagesInstall         []string                  `yaml:"packagesInstall"`
	PackageListsRemove      []string                  `yaml:"packageListsRemove"`
	PackagesRemove          []string                  `yaml:"packagesRemove"`
	PackageListsUpdate      []string                  `yaml:"packageListsUpdate"`
	PackagesUpdate          []string                  `yaml:"packagesUpdate"`
	KernelCommandLine       KernelCommandLine         `yaml:"kernelCommandLine"`
	AdditionalFiles         map[string]FileConfigList `yaml:"additionalFiles"`
	PartitionSettings       []PartitionSetting        `yaml:"partitionSettings"`
	PostInstallScripts      []Script                  `yaml:"postInstallScripts"`
	FinalizeImageScripts    []Script                  `yaml:"finalizeImageScripts"`
	Users                   []User                    `yaml:"users"`
	Services                Services                  `yaml:"services"`
	Modules                 Modules                   `yaml:"modules"`
	Verity                  *Verity                   `yaml:"verity"`
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

	for sourcePath, fileConfigList := range s.AdditionalFiles {
		err = fileConfigList.IsValid()
		if err != nil {
			return fmt.Errorf("invalid file configs for (%s):\n%w", sourcePath, err)
		}
	}

	partitionIDSet := make(map[string]bool)
	for i, partition := range s.PartitionSettings {
		err = partition.IsValid()
		if err != nil {
			return fmt.Errorf("invalid PartitionSettings item at index %d: %w", i, err)
		}

		if _, existingName := partitionIDSet[partition.ID]; existingName {
			return fmt.Errorf("duplicate PartitionSettings ID used (%s) at index %d", partition.ID, i)
		}

		partitionIDSet[partition.ID] = false // dummy value
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

	if s.Verity != nil {
		err = s.Verity.IsValid()
		if err != nil {
			return fmt.Errorf("invalid Verity: %w", err)
		}
	}

	return nil
}
