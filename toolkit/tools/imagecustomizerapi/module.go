// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
	"strings"
)

type ModuleOptions map[string]string

type Module struct {
    Name     string            `yaml:"Name"`
    LoadMode string            `yaml:"LoadMode"`
    Options  map[string]string `yaml:"Options"`
}

func (m *Module) IsValid() error {
	if err := validateModuleName(m.Name); err != nil {
		return err
	}

	if err := validateModuleLoadMode(m.LoadMode); err != nil {
		return err
	}

	if len(m.Options) > 0 {
		for optionKey, optionValue := range m.Options {
			if optionKey == "" || optionValue == "" {
				return fmt.Errorf("option key or value cannot be empty for module %s", m.Name)
			}

			if strings.ContainsAny(optionKey, " \n") || strings.ContainsAny(optionValue, " \n") {
				return fmt.Errorf("option key or value cannot contain spaces or newline characters for module %s", m.Name)
			}
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

func validateModuleLoadMode(loadMode string) error {
    validLoadModes := []string{"always", "boot", "disable", "auto"}
    isValid := false
    for _, v := range validLoadModes {
        if loadMode == v {
            isValid = true
            break
        }
    }
    if !isValid {
        return fmt.Errorf("invalid module load mode '%s'; it can only be 'always', 'boot', 'disable', or 'auto'", loadMode)
    }
    return nil
}
