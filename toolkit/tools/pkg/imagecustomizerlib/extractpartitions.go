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

// Extract all partitions of connected image into separate files with specified format.
func extractPartitions(imageLoopDevice string, outDir string, basename string, partitionFormat string) error {

	// Get partition info.
	diskPartitions, err := diskutils.GetDiskPartitions(imageLoopDevice)
	if err != nil {
		return err
	}

	// Create skippable frame metadata defined as a random 128-Bit number
	metadata, err := createSkippableFrameMetadata()
	if err != nil {
		return err
	}

	// Encode metadata into a payload defined as a uint32 array
	payload := Encode128BitLittleEndian(metadata)
	logger.Log.Infof("Skippable frame payload has been created: %d", payload)

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

			// Create a skippable frame containing the metadata payload and prepend the frame to the partition file
			err = addSkippableFrame(partitionFilepath, payload)
			if err != nil {
				return err
			}

			logger.Log.Infof("Skippable frame payload has been added to parition: %d", payload)

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
func addSkippableFrame(partitionFilepath string, payload [4]uint32) (err error) {
	// Read existing data from the partition file.
	existingData, err := os.ReadFile(partitionFilepath)
	if err != nil {
		return fmt.Errorf("failed to read partition file %s:\n%w", partitionFilepath, err)
	}

	// Create a skippable frame.
	skippableFrame := createSkippableFrame(payload)

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
func createSkippableFrame(payload [4]uint32) (skippableFrame []byte) {
	skippableFrame = make([]byte, 24)
	// Magic_Number
	binary.LittleEndian.PutUint32(skippableFrame, 0x184D2A50)
	// Frame_Size
	binary.LittleEndian.PutUint32(skippableFrame[4:8], 16)
	// User_Data
	binary.LittleEndian.PutUint32(skippableFrame[8:12], payload[0])
	binary.LittleEndian.PutUint32(skippableFrame[12:16], payload[1])
	binary.LittleEndian.PutUint32(skippableFrame[16:20], payload[2])
	binary.LittleEndian.PutUint32(skippableFrame[20:24], payload[3])
	return skippableFrame
}

// Create user metadata that will be inserted into the skippable frame.
func createSkippableFrameMetadata() (metadata [16]byte, err error) {
	// Set the metadata to be a random 128-Bit number
	metadata, err = generateRandom128BitNumber()
	if err != nil {
		return metadata, err
	}
	return metadata, nil
}

// Generates a Random 128-Bit number.
func generateRandom128BitNumber() ([16]byte, error) {
	var randomBytes [16]byte
	_, err := rand.Read(randomBytes[:])
	if err != nil {
		return randomBytes, err
	}
	return randomBytes, nil
}

// Encodes a 128-Bit number into an array of uint32 in little-endian order.
func Encode128BitLittleEndian(number [16]byte) [4]uint32 {
	var encoded [4]uint32
	for i := 0; i < 4; i++ {
		offset := i * 4
		encoded[i] = binary.LittleEndian.Uint32(number[offset : offset+4])
	}
	return encoded
}

// Decodes an array of uint32 into a 128-Bit number in little-endian order.
func Decode128BitLittleEndian(encoded [4]uint32) [16]byte {
	var number [16]byte
	for i := 0; i < 4; i++ {
		offset := i * 4
		binary.LittleEndian.PutUint32(number[offset:offset+4], encoded[i])
	}
	return number
}
