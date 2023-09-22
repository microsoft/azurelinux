// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

// SystemConfig defines how each system present on the image is supposed to be configured.
type SystemConfig struct {
	AdditionalFiles map[string]FileConfigList `yaml:"AdditionalFiles"`
}

func (s *SystemConfig) IsValid() error {
	var err error

	for sourcePath, fileConfigList := range s.AdditionalFiles {
		err = fileConfigList.IsValid()
		if err != nil {
			return fmt.Errorf("invalid file configs for (%s): %w", sourcePath, err)
		}
	}

	return nil
}
