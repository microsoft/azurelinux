// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"path/filepath"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

func customizePartitions(buildDir string, baseConfigPath string, config *imagecustomizerapi.Config,
	buildImageFile string,
) (bool, string, error) {
	switch {
	case config.Storage != nil:
		logger.Log.Infof("Customizing partitions")

		newBuildImageFile := filepath.Join(buildDir, PartitionCustomizedImageName)

		// If there is no known way to create the new partition layout from the old one,
		// then fallback to creating the new partitions from scratch and doing a file copy.
		err := customizePartitionsUsingFileCopy(buildDir, baseConfigPath, config, buildImageFile, newBuildImageFile)
		if err != nil {
			return false, "", err
		}

		return true, newBuildImageFile, nil

	case config.ResetPartitionsUuidsType != imagecustomizerapi.ResetPartitionsUuidsTypeDefault:
		err := resetPartitionsUuids(buildImageFile, buildDir)
		if err != nil {
			return false, "", err
		}

		return true, buildImageFile, nil

	default:
		// No changes to make to the partitions.
		// So, just use the original disk.
		return false, buildImageFile, nil
	}
}
