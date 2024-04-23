// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type CorruptionOption string

const (
	CorruptionOptionIoError CorruptionOption = "io-error"
	CorruptionOptionIgnore  CorruptionOption = "ignore"
	CorruptionOptionPanic   CorruptionOption = "panic"
	CorruptionOptionRestart CorruptionOption = "restart"
)

func (c CorruptionOption) IsValid() error {
	switch c {
	case CorruptionOptionIoError, CorruptionOptionIgnore, CorruptionOptionPanic, CorruptionOptionRestart:
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid CorruptionOption value (%v)", c)
	}
}
