// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
)

// RaidConfig holds the raid configuration information for a software raid disk
// valid levels:
// 0: No parity, striping only
// 1: Mirror on two+ disks
// 4: Parity with 1 dedicated parity disk
// 5: Parity on three+ disks with distributed parity
// 6: Raid 5 with additional parity blocks
// 10: Four+ disks with striped mirrors
type RaidConfig struct {
	ComponentPartIDs []string `json:"ComponentPartIDs"` // PartIDs of the partitions to be used in the raid
	Level            int      `json:"Level"`            // 0, 1, 4, 5, 6, 10
	RaidID           string   `json:"RaidID"`           // ID of the raid device used for mdadm
	LegacyMetadata   bool     `json:"LegacyMetadata"`   // Use legacy metadata for mdadm to support efi boot partitions
}

// IsEmpty returns true if the RaidConfig is empty
func (r *RaidConfig) IsEmpty() bool {
	return len(r.ComponentPartIDs) == 0 && r.Level == 0 && len(r.RaidID) == 0
}

// IsValid returns an error if the RaidConfig is not valid
func (r *RaidConfig) IsValid() (err error) {

	switch r.Level {
	case 0, 1, 4, 5, 6, 10:
		// Valid
	default:
		return fmt.Errorf("invalid [RaidConfig]: Level must be one of 0, 1, 4, 5, 6, 10")
	}

	if !r.IsEmpty() && (len(r.ComponentPartIDs) == 0 || len(r.RaidID) == 0) {
		return fmt.Errorf("invalid [RaidConfig]: Raid '%s' must have non-empty ComponentPartIDs and RaidID", r.RaidID)
	}

	return nil
}

// UnmarshalJSON Unmarshals a RaidConfig entry
func (r *RaidConfig) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypeRaidConfig RaidConfig
	err = json.Unmarshal(b, (*IntermediateTypeRaidConfig)(r))
	if err != nil {
		return fmt.Errorf("failed to parse [RaidConfig]: %w", err)
	}

	// Now validate the resulting unmarshaled object
	err = r.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [RaidConfig]: %w", err)
	}
	return
}
