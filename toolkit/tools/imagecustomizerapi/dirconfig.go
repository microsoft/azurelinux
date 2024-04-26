// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

//

package imagecustomizerapi

import (
	"fmt"
)

// DirConfigList is a list of destination files where the source file will be copied to in the final image.
// This type exists to allow a custom marshaller to be attached to it.
type DirConfigList []DirConfig

type DirConfig struct {
	// The path in the target OS that the directory will be copied to.
	SourcePath string `yaml:"sourcePath"`

	// The path in the target OS that the directory will be copied to.
	DestinationPath string `yaml:"destinationPath"`

	// The permissions to set on all of the new directories being created on the target OS (including the top-level directory).
	// Note: If this value is not specified in the config, the permissions for these directories will be set to 0777.
	NewDirPermissions *FilePermissions `yaml:"newDirPermissions"`

	// The permissions to set on the directories being copied that already do exist on the target OS (including the top-level directory).
	// Note: If this value is not specified in the config, the permissions for this field will be the same as that of the pre-existing directory.
	MergedDirPermissions *FilePermissions `yaml:"mergedDirPermissions"`

	// The permissions to set on the children file of the directory.
	// Note: If this value is not specified in the config, the permissions for these directories will be set to 0777.
	ChildFilePermissions *FilePermissions `yaml:"childFilePermissions"`
}

func (l *DirConfigList) IsValid() (err error) {
	for i, dirConfig := range *l {
		err = dirConfig.IsValid()
		if err != nil {
			return fmt.Errorf("invalid [dirConfig] at index %d: %w", i, err)
		}
	}

	return nil
}

func (d *DirConfig) IsValid() (err error) {
	// Paths
	if d.SourcePath == "" {
		return fmt.Errorf("invalid [sourcePath] value: empty string")
	}
	if d.DestinationPath == "" {
		return fmt.Errorf("invalid [destinationPath] value: empty string")
	}

	// Permissions
	if d.NewDirPermissions != nil {
		err = d.NewDirPermissions.IsValid()
		if err != nil {
			return fmt.Errorf("invalid [newDirPermissions] value: %w", err)
		}
	}
	if d.MergedDirPermissions != nil {
		err = d.MergedDirPermissions.IsValid()
		if err != nil {
			return fmt.Errorf("invalid [mergedDirPermissions] value: %w", err)
		}
	}
	if d.ChildFilePermissions != nil {
		err = d.ChildFilePermissions.IsValid()
		if err != nil {
			return fmt.Errorf("invalid [childFilePermissions] value: %w", err)
		}
	}

	return nil
}
