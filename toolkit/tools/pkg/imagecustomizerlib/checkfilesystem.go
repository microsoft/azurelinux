// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safeloopback"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

func checkFileSystems(rawImageFile string) error {
	logger.Log.Infof("Checking for file system errors")

	imageLoopback, err := safeloopback.NewLoopback(rawImageFile)
	if err != nil {
		return err
	}
	defer imageLoopback.Close()

	err = checkFileSystemsHelper(imageLoopback.DevicePath())
	if err != nil {
		return err
	}

	err = imageLoopback.CleanClose()
	if err != nil {
		return err
	}

	return nil
}

func checkFileSystemsHelper(diskDevice string) error {
	// Get partitions info
	diskPartitions, err := diskutils.GetDiskPartitions(diskDevice)
	if err != nil {
		return err
	}

	for _, diskPartition := range diskPartitions {
		if diskPartition.Type != "part" {
			continue
		}

		// Check the file system for corruption.
		switch diskPartition.FileSystemType {
		case "ext2", "ext3", "ext4":
			// Add -f flag to force check to run even if the journal is marked as clean.
			err := shell.ExecuteLive(true /*squashErrors*/, "e2fsck", "-fn", diskPartition.Path)
			if err != nil {
				return fmt.Errorf("failed to check (%s) with e2fsck:\n%w", diskPartition.Path, err)
			}

		case "xfs":
			// The fsck.xfs tool doesn't do anything. So, call xfs_repair instead.
			err := shell.ExecuteLive(true /*squashErrors*/, "xfs_repair", "-n", diskPartition.Path)
			if err != nil {
				return fmt.Errorf("failed to check (%s) with xfs_repair:\n%w", diskPartition.Path, err)
			}

		default:
			err := shell.ExecuteLive(true /*squashErrors*/, "fsck", "-n", diskPartition.Path)
			if err != nil {
				return fmt.Errorf("failed to check (%s) with fsck:\n%w", diskPartition.Path, err)
			}
		}
	}

	return nil
}
