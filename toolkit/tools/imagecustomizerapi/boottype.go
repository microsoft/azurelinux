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
	BootTypeUnset  BootType = ""
)

func (t BootType) IsValid() error {
	switch t {
	case BootTypeEfi, BootTypeLegacy, BootTypeUnset:
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid BootType value (%v)", t)
	}
}
