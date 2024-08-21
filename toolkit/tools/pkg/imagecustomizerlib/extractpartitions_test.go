package imagecustomizerlib

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"os"
	"path/filepath"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safeloopback"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safemount"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/stretchr/testify/assert"
	"golang.org/x/sys/unix"
)

func TestAddSkippableFrame(t *testing.T) {
	// Create a skippable frame containing the metadata and prepend the frame to the partition file
	skippableFrameMetadata, _, err := createUuid()
	assert.NoError(t, err)

	// Create test raw partition file
	partitionFilename := "test"
	partitionRawFilepath, err := createTestRawPartitionFile(partitionFilename)
	assert.NoError(t, err)

	// Compress to .raw.zst partition file
	tempPartitionFilepath := testDir + partitionFilename + "_temp.raw.zst"
	err = compressWithZstd(partitionRawFilepath, tempPartitionFilepath)
	assert.NoError(t, err)

	// Test adding the skippable frame
	partitionFilepath, err := addSkippableFrame(tempPartitionFilepath, skippableFrameMetadata, partitionFilename, testDir)
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
	err := os.WriteFile(outputFilename, testData, os.ModePerm)
	if err != nil {
		return "", fmt.Errorf("failed to write test data to partition file %s:\n%w", filename, err)
	}
	logger.Log.Infof("Test raw partition file created: %s", outputFilename)
	return outputFilename, nil
}

func extractZstFile(zstFilePath string, outputFilePath string) error {
	err := shell.ExecuteLive(true, "zstd", "-d", zstFilePath, "-o", outputFilePath)
	if err != nil {
		return fmt.Errorf("failed to decompress %s with zstd:\n%w", zstFilePath, err)
	}

	return nil
}

// Decompress the .raw.zst partition file and verify the hash matches with the source .raw file
func verifySkippableFrameDecompression(rawPartitionFilepath string, rawZstPartitionFilepath string) (err error) {
	// Decompressing .raw.zst file
	decompressedPartitionFilepath := "decompressed.raw"
	err = extractZstFile(rawZstPartitionFilepath, decompressedPartitionFilepath)
	if err != nil {
		return err
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

// Tests partition extracting with partition resize enabled, but where the partition resize is a no-op.
func TestCustomizeImageNopShrink(t *testing.T) {
	var err error

	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	buildDir := filepath.Join(tmpDir, "TestCustomizeImageNopShrink")
	configFile := filepath.Join(testDir, "consume-space.yaml")
	outImageFilePath := filepath.Join(buildDir, "image.qcow2")

	// Customize image.
	err = CustomizeImageWithConfigFile(buildDir, configFile, baseImage, nil, outImageFilePath, "", "raw-zst",
		false /*useBaseImageRpmRepos*/, true /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	espPartitionZstFilePath := filepath.Join(buildDir, "image_1.raw.zst")
	rootfsPartitionZstFilePath := filepath.Join(buildDir, "image_2.raw.zst")

	espPartitionFilePath := filepath.Join(buildDir, "image_1.raw")
	rootfsPartitionFilePath := filepath.Join(buildDir, "image_2.raw")

	// Check the file type of the output files.
	checkFileType(t, espPartitionZstFilePath, "zst")
	checkFileType(t, rootfsPartitionZstFilePath, "zst")

	// Extract partitions.
	err = extractZstFile(espPartitionZstFilePath, espPartitionFilePath)
	if !assert.NoError(t, err) {
		return
	}

	err = extractZstFile(rootfsPartitionZstFilePath, rootfsPartitionFilePath)
	if !assert.NoError(t, err) {
		return
	}

	// Mount the partitions.
	mountsDir := filepath.Join(buildDir, "testmounts")
	espMountDir := filepath.Join(mountsDir, "esp")
	rootfsMountDir := filepath.Join(mountsDir, "rootfs")

	espLoopback, err := safeloopback.NewLoopback(espPartitionFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer espLoopback.Close()

	rootfsLoopback, err := safeloopback.NewLoopback(rootfsPartitionFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer espLoopback.Close()

	espMount, err := safemount.NewMount(espLoopback.DevicePath(), espMountDir, "vfat", 0, "", true)
	if !assert.NoError(t, err) {
		return
	}
	defer espMount.Close()

	rootfsMount, err := safemount.NewMount(rootfsLoopback.DevicePath(), rootfsMountDir, "ext4", 0, "", true)
	if !assert.NoError(t, err) {
		return
	}
	defer rootfsMount.Close()

	// Get the file sizes.
	var rootfsStat unix.Statfs_t
	err = unix.Statfs(rootfsMountDir, &rootfsStat)
	if !assert.NoError(t, err) {
		return
	}

	bigFileStat, err := os.Stat(filepath.Join(rootfsMountDir, "bigfile"))
	if !assert.NoError(t, err) {
		return
	}

	rootfsZstFileStat, err := os.Stat(rootfsPartitionZstFilePath)
	if !assert.NoError(t, err) {
		return
	}

	// Confirm that there is almost 0 free space left, thus preventing the shrink partition operation from doing
	// anything.
	rootfsFreeSpace := int64(rootfsStat.Bfree) * rootfsStat.Frsize
	assert.LessOrEqual(t, rootfsFreeSpace, int64(32*diskutils.MiB), "check rootfs free space")

	// Ensure that zst succesfully compressed the rootfs partition.
	// In particular, bigfile, which is all 0s, should compress down to basically nothing.
	rootfsSizeLessBigFile := int64(rootfsStat.Blocks)*rootfsStat.Frsize - bigFileStat.Size()
	assert.LessOrEqual(t, rootfsZstFileStat.Size(), rootfsSizeLessBigFile, "check compression size")
}
