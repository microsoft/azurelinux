// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
)

// TargetDisk [kickstart-only] defines the physical disk, to which
// Mariner should be installed.
type TargetDisk struct {
	Type  TargetDiskType `json:"Type"`
	Value string         `json:"Value"`
}

// IsValid returns an error if the RaidConfig is not valid
func (t *TargetDisk) IsValid() (err error) {

	// Validate TargetDiskType
	if err = t.Type.IsValid(); err != nil {
		return fmt.Errorf("invalid [TargetDisk]: %w", err)
	}

	// Path must include a path to a disk
	if t.Type == TargetDiskTypePath {
		if t.Value == "" {
			return fmt.Errorf("invalid [TargetDisk]: Value must be specified for TargetDiskType of '%s'", TargetDiskTypePath)
		}
	}

	// Only allow empty struct if target type is empty
	if t.Type == TargetDiskTypeNone {
		if t.Value != "" {
			return fmt.Errorf("invalid [TargetDisk]: Value must be empty for TargetDiskType of '%s'", TargetDiskTypeNone)
		}
	}

	return nil
}

// UnmarshalJSON Unmarshals a RaidConfig entry
func (t *TargetDisk) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypeTargetDisk TargetDisk
	err = json.Unmarshal(b, (*IntermediateTypeTargetDisk)(t))
	if err != nil {
		return fmt.Errorf("failed to parse [TargetDisk]: %w", err)
	}

	// Now validate the resulting unmarshaled object
	err = t.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [TargetDisk]: %w", err)
	}
	return
}
