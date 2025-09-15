// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"

	"gopkg.in/yaml.v3"
)

const (
	PartitionSizeGrow = "grow"
)

type PartitionSizeType int

const (
	PartitionSizeTypeUnset PartitionSizeType = iota
	PartitionSizeTypeGrow
	PartitionSizeTypeExplicit
)

type PartitionSize struct {
	Type PartitionSizeType
	Size DiskSize
}

func (s *PartitionSize) IsValid() error {
	return nil
}

func (s *PartitionSize) UnmarshalYAML(value *yaml.Node) error {
	var err error

	var stringValue string
	err = value.Decode(&stringValue)
	if err != nil {
		return fmt.Errorf("failed to parse partition size:\n%w", err)
	}

	switch stringValue {
	case PartitionSizeGrow:
		*s = PartitionSize{
			Type: PartitionSizeTypeGrow,
		}
		return nil
	}

	diskSize, err := parseDiskSize(stringValue)
	if err != nil {
		return fmt.Errorf("%w:\nexpected format: grow | <NUM>(K|M|G|T) (e.g. grow, 100M, 1G)", err)
	}

	*s = PartitionSize{
		Type: PartitionSizeTypeExplicit,
		Size: diskSize,
	}
	return nil
}
