// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

func serviceNameIsValid(name string) error {
	if name == "" {
		return fmt.Errorf("name of service may not be empty")
	}

	return nil
}

type Services struct {
	Enable  []string `yaml:"Enable"`
	Disable []string `yaml:"Disable"`
}

func (s *Services) IsValid() error {
	for i, service := range s.Enable {
		if err := serviceNameIsValid(service); err != nil {
			return fmt.Errorf("invalid service '%s' in Service.Enable at index %d: %w", service, i, err)
		}
	}

	for i, service := range s.Disable {
		if err := serviceNameIsValid(service); err != nil {
			return fmt.Errorf("invalid service '%s' in Service.Disable at index %d: %w", service, i, err)
		}
	}

	return nil
}
