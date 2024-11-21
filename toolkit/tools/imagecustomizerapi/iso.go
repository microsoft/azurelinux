// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

// Iso defines how the generated iso media should be configured.
type Iso struct {
	KernelCommandLine KernelCommandLine  `yaml:"KernelCommandLine"`
	AdditionalFiles   AdditionalFilesMap `yaml:"AdditionalFiles"`
}

func (i *Iso) IsValid() error {
	var err error

	err = i.KernelCommandLine.IsValid()
	if err != nil {
		return fmt.Errorf("invalid KernelCommandLine: %w", err)
	}

	if i.AdditionalFiles != nil {
		err := i.AdditionalFiles.IsValid()
		if err != nil {
			return fmt.Errorf("invalid AdditionalFiles: %w", err)
		}
	}

	return nil
}
