package imagecustomizerlib

import (
	"fmt"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
)

// Extract all partitions of connected image into separate files with specified format.
func extractPartitions(imageLoopDevice string, outputImageFile string, partitionFormat string) error {

	// Extract basename from outputImageFile. E.g. if outputImageFile is "image.qcow2", then basename is "image".
	basename := strings.TrimSuffix(filepath.Base(outputImageFile), filepath.Ext(outputImageFile))

	// Get output directory path.
	outDir := filepath.Dir(outputImageFile)

	// Get partition info.
	diskPartitions, err := diskutils.GetDiskPartitions(imageLoopDevice)
	if err != nil {
		return err
	}

	for partitionNum := 0; partitionNum < len(diskPartitions); partitionNum++ {
		if diskPartitions[partitionNum].Type == "part" {
			rawFilename := basename + "_" + strconv.Itoa(partitionNum) + ".raw"
			partitionLoopDevice := diskPartitions[partitionNum].Path

			partitionFilepath, err := copyBlockDeviceToFile(outDir, partitionLoopDevice, rawFilename)
			if err != nil {
				return err
			}

			switch partitionFormat {
			case "raw":
				// Do nothing for "raw" case.
			case "raw-zstd":
				fstype := diskPartitions[partitionNum].FileSystemType
				err = resizePartition(partitionFilepath, fstype)
				if err != nil {
					return err
				}
				partitionFilepath, err = compressWithZstd(partitionFilepath)
				if err != nil {
					return err
				}
			default:
				return fmt.Errorf("unsupported partition format (supported: raw, raw-zstd): %s", partitionFormat)
			}

			logger.Log.Infof("Partition file created: %s", partitionFilepath)
		}
	}
	return nil
}

// Creates .raw file for the mentioned partition path.
func copyBlockDeviceToFile(outDir, devicePath, name string) (filename string, err error) {
	const (
		defaultBlockSize = 1024 * 1024 // 1MB
		squashErrors     = true
	)

	fullPath := filepath.Join(outDir, name)
	ddArgs := []string{
		fmt.Sprintf("if=%s", devicePath),       // Input file.
		fmt.Sprintf("of=%s", fullPath),         // Output file.
		fmt.Sprintf("bs=%d", defaultBlockSize), // Size of one copied block.
	}

	err = shell.ExecuteLive(squashErrors, "dd", ddArgs...)
	if err != nil {
		return "", fmt.Errorf("failed to copy block device into file:\n%w", err)
	}

	return fullPath, nil
}

// Compress file from raw to raw-zstd format using zstd.
func compressWithZstd(partitionRawFilepath string) (partitionFilepath string, err error) {
	// Using -f to overwrite a file with same name if it exists.
	cmd := exec.Command("zstd", "-f", "-9", "-T0", partitionRawFilepath)
	_, err = cmd.Output()
	if err != nil {
		return "", fmt.Errorf("failed to compress %s with zstd:\n%w", partitionRawFilepath, err)
	}

	// Remove raw file since output partition format is raw-zstd.
	err = os.Remove(partitionRawFilepath)
	if err != nil {
		return "", fmt.Errorf("failed to remove raw file %s:\n%w", partitionRawFilepath, err)
	}

	return partitionRawFilepath + ".zst", nil
}

// Resize partition that has fstype ext2/ext3/ext4
func resizePartition(partitionRawFilepath string, fstype string) (err error) {
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
