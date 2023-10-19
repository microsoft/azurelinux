// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type Module struct {
	Name    string            `yaml:"Name"`
	Options map[string]string `yaml:"Options,omitempty"`
}

func (m *Module) IsValid() error {
	if m.Name == "" {
		return fmt.Errorf("name of module may not be empty")
	}

	if len(m.Options) == 0 {
		for key, value := range m.Options {
			if key == "" || value == "" {
				return fmt.Errorf("invalid key:value pair in options")
			}
		}
	}

	return nil
}

type Modules struct {
	Load    []Module `yaml:"Load"`
	Disable []Module `yaml:"Disable"`
}

func (m *Modules) IsValid() error {
	for i, module := range m.Load {
		if err := module.IsValid(); err != nil {
			return fmt.Errorf("invalid module '%s' in Modules.Load at index %d: %w", module.Name, i, err)
		}
	}

	for i, module := range m.Disable {
		if err := module.IsValid(); err != nil {
			return fmt.Errorf("invalid module '%s' in Modules.Disable at index %d: %w", module.Name, i, err)
		}
	}

	return nil
}
