// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

type KernelCommandLine struct {
	ExtraCommandLine string `yaml:"ExtraCommandLine"`
}

func (s *KernelCommandLine) IsValid() error {
	return nil
}
