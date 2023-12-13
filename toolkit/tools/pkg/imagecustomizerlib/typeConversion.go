// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/configuration"
)

func bootTypeToImager(bootType imagecustomizerapi.BootType) (string, error) {
	switch bootType {
	case imagecustomizerapi.BootTypeEfi:
		return "efi", nil

	case imagecustomizerapi.BootTypeLegacy:
		return "legacy", nil

	default:
		return "", fmt.Errorf("invalid BootType value (%s)", bootType)
	}
}

func diskConfigToImager(diskConfig imagecustomizerapi.Disk) (configuration.Disk, error) {
	imagerPartitionTableType, err := partitionTableTypeToImager(diskConfig.PartitionTableType)
	if err != nil {
		return configuration.Disk{}, err
	}

	imagerPartitions, err := partitionsToImager(diskConfig.Partitions)
	if err != nil {
		return configuration.Disk{}, err
	}

	imagerDisk := configuration.Disk{
		PartitionTableType: imagerPartitionTableType,
		MaxSize:            diskConfig.MaxSize,
		Partitions:         imagerPartitions,
	}
	return imagerDisk, err
}

func partitionTableTypeToImager(partitionTableType imagecustomizerapi.PartitionTableType,
) (configuration.PartitionTableType, error) {
	switch partitionTableType {
	case imagecustomizerapi.PartitionTableTypeGpt:
		return configuration.PartitionTableTypeGpt, nil

	default:
		return "", fmt.Errorf("unknown partition table type (%s)", partitionTableType)
	}
}

func partitionsToImager(partitions []imagecustomizerapi.Partition) ([]configuration.Partition, error) {
	imagerPartitions := []configuration.Partition(nil)
	for _, partition := range partitions {
		imagerPartition, err := partitionToImager(partition)
		if err != nil {
			return nil, err
		}

		imagerPartitions = append(imagerPartitions, imagerPartition)
	}

	return imagerPartitions, nil
}

func partitionToImager(partition imagecustomizerapi.Partition) (configuration.Partition, error) {
	imagerEnd, _ := partition.GetEnd()

	imagerFlags, err := partitionFlagsToImager(partition.Flags)
	if err != nil {
		return configuration.Partition{}, err
	}

	imagerPartition := configuration.Partition{
		ID:     partition.ID,
		FsType: string(partition.FsType),
		Name:   partition.Name,
		Start:  partition.Start,
		End:    imagerEnd,
		Flags:  imagerFlags,
	}
	return imagerPartition, nil
}

func partitionFlagsToImager(flags []imagecustomizerapi.PartitionFlag) ([]configuration.PartitionFlag, error) {
	imagerFlags := []configuration.PartitionFlag(nil)
	for _, flag := range flags {
		imagerFlag, err := partitionFlagToImager(flag)
		if err != nil {
			return nil, err
		}

		imagerFlags = append(imagerFlags, imagerFlag)
	}

	return imagerFlags, nil
}

func partitionFlagToImager(flag imagecustomizerapi.PartitionFlag) (configuration.PartitionFlag, error) {
	switch flag {
	case imagecustomizerapi.PartitionFlagESP:
		return configuration.PartitionFlagESP, nil

	case imagecustomizerapi.PartitionFlagBiosGrub:
		return configuration.PartitionFlagBiosGrub, nil

	case imagecustomizerapi.PartitionFlagBoot:
		return configuration.PartitionFlagBoot, nil

	default:
		return "", fmt.Errorf("unknown partition flag (%s)", flag)
	}
}

func partitionSettingsToImager(partitionSettings []imagecustomizerapi.PartitionSetting,
) ([]configuration.PartitionSetting, error) {
	imagerPartitionSettings := []configuration.PartitionSetting(nil)
	for _, partitionSetting := range partitionSettings {
		imagerPartitionSetting, err := partitionSettingToImager(partitionSetting)
		if err != nil {
			return nil, err
		}
		imagerPartitionSettings = append(imagerPartitionSettings, imagerPartitionSetting)
	}
	return imagerPartitionSettings, nil
}

func partitionSettingToImager(partitionSettings imagecustomizerapi.PartitionSetting,
) (configuration.PartitionSetting, error) {
	imagerMountIdentifierType, err := mountIdentifierTypeToImager(partitionSettings.MountIdentifier)
	if err != nil {
		return configuration.PartitionSetting{}, err
	}

	imagerPartitionSetting := configuration.PartitionSetting{
		ID:              partitionSettings.ID,
		MountIdentifier: imagerMountIdentifierType,
		MountOptions:    partitionSettings.MountOptions,
		MountPoint:      partitionSettings.MountPoint,
	}
	return imagerPartitionSetting, nil
}

func mountIdentifierTypeToImager(mountIdentifierType imagecustomizerapi.MountIdentifierType,
) (configuration.MountIdentifier, error) {
	switch mountIdentifierType {
	case imagecustomizerapi.MountIdentifierTypeUuid:
		return configuration.MountIdentifierUuid, nil

	case imagecustomizerapi.MountIdentifierTypePartUuid, imagecustomizerapi.MountIdentifierTypeDefault:
		return configuration.MountIdentifierPartUuid, nil

	case imagecustomizerapi.MountIdentifierTypePartLabel:
		return configuration.MountIdentifierPartLabel, nil

	default:
		return "", fmt.Errorf("unknwon MountIdentifierType value (%s)", mountIdentifierType)
	}
}
