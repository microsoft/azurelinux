// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type Storage struct {
	ResetPartitionsUuidsType ResetPartitionsUuidsType `yaml:"resetPartitionsUuidsType"`
	BootType                 BootType                 `yaml:"bootType"`
	Disks                    []Disk                   `yaml:"disks"`
	FileSystems              []FileSystem             `yaml:"filesystems"`
	Verity                   []Verity                 `yaml:"verity"`
}

func (s *Storage) IsValid() error {
	var err error

	err = s.ResetPartitionsUuidsType.IsValid()
	if err != nil {
		return err
	}

	err = s.BootType.IsValid()
	if err != nil {
		return err
	}

	if len(s.Disks) > 1 {
		return fmt.Errorf("defining multiple disks is not currently supported")
	}

	for i := range s.Disks {
		disk := &s.Disks[i]

		err := disk.IsValid()
		if err != nil {
			return fmt.Errorf("invalid disk at index %d:\n%w", i, err)
		}
	}

	for i, verity := range s.Verity {
		err = verity.IsValid()
		if err != nil {
			return fmt.Errorf("invalid verity item at index %d:\n%w", i, err)
		}
	}

	for i, fileSystem := range s.FileSystems {
		err = fileSystem.IsValid()
		if err != nil {
			return fmt.Errorf("invalid filesystems item at index %d:\n%w", i, err)
		}
	}

	hasResetUuids := s.ResetPartitionsUuidsType != ResetPartitionsUuidsTypeDefault
	hasBootType := s.BootType != BootTypeNone
	hasDisks := len(s.Disks) > 0
	hasFileSystems := len(s.FileSystems) > 0
	hasVerity := len(s.Verity) > 0

	if hasResetUuids && hasDisks {
		return fmt.Errorf("cannot specify both 'resetPartitionsUuidsType' and 'disks'")
	}

	if !hasBootType && hasDisks {
		return fmt.Errorf("must specify 'bootType' if 'disks' are specified")
	}

	if hasBootType && !hasDisks {
		return fmt.Errorf("cannot specify 'bootType' without specifying 'disks'")
	}

	if hasFileSystems && !hasDisks {
		return fmt.Errorf("cannot specify 'filesystems' without specifying 'disks'")
	}

	if hasVerity && !hasDisks {
		return fmt.Errorf("cannot specify 'verity' without specifying 'disks'")
	}

	// Create a set of all block devices by their Id.
	deviceMap, partitionLabelCounts, err := s.buildDeviceMap()
	if err != nil {
		return err
	}

	// Check that all child block devices exist and are not used by multiple things.
	deviceParents, err := s.checkDeviceTree(deviceMap, partitionLabelCounts)
	if err != nil {
		return err
	}

	espPartitionExists := false
	biosBootPartitionExists := false

	for _, disk := range s.Disks {
		for _, partition := range disk.Partitions {
			fileSystem, hasFileSystem := deviceParents[partition.Id].(*FileSystem)

			// Ensure special partitions have the correct filesystem type.
			switch partition.Type {
			case PartitionTypeESP:
				espPartitionExists = true

				if !hasFileSystem || (fileSystem.Type != FileSystemTypeFat32 && fileSystem.Type != FileSystemTypeVfat) {
					return fmt.Errorf("ESP partition (%s) must have 'fat32' or 'vfat' filesystem type", partition.Id)
				}

			case PartitionTypeBiosGrub:
				biosBootPartitionExists = true

				if hasFileSystem {
					if fileSystem.Type != "" {
						return fmt.Errorf("BIOS boot partition (%s) must not have a filesystem 'type'",
							partition.Id)
					}

					if fileSystem.MountPoint != nil {
						return fmt.Errorf("BIOS boot partition (%s) must not have a 'mountPoint'", partition.Id)
					}
				}
			}
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

	// Validate verity filesystem settings.
	for i := range s.Verity {
		verity := &s.Verity[i]

		filesystem, hasFileSystem := deviceParents[verity.Id].(*FileSystem)
		if hasFileSystem {
			verity.FileSystem = filesystem
		}

		if !hasFileSystem || filesystem.MountPoint == nil || filesystem.MountPoint.Path != "/" {
			return fmt.Errorf("defining non-root verity devices is not currently supported:\n"+
				"filesystems[].mountPoint.path' of verity device (%s) must be set to '/'",
				verity.Id)
		}

		if verity.Name != VerityRootDeviceName {
			return fmt.Errorf("verity 'name' (%s) must be \"%s\" for filesystem (%s) partition (%s)", verity.Name,
				VerityRootDeviceName, filesystem.MountPoint.Path, verity.DataDeviceId)
		}
	}

	return nil
}

func (s *Storage) CustomizePartitions() bool {
	return len(s.Disks) > 0
}

func (s *Storage) buildDeviceMap() (map[string]any, map[string]int, error) {
	deviceMap := make(map[string]any)
	partitionLabelCounts := make(map[string]int)

	for i, disk := range s.Disks {
		for j := range disk.Partitions {
			partition := &disk.Partitions[j]

			if _, existingName := deviceMap[partition.Id]; existingName {
				return nil, nil, fmt.Errorf("invalid disk at index %d:\ninvalid partition at index %d:\nduplicate id (%s)",
					i, j, partition.Id)
			}

			deviceMap[partition.Id] = partition

			// Count the number of partitions that use each label.
			partitionLabelCounts[partition.Label] += 1
		}
	}

	for i := range s.Verity {
		verity := &s.Verity[i]

		if _, existingName := deviceMap[verity.Id]; existingName {
			return nil, nil, fmt.Errorf("invalid verity item at index %d:\nduplicate id (%s)", i, verity.Id)
		}

		deviceMap[verity.Id] = verity
	}

	return deviceMap, partitionLabelCounts, nil
}

func (s *Storage) checkDeviceTree(deviceMap map[string]any, partitionLabelCounts map[string]int,
) (map[string]any, error) {
	deviceParents := make(map[string]any)

	for i := range s.Verity {
		verity := &s.Verity[i]

		err := checkDeviceTreeVerityItem(verity, deviceMap, deviceParents)
		if err != nil {
			return nil, fmt.Errorf("invalid verity item at index %d:\n%w", i, err)
		}
	}

	mountPaths := make(map[string]bool)
	for i := range s.FileSystems {
		filesystem := &s.FileSystems[i]

		err := checkDeviceTreeFileSystemItem(filesystem, deviceMap, deviceParents, partitionLabelCounts, mountPaths)
		if err != nil {
			return nil, fmt.Errorf("invalid filesystem item at index %d:\n%w", i, err)
		}
	}

	return deviceParents, nil
}

func checkDeviceTreeVerityItem(verity *Verity, deviceMap map[string]any, deviceParents map[string]any) error {
	err := addVerityParentToDevice(verity.DataDeviceId, deviceMap, deviceParents, verity)
	if err != nil {
		return fmt.Errorf("invalid 'dataDeviceId':\n%w", err)
	}

	err = addVerityParentToDevice(verity.HashDeviceId, deviceMap, deviceParents, verity)
	if err != nil {
		return fmt.Errorf("invalid 'hashDeviceId':\n%w", err)
	}

	return nil
}

func addVerityParentToDevice(deviceId string, deviceMap map[string]any, deviceParents map[string]any, parent *Verity,
) error {
	device, err := addParentToDevice(deviceId, deviceMap, deviceParents, parent)
	if err != nil {
		return err
	}

	switch device.(type) {
	case *Partition:

	default:
		return fmt.Errorf("device (%s) must be a partition", deviceId)
	}

	return nil
}

func checkDeviceTreeFileSystemItem(filesystem *FileSystem, deviceMap map[string]any, deviceParents map[string]any,
	partitionLabelCounts map[string]int, mountPaths map[string]bool,
) error {
	device, err := addParentToDevice(filesystem.DeviceId, deviceMap, deviceParents, filesystem)
	if err != nil {
		return fmt.Errorf("invalid 'deviceId':\n%w", err)
	}

	if filesystem.MountPoint != nil {
		if _, existingMountPath := mountPaths[filesystem.MountPoint.Path]; existingMountPath {
			return fmt.Errorf("duplicate 'mountPoint.path' (%s)", filesystem.MountPoint.Path)
		}

		mountPaths[filesystem.MountPoint.Path] = true
	}

	switch device := device.(type) {
	case *Partition:
		filesystem.PartitionId = filesystem.DeviceId

		if filesystem.MountPoint != nil && filesystem.MountPoint.IdType == MountIdentifierTypePartLabel {
			if device.Label == "" {
				return fmt.Errorf("idType is set to (part-label) but partition (%s) has no label set", device.Id)
			}

			labelCount := partitionLabelCounts[device.Label]
			if labelCount > 1 {
				return fmt.Errorf("more than one partition has a label of (%s)", device.Label)
			}
		}

	case *Verity:
		filesystem.PartitionId = device.DataDeviceId

		if filesystem.MountPoint != nil && filesystem.MountPoint.IdType != MountIdentifierTypeDefault {
			return fmt.Errorf("filesystem for verity device (%s) may not specify 'mountPoint.idType'",
				filesystem.DeviceId)
		}

	default:

	}

	return nil
}

func addParentToDevice(deviceId string, deviceMap map[string]any, deviceParents map[string]any, parent any,
) (any, error) {
	device, deviceExists := deviceMap[deviceId]
	if !deviceExists {
		return nil, fmt.Errorf("device (%s) not found", deviceId)
	}

	if _, deviceInUse := deviceParents[deviceId]; deviceInUse {
		return nil, fmt.Errorf("device (%s) is used by multiple things", deviceId)
	}

	deviceParents[deviceId] = parent
	return device, nil
}
