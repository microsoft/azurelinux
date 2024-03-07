package imagecustomizerlib

import (
	"bytes"
	"crypto/rand"
	"crypto/sha256"
	"encoding/binary"
	"encoding/hex"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strconv"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

// Define global constants
const (
	MagicNumber uint32 = 0x184D2A50
	FrameSize   uint32 = 16
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

	for partitionNum := 0; partitionNum < len(diskPartitions); partitionNum++ {
		if diskPartitions[partitionNum].Type == "part" {
			rawFilename := basename + "_" + strconv.Itoa(partitionNum) + ".raw"
			partitionLoopDevice := diskPartitions[partitionNum].Path

			partitionFilePath, err := copyBlockDeviceToFile(outDir, partitionLoopDevice, rawFilename)
			if err != nil {
				return err
			}

			switch partitionFormat {
			case "raw":
				// Do nothing for "raw" case.
			case "raw-zst":
				partitionRawFilePath := partitionFilePath
				partitionFilepath, err := compressWithZstd(partitionRawFilePath)
				if err != nil {
					return err
				}
				// Create a skippable frame containing the metadata payload and prepend the frame to the partition file
				err = addSkippableFrame(partitionFilepath, MagicNumber, FrameSize, payload)
				if err != nil {
					return err
				}
				// Verify decompression with skippable frame
				err = verifySkippableFrameDecompression(partitionRawFilePath, partitionFilepath)
				if err != nil {
					return err
				}
				// Remove raw file since output partition format is raw-zst.
				err = os.Remove(partitionRawFilePath)
				if err != nil {
					return fmt.Errorf("failed to remove raw file %s:\n%w", partitionRawFilePath, err)
				}
				// Verify skippable frame metadata
				err = verifySkippableFrameMetadataFromFile(partitionFilepath, MagicNumber, FrameSize, metadata)
				if err != nil {
					return err
				}
				logger.Log.Infof("Partition file created: %s", partitionFilepath)
			default:
				return fmt.Errorf("unsupported partition format (supported: raw, raw-zst): %s", partitionFormat)
			}
			logger.Log.Infof("Partition file created: %s", partitionFilePath)
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

// Prepend a skippable frame with the metadata payload to the specified partition file.
func addSkippableFrame(partitionFilepath string, magicNumber uint32, frameSize uint32, payload [4]uint32) (err error) {
	// Read existing data from the partition file.
	existingData, err := os.ReadFile(partitionFilepath)
	if err != nil {
		return fmt.Errorf("failed to read partition file %s:\n%w", partitionFilepath, err)
	}

	// Create a skippable frame.
	skippableFrame := createSkippableFrame(magicNumber, frameSize, payload)

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
func createSkippableFrame(magicNumber uint32, frameSize uint32, payload [4]uint32) (skippableFrame []byte) {
	// Calculate the length of the byte array
	lengthOfByteArray := 4 + 4 + (4 * len(payload))
	// Define the Skippable frame
	skippableFrame = make([]byte, lengthOfByteArray)
	// Magic_Number
	binary.LittleEndian.PutUint32(skippableFrame, magicNumber)
	// Frame_Size
	binary.LittleEndian.PutUint32(skippableFrame[4:8], frameSize)
	// User_Data
	binary.LittleEndian.PutUint32(skippableFrame[8:12], payload[0])
	binary.LittleEndian.PutUint32(skippableFrame[12:16], payload[1])
	binary.LittleEndian.PutUint32(skippableFrame[16:20], payload[2])
	binary.LittleEndian.PutUint32(skippableFrame[20:24], payload[3])

	logger.Log.Infof("Skippable frame has been created with the following metadata: %d", skippableFrame[8:24])

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

// Calculates sha256sum hash for a given file
func calculateSHA256(filePath string) (string, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return "", err
	}
	defer file.Close()

	hash := sha256.New()
	if _, err := io.Copy(hash, file); err != nil {
		return "", err
	}

	hashInBytes := hash.Sum(nil)
	hashString := hex.EncodeToString(hashInBytes)

	return hashString, nil
}

// Decompress the .raw.zst partition file and verifies the hash matches with the source .raw file
func verifySkippableFrameDecompression(rawPartitionFilepath string, rawZstPartitionFilepath string) (err error) {
	// Decompressing .raw.zst file
	decompressedPartitionFilePath := "build/decompressed.raw"
	err = shell.ExecuteLive(true, "zstd", "-d", rawZstPartitionFilepath, "-o", decompressedPartitionFilePath)
	if err != nil {
		return fmt.Errorf("failed to decompress %s with zstd:\n%w", rawZstPartitionFilepath, err)
	}

	// Calculating hashes
	rawPartitionFileHash, err := calculateSHA256(rawPartitionFilepath)
	if err != nil {
		return fmt.Errorf("error: %w", err)
	}
	decompressedPartitionFileHash, err := calculateSHA256(decompressedPartitionFilePath)
	if err != nil {
		return fmt.Errorf("error: %w", err)
	}

	// Verifying hashes are equal
	if rawPartitionFileHash != decompressedPartitionFileHash {
		return fmt.Errorf("decompressed partition file hash does not match source partition file hash: %s != %s", decompressedPartitionFileHash, rawPartitionFilepath)
	}
	logger.Log.Infof("Decompressed partition file hash matches source partition file hash!")

	// Removing decompressed file
	err = os.Remove(decompressedPartitionFilePath)
	if err != nil {
		return fmt.Errorf("failed to remove raw file %s:\n%w", decompressedPartitionFilePath, err)
	}

	return nil
}

// Verifies that the skippable frame has been correctly prepended to the partition file with the correct data
func verifySkippableFrameMetadataFromFile(partitionFilepath string, magicNumber uint32, frameSize uint32, metadata [16]byte) (err error) {
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

	// verify that the skippable frame has the correct inserted metadata by validating metadata
	if !bytes.Equal(existingData[8:8+frameSize], metadata[:]) {
		return fmt.Errorf("skippable frame metadata does not match the inserted metadata:\n %d != %d", existingData[8:8+frameSize], metadata[:])
	}
	logger.Log.Infof("Skippable frame is valid and contains the correct metadata!")

	return nil
}
