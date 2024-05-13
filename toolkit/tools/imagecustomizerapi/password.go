// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type Password struct {
	// The way the password is provided.
	Type PasswordType `yaml:"type"`
	// The value of the password.
	Value string `yaml:"value"`
}

func (p *Password) IsValid() error {
	err := p.Type.IsValid()
	if err != nil {
		return err
	}

	switch p.Type {
	case PasswordTypeLocked:
		if p.Value != "" {
			return fmt.Errorf("password value must be empty with type (%s)", p.Type)
		}

	case PasswordTypePlainText, PasswordTypeHashed, PasswordTypePlainTextFile, PasswordTypeHashedFile:
		if p.Value == "" {
			return fmt.Errorf("password value can't be empty with type (%s)", p.Type)
		}
	}

	return nil
}
