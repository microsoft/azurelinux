// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"errors"
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

	errs := []error(nil)
	for _, diskPartition := range diskPartitions {
		if diskPartition.Type != "part" {
			// Skip the disk entry.
			continue
		}

		if diskPartition.FileSystemType == "" {
			// Skip partitions that don't have a known file system type (e.g. the BIOS boot partition).
			logger.Log.Debugf("Skipping file system check (%s)", diskPartition.Path)
			continue
		}

		err = checkFileSystem(diskPartition.FileSystemType, diskPartition.Path)
		if err != nil {
			errs = append(errs, err)
		}
	}

	if len(errs) > 0 {
		return errors.Join(errs...)
	}

	return nil
}

func checkFileSystemFile(fileSystemType string, path string) error {
	loopback, err := safeloopback.NewLoopback(path)
	if err != nil {
		return err
	}
	defer loopback.Close()

	err = checkFileSystem(fileSystemType, loopback.DevicePath())
	if err != nil {
		return err
	}

	err = loopback.CleanClose()
	if err != nil {
		return err
	}

	return nil
}

func checkFileSystem(fileSystemType string, path string) error {
	logger.Log.Debugf("Check file system (%s) at (%s)", fileSystemType, path)

	// Check the file system for corruption.
	switch fileSystemType {
	case "ext2", "ext3", "ext4":
		// Add -f flag to force check to run even if the journal is marked as clean.
		err := shell.ExecuteLive(true /*squashErrors*/, "e2fsck", "-fn", path)
		if err != nil {
			return fmt.Errorf("failed to check (%s) with e2fsck:\n%w", path, err)

		}

	case "xfs":
		// The fsck.xfs tool doesn't do anything. So, call xfs_repair instead.
		err := shell.ExecuteLive(true /*squashErrors*/, "xfs_repair", "-n", path)
		if err != nil {
			return fmt.Errorf("failed to check (%s) with xfs_repair:\n%w", path, err)
		}

	default:
		err := shell.ExecuteLive(true /*squashErrors*/, "fsck", "-n", path)
		if err != nil {
			return fmt.Errorf("failed to check (%s) with fsck:\n%w", path, err)
		}
	}

	return nil
}
