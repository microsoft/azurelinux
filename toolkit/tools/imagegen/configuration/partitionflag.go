// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
)

// PartitionFlag describes the features of a partition
type PartitionFlag string

const (
	// PartitionFlagESP indicates this is the UEFI esp partition
	PartitionFlagESP PartitionFlag = "esp"
	// PartitionFlagGrub indicates this is a grub boot partition
	PartitionFlagGrub PartitionFlag = "grub"
	// PartitionFlagBiosGrub indicates this is a bios grub boot partition
	PartitionFlagBiosGrub PartitionFlag = "bios_grub"
	// PartitionFlagBiosGrubLegacy indicates this is a bios grub boot partition. Needed to preserve legacy config behavior.
	PartitionFlagBiosGrubLegacy PartitionFlag = "bios-grub"
	// PartitionFlagBoot indicates this is a boot partition
	PartitionFlagBoot PartitionFlag = "boot"
	// PartitionFlagDeviceMapperRoot indicates this partition will be used for a device mapper root device
	PartitionFlagDeviceMapperRoot PartitionFlag = "dmroot"
)

func (p PartitionFlag) String() string {
	return fmt.Sprint(string(p))
}

// GetValidPartitionFlags returns a list of all the supported
// partition flags
func (p *PartitionFlag) GetValidPartitionFlags() (types []PartitionFlag) {
	return []PartitionFlag{
		PartitionFlagESP,
		PartitionFlagGrub,
		PartitionFlagBiosGrub,
		PartitionFlagBiosGrubLegacy,
		PartitionFlagBoot,
		PartitionFlagDeviceMapperRoot,
	}
}

// IsValid returns an error if the PartitionFlag is not valid
func (p *PartitionFlag) IsValid() (err error) {
	for _, valid := range p.GetValidPartitionFlags() {
		if *p == valid {
			return
		}
	}
	return fmt.Errorf("invalid value for Flag (%s)", p)
}

// UnmarshalJSON Unmarshals an PartitionFlag entry
func (p *PartitionFlag) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypePartitionFlag PartitionFlag
	err = json.Unmarshal(b, (*IntermediateTypePartitionFlag)(p))
	if err != nil {
		return fmt.Errorf("failed to parse [Flag]: %w", err)
	}

	// Now validate the resulting unmarshaled object
	err = p.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [Flag]: %w", err)
	}
	return
}
