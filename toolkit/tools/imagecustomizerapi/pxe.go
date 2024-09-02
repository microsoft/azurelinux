// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

// Iso defines how the generated iso media should be configured.
type Pxe struct {
	IsoUrl string `yaml:"isoUrl"`
}

func (i *Pxe) IsValid() error {
	return nil
}
