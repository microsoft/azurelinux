// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
)

// PartitionSetting holds the mounting information for each partition.
type PartitionSetting struct {
	RemoveDocs       bool            `json:"RemoveDocs"`
	ID               string          `json:"ID"`
	MountIdentifier  MountIdentifier `json:"MountIdentifier"`
	MountOptions     string          `json:"MountOptions"`
	MountPoint       string          `json:"MountPoint"`
	OverlayBaseImage string          `json:"OverlayBaseImage"`
	RdiffBaseImage   string          `json:"RdiffBaseImage"`
}

var defaultPartitionSetting PartitionSetting = PartitionSetting{
	MountIdentifier: GetDefaultMountIdentifier(),
}

// GetDefaultPartitionSetting returns a copy of the default partition setting
func GetDefaultPartitionSetting() (defaultVal PartitionSetting) {
	defaultVal = defaultPartitionSetting
	return defaultVal
}

// IsValid returns an error if the PartitionSetting is not valid
func (p *PartitionSetting) IsValid() (err error) {
	return nil
}

// UnmarshalJSON Unmarshals a PartitionSetting entry
func (p *PartitionSetting) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypePartitionSetting PartitionSetting

	// Populate non-standard default values
	*p = GetDefaultPartitionSetting()

	err = json.Unmarshal(b, (*IntermediateTypePartitionSetting)(p))
	if err != nil {
		return fmt.Errorf("failed to parse [PartitionSetting]: %w", err)
	}

	// Now validate the resulting unmarshaled object
	err = p.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [PartitionSetting]: %w", err)
	}
	return
}

// FindRootPartitionSetting returns a pointer to the partition setting describing the disk which
// will be mounted at "/", or nil if no partition is found
func FindRootPartitionSetting(partitionSettings []PartitionSetting) (rootPartitionSetting *PartitionSetting) {
	return FindMountpointPartitionSetting(partitionSettings, "/")
}

// FindMountpointPartitionSetting will search a list of partition settings for the partition setting
// corresponding to a mount point.
func FindMountpointPartitionSetting(partitionSettings []PartitionSetting, mountPoint string) (partitionSetting *PartitionSetting) {
	for _, p := range partitionSettings {
		if p.MountPoint == mountPoint {
			// We want to reference the actual object in the slice
			return &p
		}
	}
	return nil
}
