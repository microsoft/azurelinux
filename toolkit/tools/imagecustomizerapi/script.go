// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type Script struct {
	Path string `yaml:"path"`
	Args string `yaml:"args"`
}

func (s *Script) IsValid() error {
	if s.Path == "" {
		return fmt.Errorf("value of Path may not be empty")
	}

	return nil
}
