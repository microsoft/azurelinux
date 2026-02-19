// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type Uki struct {
	Kernels UkiKernels `yaml:"kernels"`
}

func (u Uki) IsValid() error {
	err := u.Kernels.IsValid()
	if err != nil {
		return fmt.Errorf("invalid uki kernels: %w", err)
	}

	return nil
}
