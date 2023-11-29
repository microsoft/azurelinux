// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

// PartitionFlag describes the features of a partition.
type PartitionFlag string

const (
	// PartitionFlagEsp indicates this is a UEFI System Partition (ESP).
	//
	// On GPT disks, "boot" and "esp" must always be specified together.
	PartitionFlagESP PartitionFlag = "esp"

	// PartitionFlagBiosGrub indicates this is the BIOS boot partition.
	// This is required for GPT disks that wish to be bootable using legacy BIOS mode.
	// This partition must start at block 1.
	//
	// See, https://en.wikipedia.org/wiki/BIOS_boot_partition
	PartitionFlagBiosGrub PartitionFlag = "bios_grub"

	// PartitionFlagBoot indicates this is a boot partition.
	//
	// On GPT disks, "boot" and "esp" must always be specified together.
	PartitionFlagBoot PartitionFlag = "boot"
)

func (p PartitionFlag) IsValid() (err error) {
	switch p {
	case PartitionFlagBoot, PartitionFlagBiosGrub, PartitionFlagESP:
		// All good.
		return nil

	default:
		return fmt.Errorf("unknown PartitionFlag value (%s)", p)
	}
}
