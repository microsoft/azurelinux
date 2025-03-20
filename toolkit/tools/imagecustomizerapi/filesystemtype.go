// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import "fmt"

// FileSystemType is a type of file system (e.g. ext4, xfs, etc.)
type FileSystemType string

const (
	FileSystemTypeExt4  FileSystemType = "ext4"
	FileSystemTypeXfs   FileSystemType = "xfs"
	FileSystemTypeFat32 FileSystemType = "fat32"
)

func (t FileSystemType) IsValid() error {
	switch t {
	case FileSystemTypeExt4, FileSystemTypeXfs, FileSystemTypeFat32:
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid fileSystemType value (%s)", t)
	}
}
