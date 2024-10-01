// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

// FileSystemType is a type of file system (e.g. ext4, xfs, etc.)
type FileSystemType string

const (
	FileSystemTypeNone  FileSystemType = ""
	FileSystemTypeExt4  FileSystemType = "ext4"
	FileSystemTypeXfs   FileSystemType = "xfs"
	FileSystemTypeFat32 FileSystemType = "fat32"
	FileSystemTypeVfat  FileSystemType = "vfat"
)

func (t FileSystemType) IsValid() error {
	switch t {
	case FileSystemTypeNone, FileSystemTypeExt4, FileSystemTypeXfs, FileSystemTypeFat32, FileSystemTypeVfat:
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid fileSystemType value (%s)", t)
	}
}
