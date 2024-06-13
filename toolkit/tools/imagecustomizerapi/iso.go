// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

// Iso defines how the generated iso media should be configured.
type Iso struct {
	KernelCommandLine KernelCommandLine  `yaml:"kernelCommandLine"`
	AdditionalFiles   AdditionalFilesMap `yaml:"additionalFiles"`
}

func (i *Iso) IsValid() error {
	err := i.KernelCommandLine.IsValid()
	if err != nil {
		return fmt.Errorf("invalid kernelCommandLine: %w", err)
	}

	if i.AdditionalFiles != nil {
		err := i.AdditionalFiles.IsValid()
		if err != nil {
			return fmt.Errorf("invalid additionalFiles: %w", err)
		}
	}

	return nil
}
