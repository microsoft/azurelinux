// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

// FileSystem holds the file system information for a partition.
type FileSystem struct {
	// DeviceId is the ID of the source partition.
	DeviceId string `yaml:"deviceId"`
	// FileSystemType is the type of file system to use on the partition.
	Type FileSystemType `yaml:"type"`
	// MountPoint contains the mount settings.
	MountPoint *MountPoint `yaml:"mountPoint"`
}

// IsValid returns an error if the MountPoint is not valid
func (f *FileSystem) IsValid() error {
	if f.DeviceId == "" {
		return fmt.Errorf("invalid deviceId value: must not be empty")
	}

	err := f.Type.IsValid()
	if err != nil {
		return fmt.Errorf("invalid fileSystem (%s) type value:\n%w", f.DeviceId, err)
	}

	if f.MountPoint != nil {
		err := f.MountPoint.IsValid()
		if err != nil {
			return fmt.Errorf("invalid mountPoint value:\n%w", err)
		}
	}

	return nil
}
