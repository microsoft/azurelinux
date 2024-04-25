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

	// The permissions to set on the top-level directory, given that it does not exist already.
	// If directory being copied does exist on the image, the permissions will not be overridden with this value.
	Permissions *DirPermissions `yaml:"permissions"`

	// The permissions to set on the children of the directory.
	ChildPermissions *DirPermissions `yaml:"childPermissions"`
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
	if d.Permissions != nil {
		err = d.Permissions.IsValid()
		if err != nil {
			return fmt.Errorf("invalid [permissions] value: %w", err)
		}
	}
	if d.ChildPermissions != nil {
		err = d.ChildPermissions.IsValid()
		if err != nil {
			return fmt.Errorf("invalid [childPermissions] value: %w", err)
		}
	}

	return nil
}
