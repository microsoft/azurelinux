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

type ModuleList struct {
	Modules []Module `yaml:"modules"`
}

func (m *ModuleList) IsValid() error {
	moduleMap := make(map[string]int)
	for i, module := range m.Modules {
		// Check if module is duplicated to avoid conflicts with modules potentially having different LoadMode
		if _, exists := moduleMap[module.Name]; exists {
			return fmt.Errorf("duplicate module found: %s at index %d", module.Name, i)
		}
		moduleMap[module.Name] = i
		err := module.IsValid()
		if err != nil {
			return fmt.Errorf("invalid modules item at index %d:\n%w", i, err)
		}
	}

	return nil
}

func (m *Module) IsValid() error {
	if err := validateModuleName(m.Name); err != nil {
		return err
	}

	if err := m.LoadMode.IsValid(); err != nil {
		return fmt.Errorf("invalid module (%s):\n%w", m.Name, err)
	}

	for optionKey, optionValue := range m.Options {
		if optionKey == "" {
			return fmt.Errorf("invalid module (%s):\noption key cannot be empty", m.Name)
		}
		if optionValue == "" {
			return fmt.Errorf("invalid module (%s):\noption value cannot be empty", m.Name)
		}

		if strings.ContainsAny(optionKey, " \n") {
			return fmt.Errorf("invalid module (%s):\noption key (%s) cannot contain spaces or newline characters", m.Name, optionKey)
		}
		if strings.ContainsAny(optionValue, " \n") {
			return fmt.Errorf("invalid module (%s):\noption value (%s) cannot contain spaces or newline characters", m.Name, optionValue)
		}
	}
	return nil
}

func validateModuleName(moduleName string) error {
	if moduleName == "" {
		return fmt.Errorf("module name cannot be empty")
	}
	if strings.ContainsAny(moduleName, " \n") {
		return fmt.Errorf("module name (%s) cannot contain spaces or newline characters", moduleName)
	}
	return nil
}
