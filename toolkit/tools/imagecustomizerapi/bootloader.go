// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type BootLoader struct {
	Type  BootLoaderType      `yaml:"type"`
	Reset ResetBootLoaderType `yaml:"reset"`
}

func (b BootLoader) IsValid() error {
	err := b.Type.IsValid() 
	if err != nil {
		return fmt.Errorf("invalid 'type' field in BootLoader: %w", err)
	}

	err = b.Reset.IsValid()
	if err != nil {
		return fmt.Errorf("invalid 'reset' field in BootLoader: %w", err)
	}

	// Temporary limitation: 'os.bootloader.reset' must currently be set to 'hard-reset' when 'os.bootloader.type' is 'systemd-boot'.
	// In the future, this hard-reset requirement may be removed as we continue to design and improve the bootloader functionality.
	if b.Type == BootLoaderTypeSystemdBoot && b.Reset != ResetBootLoaderTypeHard {
		return fmt.Errorf("'reset' must be 'hard-reset' when 'type' is 'systemd-boot'")
	}

	return nil
}
