package imagecustomizerlib

import (
	"fmt"
	"os"
	"path/filepath"
	"strconv"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

// Extract all partitions of connected image into separate files with specified format.
func extractPartitions(imageLoopDevice string, outDir string, basename string, partitionFormat string) error {

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
			case "raw-zst":
				partitionFilepath, err = compressWithZstd(partitionFilepath)
				if err != nil {
					return err
				}
			default:
				return fmt.Errorf("unsupported partition format (supported: raw, raw-zst): %s", partitionFormat)
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
		"conv=sparse",
	}

	err = shell.ExecuteLive(squashErrors, "dd", ddArgs...)
	if err != nil {
		return "", fmt.Errorf("failed to copy block device into file:\n%w", err)
	}

	return fullPath, nil
}

// Compress file from .raw to .raw.zst format using zstd.
func compressWithZstd(partitionRawFilepath string) (partitionFilepath string, err error) {
	// Using -f to overwrite a file with same name if it exists.
	err = shell.ExecuteLive(true, "zstd", "-f", "-9", "-T0", partitionRawFilepath)
	if err != nil {
		return "", fmt.Errorf("failed to compress %s with zstd:\n%w", partitionRawFilepath, err)
	}

	// Remove raw file since output partition format is raw-zst.
	err = os.Remove(partitionRawFilepath)
	if err != nil {
		return "", fmt.Errorf("failed to remove raw file %s:\n%w", partitionRawFilepath, err)
	}

	return partitionRawFilepath + ".zst", nil
}
