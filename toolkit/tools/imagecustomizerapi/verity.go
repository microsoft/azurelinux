// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type VerityPartition struct {
	IdType IdType `yaml:"IdType"`
	Id     string `yaml:"Id"`
}

type Verity struct {
	DataPartition VerityPartition `yaml:"DataPartition"`
	HashPartition VerityPartition `yaml:"HashPartition"`
}

func (v *Verity) IsSet() bool {
	return v.DataPartition != VerityPartition{} ||
		v.HashPartition != VerityPartition{}
}

func (v *Verity) IsValid() error {
	if err := v.DataPartition.IdType.IsValid(); err != nil || v.DataPartition.Id == "" {
		return fmt.Errorf("invalid DataPartition: %v", err)
	}

	if err := v.HashPartition.IdType.IsValid(); err != nil || v.HashPartition.Id == "" {
		return fmt.Errorf("invalid HashPartition: %v", err)
	}

	return nil
}
