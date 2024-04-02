// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

// BootPartitionType describes the type of boot partition.
type BootPartitionType string

const (
	// PartitionBootTypeDefault indicates this is a normal partition.
	BootPartitionTypeDefault BootPartitionType = ""

	// PartitionFlagEsp indicates this is a UEFI System Partition (ESP).
	BootPartitionTypeESP BootPartitionType = "esp"

	// PartitionFlagBiosGrub indicates this is the BIOS boot partition.
	// This is required for GPT disks that wish to be bootable using legacy BIOS mode.
	// This partition must start at block 1.
	//
	// See, https://en.wikipedia.org/wiki/BIOS_boot_partition
	BootPartitionTypeBiosGrub BootPartitionType = "bios-grub"
)

func (p BootPartitionType) IsValid() (err error) {
	switch p {
	case BootPartitionTypeDefault, BootPartitionTypeESP, BootPartitionTypeBiosGrub:
		// All good.
		return nil

	default:
		return fmt.Errorf("unknown partition boot type value (%s)", p)
	}
}
