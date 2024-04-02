// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type Verity struct {
	DataPartition VerityPartition `yaml:"DataPartition"`
	HashPartition VerityPartition `yaml:"HashPartition"`
}

func (v *Verity) IsValid() error {
	if err := v.DataPartition.IdType.IsValid(); err != nil {
		return fmt.Errorf("invalid DataPartition: %v", err)
	}

	if err := v.HashPartition.IdType.IsValid(); err != nil {
		return fmt.Errorf("invalid HashPartition: %v", err)
	}

	return nil
}
