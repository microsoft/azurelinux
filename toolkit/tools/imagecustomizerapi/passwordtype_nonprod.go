//go:build !prod

// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

func (t PasswordType) IsValid() error {
	switch t {
	case PasswordTypeLocked, PasswordTypePlainText, PasswordTypeHashed, PasswordTypePlainTextFile,
		PasswordTypeHashedFile:
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid password type (%s)", t)
	}
}
