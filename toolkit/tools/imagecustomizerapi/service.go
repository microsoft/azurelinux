// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type Service struct {
	Name string `yaml:"Name"`
}

func (s *Service) IsValid() error {
	if s.Name == "" {
		return fmt.Errorf("name of service may not be empty")
	}

	return nil
}

type Services struct {
	Enable  []Service `yaml:"Enable"`
	Disable []Service `yaml:"Disable"`
}

func (s *Services) IsValid() error {
	for i, service := range s.Enable {
		if err := service.IsValid(); err != nil {
			return fmt.Errorf("invalid service '%s' in Service.Enable at index %d: %w", service.Name, i, err)
		}
	}

	for i, service := range s.Disable {
		if err := service.IsValid(); err != nil {
			return fmt.Errorf("invalid service '%s' in Service.Disable at index %d: %w", service.Name, i, err)
		}
	}

	return nil
}
