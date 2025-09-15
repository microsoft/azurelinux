// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type ModuleLoadMode string

const (
	ModuleLoadModeAlways  ModuleLoadMode = "always"
	ModuleLoadModeAuto    ModuleLoadMode = "auto"
	ModuleLoadModeDisable ModuleLoadMode = "disable"
	ModuleLoadModeInherit ModuleLoadMode = "inherit"
	ModuleLoadModeDefault ModuleLoadMode = ""
)

func (loadmode ModuleLoadMode) IsValid() error {
	switch loadmode {
	case ModuleLoadModeAlways, ModuleLoadModeAuto, ModuleLoadModeDisable, ModuleLoadModeInherit, ModuleLoadModeDefault:
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid module load mode value (%s):\nvalid values: 'always', 'auto', 'disable', 'inherit', or ''", loadmode)
	}
}
