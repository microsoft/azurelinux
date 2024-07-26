// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
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
		return fmt.Errorf("defining multiple disks is not currently supported")
	}

	for i, disk := range s.Disks {
		err := disk.IsValid()
		if err != nil {
			return fmt.Errorf("invalid disk at index %d:\n%w", i, err)
		}
	}

	fileSystemSet := make(map[string]FileSystem)
	for i, fileSystem := range s.FileSystems {
		err = fileSystem.IsValid()
		if err != nil {
			return fmt.Errorf("invalid fileSystems item at index %d: %w", i, err)
		}

		if _, existingName := fileSystemSet[fileSystem.DeviceId]; existingName {
			return fmt.Errorf("duplicate fileSystem deviceId used (%s) at index %d", fileSystem.DeviceId, i)
		}

		fileSystemSet[fileSystem.DeviceId] = fileSystem
	}

	partitionSet := make(map[string]Partition)
	espPartitionExists := false
	biosBootPartitionExists := false
	partitionLabelCounts := make(map[string]int)

	for i, disk := range s.Disks {
		for j, partition := range disk.Partitions {
			if _, existingName := partitionSet[partition.Id]; existingName {
				return fmt.Errorf("invalid disk at index %d:\nduplicate partition id used (%s) at index %d", i,
					partition.Id, j)
			}

			partitionSet[partition.Id] = partition

			// Ensure special partitions have the correct filesystem type.
			fileSystem, hasFileSystem := fileSystemSet[partition.Id]

			if partition.IsESP() {
				espPartitionExists = true

				if !hasFileSystem || fileSystem.Type != FileSystemTypeFat32 {
					return fmt.Errorf("ESP partition must have 'fat32' filesystem type")
				}
			}

			if partition.IsBiosBoot() {
				biosBootPartitionExists = true

				if !hasFileSystem || fileSystem.Type != FileSystemTypeFat32 {
					return fmt.Errorf("BIOS boot partition must have 'fat32' filesystem type")
				}
			}

			// Count the number of partitions that use each label.
			partitionLabelCounts[partition.Label] += 1
		}
	}

	// Ensure the correct partitions exist to support the specified the boot type.
	switch s.BootType {
	case BootTypeEfi:
		if !espPartitionExists {
			return fmt.Errorf("'esp' partition must be provided for 'efi' boot type")
		}

	case BootTypeLegacy:
		if !biosBootPartitionExists {
			return fmt.Errorf("'bios-grub' partition must be provided for 'legacy' boot type")
		}
	}

	// Ensure all the filesystems objects have an equivalent partition object.
	for i, fileSystem := range s.FileSystems {
		partition, found := partitionSet[fileSystem.DeviceId]
		if !found {
			return fmt.Errorf("invalid fileSystem at index %d:\nno partition with matching ID (%s)", i,
				fileSystem.DeviceId)
		}

		if fileSystem.MountPoint != nil && fileSystem.MountPoint.IdType == MountIdentifierTypePartLabel {
			if partition.Label == "" {
				return fmt.Errorf("invalid fileSystem at index %d:\nidType is set to (part-label) but partition (%s) has no label set",
					i, partition.Id)
			}

			labelCount := partitionLabelCounts[partition.Label]
			if labelCount > 0 {
				return fmt.Errorf("invalid fileSystem at index %d:\nmore than one partition has a label of (%s)", i,
					partition.Label)
			}
		}
	}

	return nil
}
