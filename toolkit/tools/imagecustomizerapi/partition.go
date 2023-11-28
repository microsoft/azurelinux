// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
	"unicode"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/sliceutils"
)

type Partition struct {
	// ID is used to correlate `Partition` objects with `PartitionSetting` objects.
	ID string `yaml:"ID"`
	// FsType is the type of file system to use on the partition.
	FsType FileSystemType `yaml:"FsType"`
	// Name is the label to assign to the partition.
	Name string `yaml:"Name"`
	// Start is the offset where the partition begins (inclusive), in MiBs.
	Start uint64 `yaml:"Start"`
	// End is the offset where the partition ends (exclusive), in MiBs.
	End *uint64 `yaml:"End"`
	// Size is the size of the partition in MiBs.
	Size *uint64 `yaml:"Size"`
	// Flags assigns features to the partition.
	Flags []PartitionFlag `yaml:"Flags"`
}

func (p *Partition) IsValid() error {
	err := p.FsType.IsValid()
	if err != nil {
		return fmt.Errorf("invalid partition (%s) FsType value:\n%w", p.ID, err)
	}

	err = isGPTNameValid(p.Name)
	if err != nil {
		return err
	}

	if p.End != nil && p.Size != nil {
		return fmt.Errorf("cannot specify both End and Size on partition (%s)", p.ID)
	}

	if (p.End != nil && p.Start >= *p.End) || (p.Size != nil && *p.Size <= 0) {
		return fmt.Errorf("partition's (%s) size can't be 0 or negative", p.ID)
	}

	for _, f := range p.Flags {
		err := f.IsValid()
		if err != nil {
			return err
		}
	}

	isESP := sliceutils.ContainsValue(p.Flags, PartitionFlagESP)
	if isESP {
		if p.FsType != FileSystemTypeFat32 {
			return fmt.Errorf("ESP partition must have 'fat32' filesystem type")
		}
	}

	isBiosBoot := sliceutils.ContainsValue(p.Flags, PartitionFlagBiosGrub)
	if isBiosBoot {
		if p.Start != 1 {
			return fmt.Errorf("BIOS boot partition must start at block 1")
		}

		if p.FsType != FileSystemTypeFat32 {
			return fmt.Errorf("BIOS boot partition must have 'fat32' filesystem type")
		}
	}

	return nil
}

func (p *Partition) GetEnd() (uint64, bool) {
	if p.End != nil {
		return *p.End, true
	}

	if p.Size != nil {
		return p.Start + *p.Size, true
	}

	return 0, false
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
