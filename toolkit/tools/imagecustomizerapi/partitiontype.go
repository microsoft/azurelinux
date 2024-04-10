// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

// PartitionType describes the type of boot partition.
type PartitionType string

const (
	// PartitionTypeDefault indicates this is a normal partition.
	PartitionTypeDefault PartitionType = ""

	// PartitionTypeESP indicates this is a UEFI System Partition (ESP).
	PartitionTypeESP PartitionType = "esp"

	// PartitionTypeBiosGrub indicates this is the BIOS boot partition.
	// This is required for GPT disks that wish to be bootable using legacy BIOS mode.
	// This partition must start at block 1.
	//
	// See, https://en.wikipedia.org/wiki/BIOS_boot_partition
	PartitionTypeBiosGrub PartitionType = "bios-grub"
)

func (p PartitionType) IsValid() (err error) {
	switch p {
	case PartitionTypeDefault, PartitionTypeESP, PartitionTypeBiosGrub:
		// All good.
		return nil

	default:
		return fmt.Errorf("unknown partition type (%s)", p)
	}
}
