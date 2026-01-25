// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type UkiKernels struct {
	Auto    bool     `yaml:"auto"`
	Kernels []string `yaml:"kernels"`
}

func (u UkiKernels) IsValid() error {
	if u.Auto && len(u.Kernels) > 0 {
		return fmt.Errorf("invalid uki kernels: kernels cannot be both 'auto' and a list of kernel names")
	}
	if !u.Auto && len(u.Kernels) == 0 {
		return fmt.Errorf("invalid uki kernels: kernels must be either 'auto' or a non-empty list of kernel names")
	}
	for _, kernel := range u.Kernels {
		if kernel == "" {
			return fmt.Errorf("invalid uki kernels: kernel names in the list cannot be empty")
		}
	}

	return nil
}
