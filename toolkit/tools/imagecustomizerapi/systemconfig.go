// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

// SystemConfig defines how each system present on the image is supposed to be configured.
type SystemConfig struct {
	AdditionalFiles      map[string]FileConfigList `yaml:"AdditionalFiles"`
	PostInstallScripts   []Script                  `yaml:"PostInstallScripts"`
	FinalizeImageScripts []Script                  `yaml:"FinalizeImageScripts"`
}

func (s *SystemConfig) IsValid() error {
	var err error

	for sourcePath, fileConfigList := range s.AdditionalFiles {
		err = fileConfigList.IsValid()
		if err != nil {
			return fmt.Errorf("invalid file configs for (%s):\n%w", sourcePath, err)
		}
	}

	for i, script := range s.PostInstallScripts {
		err = script.IsValid()
		if err != nil {
			return fmt.Errorf("invalid PostInstallScripts item at index %d: %w", i, err)
		}
	}

	for i, script := range s.FinalizeImageScripts {
		err = script.IsValid()
		if err != nil {
			return fmt.Errorf("invalid FinalizeImageScripts item at index %d: %w", i, err)
		}
	}

	return nil
}
