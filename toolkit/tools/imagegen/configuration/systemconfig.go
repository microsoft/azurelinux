// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
	"strings"
)

// SystemConfig defines how each system present on the image is supposed to be configured.
type SystemConfig struct {
	IsDefault          bool                `json:"IsDefault"`
	BootType           string              `json:"BootType"`
	Hostname           string              `json:"Hostname"`
	Name               string              `json:"Name"`
	PackageLists       []string            `json:"PackageLists"`
	KernelOptions      map[string]string   `json:"KernelOptions"`
	KernelCommandLine  KernelCommandLine   `json:"KernelCommandLine"`
	AdditionalFiles    map[string]string   `json:"AdditionalFiles"`
	PartitionSettings  []PartitionSetting  `json:"PartitionSettings"`
	PostInstallScripts []PostInstallScript `json:"PostInstallScripts"`
	Groups             []Group             `json:"Groups"`
	Users              []User              `json:"Users"`
	Encryption         RootEncryption      `json:"Encryption"`
}

// IsValid returns an error if the SystemConfig is not valid
func (s *SystemConfig) IsValid() (err error) {
	// IsDefault must be validated by a parent struct

	// Validate BootType

	// Validate HostName

	if strings.TrimSpace(s.Name) == "" {
		return fmt.Errorf("missing [Name] field")
	}

	if len(s.PackageLists) == 0 {
		return fmt.Errorf("system configuration must provide at least one package list inside the [PackageLists] field")
	}

	// Enforce that any non-rootfs configuration has a default kernel.
	if len(s.PartitionSettings) != 0 {
		// Ensure that default option is always present
		if _, ok := s.KernelOptions["default"]; !ok {
			return fmt.Errorf("system configuration must always provide default kernel inside the [KernelOptions] field; remember that kernels are FORBIDDEN from appearing in any of the [PackageLists]")
		}
		// Ensure that non-comment options are not blank
		for name, kernelName := range s.KernelOptions {
			// Skip comments
			if name[0] == '_' {
				continue
			}
			if strings.TrimSpace(kernelName) == "" {
				return fmt.Errorf("empty kernel entry found in the [KernelOptions] field (%s); remember that kernels are FORBIDDEN from appearing in any of the [PackageLists]", name)
			}
		}

		// for _, partitionSetting := range sysConfig.PartitionSettings {
		// 	if err = partitionSetting.IsValid(); err != nil {
		// 		return fmt.Errorf("invalid [PartitionSettings]: %w", err)
		// 	}
		// }
	}

	if err = s.KernelCommandLine.IsValid(); err != nil {
		return fmt.Errorf("invalid [KernelCommandLine]: %w", err)
	}

	//Validate PartitionSettings
	//Validate PostInstallScripts
	//Validate Groups
	//Validate Users
	for _, b := range s.Users {
		if err = b.IsValid(); err != nil {
			return fmt.Errorf("invalid [User]: %w", err)
		}
	}

	//Validate Encryption

	return
}

// UnmarshalJSON Unmarshals a Disk entry
func (s *SystemConfig) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypeSystemConfig SystemConfig
	err = json.Unmarshal(b, (*IntermediateTypeSystemConfig)(s))
	if err != nil {
		return fmt.Errorf("failed to parse [SystemConfig]: %w", err)
	}

	// Now validate the resulting unmarshaled object
	err = s.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [SystemConfig]: %w", err)
	}
	return
}
