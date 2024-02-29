// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
	"unicode"
	"unicode/utf16"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
)

const (
	EFIPartitionType    = "efi"
	LegacyPartitionType = "legacy"
)

// Partition defines the size, name and file system type
// for a partition.
// "Start" and "End" fields define the offset from the beginning of the disk in MBs.
// An "End" value of 0 will determine the size of the partition using the next
// partition's start offset or the value defined by "MaxSize", if this is the last
// partition on the disk.
// "Grow" tells the logical volume to fill up any available space (**Only used for
// kickstart-style unattended installation**)
type Partition struct {
	FsType    string          `json:"FsType"`
	ID        string          `json:"ID"`
	Name      string          `json:"Name"`
	End       uint64          `json:"End"`
	Start     uint64          `json:"Start"`
	Flags     []PartitionFlag `json:"Flags"`
	Artifacts []Artifact      `json:"Artifacts"`
}

// HasFlag returns true if a given partition has a specific flag set.
func (p *Partition) HasFlag(flag PartitionFlag) bool {
	for _, f := range p.Flags {
		if f == flag {
			return true
		}
	}
	return false
}

// nameCheck makes sure the Name can fit in the alloted space in the GPT, and since parted works best with ASCII we check
// for any non-ASCII characters
// header (72 bytes of UTF-16)
func nameCheck(name string) (err error) {
	const maxLength = 36

	encodedString := utf16.Encode([]rune(name))
	stringLengthWithNull := len(encodedString) + 1

	for pos, char := range name {
		if char > unicode.MaxASCII {
			return fmt.Errorf("[Name] (%s) contains a non-ASCII character '%c' at position (%d)", name, char, pos)
		}
	}

	if stringLengthWithNull > maxLength {
		return fmt.Errorf("[Name] is too long, GPT header can hold only 72 bytes of UTF-16 (35 normal characters + null) while (%s) needs %d bytes", name, stringLengthWithNull*2)
	}
	return
}

// IsValid returns an error if the Partition is not valid
func (p *Partition) IsValid() (err error) {
	for _, f := range p.Flags {
		if err = f.IsValid(); err != nil {
			return
		}
	}

	err = nameCheck(p.Name)
	if err != nil {
		return err
	}

	return nil
}

// UnmarshalJSON Unmarshals a Partition entry
func (p *Partition) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypePartition Partition
	err = json.Unmarshal(b, (*IntermediateTypePartition)(p))
	if err != nil {
		return fmt.Errorf("failed to parse [Partition]: %w", err)
	}

	// Now validate the resulting unmarshaled object
	err = p.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [Partition]: %w", err)
	}
	return
}

// SystemBootType returns the current boot type of the system being ran on.
func SystemBootType() (bootType string) {
	// If a system booted with EFI, /sys/firmware/efi will exist
	const efiFirmwarePath = "/sys/firmware/efi"

	exist, _ := file.DirExists(efiFirmwarePath)
	if exist {
		bootType = EFIPartitionType
	} else {
		bootType = LegacyPartitionType
	}

	return
}

// BootPartitionConfig returns the partition flags and mount point that should be used
// for a given boot type.
func BootPartitionConfig(bootType string, partitionTableType PartitionTableType) (mountPoint, mountOptions string, flags []PartitionFlag, err error) {
	switch bootType {
	case EFIPartitionType:
		flags = []PartitionFlag{PartitionFlagESP, PartitionFlagBoot}
		mountPoint = "/boot/efi"
		mountOptions = "umask=0077,nodev"
	case LegacyPartitionType:
		if partitionTableType == PartitionTableTypeGpt {
			flags = []PartitionFlag{PartitionFlagGrub}
		} else if partitionTableType == PartitionTableTypeMbr {
			flags = []PartitionFlag{PartitionFlagBoot}
		} else {
			err = fmt.Errorf("unknown partition table type (%s)", partitionTableType)
		}

		mountPoint = ""
		mountOptions = ""
	default:
		err = fmt.Errorf("unknown boot type (%s)", bootType)
	}

	return
}
