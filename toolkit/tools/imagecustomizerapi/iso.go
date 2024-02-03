// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

// Iso defines how the generated iso media should be configured.
type Iso struct {
	AdditionalFiles map[string]FileConfigList `yaml:"AdditionalFiles"`
}

func (s *Iso) IsValid() error {
	var err error

	for sourcePath, fileConfigList := range s.AdditionalFiles {
		err = fileConfigList.IsValid()
		if err != nil {
			return fmt.Errorf("invalid file configs for (%s):\n%w", sourcePath, err)
		}
	}

	return nil
}
