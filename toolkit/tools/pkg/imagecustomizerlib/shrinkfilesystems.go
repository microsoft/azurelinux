package imagecustomizerlib

import (
	"fmt"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/diskutils"
	// "github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	// "github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	// "os"
	"os/exec"
	// "path/filepath"
	// "strconv"
	// "strings"
	// "github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
)

func shrinkFilesystems(imageConnection *ImageConnection, outputImageFile string) error {
	imageLoopDevice := imageConnection.Loopback().DevicePath()

	// Get partition info.
	diskPartitions, err := diskutils.GetDiskPartitions(imageLoopDevice)
	if err != nil {
		return err
	}

	for partitionNum := 0; partitionNum < len(diskPartitions); partitionNum++ {
		if diskPartitions[partitionNum].Type == "part" {
			fstype := diskPartitions[partitionNum].FileSystemType
			err = resizeFilesystem(fstype)
			if err != nil {
				return err
			}
		}	
	}
	
}

// Resize filesystem that has fstype ext2/ext3/ext4
func resizeFilesystem(fstype string) (err error) {
	if fstype != "ext2" && fstype != "ext3" && fstype != "ext4" {
		return nil
	}
	// Check the file system with e2fsck
	cmd := exec.Command("sudo", "e2fsck", "-fy", partitionRawFilepath)
	_, err = cmd.Output()
	if err != nil {
		return fmt.Errorf("failed to check %s with e2fsck:\n%w", partitionRawFilepath, err)
	}

	// Resize the file system with resize2fs
	cmd = exec.Command("sudo", "resize2fs", "-M", partitionRawFilepath)
	_, err = cmd.Output()
	if err != nil {
		return fmt.Errorf("failed to resize %s with resize2fs:\n%w", partitionRawFilepath, err)
	}

	return nil
}
