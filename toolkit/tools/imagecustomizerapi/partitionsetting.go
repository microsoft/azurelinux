// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
	"path"
)

// PartitionSetting holds the mounting information for each partition.
type PartitionSetting struct {
	ID                  string              `yaml:"id"`
	MountIdentifierType MountIdentifierType `yaml:"mountIdentifierType"`
	MountOptions        string              `yaml:"mountOptions"`
	MountPoint          string              `yaml:"mountPoint"`
}

// IsValid returns an error if the PartitionSetting is not valid
func (p *PartitionSetting) IsValid() error {
	err := p.MountIdentifierType.IsValid()
	if err != nil {
		return err
	}

	if p.MountPoint != "" && !path.IsAbs(p.MountPoint) {
		return fmt.Errorf("mountPoint (%s) must be an absolute path", p.MountPoint)
	}

	return nil
}
