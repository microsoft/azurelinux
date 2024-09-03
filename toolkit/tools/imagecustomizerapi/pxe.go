// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

// Iso defines how the generated iso media should be configured.
type Pxe struct {
	IsoImageUrl string `yaml:"isoImageUrl"`
}

func (i *Pxe) IsValid() error {
	return nil
}
