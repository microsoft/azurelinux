package imagecustomizerlib

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"os"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/stretchr/testify/assert"
)

func TestAddSkippableFrame(t *testing.T) {
	// Create a skippable frame containing the metadata and prepend the frame to the partition file
	skippableFrameMetadata, err := createSkippableFrameMetadata()
	assert.NoError(t, err)

	// Create test raw partition file
	partitionfileName := "test"
	partitionRawFilepath, err := createTestRawPartitionFile(partitionfileName)
	assert.NoError(t, err)

	// Compress to .raw.zst partition file
	tempPartitionFilepath, err := compressWithZstd(partitionRawFilepath)
	assert.NoError(t, err)

	// Test adding the skippable frame
	partitionFilepath, err := addSkippableFrame(tempPartitionFilepath, skippableFrameMetadata, partitionfileName, testDir)
	assert.NoError(t, err)

	// Verify decompression with skippable frame
	err = verifySkippableFrameDecompression(partitionRawFilepath, partitionFilepath)
	assert.NoError(t, err)

	// Verify skippable frame metadata
	err = verifySkippableFrameMetadataFromFile(partitionFilepath, SkippableFrameMagicNumber, SkippableFramePayloadSize, skippableFrameMetadata)
	assert.NoError(t, err)

	// Remove test partition files
	err = os.Remove(partitionRawFilepath)
	assert.NoError(t, err)
	err = os.Remove(tempPartitionFilepath)
	assert.NoError(t, err)
	err = os.Remove(partitionFilepath)
	assert.NoError(t, err)
}

func createTestRawPartitionFile(filename string) (string, error) {
	// Test data
	testData := []byte{0x01, 0x02, 0x03, 0x04, 0x05}

	// Output file name
	outputFilename := filename + ".raw"

	// Write data to file
	err := os.WriteFile(outputFilename, testData, PartitionFilePermissions)
	if err != nil {
		return "", fmt.Errorf("failed to write test data to partition file %s:\n%w", filename, err)
	}
	logger.Log.Infof("Test raw partition file created: %s", outputFilename)
	return outputFilename, nil
}

// Decompress the .raw.zst partition file and verify the hash matches with the source .raw file
func verifySkippableFrameDecompression(rawPartitionFilepath string, rawZstPartitionFilepath string) (err error) {
	// Decompressing .raw.zst file
	decompressedPartitionFilepath := "decompressed.raw"
	err = shell.ExecuteLive(true, "zstd", "-d", rawZstPartitionFilepath, "-o", decompressedPartitionFilepath)
	if err != nil {
		return fmt.Errorf("failed to decompress %s with zstd:\n%w", rawZstPartitionFilepath, err)
	}

	// Calculating hashes
	rawPartitionFileHash, err := file.GenerateSHA256(rawPartitionFilepath)
	if err != nil {
		return fmt.Errorf("error generating SHA256:\n%w", err)
	}
	decompressedPartitionFileHash, err := file.GenerateSHA256(decompressedPartitionFilepath)
	if err != nil {
		return fmt.Errorf("error generating SHA256:\n%w", err)
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
func verifySkippableFrameMetadataFromFile(partitionFilepath string, magicNumber uint32, frameSize uint32, skippableFrameMetadata [SkippableFramePayloadSize]byte) (err error) {
	// Read existing data from the partition file
	existingData, err := os.ReadFile(partitionFilepath)
	if err != nil {
		return fmt.Errorf("failed to read partition file %s:\n%w", partitionFilepath, err)
	}

	// Verify that the skippable frame has been prepended to the partition file by validating magicNumber
	if binary.LittleEndian.Uint32(existingData[0:4]) != magicNumber {
		return fmt.Errorf("skippable frame has not been prepended to the partition file:\n %d != %d", binary.LittleEndian.Uint32(existingData[0:4]), magicNumber)
	}
	logger.Log.Infof("Skippable frame had been correctly prepended to the partition file.")

	// Verify that the skippable frame has the correct frame size by validating frameSize
	if binary.LittleEndian.Uint32(existingData[4:8]) != frameSize {
		return fmt.Errorf("skippable frame frameSize field does not match the defined frameSize:\n %d != %d", binary.LittleEndian.Uint32(existingData[4:8]), frameSize)
	}
	logger.Log.Infof("Skippable frame frameSize field is correct.")

	// Verify that the skippable frame has the correct inserted metadata by validating skippableFrameMetadata
	if !bytes.Equal(existingData[8:8+frameSize], skippableFrameMetadata[:]) {
		return fmt.Errorf("skippable frame metadata does not match the inserted metadata:\n %d != %d", existingData[8:8+frameSize], skippableFrameMetadata[:])
	}
	logger.Log.Infof("Skippable frame is valid and contains the correct metadata!")

	return nil
}
