// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
	"unicode"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
)

type Partition struct {
	// ID is used to correlate `Partition` objects with `PartitionSetting` objects.
	Id string `yaml:"id"`
	// Name is the label to assign to the partition.
	Label string `yaml:"label"`
	// Start is the offset where the partition begins (inclusive), in MiBs.
	Start DiskSize `yaml:"start"`
	// End is the offset where the partition ends (exclusive), in MiBs.
	End *DiskSize `yaml:"end"`
	// Size is the size of the partition in MiBs.
	Size *DiskSize `yaml:"size"`
	// Type specifies the type of partition the partition is.
	Type PartitionType `yaml:"type"`
}

func (p *Partition) IsValid() error {
	err := isGPTNameValid(p.Label)
	if err != nil {
		return err
	}

	if p.End != nil && p.Size != nil {
		return fmt.Errorf("cannot specify both end and size on partition (%s)", p.Id)
	}

	if (p.End != nil && p.Start >= *p.End) || (p.Size != nil && *p.Size <= 0) {
		return fmt.Errorf("partition's (%s) size can't be 0 or negative", p.Id)
	}

	err = p.Type.IsValid()
	if err != nil {
		return err
	}

	if p.IsBiosBoot() {
		if p.Start != diskutils.MiB {
			return fmt.Errorf("BIOS boot partition must start at 1 MiB")
		}
	}

	return nil
}

func (p *Partition) GetEnd() (DiskSize, bool) {
	if p.End != nil {
		return *p.End, true
	}

	if p.Size != nil {
		return p.Start + *p.Size, true
	}

	return 0, false
}

func (p *Partition) IsESP() bool {
	return p.Type == PartitionTypeESP
}

func (p *Partition) IsBiosBoot() bool {
	return p.Type == PartitionTypeBiosGrub
}

// isGPTNameValid checks if a GPT partition name is valid.
func isGPTNameValid(name string) error {
	// The max partition name length is 36 UTF-16 code units, including a null terminator.
	// Since we are also restricting the name to ASCII, this means 35 ASCII characters.
	const maxLength = 35

	// Restrict the name to only ASCII characters as some tools (e.g. parted) work better
	// with only ASCII characters.
	for _, char := range name {
		if char > unicode.MaxASCII {
			return fmt.Errorf("partition name (%s) contains a non-ASCII character (%c)", name, char)
		}
	}

	if len(name) > maxLength {
		return fmt.Errorf("partition name (%s) is too long", name)
	}

	return nil
}
