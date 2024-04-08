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

	match := diskSizeRegex.FindStringSubmatch(stringValue)
	if match == nil {
		return fmt.Errorf("disk size (%s) has incorrect format: <num>[KMGT] (e.g. 100M, 1G)", stringValue)
	}

	numString := match[1]
	num, err := strconv.ParseUint(numString, 0, 64)
	if err != nil {
		return fmt.Errorf("failed to parse disk size:\n%w", err)
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
			return fmt.Errorf("disk size (%s) must have a suffix (i.e. K, M, G, or T)", numString)
		}

		num *= multiplier
	}

	// The imager's diskutils works in MiB. So, restrict disk and partition sizes to multiples of 1 MiB.
	if num%diskutils.MiB != 0 {
		return fmt.Errorf("disk size (%d) must be a multiple of 1 MiB", num)
	}

	*s = DiskSize(num)
	return nil
}
