// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type OverlayFS struct {
	LowerDir            string           `yaml:"LowerDir"`
	UpperDir            string           `yaml:"UpperDir"`
	WorkDir             string           `yaml:"WorkDir"`
	PersistentPartition *VerityPartition `yaml:"PersistentPartition"`
}

func (o *OverlayFS) IsValid() error {
	if o.LowerDir == "" {
		return fmt.Errorf("value of LowerDir may not be empty")
	}

	if o.UpperDir == "" {
		return fmt.Errorf("value of UpperDir may not be empty")
	}

	if o.WorkDir == "" {
		return fmt.Errorf("value of WorkDir may not be empty")
	}

	if o.PersistentPartition != nil {
		if err := o.PersistentPartition.IsValid(); err != nil {
			return fmt.Errorf("invalid PersistentPartition: %v", err)
		}
	}

	return nil
}
