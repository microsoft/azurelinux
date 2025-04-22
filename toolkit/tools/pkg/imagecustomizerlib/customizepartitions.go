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
) (bool, string, map[string]string, error) {
	switch {
	case config.CustomizePartitions():
		logger.Log.Infof("Customizing partitions")

		newBuildImageFile := filepath.Join(buildDir, PartitionCustomizedImageName)

		// If there is no known way to create the new partition layout from the old one,
		// then fallback to creating the new partitions from scratch and doing a file copy.
		partIdToPartUuid, err := customizePartitionsUsingFileCopy(buildDir, baseConfigPath, config,
			buildImageFile, newBuildImageFile)
		if err != nil {
			return false, "", nil, err
		}

		return true, newBuildImageFile, partIdToPartUuid, nil

	case config.Storage.ResetPartitionsUuidsType != imagecustomizerapi.ResetPartitionsUuidsTypeDefault:
		err := resetPartitionsUuids(buildImageFile, buildDir)
		if err != nil {
			return false, "", nil, err
		}

		return true, buildImageFile, nil, nil

	default:
		// No changes to make to the partitions.
		// So, just use the original disk.
		return false, buildImageFile, nil, nil
	}
}
