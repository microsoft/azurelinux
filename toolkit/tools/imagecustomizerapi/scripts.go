// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type Scripts struct {
	PostCustomization     []Script `yaml:"postCustomization"`
	FinalizeCustomization []Script `yaml:"finalizeCustomization"`
}

func (s *Scripts) IsValid() error {
	for i, script := range s.PostCustomization {
		err := script.IsValid()
		if err != nil {
			return fmt.Errorf("invalid postCustomization script at index %d:\n%w", i, err)
		}
	}

	for i, script := range s.FinalizeCustomization {
		err := script.IsValid()
		if err != nil {
			return fmt.Errorf("invalid finalizeCustomization script at index %d:\n%w", i, err)
		}
	}

	return nil
}
