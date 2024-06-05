//go:build prod

// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

func (t PasswordType) IsValid() error {
	switch t {
	case PasswordTypeLocked:
		// All good.
		return nil

	case PasswordTypePlainText, PasswordTypeHashed, PasswordTypePlainTextFile, PasswordTypeHashedFile:
		return fmt.Errorf("password type (%s) only supported in dev builds", t)

	default:
		return fmt.Errorf("invalid password type (%s)", t)
	}
}
