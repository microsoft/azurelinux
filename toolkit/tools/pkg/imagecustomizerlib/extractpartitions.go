package imagecustomizerlib

import (
	"crypto/rand"
	"encoding/binary"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strconv"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

type outputPartitionMetadata struct {
	PartitionNum      int    `json:"partitionnum"` // Example: 1
	PartitionFilename string `json:"filename"`     // Example: image_1.raw.zst
	PartLabel         string `json:"partlabel"`    // Example: boot
	FileSystemType    string `json:"fstype"`       // Example: vfat
	PartitionTypeUuid string `json:"parttype"`     // Example: c12a7328-f81f-11d2-ba4b-00a0c93ec93b
	Uuid              string `json:"uuid"`         // Example: 4BD9-3A78
	PartUuid          string `json:"partuuid"`     // Example: 7b1367a6-5845-43f2-99b1-a742d873f590
	Mountpoint        string `json:"mountpoint"`   // Example: /mnt/os/boot
}

const (
	SkippableFrameMagicNumber uint32 = 0x184D2A50
	SkippableFramePayloadSize uint32 = 16
	SkippableFrameHeaderSize  int    = 8
)

// Extract all partitions of connected image into separate files with specified format.
func extractPartitions(imageLoopDevice string, outDir string, basename string, partitionFormat string) error {

	// Get partition info
	diskPartitions, err := diskutils.GetDiskPartitions(imageLoopDevice)
	if err != nil {
		return err
	}

	// Stores the output partition metadata that will be written to JSON file
	var partitionMetadataOutput []outputPartitionMetadata

	// Create skippable frame metadata defined as a random 128-bit number
	skippableFrameMetadata, err := createSkippableFrameMetadata()
	if err != nil {
		return err
	}

	// Extract partitions to files
	for partitionNum := range diskPartitions {
		partition := diskPartitions[partitionNum]
		if partition.Type != "part" {
			continue
		}

		partitionFilename := basename + "_" + strconv.Itoa(partitionNum)
		rawFilename := partitionFilename + ".raw"
		partitionLoopDevice := partition.Path

		partitionFilepath, err := copyBlockDeviceToFile(outDir, partitionLoopDevice, rawFilename)
		if err != nil {
			return err
		}

		partitionFullFilePath, err := filepath.Abs(partitionFilepath)
		if err != nil {
			return fmt.Errorf("failed to get absolute path (%s):\n%w", partitionFilepath, err)
		}

		// Sanity check the partition file.
		err = checkFileSystemFile(partition.FileSystemType, partitionFullFilePath)
		if err != nil {
			return fmt.Errorf("failed to check file system integrity (%s):\n%w", partitionFilepath, err)
		}

		switch partitionFormat {
		case "raw":
			// Do nothing for "raw" case
		case "raw-zst":
			partitionFilepath, err = extractRawZstPartition(partitionFilepath, skippableFrameMetadata, partitionFilename, outDir)
			if err != nil {
				return err
			}
		default:
			return fmt.Errorf("unsupported partition format (supported: raw, raw-zst): %s", partitionFormat)
		}

		partitionMetadata, err := constructOutputPartitionMetadata(partition, partitionNum, partitionFilepath)
		if err != nil {
			return fmt.Errorf("failed to construct partition metadata:\n%w", err)
		}
		partitionMetadataOutput = append(partitionMetadataOutput, partitionMetadata)
		logger.Log.Infof("Partition file created: %s", partitionFilepath)
	}

	// Write partition metadata JSON to a file
	jsonFilename := basename + "_partition_metadata.json"
	err = writePartitionMetadataJson(outDir, jsonFilename, &partitionMetadataOutput)
	if err != nil {
		return fmt.Errorf("failed to write partition metadata json:\n%w", err)
	}
	return nil
}

// Extract raw-zst partition.
func extractRawZstPartition(partitionRawFilepath string, skippableFrameMetadata [SkippableFramePayloadSize]byte, partitionFilename string, outDir string) (partitionFilepath string, err error) {
	// Define file path for temporary partition
	tempPartitionFilepath := outDir + "/" + partitionFilename + "_temp.raw.zst"
	// Compress raw partition with zstd
	err = compressWithZstd(partitionRawFilepath, tempPartitionFilepath)
	if err != nil {
		return "", err
	}
	// Remove raw file since output partition format is raw-zst
	err = os.Remove(partitionRawFilepath)
	if err != nil {
		return "", fmt.Errorf("failed to remove raw file %s:\n%w", partitionRawFilepath, err)
	}
	// Create a skippable frame containing the metadata and prepend the frame to the partition file
	partitionFilepath, err = addSkippableFrame(tempPartitionFilepath, skippableFrameMetadata, partitionFilename, outDir)
	if err != nil {
		return "", err
	}
	// Remove temp partition file
	err = os.Remove(tempPartitionFilepath)
	if err != nil {
		return "", fmt.Errorf("failed to remove temp file %s:\n%w", tempPartitionFilepath, err)
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
func compressWithZstd(partitionRawFilepath string, outputPartitionFilepath string) (err error) {
	// Using -f to overwrite a file with same name if it exists.
	err = shell.ExecuteLive(true, "zstd", "-f", "-9", "-T0", partitionRawFilepath, "-o", outputPartitionFilepath)
	if err != nil {
		return fmt.Errorf("failed to compress %s with zstd:\n%w", partitionRawFilepath, err)
	}

	return nil
}

// Prepend a skippable frame with the metadata to the specified partition file.
func addSkippableFrame(tempPartitionFilepath string, skippableFrameMetadata [SkippableFramePayloadSize]byte, partitionFilename string, outDir string) (partitionFilepath string, err error) {
	// Open tempPartitionFile for reading
	tempPartitionFile, err := os.OpenFile(tempPartitionFilepath, os.O_RDWR, os.ModePerm)
	if err != nil {
		return "", fmt.Errorf("failed to open partition file %s:\n%w", tempPartitionFilepath, err)
	}
	// Create a skippable frame
	skippableFrame := createSkippableFrame(SkippableFrameMagicNumber, SkippableFramePayloadSize, skippableFrameMetadata)
	// Define the final partition file path
	partitionFilepath = outDir + "/" + partitionFilename + ".raw.zst"
	// Create partition file
	finalFile, err := os.Create(partitionFilepath)
	if err != nil {
		return "", err
	}
	// Write the skippable frame to file
	_, err = finalFile.Write(skippableFrame)
	if err != nil {
		return "", err
	}
	// Copy the data from the tempPartitionFile into finalFile
	_, err = io.Copy(finalFile, tempPartitionFile)
	if err != nil {
		return "", err
	}
	return partitionFilepath, nil
}

// Creates a skippable frame.
func createSkippableFrame(magicNumber uint32, frameSize uint32, skippableFrameMetadata [SkippableFramePayloadSize]byte) (skippableFrame []byte) {
	// Calculate the length of the byte array
	lengthOfByteArray := SkippableFrameHeaderSize + len(skippableFrameMetadata)
	// Define the Skippable frame
	skippableFrame = make([]byte, lengthOfByteArray)
	// Magic_Number
	binary.LittleEndian.PutUint32(skippableFrame, magicNumber)
	// Frame_Size
	binary.LittleEndian.PutUint32(skippableFrame[4:8], frameSize)
	// User_Data
	copy(skippableFrame[8:8+frameSize], skippableFrameMetadata[:])

	logger.Log.Infof("Skippable frame has been created with the following metadata: %d", skippableFrame[8:8+frameSize])

	return skippableFrame
}

// Create user metadata that will be inserted into the skippable frame.
func createSkippableFrameMetadata() (skippableFrameMetadata [SkippableFramePayloadSize]byte, err error) {
	// Set the skippableFrameMetadata to be a random 128-Bit number
	skippableFrameMetadata, err = generateRandom128BitNumber()
	if err != nil {
		return skippableFrameMetadata, err
	}
	return skippableFrameMetadata, nil
}

// Generates a Random 128-Bit number.
func generateRandom128BitNumber() ([SkippableFramePayloadSize]byte, error) {
	var randomBytes [SkippableFramePayloadSize]byte
	_, err := rand.Read(randomBytes[:])
	if err != nil {
		return randomBytes, err
	}
	return randomBytes, nil
}

// Construct outputPartitionMetadata for given partition.
func constructOutputPartitionMetadata(diskPartition diskutils.PartitionInfo, partitionNum int, partitionFilepath string) (partitionMetadata outputPartitionMetadata, err error) {
	partitionMetadata.PartitionNum = partitionNum
	partitionMetadata.PartitionFilename = filepath.Base(partitionFilepath)
	partitionMetadata.PartLabel = diskPartition.PartLabel
	partitionMetadata.FileSystemType = diskPartition.FileSystemType
	partitionMetadata.PartitionTypeUuid = diskPartition.PartitionTypeUuid
	partitionMetadata.Uuid = diskPartition.Uuid
	partitionMetadata.PartUuid = diskPartition.PartUuid
	partitionMetadata.Mountpoint = diskPartition.Mountpoint

	return partitionMetadata, nil
}

// Write partition metadata as JSON to a file.
func writePartitionMetadataJson(outDir string, name string, output *[]outputPartitionMetadata) (err error) {
	fullPath := filepath.Join(outDir, name)

	err = jsonutils.WriteJSONFile(fullPath, output)
	if err != nil {
		return err
	}

	logger.Log.Infof("Partition metadata file created: %s", fullPath)
	return nil
}
