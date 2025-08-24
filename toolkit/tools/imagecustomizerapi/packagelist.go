// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

type PackageList struct {
	Packages []string `yaml:"packages"`
}

func (s *PackageList) IsValid() error {
	return nil
}
