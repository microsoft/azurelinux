package imagecustomizerlib

import (
	"crypto/rand"
	"encoding/binary"
	"fmt"
	"os"
	"path/filepath"
	"strconv"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

const (
	SkippableFrameMagicNumber uint32 = 0x184D2A50
	SkippableFrameSize        uint32 = 16
)

// Extract all partitions of connected image into separate files with specified format.
func extractPartitions(imageLoopDevice string, outDir string, basename string, partitionFormat string) error {

	// Get partition info.
	diskPartitions, err := diskutils.GetDiskPartitions(imageLoopDevice)
	if err != nil {
		return err
	}

	// Create skippable frame metadata defined as a random 128-Bit number
	skippableFrameMetadata, err := createSkippableFrameMetadata()
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
				partitionFilepath, err = extractRawZstPartition(partitionFilepath, skippableFrameMetadata)
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

// Extract raw-zstd partition
func extractRawZstPartition(partitionRawFilepath string, skippableFrameMetadata [SkippableFrameSize]byte) (partitionFilepath string, err error) {
	// Compress raw partition with zstd and output it
	partitionFilepath, err = compressWithZstd(partitionRawFilepath)
	if err != nil {
		return "", err
	}
	// Create a skippable frame containing the metadata and prepend the frame to the partition file
	err = addSkippableFrame(partitionFilepath, SkippableFrameMagicNumber, SkippableFrameSize, skippableFrameMetadata)
	if err != nil {
		return "", err
	}
	// Remove raw file since output partition format is raw-zst.
	err = os.Remove(partitionRawFilepath)
	if err != nil {
		return "", fmt.Errorf("failed to remove raw file %s:\n%w", partitionRawFilepath, err)
	}
	return partitionFilepath, nil
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

	return partitionRawFilepath + ".zst", nil
}

// Prepend a skippable frame with the metadata to the specified partition file.
func addSkippableFrame(partitionFilepath string, magicNumber uint32, frameSize uint32, skippableFrameMetadata [SkippableFrameSize]byte) (err error) {
	// Read existing data from the partition file.
	existingData, err := os.ReadFile(partitionFilepath)
	if err != nil {
		return fmt.Errorf("failed to read partition file %s:\n%w", partitionFilepath, err)
	}

	// Create a skippable frame.
	skippableFrame := createSkippableFrame(magicNumber, frameSize, skippableFrameMetadata)

	// Combine the skippable frame and existing data.
	newData := append(skippableFrame, existingData...)

	// Write the combined data back to the partition file.
	err = os.WriteFile(partitionFilepath, newData, 0644)
	if err != nil {
		return fmt.Errorf("failed to write skippable frame to partition file %s:\n%w", partitionFilepath, err)
	}

	return nil
}

// Creates a skippable frame.
func createSkippableFrame(magicNumber uint32, frameSize uint32, skippableFrameMetadata [SkippableFrameSize]byte) (skippableFrame []byte) {
	// Calculate the length of the byte array
	lengthOfByteArray := 4 + 4 + len(skippableFrameMetadata)
	// Define the Skippable frame
	skippableFrame = make([]byte, lengthOfByteArray)
	// Magic_Number
	binary.LittleEndian.PutUint32(skippableFrame, magicNumber)
	// Frame_Size
	binary.LittleEndian.PutUint32(skippableFrame[4:8], frameSize)
	// User_Data
	copy(skippableFrame[8:24], skippableFrameMetadata[:])

	logger.Log.Infof("Skippable frame has been created with the following metadata: %d", skippableFrame[8:24])

	return skippableFrame
}

// Create user metadata that will be inserted into the skippable frame.
func createSkippableFrameMetadata() (skippableFrameMetadata [SkippableFrameSize]byte, err error) {
	// Set the skippableFrameMetadata to be a random 128-Bit number
	skippableFrameMetadata, err = generateRandom128BitNumber()
	if err != nil {
		return skippableFrameMetadata, err
	}
	return skippableFrameMetadata, nil
}

// Generates a Random 128-Bit number.
func generateRandom128BitNumber() ([SkippableFrameSize]byte, error) {
	var randomBytes [SkippableFrameSize]byte
	_, err := rand.Read(randomBytes[:])
	if err != nil {
		return randomBytes, err
	}
	return randomBytes, nil
}
