// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
	"strings"
)

type ModuleOptions map[string]string
type LoadMode string

const (
	LoadModeAlways  LoadMode = "always"
	LoadModeAuto    LoadMode = "auto"
	LoadModeDisable LoadMode = "disable"
	LoadModeInherit LoadMode = "inherit"
)

type Module struct {
	Name     string            `yaml:"name"`
	LoadMode LoadMode          `yaml:"loadMode"`
	Options  map[string]string `yaml:"options"`
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

func validateModuleLoadMode(loadmode LoadMode) error {
	switch loadmode {
	case LoadModeAuto, LoadModeDisable, LoadModeAlways, LoadModeInherit, "":
		// All good.
		return nil

	default:
		return fmt.Errorf("invalid module load mode value (%v), it can only be 'always', 'auto', 'disable','inherit' or ''", loadmode)
	}
}
