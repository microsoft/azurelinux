// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
	"path"
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

	if p.Path == "" {
		return fmt.Errorf("invalid path (%s): must not be empty", p.Path)
	}

	if !path.IsAbs(p.Path) {
		return fmt.Errorf("invalid path (%s): must be an absolute path", p.Path)
	}

	return nil
}
