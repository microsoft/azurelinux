package imagecustomizerlib

import (
	"encoding/binary"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"time"

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

	metadata := createSkippableFrameMetadata()
	logger.Log.Infof("Skippable frame metadata has been created: %d", metadata)

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

			err = addSkippableFrame(partitionFilepath, metadata)
			if err != nil {
				return err
			}

			logger.Log.Infof("Skippable frame has been added to parition: %d", metadata)

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

// Add a skippable frame to the specified partition file.
func addSkippableFrame(partitionFilepath string, metadata uint32) (err error) {
	// Read existing data from the partition file.
	existingData, err := os.ReadFile(partitionFilepath)
	if err != nil {
		return fmt.Errorf("failed to read partition file %s:\n%w", partitionFilepath, err)
	}

	// Create a skippable frame.
	skippableFrame := createSkippableFrame(metadata)

	// Combine the skippable frame and existing data.
	newData := append(skippableFrame, existingData...)

	// Write the combined data back to the partition file.
	err = os.WriteFile(partitionFilepath, newData, 0644)
	if err != nil {
		return fmt.Errorf("failed to write skippable frame to partition file %s:\n%w", partitionFilepath, err)
	}

	return nil
}

// Create a skippable frame.
func createSkippableFrame(metadata uint32) (skippableFrame []byte) {
	skippableFrame = make([]byte, 12)
	binary.LittleEndian.PutUint32(skippableFrame, 0x184D2A50)   // Magic_Number
	binary.LittleEndian.PutUint32(skippableFrame[4:], 4)        // Frame_Size
	binary.LittleEndian.PutUint32(skippableFrame[8:], metadata) // User_Data
	return skippableFrame
}

// Create user metadata that will be inserted into the skippable frame
func createSkippableFrameMetadata() (metadata uint32) {
	// Set the metadata to be the current timestamp of the run
	currentTime := time.Now()
	metadata = uint32(currentTime.Unix())
	return metadata
}
