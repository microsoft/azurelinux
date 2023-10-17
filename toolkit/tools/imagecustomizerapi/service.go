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

func (s *Services) IsValid() error {
	for i, service := range s.Enable {
		if err := service.IsValid(); err != nil {
			return fmt.Errorf("invalid Service.Enable item at index %d: %w", i, err)
		}
	}

	for i, service := range s.Disable {
		if err := service.IsValid(); err != nil {
			return fmt.Errorf("invalid Service.Disable item at index %d: %w", i, err)
		}
	}

	return nil
}
