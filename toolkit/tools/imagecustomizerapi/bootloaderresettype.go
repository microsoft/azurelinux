// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type ResetBootLoaderType string

const (
	ResetBootLoaderTypeDefault ResetBootLoaderType = ""
	ResetBootLoaderTypeHard    ResetBootLoaderType = "hard-reset"
)

func (t ResetBootLoaderType) IsValid() error {
	switch t {
	case ResetBootLoaderTypeDefault, ResetBootLoaderTypeHard:
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid resetBootLoaderType value (%v)", t)
	}
}
