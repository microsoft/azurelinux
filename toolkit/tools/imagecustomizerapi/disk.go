// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/ptrutils"
)

const (
	DefaultSectorSize = 512

	// For SSDs, aligning partition's to 1 MiB is beneficial for performance reasons.
	// In addition, the imager's diskutils works in MiB.
	DefaultPartitionAlignment = diskutils.MiB

	// The number of sectors (LBA) that the GPT header requires.
	GptHeaderSectorNum = 34

	// The number of sectors (LBA) that the GPT footer requires.
	GptFooterSectorNum = 33
)

type Disk struct {
	// The type of partition table to use (e.g. mbr, gpt)
	PartitionTableType PartitionTableType `yaml:"partitionTableType"`

	// The virtual size of the disk.
	// Note: This value is filled in by IsValid().
	MaxSize *DiskSize `yaml:"maxSize"`

	// The partitions to allocate on the disk.
	Partitions []Partition `yaml:"partitions"`
}

func (d *Disk) IsValid() error {
	err := d.PartitionTableType.IsValid()
	if err != nil {
		return err
	}

	if d.MaxSize != nil {
		if *d.MaxSize <= 0 {
			return fmt.Errorf("a disk's maxSize value (%d) must be a positive non-zero number", *d.MaxSize)
		}
	}

	for i, partition := range d.Partitions {
		err := partition.IsValid()
		if err != nil {
			return fmt.Errorf("invalid partition at index %d:\n%w", i, err)
		}
	}

	gptHeaderSize := DiskSize(roundUp(GptHeaderSectorNum*DefaultSectorSize, DefaultPartitionAlignment))
	gptFooterSize := DiskSize(roundUp(GptFooterSectorNum*DefaultSectorSize, DefaultPartitionAlignment))

	// Auto-fill the start value from the previous partition's end value.
	for i := range d.Partitions {
		partition := &d.Partitions[i]

		if partition.Start == nil {
			if i == 0 {
				partition.Start = ptrutils.PtrTo(DiskSize(DefaultPartitionAlignment))
			} else {
				prev := d.Partitions[i-1]
				prevEnd, prevHasEnd := prev.GetEnd()
				if !prevHasEnd {
					return fmt.Errorf("partition (%s) omitted start value but previous partition (%s) has no size or end value",
						partition.Id, prev.Id)
				}
				partition.Start = &prevEnd
			}
		}

		if partition.Type == PartitionTypeBiosGrub {
			if *partition.Start != diskutils.MiB {
				return fmt.Errorf("BIOS boot partition must start at 1 MiB")
			}
		}
	}

	// Confirm each partition ends before the next starts.
	for i := 0; i < len(d.Partitions)-1; i++ {
		a := d.Partitions[i]
		b := d.Partitions[i+1]

		aEnd, aHasEnd := a.GetEnd()
		if !aHasEnd {
			return fmt.Errorf("partition (%s) is not last partition but size is set to \"grow\"", a.Id)
		}
		if aEnd > *b.Start {
			bEnd, bHasEnd := b.GetEnd()
			bEndStr := ""
			if bHasEnd {
				bEndStr = bEnd.HumanReadable()
			}
			return fmt.Errorf("partition's (%s) range [%s, %s) overlaps partition's (%s) range [%s, %s)",
				a.Id, a.Start.HumanReadable(), aEnd.HumanReadable(), b.Id, b.Start.HumanReadable(), bEndStr)
		}
	}

	if d.MaxSize == nil && len(d.Partitions) <= 0 {
		return fmt.Errorf("either disk must specify maxSize or last partition must have an end or size value")
	}

	if len(d.Partitions) > 0 {
		// Make sure the first block isn't used.
		firstPartition := d.Partitions[0]
		if *firstPartition.Start < gptHeaderSize {
			return fmt.Errorf("invalid partition (%s) start:\nfirst %s of disk is reserved for the GPT header",
				firstPartition.Id, gptHeaderSize.HumanReadable())
		}

		// Verify MaxSize value.
		lastPartition := d.Partitions[len(d.Partitions)-1]
		lastPartitionEnd, lastPartitionHasEnd := lastPartition.GetEnd()

		switch {
		case !lastPartitionHasEnd && d.MaxSize == nil:
			return fmt.Errorf("either disk must specify maxSize or last partition (%s) must have an end or size value",
				lastPartition.Id)

		case d.MaxSize == nil:
			// Fill in the disk's size.
			diskSize := lastPartitionEnd + gptFooterSize
			d.MaxSize = &diskSize

		default:
			// Check that the disk is big enough for the partition layout.
			var requiredSize DiskSize
			if !lastPartitionHasEnd {
				requiredSize = *lastPartition.Start + DefaultPartitionAlignment
			} else {
				requiredSize = lastPartitionEnd
			}

			requiredSize += gptFooterSize

			if requiredSize > *d.MaxSize {
				return fmt.Errorf("disk's partitions need %s but maxSize is only %s:\nGPT footer size is %s",
					requiredSize.HumanReadable(), d.MaxSize.HumanReadable(), gptFooterSize.HumanReadable())
			}
		}
	}

	return nil
}

func roundUp(size uint64, alignment uint64) uint64 {
	div := size / alignment
	mod := size % alignment
	if mod == 0 {
		return size
	}
	return (div + 1) * alignment
}
