// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
)

type LoadMode string

const (
	LoadModeBoot    LoadMode = "boot"
	LoadModeAuto    LoadMode = "auto"
	LoadModeDisable LoadMode = "disable"
	LoadModeInherit LoadMode = "inherit"
)

func loadOrDisableModules(modules []imagecustomizerapi.Module, imageChroot *safechroot.Chroot) error {
	var err error
	var modulesToLoad []string
	var modulesToDisable []string
	var moduleOptionsUpdates map[string]map[string]string = make(map[string]map[string]string)
	moduleMap := make(map[string]int)
	moduleDisableFilePath := filepath.Join(imageChroot.RootDir(), "/etc/modprobe.d/modules-disabled.conf")
	moduleLoadFilePath := filepath.Join(imageChroot.RootDir(), "/etc/modules-load.d/modules-load.conf")
	moduleOptionsFilePath := filepath.Join(imageChroot.RootDir(), "/etc/modprobe.d/module-options.conf")

	for i, module := range modules {
		// Check if module is duplicated to avoid conflicts with modules potentially having different LoadMode
		if _, exists := moduleMap[module.Name]; exists {
			return fmt.Errorf("duplicate module found: %s at index %d", module.Name, i)
		}
		moduleMap[module.Name] = i

		switch module.LoadMode {
		case imagecustomizerapi.LoadModeAlways:
			// If a module is disabled, remove it. Add the module to modules-load.d/. Write options if provided.
			err = removeModuleFromDisableList(module.Name, moduleDisableFilePath)
			if err != nil {
				logger.Log.Infof("Error removing module %s from the disabled list", module.Name)
				return err
			}
			modulesToLoad = append(modulesToLoad, module.Name)

			if len(module.Options) > 0 {
				moduleOptionsUpdates[module.Name] = module.Options
			}

		case imagecustomizerapi.LoadModeAuto:
			// If a module is disabled, enable it. Write options if provided
			err = removeModuleFromDisableList(module.Name, moduleDisableFilePath)
			if err != nil {
				logger.Log.Infof("Error removing module %s from the disabled list", module.Name)
				return err
			}

			if len(module.Options) > 0 {
				moduleOptionsUpdates[module.Name] = module.Options
			}

		case imagecustomizerapi.LoadModeDisable:
			// Disable a module, throw error if options are provided
			if len(module.Options) > 0 {
				return fmt.Errorf("cannot add options for disabled module %s at index %d. Specify auto or always as loadMode to override setting in base image", module.Name, i)
			}

			modulesToDisable = append(modulesToDisable, module.Name)

		case imagecustomizerapi.LoadModeInherit, "":
			// inherits the behavior of the base image, modify the options without changing the loading state
			if len(module.Options) > 0 {
				disabled, err := isModuleDisabled(module.Name, moduleDisableFilePath)
				if err != nil {
					logger.Log.Infof("Error checking %s", moduleDisableFilePath)
					return err
				}

				if disabled {
					return fmt.Errorf("cannot add options for disabled module %s at index %d. Specify auto or always as loadMode to override setting in base image", module.Name, i)
				}

				if len(module.Options) > 0 {
					moduleOptionsUpdates[module.Name] = module.Options
				}
			}
		}
	}

	// Batch process module to load
	err = ensureModulesLoaded(modulesToLoad, moduleLoadFilePath)
	if err != nil {
		return err
	}

	// Batch process module to disable
	err = ensureModulesDisabled(modulesToDisable, moduleLoadFilePath)
	if err != nil {
		return err
	}

	// Batch process module options
	err = updateModulesOptions(moduleOptionsUpdates, moduleOptionsFilePath)
	if err != nil {
		return err
	}

	return nil
}

func ensureModulesLoaded(moduleNames []string, moduleLoadFilePath string) error {
	content, err := os.ReadFile(moduleLoadFilePath)
	if err != nil {
		if !os.IsNotExist(err) {
			return fmt.Errorf("failed to read module load configuration: %w", err)
		}
		// If the file does not exist, initialize content as empty
		content = []byte{}
	}

	needUpdate := false

	for _, moduleName := range moduleNames {
		if !strings.Contains(string(content), moduleName+"\n") {
			content = append(content, (moduleName + "\n")...)
			needUpdate = true
			logger.Log.Infof("Loading module %s", moduleName)
		} else {
			logger.Log.Infof("Module %s is already loaded", moduleName)
		}
	}

	if needUpdate {
		err = os.WriteFile(moduleLoadFilePath, content, 0644)
		if err != nil {
			return fmt.Errorf("failed to update module load configuration: %w", err)
		}
	}
	return nil
}

func ensureModulesDisabled(moduleNames []string, moduleDisableFilePath string) error {
	content, err := os.ReadFile(moduleDisableFilePath)
	if err != nil && !os.IsNotExist(err) {
		return fmt.Errorf("failed to read disable configuration: %w", err)
	}

	contentString := string(content)
	updatedContent := contentString
	needUpdate := false

	for _, moduleName := range moduleNames {
		blacklistEntry := "blacklist " + moduleName
		if !strings.Contains(contentString, blacklistEntry+"\n") {
			// Append the module to be disabled if it's not already in the file
			updatedContent += blacklistEntry + "\n"
			needUpdate = true
			logger.Log.Infof("Disabling module %s", moduleName)
		}
	}

	if needUpdate {
		err = os.WriteFile(moduleDisableFilePath, []byte(updatedContent), 0644)
		if err != nil {
			return fmt.Errorf("failed to update disable configuration: %w", err)
		}
	}

	return nil
}

func isModuleDisabled(moduleName, moduleDisableFilePath string) (bool, error) {
	_, err := os.Stat(moduleDisableFilePath)
	if os.IsNotExist(err) {
		// File doesn't exist, treat as not disabled.
		return false, nil
	} else if err != nil {
		return false, err
	}

	content, err := os.ReadFile(moduleDisableFilePath)
	if err != nil {
		logger.Log.Errorf("Failed to scan file %s with error %s", moduleDisableFilePath, err)
		return false, err
	}

	if strings.Contains(string(content), moduleName) {
		return true, nil
	}

	return false, nil
}

func removeModuleFromDisableList(moduleName, moduleDisableFilePath string) error {
	disabled, err := isModuleDisabled(moduleName, moduleDisableFilePath)
	if err != nil {
		logger.Log.Infof("Error checking %s", moduleDisableFilePath)
		return err
	}

	if disabled {
		logger.Log.Infof("Module %s found in the disabled list. Removing...", moduleName)
		lines, err := os.ReadFile(moduleDisableFilePath)
		if err != nil {
			return fmt.Errorf("failed to write module disable configuration: %w", err)
		}

		// Filter out the line that contains the module name.
		var updatedLines []string
		for _, line := range strings.Split(string(lines), "\n") {
			if !strings.Contains(line, moduleName) {
				updatedLines = append(updatedLines, line)
			}
		}

		return os.WriteFile(moduleDisableFilePath, []byte(strings.Join(updatedLines, "\n")), 0644)
	}

	return nil
}

func updateModulesOptions(moduleOptionsUpdates map[string]map[string]string, moduleOptionsFilePath string) error {
	aggregatedOptions := []string{}
	var err error

	if len(moduleOptionsUpdates) > 0 {
		for moduleName, options := range moduleOptionsUpdates {
			for key, value := range options {
				logger.Log.Infof("Writing module options %s=%s for module %s", key, value, moduleName)
				aggregatedOptions, err = aggregateModuleOptions(aggregatedOptions, moduleOptionsFilePath, moduleName, key, value)
				if err != nil {
					return fmt.Errorf("failed to append module option for module %s: %w", moduleName, err)
				}
			}
		}

		file, err := os.OpenFile(moduleOptionsFilePath, os.O_WRONLY|os.O_CREATE|os.O_APPEND, 0644)
		if err != nil {
			return fmt.Errorf("failed to open %s: %w", moduleOptionsFilePath, err)
		}
		defer file.Close()

		content := strings.Join(aggregatedOptions, "\n") + "\n"
		if _, err = file.WriteString(content); err != nil {
			return fmt.Errorf("failed to write module options to %s: %w", moduleOptionsFilePath, err)
		}
	}

	return nil
}

func aggregateModuleOptions(aggregatedOptions []string, moduleOptionsFilePath string, moduleName string, optionKey string, optionValue string) ([]string, error) {
	if _, err := os.Stat(moduleOptionsFilePath); err != nil {
		if os.IsNotExist(err) {
			// If the file does not exist, append the new option and return the options
			return append(aggregatedOptions, fmt.Sprintf("options %s %s=%s", moduleName, optionKey, optionValue)), nil
		}
		return nil, err
	}

	// File exists, if the option exists in the file, directly update the file, otherwise, append it and return the options
	// Read the entire file as a string
	content, err := os.ReadFile(moduleOptionsFilePath)
	if err != nil {
		return nil, err
	}

	lines := strings.Split(string(content), "\n")
	var updatedLines []string
	found := false

	for _, line := range lines {
		if strings.HasPrefix(line, "options "+moduleName) {
			fields := strings.Fields(line)
			updatedLine := []string{fields[0]}

			for _, field := range fields[1:] {
				if strings.HasPrefix(field, optionKey+"=") {
					// Update the existing option value
					updatedLine = append(updatedLine, optionKey+"="+optionValue)
					found = true
				} else {
					// Keep other options as they are
					updatedLine = append(updatedLine, field)
				}
			}
			line = strings.Join(updatedLine, " ")
		}
		updatedLines = append(updatedLines, line)
	}

	// Directly write back to file as this is updating existing option
	if found {
		err = os.WriteFile(moduleOptionsFilePath, []byte(strings.Join(updatedLines, "\n")), 0644)
		if err != nil {
			return nil, err
		}
	}

	// If option is not found, append it for a subsequent batch write operation
	if !found {
		aggregatedOptions = append(aggregatedOptions, fmt.Sprintf("options %s %s=%s", moduleName, optionKey, optionValue))
	}

	return aggregatedOptions, nil
}
