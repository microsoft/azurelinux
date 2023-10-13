// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type Modules struct {
	Load   []Module `yaml:"Load"`
	Unload []Module `yaml:"Unload"`
}

type Module struct {
	Name string `yaml:"Name"`
}

func (m *Module) IsValid() error {
	if m.Name == "" {
		return fmt.Errorf("name of module may not be empty")
	}

	return nil
}

func (m *Modules) IsValid() error {
	for i, module := range m.Load {
		if err := module.IsValid(); err != nil {
			return fmt.Errorf("invalid Modules.Load item at index %d: %w", i, err)
		}
	}

	for i, module := range m.Unload {
		if err := module.IsValid(); err != nil {
			return fmt.Errorf("invalid Modules.Unload item at index %d: %w", i, err)
		}
	}

	return nil
}
