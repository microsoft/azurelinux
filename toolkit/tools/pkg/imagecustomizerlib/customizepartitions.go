// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"path/filepath"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerapi"
)

func customizePartitions(buildDir string, baseConfigPath string, config *imagecustomizerapi.Config,
	buildImageFile string,
) (bool, string, error) {
	if config.Disks == nil && config.SystemConfig.BootType == imagecustomizerapi.BootTypeUnset {
		// No changes to make to the partitions.
		// So, just use the original disk.
		return false, buildImageFile, nil
	}

	newBuildImageFile := filepath.Join(buildDir, PartitionCustomizedImageName)

	// If there is no known way to create the new partition layout from the old one,
	// then fallback to creating the new partitions from scratch and doing a file copy.
	err := customizePartitionsUsingFileCopy(buildDir, baseConfigPath, config, buildImageFile, newBuildImageFile)
	if err != nil {
		return false, "", err
	}

	return true, newBuildImageFile, nil
}
