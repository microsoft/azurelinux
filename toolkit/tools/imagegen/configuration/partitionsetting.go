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
	RemoveDocs       bool   `json:"RemoveDocs"`
	ID               string `json:"ID"`
	MountOptions     string `json:"MountOptions"`
	MountPoint       string `json:"MountPoint"`
	OverlayBaseImage string `json:"OverlayBaseImage"`
	RdiffBaseImage   string `json:"RdiffBaseImage"`
}

// IsValid returns an error if the PartitionSetting is not valid
func (p *PartitionSetting) IsValid() (err error) {
	return nil
}

// UnmarshalJSON Unmarshals a PartitionSetting entry
func (p *PartitionSetting) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypePartitionSetting PartitionSetting
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
