// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"
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

func diskConfigToImager(diskConfig imagecustomizerapi.Disk, fileSystems []imagecustomizerapi.FileSystem,
) (configuration.Disk, error) {
	imagerPartitionTableType, err := partitionTableTypeToImager(diskConfig.PartitionTableType)
	if err != nil {
		return configuration.Disk{}, err
	}

	imagerPartitions, err := partitionsToImager(diskConfig.Partitions, fileSystems)
	if err != nil {
		return configuration.Disk{}, err
	}

	imagerMaxSize := diskConfig.MaxSize / diskutils.MiB
	if diskConfig.MaxSize%diskutils.MiB != 0 {
		return configuration.Disk{}, fmt.Errorf("disk max size (%d) must be a multiple of 1 MiB", diskConfig.MaxSize)
	}

	imagerDisk := configuration.Disk{
		PartitionTableType: imagerPartitionTableType,
		MaxSize:            uint64(imagerMaxSize),
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

func partitionsToImager(partitions []imagecustomizerapi.Partition, fileSystems []imagecustomizerapi.FileSystem,
) ([]configuration.Partition, error) {
	imagerPartitions := []configuration.Partition(nil)
	for _, partition := range partitions {
		imagerPartition, err := partitionToImager(partition, fileSystems)
		if err != nil {
			return nil, err
		}

		imagerPartitions = append(imagerPartitions, imagerPartition)
	}

	return imagerPartitions, nil
}

func partitionToImager(partition imagecustomizerapi.Partition, fileSystems []imagecustomizerapi.FileSystem,
) (configuration.Partition, error) {
	fileSystem, foundMountPoint := sliceutils.FindValueFunc(fileSystems,
		func(fileSystem imagecustomizerapi.FileSystem) bool {
			return fileSystem.DeviceId == partition.Id
		},
	)
	if !foundMountPoint {
		return configuration.Partition{}, fmt.Errorf("failed to find filesystem entry with ID (%s)", partition.Id)
	}

	imagerStart := partition.Start / diskutils.MiB
	if partition.Start%diskutils.MiB != 0 {
		return configuration.Partition{}, fmt.Errorf("partition start (%d) must be a multiple of 1 MiB", partition.Start)
	}

	end, _ := partition.GetEnd()
	imagerEnd := end / diskutils.MiB
	if end%diskutils.MiB != 0 {
		return configuration.Partition{}, fmt.Errorf("partition end (%d) must be a multiple of 1 MiB", end)
	}

	imagerFlags, err := toImagerPartitionFlags(partition.Type)
	if err != nil {
		return configuration.Partition{}, err
	}

	imagerPartition := configuration.Partition{
		ID:     partition.Id,
		FsType: string(fileSystem.Type),
		Name:   partition.Label,
		Start:  uint64(imagerStart),
		End:    uint64(imagerEnd),
		Flags:  imagerFlags,
	}
	return imagerPartition, nil
}

func toImagerPartitionFlags(partitionType imagecustomizerapi.PartitionType) ([]configuration.PartitionFlag, error) {
	switch partitionType {
	case imagecustomizerapi.PartitionTypeESP:
		return []configuration.PartitionFlag{configuration.PartitionFlagESP, configuration.PartitionFlagBoot}, nil

	case imagecustomizerapi.PartitionTypeBiosGrub:
		return []configuration.PartitionFlag{configuration.PartitionFlagBiosGrub}, nil

	case imagecustomizerapi.PartitionTypeDefault:
		return nil, nil

	default:
		return nil, fmt.Errorf("unknown partition type (%s)", partitionType)
	}
}

func partitionSettingsToImager(fileSystems []imagecustomizerapi.FileSystem,
) ([]configuration.PartitionSetting, error) {
	imagerPartitionSettings := []configuration.PartitionSetting(nil)
	for _, fileSystem := range fileSystems {
		imagerPartitionSetting, err := partitionSettingToImager(fileSystem)
		if err != nil {
			return nil, err
		}
		imagerPartitionSettings = append(imagerPartitionSettings, imagerPartitionSetting)
	}
	return imagerPartitionSettings, nil
}

func partitionSettingToImager(fileSystem imagecustomizerapi.FileSystem,
) (configuration.PartitionSetting, error) {
	mountIdType := imagecustomizerapi.MountIdentifierTypeDefault
	mountOptions := ""
	mountPath := ""
	if fileSystem.MountPoint != nil {
		mountIdType = fileSystem.MountPoint.IdType
		mountOptions = fileSystem.MountPoint.Options
		mountPath = fileSystem.MountPoint.Path
	}

	imagerMountIdentifierType, err := mountIdentifierTypeToImager(mountIdType)
	if err != nil {
		return configuration.PartitionSetting{}, err
	}

	imagerPartitionSetting := configuration.PartitionSetting{
		ID:              fileSystem.DeviceId,
		MountIdentifier: imagerMountIdentifierType,
		MountOptions:    mountOptions,
		MountPoint:      mountPath,
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
		return "", fmt.Errorf("unknown MountIdentifierType value (%s)", mountIdentifierType)
	}
}

func kernelCommandLineToImager(kernelCommandLine imagecustomizerapi.KernelCommandLine,
	selinuxConfig imagecustomizerapi.SELinux,
	currentSELinuxMode imagecustomizerapi.SELinuxMode,
) (configuration.KernelCommandLine, error) {
	imagerSELinuxMode, err := selinuxModeMaybeDefaultToImager(selinuxConfig.Mode, currentSELinuxMode)
	if err != nil {
		return configuration.KernelCommandLine{}, err
	}

	imagerKernelCommandLine := configuration.KernelCommandLine{
		ExtraCommandLine: string(kernelCommandLine.ExtraCommandLine),
		SELinux:          imagerSELinuxMode,
		SELinuxPolicy:    "",
	}
	return imagerKernelCommandLine, nil
}

func selinuxModeMaybeDefaultToImager(selinuxMode imagecustomizerapi.SELinuxMode,
	currentSELinuxMode imagecustomizerapi.SELinuxMode,
) (configuration.SELinux, error) {
	if selinuxMode == imagecustomizerapi.SELinuxModeDefault {
		selinuxMode = currentSELinuxMode
	}

	return selinuxModeToImager(selinuxMode)
}

func selinuxModeToImager(selinuxMode imagecustomizerapi.SELinuxMode) (configuration.SELinux, error) {
	switch selinuxMode {
	case imagecustomizerapi.SELinuxModeDisabled:
		return configuration.SELinuxOff, nil

	case imagecustomizerapi.SELinuxModeEnforcing:
		return configuration.SELinuxEnforcing, nil

	case imagecustomizerapi.SELinuxModePermissive:
		return configuration.SELinuxPermissive, nil

	case imagecustomizerapi.SELinuxModeForceEnforcing:
		return configuration.SELinuxForceEnforcing, nil

	default:
		return "", fmt.Errorf("unknown SELinuxMode value (%s)", selinuxMode)
	}
}
