// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"path/filepath"
	"strconv"
	"strings"

	"github.com/google/uuid"
	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safeloopback"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safemount"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

func resetPartitionsUuids(buildImageFile string, buildDir string) error {
	logger.Log.Infof("Resetting partition UUIDs")

	loopback, err := safeloopback.NewLoopback(buildImageFile)
	if err != nil {
		return err
	}
	defer loopback.Close()

	partitions, err := diskutils.GetDiskPartitions(loopback.DevicePath())
	if err != nil {
		return err
	}

	// Update the UUIDs.
	newUuids := make([]string, len(partitions))
	for i, partition := range partitions {
		if partition.Type != "part" {
			continue
		}

		newUuid, err := resetFileSystemUuid(partition)
		if err != nil {
			return fmt.Errorf("failed to reset partition's (%s) filesystem (%s) UUID:\n%w", partition.Path,
				partition.FileSystemType, err)
		}

		newUuids[i] = newUuid
	}

	// Update the PARTUUIDs.
	newPartUuids := make([]string, len(partitions))
	for i, partition := range partitions {
		if partition.Type != "part" {
			continue
		}

		newPartUuid, err := resetPartitionUuid(loopback.DevicePath(), i)
		if err != nil {
			return fmt.Errorf("failed to update partition (%s) UUID:\n%w", partition.Path, err)
		}

		newPartUuids[i] = newPartUuid
	}

	// Fix /etc/fstab file.
	err = fixPartitionUuidsInFstabFile(partitions, newUuids, newPartUuids, buildDir)
	if err != nil {
		return err
	}

	err = loopback.CleanClose()
	if err != nil {
		return err
	}

	return nil
}

func resetFileSystemUuid(partition diskutils.PartitionInfo) (string, error) {
	newUuid := ""
	switch partition.FileSystemType {
	case "ext2", "ext3", "ext4":
		// tune2fs requires you to run 'e2fsck -f' first.
		err := shell.ExecuteLive(true /*squashErrors*/, "e2fsck", "-fy", partition.Path)
		if err != nil {
			return "", fmt.Errorf("failed to check %s with e2fsck:\n%w", partition.Path, err)
		}

		newUuid = uuid.NewString()
		err = shell.ExecuteLive(true /*squashErrors*/, "tune2fs", "-U", newUuid, partition.Path)
		if err != nil {
			return "", err
		}

	case "xfs":
		newUuid = uuid.NewString()
		err := shell.ExecuteLive(true /*squashErrors*/, "xfs_admin", "-U", newUuid, partition.Path)
		if err != nil {
			return "", err
		}

	case "vfat":
		newUuidBytes := make([]byte, 4)
		_, err := rand.Read(newUuidBytes)
		if err != nil {
			return "", fmt.Errorf("failed to generate new random ID for vfat partition:\n%w", err)
		}

		newUuid = hex.EncodeToString(newUuidBytes)
		err = shell.ExecuteLive(true /*squashErrors*/, "fatlabel", "--volume-id", partition.Path, newUuid)
		if err != nil {
			return "", err
		}

		// Change the UUID string format to match what is expected by fstab.
		newUuid = strings.ToUpper(newUuid)
		newUuid = newUuid[:4] + "-" + newUuid[4:]

	default:
		return "", fmt.Errorf("unsupported filesystem type (%s)", partition.FileSystemType)
	}

	return newUuid, nil
}

func resetPartitionUuid(device string, partNum int) (string, error) {
	newUuid := uuid.NewString()
	err := shell.ExecuteLive(true /*squashErrors*/, "sfdisk", "--part-uuid", device, strconv.Itoa(partNum), newUuid)
	if err != nil {
		return "", err
	}

	return newUuid, nil
}

func fixPartitionUuidsInFstabFile(partitions []diskutils.PartitionInfo, newUuids []string, newPartUuids []string,
	buildDir string,
) error {
	rootfsPartition, err := findRootfsPartition(partitions, buildDir)
	if err != nil {
		return err
	}

	// Mount the rootfs partition.
	tmpDir := filepath.Join(buildDir, tmpParitionDirName)
	partitionMount, err := safemount.NewMount(rootfsPartition.Path, tmpDir, rootfsPartition.FileSystemType, 0, "", true)
	if err != nil {
		return err
	}
	defer partitionMount.Close()

	// Read the existing fstab file.
	fsTabFilePath := filepath.Join(partitionMount.Target(), "/etc/fstab")
	fstabEntries, err := diskutils.ReadFstabFile(fsTabFilePath)
	if err != nil {
		return err
	}

	// Fix the fstab entries.
	for i, fstabEntry := range fstabEntries {
		// Ignore special partitions.
		if isSpecialPartition(fstabEntry) {
			continue
		}

		// Find the partition.
		// Note: The 'partitions' list was collected before all the changes were made. So, the fstab entires will still
		// match the values in the `partitions` list.
		mountIdType, _, partitionIndex, err := findSourcePartitionHelper(fstabEntry.Source, partitions)
		if err != nil {
			return err
		}

		// Create a new value for the source.
		newSource := fstabEntry.Source
		switch mountIdType {
		case imagecustomizerapi.MountIdentifierTypeUuid:
			newSource = fmt.Sprintf("UUID=%s", newUuids[partitionIndex])

		case imagecustomizerapi.MountIdentifierTypePartUuid:
			newSource = fmt.Sprintf("PARTUUID=%s", newPartUuids[partitionIndex])
		}

		logger.Log.Debugf("Fix fstab: (%s) to (%s)", fstabEntry.Source, newSource)
		fstabEntries[i].Source = newSource
	}

	// Write the updated fstab entries back to the fstab file.
	err = diskutils.WriteFstabFile(fstabEntries, fsTabFilePath)
	if err != nil {
		return err
	}

	err = partitionMount.CleanClose()
	if err != nil {
		return err
	}

	return nil
}
