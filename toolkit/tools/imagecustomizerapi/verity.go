// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type Verity struct {
	DataPartition    IdentifiedPartition `yaml:"dataPartition"`
	HashPartition    IdentifiedPartition `yaml:"hashPartition"`
	CorruptionOption CorruptionOption    `yaml:"corruptionOption"`
}

func (v *Verity) IsValid() error {
	if err := v.DataPartition.IsValid(); err != nil {
		return fmt.Errorf("invalid dataPartition: %v", err)
	}

	if err := v.HashPartition.IsValid(); err != nil {
		return fmt.Errorf("invalid hashPartition: %v", err)
	}

	if err := v.CorruptionOption.IsValid(); err != nil {
		return fmt.Errorf("invalid corruptionOption: %v", err)
	}

	return nil
}
