// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

// MountPoint holds the mounting information for each partition.
type MountPoint struct {
	// The ID type to use for the source in the /etc/fstab file.
	IdType MountIdentifierType `yaml:"idType"`
	// The additional options for the mount.
	Options string `yaml:"options"`
	// The target directory path of the mount.
	Path string `yaml:"path"`
}

// IsValid returns an error if the MountPoint is not valid
func (p *MountPoint) IsValid() error {
	err := p.IdType.IsValid()
	if err != nil {
		return fmt.Errorf("invalid idType value:\n%w", err)
	}

	// Use validatePath to check the Path field.
	if err := validatePath(p.Path); err != nil {
		return fmt.Errorf("invalid path:\n%w", err)
	}

	// Use validateMountOptions to check Options.
	if validateMountOptions(p.Options) {
		return fmt.Errorf("options (%s) contain spaces, tabs, or newlines and are invalid", p.Options)
	}

	return nil
}
