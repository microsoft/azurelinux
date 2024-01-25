// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type Module struct {
	Name string `yaml:"name"`
}

func (m *Module) IsValid() error {
	if m.Name == "" {
		return fmt.Errorf("name of module may not be empty")
	}

	return nil
}

type Modules struct {
	Load    []Module `yaml:"load"`
	Disable []Module `yaml:"disable"`
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
