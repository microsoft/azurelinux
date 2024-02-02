// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type Verity struct {
	DataPartition VerityPartition `yaml:"dataPartition"`
	HashPartition VerityPartition `yaml:"hashPartition"`
}

func (v *Verity) IsValid() error {
	if err := v.DataPartition.IdType.IsValid(); err != nil {
		return fmt.Errorf("invalid dataPartition: %v", err)
	}

	if err := v.HashPartition.IdType.IsValid(); err != nil {
		return fmt.Errorf("invalid hashPartition: %v", err)
	}

	return nil
}
