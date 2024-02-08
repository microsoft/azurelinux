// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

// Iso defines how the generated iso media should be configured.
type Iso struct {
	AdditionalFiles AdditionalFilesMap `yaml:"AdditionalFiles"`
}

func (i *Iso) IsValid() error {
	err := i.AdditionalFiles.IsValid()
	if err != nil {
		return fmt.Errorf("invalid AdditionalFiles: %w", err)
	}
	return nil
}
