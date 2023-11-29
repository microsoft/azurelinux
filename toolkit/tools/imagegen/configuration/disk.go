// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
	"sort"
	"strconv"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
)

// Disk holds the disk partitioning, formatting and size information.
// It may also define artifacts generated for each disk.
type Disk struct {
	PartitionTableType PartitionTableType `json:"PartitionTableType"`
	MaxSize            uint64             `json:"MaxSize"`
	BlockSize          uint32             `json:"BlockSize"`
	TargetDisk         TargetDisk         `json:"TargetDisk"`
	Artifacts          []Artifact         `json:"Artifacts"`
	Partitions         []Partition        `json:"Partitions"`
	RawBinaries        []RawBinary        `json:"RawBinaries"`
}

// checkOverlappingPartitions checks that start and end positions of the defined partitions don't overlap.
func checkOverlappingePartitions(disk *Disk) (err error) {
	partIntervals := [][]uint64{}
	//convert  partition entries to array of [start,end] locations
	for _, part := range disk.Partitions {
		partIntervals = append(partIntervals, []uint64{part.Start, part.End})
	}
	//sorting paritions by start position
	sort.Slice(partIntervals, func(i, j int) bool {
		return partIntervals[i][0] < partIntervals[j][0]
	})
	//confirm each partition ends before the next starts
	for i := 0; i < len(partIntervals)-1; i++ {
		if partIntervals[i][1] > partIntervals[i+1][0] {
			return fmt.Errorf("a [Partition] with an end location %d overlaps with a [Partition] with a start location %d", partIntervals[i][1], partIntervals[i+1][0])
		}
	}
	return
}

// checkMaxSizeCorrectness checks that MaxSize is non-zero for cases in which it's used to clear disk space. This check
// also confirms that the MaxSize defined is large enough to accomodate all partitions. No partition should have an
// end position that exceeds the MaxSize
func checkMaxSizeCorrectness(disk *Disk) (err error) {
	const (
		realDiskType = "path"
	)
	//MaxSize is not relevant if target disk is specified.
	if disk.TargetDisk.Type != realDiskType {
		//Complain about 0 maxSize only when partitions are defined.
		if disk.MaxSize <= 0 && len(disk.Partitions) != 0 {
			return fmt.Errorf("a configuration without a defined target disk must have a non-zero MaxSize")
		}
		lastPartitionEnd := uint64(0)
		maxSize := disk.MaxSize
		//check last parition end location does not surpass MaxSize
		for _, part := range disk.Partitions {
			if part.End == 0 {
				lastPartitionEnd = part.Start
			} else if part.End > lastPartitionEnd {
				lastPartitionEnd = part.End
			}
		}
		maxSizeString := strconv.FormatUint(maxSize, 10)
		lastPartitionEndString := strconv.FormatUint(lastPartitionEnd, 10)
		if maxSize < lastPartitionEnd {
			return fmt.Errorf("the MaxSize of %s is not large enough to accomodate defined partitions ending at %s", maxSizeString, lastPartitionEndString)
		}
	} else if disk.MaxSize != 0 {
		logger.Log.Warnf("defining both a maxsize and target disk in the same config should be avoided as maxsize value will not be used")
	}
	return
}

// IsValid returns an error if the PartitionTableType is not valid
func (d *Disk) IsValid() (err error) {
	if d.BlockSize != 0 && d.BlockSize != 512 && d.BlockSize != 4096 {
		return fmt.Errorf("invalid [BlockSize]: %d. Must be 0, 512, or 4096", d.BlockSize)
	}
	if err = d.PartitionTableType.IsValid(); err != nil {
		return fmt.Errorf("invalid [PartitionTableType]: %w", err)
	}

	err = checkOverlappingePartitions(d)
	if err != nil {
		return fmt.Errorf("invalid [Disk]: %w", err)
	}

	err = checkMaxSizeCorrectness(d)
	if err != nil {
		return fmt.Errorf("invalid [Disk]: %w", err)
	}

	// if err = disk.PartitionTableType.IsValid(); err != nil {
	// 	return
	// }
	// for _, artifact := range disk.Artifacts {
	// 	if err = artifact.IsValid(); err != nil {
	// 		return
	// 	}
	// }
	for _, partition := range d.Partitions {
		if err = partition.IsValid(); err != nil {
			return
		}
	}
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
