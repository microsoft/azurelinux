// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type BootType string

const (
	BootTypeEfi    BootType = "efi"
	BootTypeLegacy BootType = "legacy"
)

func (t BootType) IsValid() error {
	switch t {
	case BootTypeEfi, BootTypeLegacy:
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid bootType value (%v)", t)
	}
}
