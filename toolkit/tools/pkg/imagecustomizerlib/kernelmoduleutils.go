// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

func loadOrDisableModules(modules []imagecustomizerapi.Module, rootDir string) error {
	var err error
	var modulesToLoad []string
	var modulesToDisable []string
	moduleOptionsUpdates := make(map[string]map[string]string)
	moduleDisableFilePath := filepath.Join(rootDir, "etc/modprobe.d/modules-disabled.conf")
	moduleLoadFilePath := filepath.Join(rootDir, "etc/modules-load.d/modules-load.conf")
	moduleOptionsFilePath := filepath.Join(rootDir, "etc/modprobe.d/module-options.conf")

	for i, module := range modules {
		switch module.LoadMode {
		case imagecustomizerapi.ModuleLoadModeAlways:
			// If a module is disabled, remove it. Add the module to modules-load.d/. Write options if provided.
			err = removeModuleFromDisableList(module.Name, moduleDisableFilePath)
			if err != nil {
				return fmt.Errorf("failed to remove module (%s) from the disabled list:\n%w", module.Name, err)
			}
			modulesToLoad = append(modulesToLoad, module.Name)

			if len(module.Options) > 0 {
				moduleOptionsUpdates[module.Name] = module.Options
			}

		case imagecustomizerapi.ModuleLoadModeAuto:
			// If a module is disabled, enable it. Write options if provided
			err = removeModuleFromDisableList(module.Name, moduleDisableFilePath)
			if err != nil {
				return fmt.Errorf("failed to remove module (%s) from the disabled list:\n%w", module.Name, err)
			}

			if len(module.Options) > 0 {
				moduleOptionsUpdates[module.Name] = module.Options
			}

		case imagecustomizerapi.ModuleLoadModeDisable:
			// Disable a module, throw error if options are provided
			if len(module.Options) > 0 {
				return fmt.Errorf("cannot add options for disabled module (%s) at index %d:\nspecify auto or always as loadMode to override setting in base image", module.Name, i)
			}

			modulesToDisable = append(modulesToDisable, module.Name)

		case imagecustomizerapi.ModuleLoadModeInherit, imagecustomizerapi.ModuleLoadModeDefault:
			// inherits the behavior of the base image, modify the options without changing the loading state
			if len(module.Options) > 0 {
				disabled, err := isModuleDisabled(module.Name, moduleDisableFilePath)
				if err != nil {
					return fmt.Errorf("failed to check if (%s) is disabled", module)
				}

				if disabled {
					return fmt.Errorf("cannot add options for disabled module (%s) at index %d:\nspecify auto or always as loadMode to override setting in base image", module.Name, i)
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
	err = ensureModulesDisabled(modulesToDisable, moduleDisableFilePath)
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
	// Ensure the directory exists
	dir := filepath.Dir(moduleLoadFilePath)
	if err := os.MkdirAll(dir, os.ModePerm); err != nil {
		return fmt.Errorf("failed to create directory for module load configuration: %w", err)
	}

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
			logger.Log.Infof("Setting module (%s) to load at boot", moduleName)
		} else {
			logger.Log.Infof("Module (%s) is already set to load at boot", moduleName)
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
	// Ensure the directory exists
	dir := filepath.Dir(moduleDisableFilePath)
	if err := os.MkdirAll(dir, os.ModePerm); err != nil {
		return fmt.Errorf("failed to create directory for module disable configuration: %w", err)
	}

	content, err := os.ReadFile(moduleDisableFilePath)
	if err != nil {
		if !os.IsNotExist(err) {
			return fmt.Errorf("failed to read module disable configuration: %w", err)
		}
		content = []byte{}
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
			logger.Log.Infof("Setting module (%s) to be disabled", moduleName)
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
		logger.Log.Errorf("Failed to scan file (%s) with error %s", moduleDisableFilePath, err)
		return false, err
	}

	blacklistEntry := "blacklist " + moduleName
	if strings.Contains(string(content), blacklistEntry+"\n") {
		return true, nil
	}

	return false, nil
}

func removeModuleFromDisableList(moduleName, moduleDisableFilePath string) error {
	disabled, err := isModuleDisabled(moduleName, moduleDisableFilePath)
	if err != nil {
		logger.Log.Infof("failed to check if (%s) is disabled", moduleName)
		return err
	}

	if disabled {
		logger.Log.Infof("Module (%s) found in the disabled list. Removing it.", moduleName)
		lines, err := file.ReadLines(moduleDisableFilePath)

		if err != nil {
			return fmt.Errorf("failed to write module disable configuration: %w", err)
		}

		// Filter out the line that contains the module name.
		var updatedLines []string
		for _, line := range lines {
			if !strings.Contains(line, moduleName) {
				updatedLines = append(updatedLines, line)
			}
		}

		if err := file.WriteLines(updatedLines, moduleDisableFilePath); err != nil {
			return fmt.Errorf("failed to write module disable configuration: %w", err)
		}
	}

	return nil
}

func updateModulesOptions(optionsMap map[string]map[string]string, moduleOptionsFilePath string) error {
	if len(optionsMap) == 0 {
		return nil
	}

	// Ensure the directory exists
	dir := filepath.Dir(moduleOptionsFilePath)
	if err := os.MkdirAll(dir, os.ModePerm); err != nil {
		return fmt.Errorf("failed to create directory for module options configuration: %w", err)
	}

	// Read the existing content of the file, if it exists
	content, err := os.ReadFile(moduleOptionsFilePath)
	if err != nil && !os.IsNotExist(err) {
		return err
	}

	lines := strings.Split(string(content), "\n")
	existingModules := make(map[string]bool)
	var updatedLines []string

	// Update existing lines with new values from optionsMap
	for _, line := range lines {
		if line == "" {
			continue
		}

		fields := strings.Fields(line)
		if len(fields) < 2 || fields[0] != "options" {
			// This might be the case for comments, empty lines. Copy unrelated lines as is
			updatedLines = append(updatedLines, line)
			continue
		}

		moduleName := fields[1]
		if moduleOptions, ok := optionsMap[moduleName]; ok {
			existingModules[moduleName] = true
			updatedLine := "options " + moduleName
			seenOptions := make(map[string]bool)

			// Update existing options in the line
			for _, field := range fields[2:] {
				optionKeyVal := strings.SplitN(field, "=", 2)
				if len(optionKeyVal) == 2 {
					optionKey := optionKeyVal[0]
					if newValue, exists := moduleOptions[optionKey]; exists {
						updatedLine += " " + optionKey + "=" + newValue
						logger.Log.Infof("Updating option key (%s) to (%s) for module (%s)", optionKey, newValue, moduleName)
						seenOptions[optionKey] = true
					} else {
						// Keep other options as is
						updatedLine += " " + field
					}
				}
			}

			// Append any new options for this module not already in the line
			for optionKey, optionValue := range moduleOptions {
				if !seenOptions[optionKey] {
					updatedLine += " " + optionKey + "=" + optionValue
					logger.Log.Infof("Adding option (%s=%s) for module (%s)", optionKey, optionValue, moduleName)
				}
			}

			updatedLines = append(updatedLines, updatedLine)
		} else {
			// Copy lines for modules not in optionsMap
			updatedLines = append(updatedLines, line)
		}
	}

	// Add new module lines for any modules in optionsMap not already in the file
	for moduleName, moduleOptions := range optionsMap {
		if !existingModules[moduleName] {
			updatedLine := "options " + moduleName
			for optionKey, optionValue := range moduleOptions {
				updatedLine += " " + optionKey + "=" + optionValue
				logger.Log.Infof("Adding option (%s=%s) for module (%s)", optionKey, optionValue, moduleName)
			}
			updatedLines = append(updatedLines, updatedLine)
		}
	}

	// Write the updated content back to the file
	updatedContent := strings.Join(updatedLines, "\n")
	return os.WriteFile(moduleOptionsFilePath, []byte(updatedContent), 0644)
}
