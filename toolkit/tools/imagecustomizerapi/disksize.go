// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
	"regexp"
	"strconv"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"gopkg.in/yaml.v3"
)

var (
	diskSizeRegex = regexp.MustCompile(`^(\d+)([KMGT])?$`)
)

type DiskSize uint64

func (s *DiskSize) IsValid() error {
	return nil
}

func (s *DiskSize) UnmarshalYAML(value *yaml.Node) error {
	var err error

	var stringValue string
	err = value.Decode(&stringValue)
	if err != nil {
		return fmt.Errorf("failed to parse disk size:\n%w", err)
	}

	diskSize, err := parseDiskSize(stringValue)
	if err != nil {
		return fmt.Errorf("%w:\nexpected format: <NUM>(K|M|G|T) (e.g. 100M, 1G)", err)
	}

	*s = diskSize
	return nil
}

func (s DiskSize) HumanReadable() string {
	switch {
	case s%diskutils.TiB == 0:
		return fmt.Sprintf("%d TiB", s/diskutils.TiB)

	case s%diskutils.GiB == 0:
		return fmt.Sprintf("%d GiB", s/diskutils.GiB)

	case s%diskutils.MiB == 0:
		return fmt.Sprintf("%d MiB", s/diskutils.MiB)

	case s%diskutils.KiB == 0:
		return fmt.Sprintf("%d KiB", s/diskutils.KiB)

	default:
		return fmt.Sprintf("%d bytes", s)
	}
}

func parseDiskSize(diskSizeString string) (DiskSize, error) {
	match := diskSizeRegex.FindStringSubmatch(diskSizeString)
	if match == nil {
		return 0, fmt.Errorf("(%s) has incorrect format", diskSizeString)
	}

	numString := match[1]
	num, err := strconv.ParseUint(numString, 0, 64)
	if err != nil {
		return 0, err
	}

	if len(match) >= 3 {
		unit := match[2]
		multiplier := uint64(1)
		switch unit {
		case "K":
			multiplier = diskutils.KiB
		case "M":
			multiplier = diskutils.MiB
		case "G":
			multiplier = diskutils.GiB
		case "T":
			multiplier = diskutils.TiB
		case "":
			return 0, fmt.Errorf("(%s) must have a unit suffix (K, M, G, or T)", diskSizeString)
		}

		num *= multiplier
	}

	// The imager's diskutils works in MiB. So, restrict disk and partition sizes to multiples of 1 MiB.
	if num%DefaultPartitionAlignment != 0 {
		return 0, fmt.Errorf("(%s) must be a multiple of %s", diskSizeString,
			DiskSize(DefaultPartitionAlignment).HumanReadable())
	}

	return DiskSize(num), nil
}
