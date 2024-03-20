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
	// Get partition info
	diskPartitions, err := diskutils.GetDiskPartitions(diskDevice)
	if err != nil {
		return err
	}

	for _, diskPartition := range diskPartitions {
		if diskPartition.Type != "part" {
			continue
		}

		// Check the file system.
		// Note: If file systems errors are found and corrected, `fsck -a` will return an exit code of 1, which is
		// currently still treated as a failure.
		err := shell.ExecuteLive(true /*squashErrors*/, "fsck", "-a", diskPartition.Path)
		if err != nil {
			return fmt.Errorf("failed to check (%s) with fsck:\n%w", diskPartition.Path, err)
		}
	}

	return nil
}
