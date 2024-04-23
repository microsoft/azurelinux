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
	SourcePath string `yaml:"SourcePath"`

	// The path in the target OS that the directory will be copied to.
	DestinationPath string `yaml:"DestinationPath"`

	// The permissions to set on the directory.
	Permissions *DirPermissions `yaml:"Permissions"`

	// The permissions to set on the children of the directory.
	ChildPermissions *DirPermissions `yaml:"ChildPermissions"`
}

func (l *DirConfigList) IsValid() (err error) {
	if len(*l) <= 0 {
		return fmt.Errorf("list is empty")
	}

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
		return fmt.Errorf("invalid [SourcePath] value: empty string")
	}
	if d.DestinationPath == "" {
		return fmt.Errorf("invalid [DestinationPath] value: empty string")
	}

	// Permissions
	if d.Permissions != nil {
		err = d.Permissions.IsValid()
		if err != nil {
			return fmt.Errorf("invalid [Permissions] value: %w", err)
		}
	}
	if d.ChildPermissions != nil {
		err = d.ChildPermissions.IsValid()
		if err != nil {
			return fmt.Errorf("invalid [ChildPermissions] value: %w", err)
		}
	}

	return nil
}
