// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type ModuleLoadMode string

const (
	LoadModeAlways  ModuleLoadMode = "always"
	LoadModeAuto    ModuleLoadMode = "auto"
	LoadModeDisable ModuleLoadMode = "disable"
	LoadModeInherit ModuleLoadMode = "inherit"
	LoadModeDefault ModuleLoadMode = ""
)

func (loadmode ModuleLoadMode) IsValid() error {
	switch loadmode {
	case LoadModeAuto, LoadModeDisable, LoadModeAlways, LoadModeInherit, LoadModeDefault:
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid module load mode value (%v), it can only be 'always', 'auto', 'disable','inherit' or ''", loadmode)
	}
}
