package imagecustomizerlib

import (
	"fmt"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
)

// Extract all partitions of connected image into separate files with specified format.
func extractPartitions(imageConnection *ImageConnection, outputImageFile string, partitionFormat string) error {

	// Extract basename from outputImageFile. E.g. if outputImageFile is "image.qcow2", then basename is "image".
	basename := strings.TrimSuffix(filepath.Base(outputImageFile), filepath.Ext(outputImageFile))

	// Get path of loop device associated with the image.
	imageLoopDevice := imageConnection.Loopback().DevicePath()

	// Get output directory path.
	outDir := filepath.Dir(outputImageFile)

	// Get partition info.
	diskPartitions, err := diskutils.GetDiskPartitions(imageLoopDevice)
	if err != nil {
		return err
	}

	// Start extracting from 1 because the diskPartitions[0] refers to the image itself.
	for partitionNum := 1; partitionNum < len(diskPartitions); partitionNum++ {
		rawFilename := basename + "_" + strconv.Itoa(partitionNum) + ".raw"
		partitionLoopDevice := diskPartitions[partitionNum].Path

		err, partitionFilepath := createRawFile(outDir, partitionLoopDevice, rawFilename)
		if err != nil {
			return err
		}

		if partitionFormat == "raw-zstd" {
			err, partitionFilepath = compressWithZstd(partitionFilepath)
			if err != nil {
				return err
			}
		}

		logger.Log.Infof("Partition file created: %s", partitionFilepath)
	}
	return nil
}

// Creates .raw file for the mentioned partition path.
func createRawFile(outDir, devicePath, name string) (err error, filename string) {
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

	return shell.ExecuteLive(squashErrors, "dd", ddArgs...), fullPath
}

// Compress file from raw to raw-zstd format using zstd.
func compressWithZstd(partitionRawFilepath string) (err error, partitionFilepath string) {
	// Using -f to overwrite a file with same name if it exists.
	cmd := exec.Command("zstd", "-f", "-9", "-T0", partitionRawFilepath)
	_, err = cmd.Output()
	if err != nil {
		return err, ""
	}

	// Remove raw file since output partition format is raw-zstd.
	file.RemoveFileIfExists(partitionRawFilepath)

	return nil, partitionRawFilepath + ".zst"
}
