// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
	"strings"

	"github.com/asaskevich/govalidator"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
)

// SystemConfig defines how each system present on the image is supposed to be configured.
type SystemConfig struct {
	IsDefault            bool                      `json:"IsDefault"`
	IsKickStartBoot      bool                      `json:"IsKickStartBoot"`
	IsIsoInstall         bool                      `json:"IsIsoInstall"`
	BootType             string                    `json:"BootType"`
	EnableGrubMkconfig   bool                      `json:"EnableGrubMkconfig"`
	Hostname             string                    `json:"Hostname"`
	Name                 string                    `json:"Name"`
	PackageLists         []string                  `json:"PackageLists"`
	Packages             []string                  `json:"Packages"`
	KernelOptions        map[string]string         `json:"KernelOptions"`
	KernelCommandLine    KernelCommandLine         `json:"KernelCommandLine"`
	AdditionalFiles      map[string]FileConfigList `json:"AdditionalFiles"`
	PartitionSettings    []PartitionSetting        `json:"PartitionSettings"`
	PreInstallScripts    []InstallScript           `json:"PreInstallScripts"`
	PostInstallScripts   []InstallScript           `json:"PostInstallScripts"`
	FinalizeImageScripts []InstallScript           `json:"FinalizeImageScripts"`
	Networks             []Network                 `json:"Networks"`
	PackageRepos         []PackageRepo             `json:"PackageRepos"`
	Groups               []Group                   `json:"Groups"`
	Users                []User                    `json:"Users"`
	Encryption           RootEncryption            `json:"Encryption"`
	RemoveRpmDb          bool                      `json:"RemoveRpmDb"`
	ReadOnlyVerityRoot   ReadOnlyVerityRoot        `json:"ReadOnlyVerityRoot"`
	EnableHidepid        bool                      `json:"EnableHidepid"`
}

// GetRootPartitionSetting returns a pointer to the partition setting describing the disk which
// will be mounted at "/", or nil if no partition is found
func (s *SystemConfig) GetRootPartitionSetting() (rootPartitionSetting *PartitionSetting) {
	return FindRootPartitionSetting(s.PartitionSettings)
}

// GetMountpointPartitionSetting will search the system configuration for the partition setting
// corresponding to a mount point.
func (s *SystemConfig) GetMountpointPartitionSetting(mountPoint string) (partitionSetting *PartitionSetting) {
	return FindMountpointPartitionSetting(s.PartitionSettings, mountPoint)
}

// IsValid returns an error if the SystemConfig is not valid
func (s *SystemConfig) IsValid() (err error) {
	// IsDefault must be validated by a parent struct

	// Validate HostName
	if (!govalidator.IsDNSName(s.Hostname) || strings.Contains(s.Hostname, "_")) && s.Hostname != "" {
		return fmt.Errorf("invalid [Hostname]: %s", s.Hostname)
	}

	if strings.TrimSpace(s.Name) == "" {
		return fmt.Errorf("missing [Name] field")
	}

	// Validate BootType
	if s.BootType != "efi" && s.BootType != "legacy" && s.BootType != "none" && s.BootType != "" {
		return fmt.Errorf("invalid [BootType]: %s. Expecting values of either 'efi', 'legacy', 'none' or empty string", s.BootType)
	}

	if len(s.PackageLists) == 0 && len(s.Packages) == 0 {
		return fmt.Errorf("system configuration must provide at least one package list inside the [PackageLists] or one package in the [Packages] field")
	}

	// Additional package list validation must be done via the imageconfigvalidator tool since there is no guranatee that
	// the paths are valid at this point.

	// Enforce that any non-rootfs configuration has a default kernel.
	if len(s.PartitionSettings) != 0 {
		// Ensure that default option is always present
		if _, ok := s.KernelOptions["default"]; !ok {
			return fmt.Errorf("system configuration must always provide default kernel inside the [KernelOptions] field; remember that kernels are FORBIDDEN from appearing in any of the [PackageLists] or [Packages]")
		}
	}
	// A rootfs MAY include a kernel (ISO), so run the full checks even if this is a rootfs
	if len(s.KernelOptions) != 0 {
		// Ensure that non-comment options are not blank
		for name, kernelName := range s.KernelOptions {
			// Skip comments
			if name[0] == '_' {
				continue
			}
			if strings.TrimSpace(kernelName) == "" {
				return fmt.Errorf("empty kernel entry found in the [KernelOptions] field (%s); remember that kernels are FORBIDDEN from appearing in any of the [PackageLists] or [Packages]", name)
			}
		}
	}

	// Validate the partitions this system config will be including
	mountPointUsed := make(map[string]bool)
	for _, partitionSetting := range s.PartitionSettings {
		if err = partitionSetting.IsValid(); err != nil {
			return fmt.Errorf("invalid [PartitionSettings]: %w", err)
		}
		if mountPointUsed[partitionSetting.MountPoint] {
			return fmt.Errorf("invalid [PartitionSettings]: duplicate mount point found at '%s'", partitionSetting.MountPoint)
		}
		if partitionSetting.MountPoint != "" {
			// Don't track unmounted partition duplication (They will all mount at "")
			mountPointUsed[partitionSetting.MountPoint] = true
		}
	}

	if s.ReadOnlyVerityRoot.Enable || s.Encryption.Enable {
		if len(mountPointUsed) == 0 {
			logger.Log.Warnf("[ReadOnlyVerityRoot] or [Encryption] is enabled, but no partitions are listed as part of System Config '%s'. This is only valid for ISO installers", s.Name)
		} else {
			if !mountPointUsed["/"] {
				return fmt.Errorf("invalid [ReadOnlyVerityRoot] or [Encryption]: must have a partition mounted at '/'")
			}
			if s.ReadOnlyVerityRoot.Enable && s.Encryption.Enable {
				return fmt.Errorf("invalid [ReadOnlyVerityRoot] and [Encryption]: verity root currently does not support root encryption")
			}
			if s.ReadOnlyVerityRoot.Enable && !mountPointUsed["/boot"] {
				return fmt.Errorf("invalid [ReadOnlyVerityRoot]: must have a separate partition mounted at '/boot'")
			}
		}
	}

	if err = s.ReadOnlyVerityRoot.IsValid(); err != nil {
		return fmt.Errorf("invalid [ReadOnlyVerityRoot]: %w", err)
	}

	if err = s.KernelCommandLine.IsValid(); err != nil {
		return fmt.Errorf("invalid [KernelCommandLine]: %w", err)
	}

	for srcFile, fileConfigList := range s.AdditionalFiles {
		err = fileConfigList.IsValid()
		if err != nil {
			return fmt.Errorf("invalid [AdditionalFiles]: (%s): %w", srcFile, err)
		}
	}

	// Validate that PackageRepos do not contain duplicate package repo name
	repoNames := make(map[string]bool)
	for _, packageRepo := range s.PackageRepos {
		if err = packageRepo.IsValid(); err != nil {
			return fmt.Errorf("invalid [PackageRepo]: %s. Error: %w", packageRepo.Name, err)
		}

		if repoNames[packageRepo.Name] {
			return fmt.Errorf("invalid [PackageRepos]: duplicate package repo names (%s)", packageRepo.Name)
		}
		repoNames[packageRepo.Name] = true
	}

	//Validate PostInstallScripts

	// Validate Networks
	for idx, network := range s.Networks {
		if err = network.IsValid(); err != nil {
			return fmt.Errorf("invalid [Network] config (%d): %w", (idx + 1), err)
		}
	}

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
