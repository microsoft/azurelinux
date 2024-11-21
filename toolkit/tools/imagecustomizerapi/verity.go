// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type Verity struct {
	DataPartition IdentifiedPartition `yaml:"DataPartition"`
	HashPartition IdentifiedPartition `yaml:"HashPartition"`
}

func (v *Verity) IsValid() error {
	if err := v.DataPartition.IsValid(); err != nil {
		return fmt.Errorf("invalid DataPartition: %v", err)
	}

	if err := v.HashPartition.IsValid(); err != nil {
		return fmt.Errorf("invalid HashPartition: %v", err)
	}

	return nil
}
