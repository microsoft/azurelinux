// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
	"strings"
)

type Module struct {
	Name     string            `yaml:"name"`
	LoadMode ModuleLoadMode    `yaml:"loadMode"`
	Options  map[string]string `yaml:"options"`
}

func (m *Module) IsValid() error {
	if err := validateModuleName(m.Name); err != nil {
		return err
	}

	if err := m.LoadMode.IsValid(); err != nil {
		return err
	}

	for optionKey, optionValue := range m.Options {
		if optionKey == "" {
			return fmt.Errorf("option key cannot be empty for module %s", m.Name)
		}
		if optionValue == "" {
			return fmt.Errorf("option value cannot be empty for module %s", m.Name)
		}

		if strings.ContainsAny(optionKey, " \n") {
			return fmt.Errorf("option key cannot contain spaces or newline characters for module %s", m.Name)
		}
		if strings.ContainsAny(optionValue, " \n") {
			return fmt.Errorf("option value cannot contain spaces or newline characters for module %s", m.Name)
		}
	}
	return nil
}

func validateModuleName(moduleName string) error {
	if moduleName == "" {
		return fmt.Errorf("module name cannot be empty")
	}
	if strings.ContainsAny(moduleName, " \n") {
		return fmt.Errorf("module name cannot contain spaces or newline characters")
	}
	return nil
}
