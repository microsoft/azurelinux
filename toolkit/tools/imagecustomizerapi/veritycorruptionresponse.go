// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type VerityCorruptionResponse string

const (
	VerityCorruptionResponseIgnore  VerityCorruptionResponse = "ignore-corruption"
	VerityCorruptionResponseRestart VerityCorruptionResponse = "restart-on-corruption"
	VerityCorruptionResponsePanic   VerityCorruptionResponse = "panic-on-corruption"
	// Default response will only print an error to dmesg and will not prevent untrusted code from running.
	VerityCorruptionResponseDefault VerityCorruptionResponse = ""
)

func (v VerityCorruptionResponse) IsValid() error {
	switch v {
	case VerityCorruptionResponseIgnore, VerityCorruptionResponseRestart, VerityCorruptionResponsePanic, VerityCorruptionResponseDefault:
		return nil
	
	default:
		return fmt.Errorf("invalid VerityCorruptionResponse value (%v)", v)
	}
}
