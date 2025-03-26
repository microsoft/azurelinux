// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
)

// TargetDiskType sets the backing disk type for the disk
type TargetDiskType string

const (
	// TargetDiskTypePath means this is a /dev/sda or similar disk that already exists
	TargetDiskTypePath TargetDiskType = "path"
	// TargetDiskTypeRAID creates a RAID disk
	TargetDiskTypeRaid TargetDiskType = "raid"
	// TargetDiskTypeNone means there is no target disk
	TargetDiskTypeNone TargetDiskType = ""
)

func (t TargetDiskType) String() string {
	return fmt.Sprint(string(t))
}

// GetValidTargetDiskTypes returns a list of all the supported
// disk types
func (t *TargetDiskType) GetValidTargetDiskTypes() (types []TargetDiskType) {
	return []TargetDiskType{
		TargetDiskTypePath,
		TargetDiskTypeRaid,
		TargetDiskTypeNone,
	}
}

// IsValid returns an error if the TargetDiskType is not valid
func (t *TargetDiskType) IsValid() (err error) {
	for _, valid := range t.GetValidTargetDiskTypes() {
		if *t == valid {
			return
		}
	}
	return fmt.Errorf("invalid value for TargetDiskType (%s)", t)
}

// UnmarshalJSON Unmarshals an TargetDiskType entry
func (t *TargetDiskType) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypeTargetDiskType TargetDiskType
	err = json.Unmarshal(b, (*IntermediateTypeTargetDiskType)(t))
	if err != nil {
		return fmt.Errorf("failed to parse [TargetDiskType]: %w", err)
	}

	// Now validate the resulting unmarshaled object
	err = t.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [TargetDiskType]: %w", err)
	}
	return
}
