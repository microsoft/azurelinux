// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
	"sort"
	"strconv"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
)

type Disk struct {
	// The type of partition table to use (e.g. mbr, gpt)
	PartitionTableType PartitionTableType `yaml:"partitionTableType"`

	// The virtual size of the disk.
	MaxSize DiskSize `yaml:"maxSize"`

	// The partitions to allocate on the disk.
	Partitions []Partition `yaml:"partitions"`
}

func (d *Disk) IsValid() error {
	err := d.PartitionTableType.IsValid()
	if err != nil {
		return err
	}

	if d.MaxSize <= 0 {
		return fmt.Errorf("a disk's maxSize value (%d) must be a positive non-zero number", d.MaxSize)
	}

	partitionIDSet := make(map[string]bool)
	for i, partition := range d.Partitions {
		err := partition.IsValid()
		if err != nil {
			return fmt.Errorf("invalid partition at index (%d):\n%w", i, err)
		}

		if _, existingName := partitionIDSet[partition.Id]; existingName {
			return fmt.Errorf("duplicate partition id used (%s) at index %d", partition.Id, i)
		}

		partitionIDSet[partition.Id] = false // dummy value
	}

	// Check for overlapping partitions.
	// First, sort partitions by start index.
	sortedPartitions := append([]Partition(nil), d.Partitions...)
	sort.Slice(sortedPartitions, func(i, j int) bool {
		return sortedPartitions[i].Start < sortedPartitions[j].Start
	})

	// Then, confirm each partition ends before the next starts.
	for i := 0; i < len(sortedPartitions)-1; i++ {
		a := &sortedPartitions[i]
		b := &sortedPartitions[i+1]

		aEnd, aHasEnd := a.GetEnd()
		if !aHasEnd {
			return fmt.Errorf("partition (%s) is not last partition but size is set to \"grow\"", a.Id)
		}
		if aEnd > b.Start {
			bEnd, bHasEnd := b.GetEnd()
			bEndStr := ""
			if bHasEnd {
				bEndStr = strconv.FormatUint(uint64(bEnd), 10)
			}
			return fmt.Errorf("partition's (%s) range [%d, %d) overlaps partition's (%s) range [%d, %s)",
				a.Id, a.Start, aEnd, b.Id, b.Start, bEndStr)
		}
	}

	if len(sortedPartitions) > 0 {
		// Make sure the first block isn't used.
		firstPartition := sortedPartitions[0]
		if firstPartition.Start < diskutils.MiB {
			return fmt.Errorf("first 1 MiB must be reserved for the MBR header (%s)", firstPartition.Id)
		}

		// Check that the disk is big enough for the partition layout.
		lastPartition := sortedPartitions[len(sortedPartitions)-1]

		lastPartitionEnd, lastPartitionHasEnd := lastPartition.GetEnd()

		var requiredSize DiskSize
		if !lastPartitionHasEnd {
			requiredSize = lastPartition.Start + diskutils.MiB
		} else {
			requiredSize = lastPartitionEnd
		}

		if requiredSize > d.MaxSize {
			return fmt.Errorf("disk's partitions need %d bytes but maxSize is only %d bytes", requiredSize, d.MaxSize)
		}
	}

	return nil
}
