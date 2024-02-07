// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

// Iso defines how the generated iso media should be configured.
type Iso struct {
	AdditionalFiles AdditionalFilesMap `yaml:"AdditionalFiles"`
}

func (i *Iso) IsValid() error {
	return i.AdditionalFiles.IsValid()
}
