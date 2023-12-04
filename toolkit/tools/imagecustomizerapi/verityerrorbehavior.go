// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type VerityErrorBehavior string

const (
	VerityErrorBehaviorIgnore  VerityErrorBehavior = "ignore-corruption"
	VerityErrorBehaviorPanic   VerityErrorBehavior = "panic-on-corruption"
	VerityErrorBehaviorRestart VerityErrorBehavior = "restart-on-corruption"
	// Default response will only print an error to dmesg and will not prevent untrusted code from running.
	VerityErrorBehaviorDefault VerityErrorBehavior = ""
)

func (v VerityErrorBehavior) IsValid() error {
	switch v {
	case VerityErrorBehaviorIgnore, VerityErrorBehaviorRestart, VerityErrorBehaviorPanic, VerityErrorBehaviorDefault:
		return nil
	
	default:
		return fmt.Errorf("invalid VerityErrorBehavior value (%v)", v)
	}
}
