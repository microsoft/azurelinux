// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"
)

type Config struct {
	Disks *[]Disk `yaml:"disks"`
	Iso   *Iso    `yaml:"iso"`
	OS    OS      `yaml:"os"`
}

func (c *Config) IsValid() (err error) {
	if c.Disks != nil {
		disks := *c.Disks
		if len(disks) < 1 {
			return fmt.Errorf("at least 1 disk must be specified (or the disks field should be ommited)")
		}
		if len(disks) > 1 {
			return fmt.Errorf("multiple disks is not currently supported")
		}

		for i, disk := range disks {
			err := disk.IsValid()
			if err != nil {
				return fmt.Errorf("invalid disk at index %d:\n%w", i, err)
			}
		}
	}

	if c.Iso != nil {
		err = c.Iso.IsValid()
		if err != nil {
			return err
		}
	}

	err = c.OS.IsValid()
	if err != nil {
		return err
	}

	hasDisks := c.Disks != nil
	hasBootType := c.OS.BootType != BootTypeUnset
	hasPartitionSettings := len(c.OS.PartitionSettings) > 0
	hasResetBootLoader := c.OS.ResetBootLoaderType != ResetBootLoaderTypeDefault

	if hasDisks != hasBootType {
		return fmt.Errorf("os.bootType and disks must be specified together")
	}

	if hasDisks != hasResetBootLoader {
		return fmt.Errorf("os.resetBootLoaderType and disks must be specified together'")
	}

	if hasPartitionSettings && !hasDisks {
		return fmt.Errorf("the disks and os.bootType values must also be specified if os.partitionSettings is specified")
	}

	// Ensure the correct partitions exist to support the specified the boot type.
	switch c.OS.BootType {
	case BootTypeEfi:
		hasEsp := sliceutils.ContainsFunc(*c.Disks, func(disk Disk) bool {
			return sliceutils.ContainsFunc(disk.Partitions, func(partition Partition) bool {
				return sliceutils.ContainsValue(partition.Flags, PartitionFlagESP)
			})
		})
		if !hasEsp {
			return fmt.Errorf("'esp' partition must be provided for 'efi' boot type")
		}

	case BootTypeLegacy:
		hasBiosBoot := sliceutils.ContainsFunc(*c.Disks, func(disk Disk) bool {
			return sliceutils.ContainsFunc(disk.Partitions, func(partition Partition) bool {
				return sliceutils.ContainsValue(partition.Flags, PartitionFlagBiosGrub)
			})
		})
		if !hasBiosBoot {
			return fmt.Errorf("'bios-grub' partition must be provided for 'legacy' boot type")
		}
	}

	// Ensure all the partition settings object have an equivalent partition object.
	for i, partitionSetting := range c.OS.PartitionSettings {
		diskExists := sliceutils.ContainsFunc(*c.Disks, func(disk Disk) bool {
			return sliceutils.ContainsFunc(disk.Partitions, func(partition Partition) bool {
				return partition.ID == partitionSetting.ID
			})
		})
		if !diskExists {
			return fmt.Errorf("invalid partitionSetting at index %d:\nno partition with matching ID (%s)", i,
				partitionSetting.ID)
		}
	}

	return nil
}
