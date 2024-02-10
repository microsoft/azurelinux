// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

// Iso defines how the generated iso media should be configured.
type Iso struct {
	KernelExtraCommandLine KernelExtraParameters `yaml:"KernelExtraCommandLine"`
	AdditionalFiles        AdditionalFilesMap    `yaml:"AdditionalFiles"`
}

func (i *Iso) IsValid() error {
	var err error

	err = i.KernelExtraCommandLine.IsValid()
	if err != nil {
		return fmt.Errorf("invalid KernelExtraCommandLine: %w", err)
	}

	if i.AdditionalFiles != nil {
		err := i.AdditionalFiles.IsValid()
		if err != nil {
			return fmt.Errorf("invalid AdditionalFiles: %w", err)
		}
	}

	return nil
}
