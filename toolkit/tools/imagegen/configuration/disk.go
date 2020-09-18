// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
)

// Disk holds the disk partitioning, formatting and size information.
// It may also define artifacts generated for each disk.
type Disk struct {
	PartitionTableType PartitionTableType `json:"PartitionTableType"`
	MaxSize            uint64             `json:"MaxSize"`
	TargetDisk         TargetDisk         `json:"TargetDisk"`
	Artifacts          []Artifact         `json:"Artifacts"`
	Partitions         []Partition        `json:"Partitions"`
	RawBinaries        []RawBinary        `json:"RawBinaries"`
}

// IsValid returns an error if the PartitionTableType is not valid
func (d *Disk) IsValid() (err error) {
	if err = d.PartitionTableType.IsValid(); err != nil {
		return fmt.Errorf("invalid [PartitionTableType]: %w", err)
	}

	// No limits on disk.MaxSize

	// if err = disk.PartitionTableType.IsValid(); err != nil {
	// 	return
	// }
	// for _, artifact := range disk.Artifacts {
	// 	if err = artifact.IsValid(); err != nil {
	// 		return
	// 	}
	// }
	// for _, partition := range disk.Partitions {
	// 	if err = partition.IsValid(); err != nil {
	// 		return
	// 	}
	// }
	// for _, rawBinary := range disk.RawBinaries {
	// 	if err = rawBinary.IsValid(); err != nil {
	// 		return
	// 	}
	// }
	return
}

// UnmarshalJSON Unmarshals a Disk entry
func (d *Disk) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypeDisk Disk
	err = json.Unmarshal(b, (*IntermediateTypeDisk)(d))
	if err != nil {
		return fmt.Errorf("failed to parse [Disk]: %w", err)
	}

	// Now validate the resulting unmarshalled object
	err = d.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [Disk]: %w", err)
	}
	return
}
