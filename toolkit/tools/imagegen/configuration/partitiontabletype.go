// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
)

// PartitionTableType is either gpt, mbr, or none
type PartitionTableType string

const (
	// PartitionTableTypeGpt selects gpt
	PartitionTableTypeGpt PartitionTableType = "gpt"
	// PartitionTableTypeMbr selects mbr
	PartitionTableTypeMbr PartitionTableType = "mbr"
	// PartitionTableTypeNone selects no partition type
	PartitionTableTypeNone PartitionTableType = ""
)

var partitionTableTypeToPartedArgument = map[PartitionTableType]string{
	PartitionTableTypeGpt:  "gpt",
	PartitionTableTypeMbr:  "msdos",
	PartitionTableTypeNone: "",
}

func (p PartitionTableType) String() string {
	return string(p)
}

// GetValidPartitionTableTypes returns a list of all the supported
// disk partition types
func (p *PartitionTableType) GetValidPartitionTableTypes() (types []PartitionTableType) {
	return []PartitionTableType{
		PartitionTableTypeGpt,
		PartitionTableTypeMbr,
		PartitionTableTypeNone,
	}
}

// IsValid returns an error if the PartitionTableType is not valid
func (p *PartitionTableType) IsValid() (err error) {
	for _, valid := range p.GetValidPartitionTableTypes() {
		if *p == valid {
			return
		}
	}
	return fmt.Errorf("invalid value for PartitionTableType (%s)", p)
}

// ConvertToPartedArgument returns the parted argument corresponding to the
// partition table type
func (p *PartitionTableType) ConvertToPartedArgument() (partedArgument string, err error) {
	if err = p.IsValid(); err != nil {
		return
	}
	partedArgument = partitionTableTypeToPartedArgument[*p]
	return
}

// UnmarshalJSON Unmarshals a PartitionTableType entry
func (p *PartitionTableType) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypePartitionTableType PartitionTableType
	err = json.Unmarshal(b, (*IntermediateTypePartitionTableType)(p))
	if err != nil {
		return fmt.Errorf("failed to parse [PartitionTableType]: %w", err)
	}

	// Now validate the resulting unmarshaled object
	err = p.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [PartitionTableType]: %w", err)
	}
	return
}
