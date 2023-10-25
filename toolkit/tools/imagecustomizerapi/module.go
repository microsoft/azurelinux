// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
	"strings"
)

type ModuleOptions map[string]string

type Modules struct {
	Load    []string                 `yaml:"Load"`
	Disable []string                 `yaml:"Disable"`
	Options map[string]ModuleOptions `yaml:"Options"`
}

func (m *Modules) IsValid() error {
	for i, moduleName := range m.Load {
		if err := validateModuleName(moduleName, "Load", i); err != nil {
			return err
		}
	}

	for i, moduleName := range m.Disable {
		if err := validateModuleName(moduleName, "Disable", i); err != nil {
			return err
		}
	}
	for moduleName, moduleOptions := range m.Options {
		if moduleName == "" {
			return fmt.Errorf("module name cannot be empty in Modules.Options")
		}

		for optionKey, optionValue := range moduleOptions {
			if optionKey == "" || optionValue == "" {
				return fmt.Errorf("option key or value cannot be empty for module %s", moduleName)
			}

			if strings.ContainsAny(optionKey, " \n") || strings.ContainsAny(optionValue, " \n") {
				return fmt.Errorf("option key or value cannot contain spaces or newline characters for module %s", moduleName)
			}
		}
	}

	return nil
}

func validateModuleName(moduleName string, source string, index int) error {
	if moduleName == "" {
		return fmt.Errorf("module name cannot be empty in Modules.%s at index %d", source, index)
	}
	if strings.ContainsAny(moduleName, " \n") {
		return fmt.Errorf("module name cannot contain spaces or newline characters in Modules.%s at index %d", source, index)
	}
	return nil
}
