// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"
)

type Config struct {
	Disks        *[]Disk      `yaml:"disks"`
	Iso          *Iso         `yaml:"iso"`
	SystemConfig SystemConfig `yaml:"systemConfig"`
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

	err = c.SystemConfig.IsValid()
	if err != nil {
		return err
	}

	hasDisks := c.Disks != nil
	hasBootType := c.SystemConfig.BootType != BootTypeUnset
	hasPartitionSettings := len(c.SystemConfig.PartitionSettings) > 0
	hasResetBootLoader := c.SystemConfig.ResetBootLoaderType != ResetBootLoaderTypeDefault

	if hasDisks != hasBootType {
		return fmt.Errorf("systemConfig.bootType and disks must be specified together")
	}

	if hasDisks != hasResetBootLoader {
		return fmt.Errorf("systemConfig.resetBootLoaderType and disks must be specified together'")
	}

	if hasPartitionSettings && !hasDisks {
		return fmt.Errorf("the disks and systemConfig.bootType values must also be specified if systemConfig.partitionSettings is specified")
	}

	// Ensure the correct partitions exist to support the specified the boot type.
	switch c.SystemConfig.BootType {
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
	for i, partitionSetting := range c.SystemConfig.PartitionSettings {
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
