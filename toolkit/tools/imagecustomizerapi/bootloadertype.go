// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type BootLoaderType string

const (
	BootLoaderTypeDefault     BootLoaderType = ""
	BootLoaderTypeGrub2       BootLoaderType = "grub2"
	BootLoaderTypeSystemdBoot BootLoaderType = "systemd-boot"
)

func (b BootLoaderType) IsValid() error {
	switch b {
	case BootLoaderTypeDefault, BootLoaderTypeGrub2, BootLoaderTypeSystemdBoot:
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid type value (%v)", b)
	}
}
