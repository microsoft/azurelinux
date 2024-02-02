// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

// PartitionTableType is either gpt, mbr, or none
type PartitionTableType string

const (
	PartitionTableTypeGpt PartitionTableType = "gpt"
)

func (t PartitionTableType) IsValid() error {
	switch t {
	case PartitionTableTypeGpt:
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid partitionTableType value (%s)", t)
	}
}
