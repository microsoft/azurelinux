// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"
)

type Storage struct {
	BootType    BootType     `yaml:"bootType"`
	Disks       []Disk       `yaml:"disks"`
	FileSystems []FileSystem `yaml:"fileSystems"`
}

func (s *Storage) IsValid() error {
	var err error

	err = s.BootType.IsValid()
	if err != nil {
		return err
	}

	if len(s.Disks) < 1 {
		return fmt.Errorf("at least 1 disk must be specified")
	}
	if len(s.Disks) > 1 {
		return fmt.Errorf("multiple disks is not currently supported")
	}

	for i, disk := range s.Disks {
		err := disk.IsValid()
		if err != nil {
			return fmt.Errorf("invalid disk at index %d:\n%w", i, err)
		}
	}

	fileSystemIDSet := make(map[string]bool)
	for i, fileSystem := range s.FileSystems {
		err = fileSystem.IsValid()
		if err != nil {
			return fmt.Errorf("invalid fileSystems item at index %d: %w", i, err)
		}

		if _, existingName := fileSystemIDSet[fileSystem.DeviceId]; existingName {
			return fmt.Errorf("duplicate fileSystem deviceId used (%s) at index %d", fileSystem.DeviceId, i)
		}

		fileSystemIDSet[fileSystem.DeviceId] = false // dummy value
	}

	// Ensure the correct partitions exist to support the specified the boot type.
	switch s.BootType {
	case BootTypeEfi:
		hasEsp := sliceutils.ContainsFunc(s.Disks, func(disk Disk) bool {
			return sliceutils.ContainsFunc(disk.Partitions, func(partition Partition) bool {
				return sliceutils.ContainsValue(partition.Flags, PartitionFlagESP)
			})
		})
		if !hasEsp {
			return fmt.Errorf("'esp' partition must be provided for 'efi' boot type")
		}

	case BootTypeLegacy:
		hasBiosBoot := sliceutils.ContainsFunc(s.Disks, func(disk Disk) bool {
			return sliceutils.ContainsFunc(disk.Partitions, func(partition Partition) bool {
				return sliceutils.ContainsValue(partition.Flags, PartitionFlagBiosGrub)
			})
		})
		if !hasBiosBoot {
			return fmt.Errorf("'bios-grub' partition must be provided for 'legacy' boot type")
		}
	}

	// Ensure all the partition settings object have an equivalent partition object.
	for i, fileSystem := range s.FileSystems {
		diskExists := sliceutils.ContainsFunc(s.Disks, func(disk Disk) bool {
			return sliceutils.ContainsFunc(disk.Partitions, func(partition Partition) bool {
				return partition.Id == fileSystem.DeviceId
			})
		})
		if !diskExists {
			return fmt.Errorf("invalid fileSystem at index %d:\nno partition with matching ID (%s)", i,
				fileSystem.DeviceId)
		}
	}

	return nil
}
