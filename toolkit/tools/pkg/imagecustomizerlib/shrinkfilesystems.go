package imagecustomizerlib

import (
	"fmt"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

func shrinkFilesystems(imageLoopDevice string, outputImageFile string) error {
	logger.Log.Infof("Shrinking filesystems")
	// Get partition info.
	diskPartitions, err := diskutils.GetDiskPartitions(imageLoopDevice)
	if err != nil {
		return err
	}

	for partitionNum := 0; partitionNum < len(diskPartitions); partitionNum++ {
		if diskPartitions[partitionNum].Type == "part" {
			fstype := diskPartitions[partitionNum].FileSystemType
			if fstype != "ext2" && fstype != "ext3" && fstype != "ext4" {
				continue
			}

			partitionLoopDevice := diskPartitions[partitionNum].Path

			// Check the file system with e2fsck
			err := shell.ExecuteLive(true /*squashErrors*/, "sudo", "e2fsck", "-fy", partitionLoopDevice)

			if err != nil {
				return fmt.Errorf("failed to check %s with e2fsck:\n%w", partitionLoopDevice, err)
			}

			// Resize the file system with resize2fs
			err = shell.ExecuteLive(true, "sudo", "resize2fs", "-M", partitionLoopDevice)
			if err != nil {
				return fmt.Errorf("failed to resize %s with resize2fs:\n%w", partitionLoopDevice, err)
			}
		}
	}
	return nil
}
