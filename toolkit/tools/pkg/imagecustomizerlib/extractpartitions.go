package imagecustomizerlib

import (
	"bytes"
	"crypto/rand"
	"encoding/binary"
	"fmt"
	"os"
	"path/filepath"
	"strconv"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
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
				partitionRawFilepath := partitionFilepath
				partitionFilepath, err := compressWithZstd(partitionRawFilepath)
				if err != nil {
					return err
				}
				// Create a skippable frame containing the metadata and prepend the frame to the partition file
				err = addSkippableFrame(partitionFilepath, SkippableFrameMagicNumber, SkippableFrameSize, skippableFrameMetadata)
				if err != nil {
					return err
				}
				// Verify decompression with skippable frame
				err = verifySkippableFrameDecompression(partitionRawFilepath, partitionFilepath)
				if err != nil {
					return err
				}
				// Remove raw file since output partition format is raw-zst.
				err = os.Remove(partitionRawFilepath)
				if err != nil {
					return fmt.Errorf("failed to remove raw file %s:\n%w", partitionRawFilepath, err)
				}
				// Verify skippable frame metadata
				err = verifySkippableFrameMetadataFromFile(partitionFilepath, SkippableFrameMagicNumber, SkippableFrameSize, skippableFrameMetadata)
				if err != nil {
					return err
				}
				logger.Log.Infof("Partition file created: %s", partitionFilepath)
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

// Decompress the .raw.zst partition file and verifies the hash matches with the source .raw file
func verifySkippableFrameDecompression(rawPartitionFilepath string, rawZstPartitionFilepath string) (err error) {
	// Decompressing .raw.zst file
	decompressedPartitionFilepath := "build/decompressed.raw"
	err = shell.ExecuteLive(true, "zstd", "-d", rawZstPartitionFilepath, "-o", decompressedPartitionFilepath)
	if err != nil {
		return fmt.Errorf("failed to decompress %s with zstd:\n%w", rawZstPartitionFilepath, err)
	}

	// Calculating hashes
	rawPartitionFileHash, err := file.GenerateSHA256(rawPartitionFilepath)
	if err != nil {
		return fmt.Errorf("error: %w", err)
	}
	decompressedPartitionFileHash, err := file.GenerateSHA256(decompressedPartitionFilepath)
	if err != nil {
		return fmt.Errorf("error: %w", err)
	}

	// Verifying hashes are equal
	if rawPartitionFileHash != decompressedPartitionFileHash {
		return fmt.Errorf("decompressed partition file hash does not match source partition file hash: %s != %s", decompressedPartitionFileHash, rawPartitionFilepath)
	}
	logger.Log.Debugf("Decompressed partition file hash matches source partition file hash!")

	// Removing decompressed file
	err = os.Remove(decompressedPartitionFilepath)
	if err != nil {
		return fmt.Errorf("failed to remove raw file %s:\n%w", decompressedPartitionFilepath, err)
	}

	return nil
}

// Verifies that the skippable frame has been correctly prepended to the partition file with the correct data
func verifySkippableFrameMetadataFromFile(partitionFilepath string, magicNumber uint32, frameSize uint32, skippableFrameMetadata [SkippableFrameSize]byte) (err error) {
	// Read existing data from the partition file.
	existingData, err := os.ReadFile(partitionFilepath)
	if err != nil {
		return fmt.Errorf("failed to read partition file %s:\n%w", partitionFilepath, err)
	}

	// verify that the skippable frame has been prepended to the partition file by validating magicNumber
	var magicNumberByteArray [4]byte
	binary.LittleEndian.PutUint32(magicNumberByteArray[:], magicNumber)
	if !bytes.Equal(existingData[0:4], magicNumberByteArray[:]) {
		return fmt.Errorf("skippable frame has not been prepended to the partition file:\n %d != %d", existingData[0:4], magicNumberByteArray[:])
	}
	logger.Log.Infof("Skippable frame had been correctly prepended to the partition file...")

	// verify that the skippable frame has the correct frame size by validating frameSize
	var frameSizeByteArray [4]byte
	binary.LittleEndian.PutUint32(frameSizeByteArray[:], frameSize)
	if !bytes.Equal(existingData[4:8], frameSizeByteArray[:]) {
		return fmt.Errorf("skippable frame frameSize field does not match the defined frameSize:\n %d != %d", existingData[4:8], frameSizeByteArray[:])
	}
	logger.Log.Infof("Skippable frame frameSize field is correct...")

	// verify that the skippable frame has the correct inserted metadata by validating skippableFrameMetadata
	if !bytes.Equal(existingData[8:8+frameSize], skippableFrameMetadata[:]) {
		return fmt.Errorf("skippable frame metadata does not match the inserted metadata:\n %d != %d", existingData[8:8+frameSize], skippableFrameMetadata[:])
	}
	logger.Log.Infof("Skippable frame is valid and contains the correct metadata!")

	return nil
}
