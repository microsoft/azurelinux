// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type Services struct {
	Enable  []Service `yaml:"Enable"`
	Disable []Service `yaml:"Disable"`
}

type Service struct {
	Name string `yaml:"Name"`
}

func (s *Service) IsValid() error {
	if s.Name == "" {
		return fmt.Errorf("name of service may not be empty")
	}

	return nil
}
