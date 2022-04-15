// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
)

// FsType defined the fsType for each partition in a config
type FsType string

const (
	FsTypeFat32 FsType = "fat32"
	FsTypeFat16 FsType = "fat16"
	FsTypeVfat FsType = "vfat"
	FsTypeExt2 FsType = "ext2"
	FsTypeExt3 FsType = "ext3"
	FsTypeExt4 FsType = "ext4"
	FsTypeSwap FsType = "linux-swap"
	FsTypeEmpty FsType = ""
)

func (f FsType) String() string {
	return fmt.Sprint(string(f))
}

// GetValidImaPolicies returns a list of all the supported
// disk partition types
func (f *FsType) GetValidFsType() (types []FsType) {
	return []FsType{
		FsTypeFat32,
		FsTypeFat16,
		FsTypeVfat,
		FsTypeExt2,
		FsTypeExt3,
		FsTypeExt4,
		FsTypeSwap,
		FsTypeEmpty,
	}
}

// IsValid returns an error if the fsType is not valid
func (f *FsType) IsValid() (err error) {
	for _, valid := range f.GetValidFsType() {
		if *f == valid {
			return
		}
	}
	return fmt.Errorf("invalid value for FsType (%s)", f)
}

// UnmarshalJSON Unmarshals an fsType entry
func (f *FsType) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypeFsType FsType
	err = json.Unmarshal(b, (*IntermediateTypeFsType)(f))
	if err != nil {
		return fmt.Errorf("failed to parse [FsType]: %w", err)
	}

	// Now validate the resulting unmarshaled object
	err = f.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [FsType]: %w", err)
	}
	return
}
