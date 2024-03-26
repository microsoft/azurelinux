// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/stretchr/testify/assert"
)

func TestLoadOrDisableModules(t *testing.T) {
	rootDir := filepath.Join(tmpDir, "TestLoadOrDisableModules")
	modules := []imagecustomizerapi.Module{
		{
			Name:     "module1",
			LoadMode: imagecustomizerapi.ModuleLoadModeAlways,
			Options:  map[string]string{"option1": "value1"},
		},
		{
			Name:     "module2",
			LoadMode: imagecustomizerapi.ModuleLoadModeDisable,
		},
		{
			Name:     "module3",
			LoadMode: imagecustomizerapi.ModuleLoadModeAuto,
			Options:  map[string]string{"option3_1": "value3_1", "option3_2": "value3_2"},
		},
	}

	err := loadOrDisableModules(modules, rootDir)
	assert.NoError(t, err)

	moduleLoadFilePath := filepath.Join(rootDir, "etc/modules-load.d/modules-load.conf")
	moduleOptionsFilePath := filepath.Join(rootDir, "etc/modprobe.d/module-options.conf")
	moduleDisableFilePath := filepath.Join(rootDir, "etc/modprobe.d/modules-disabled.conf")

	moduleLoadContent, err := os.ReadFile(moduleLoadFilePath)
	if err != nil {
		t.Errorf("Failed to read module load configuration file: %v", err)
	}

	moduleDisableContent, err := os.ReadFile(moduleDisableFilePath)
	if err != nil {
		t.Errorf("Failed to read module disable configuration file: %v", err)
	}

	moduleOptionsContent, err := os.ReadFile(moduleOptionsFilePath)
	if err != nil {
		t.Errorf("Failed to read module options configuration file: %v", err)
	}

	assert.Contains(t, string(moduleLoadContent), "module1")
	assert.Contains(t, string(moduleDisableContent), "module2")
	assert.Contains(t, string(moduleOptionsContent), "option3_1=value3_1")
	assert.Contains(t, string(moduleOptionsContent), "option3_2=value3_2")

	// Test add options for module2 which was disabled
	modules = []imagecustomizerapi.Module{
		{
			Name:    "module2",
			Options: map[string]string{"option2": "value2"},
		},
	}

	err = loadOrDisableModules(modules, rootDir)
	assert.Contains(t, err.Error(), "cannot add options for disabled module (module2)")

	// Test updating module2's loadmode and module3's option
	modules = []imagecustomizerapi.Module{
		{
			Name:     "module2",
			LoadMode: imagecustomizerapi.ModuleLoadModeAuto,
			Options:  map[string]string{"option2": "value2"},
		},
		{
			Name:    "module3",
			Options: map[string]string{"option3_1": "new_value3_1", "option3_3": "new_value3_3"},
		},
	}
	err = loadOrDisableModules(modules, rootDir)
	assert.NoError(t, err)

	moduleDisableContent, _ = os.ReadFile(moduleDisableFilePath)
	moduleOptionsContent, _ = os.ReadFile(moduleOptionsFilePath)

	assert.NotContains(t, string(moduleDisableContent), "module2")
	assert.Contains(t, string(moduleOptionsContent), "module2 option2=value2")
	assert.NotContains(t, string(moduleOptionsContent), "option3_1=value3_1")
	assert.Contains(t, string(moduleOptionsContent), "option3_1=new_value3_1")
	assert.Contains(t, string(moduleOptionsContent), "option3_3=new_value3_3")

	// Test case where a module was already set to load at boot
	modules = []imagecustomizerapi.Module{
		{
			Name:     "module1",
			LoadMode: imagecustomizerapi.ModuleLoadModeAlways,
			Options:  map[string]string{"option1": "value1"},
		},
	}

	err = loadOrDisableModules(modules, rootDir)
	assert.NoError(t, err)

	moduleLoadContent, _ = os.ReadFile(moduleLoadFilePath)
	count := strings.Count(string(moduleLoadContent), "module1\n")
	assert.Equal(t, 1, count, "module1 was already set to load. It should appear exactly once in load configuration file")

	moduleOptionsContent, _ = os.ReadFile(moduleOptionsFilePath)
	count = strings.Count(string(moduleOptionsContent), "option1=value1")
	assert.Equal(t, 1, count, "option1 for module1 should appear exactly once in options configuration file")

}

func TestEnsureModulesLoaded(t *testing.T) {
	buildDir := filepath.Join(tmpDir, "TestEnsureModulesLoaded")
	modulesLoadPath := filepath.Join(buildDir, "etc/modules-load.d")
	moduleLoadFilePath := filepath.Join(modulesLoadPath, "modules.conf")

	// Only create parent directory. Test case where the file does not exist
	err := os.MkdirAll(modulesLoadPath, os.ModePerm)
	assert.NoError(t, err)
	err = ensureModulesLoaded([]string{"module1"}, moduleLoadFilePath)
	assert.NoError(t, err)

	// Verify the file was created and contains the module name
	content, err := os.ReadFile(moduleLoadFilePath)
	assert.NoError(t, err)
	assert.Contains(t, string(content), "module1\n")

	// Test case where the file exists and already contains the module
	err = ensureModulesLoaded([]string{"module1"}, moduleLoadFilePath)
	assert.NoError(t, err)

	// Verify the file content is unchanged (module not duplicated)
	content, err = os.ReadFile(moduleLoadFilePath)
	assert.NoError(t, err)
	assert.Equal(t, "module1\n", string(content))

	// Test case where a new module is added
	err = ensureModulesLoaded([]string{"module2"}, moduleLoadFilePath)
	assert.NoError(t, err)

	// Verify the file content now includes both modules
	content, err = os.ReadFile(moduleLoadFilePath)
	assert.NoError(t, err)
	assert.Equal(t, "module1\nmodule2\n", string(content))
}

func TestEnsureModulesDisabled(t *testing.T) {
	buildDir := filepath.Join(tmpDir, "TestEnsureModulesDisabled")
	modprobePath := filepath.Join(buildDir, "etc/modprobe.d")
	moduleDisableFilePath := filepath.Join(modprobePath, "blacklist.conf")
	err := os.MkdirAll(modprobePath, os.ModePerm)
	assert.NoError(t, err)

	// Prepopulate the file with a disabled module
	initialContent := "blacklist module1\n"
	err = os.WriteFile(moduleDisableFilePath, []byte(initialContent), 0644)
	assert.NoError(t, err)

	// Test case where the module is already disabled
	err = ensureModulesDisabled([]string{"module1"}, moduleDisableFilePath)
	assert.NoError(t, err)

	// Verify the file content is unchanged
	content, err := os.ReadFile(moduleDisableFilePath)
	assert.NoError(t, err)
	assert.Equal(t, initialContent, string(content))

	// Test case where a new module needs to be disabled
	err = ensureModulesDisabled([]string{"module2"}, moduleDisableFilePath)
	assert.NoError(t, err)

	// Verify the file now contains both modules
	expectedContent := initialContent + "blacklist module2\n"
	content, err = os.ReadFile(moduleDisableFilePath)
	assert.NoError(t, err)
	assert.Equal(t, expectedContent, string(content))
}

func TestRemoveModuleFromDisableList(t *testing.T) {
	buildDir := filepath.Join(tmpDir, "TestRemoveModuleFromDisableList")
	modprobePath := filepath.Join(buildDir, "etc/modprobe.d")
	moduleDisableFilePath := filepath.Join(modprobePath, "blacklist.conf")
	err := os.MkdirAll(modprobePath, os.ModePerm)
	assert.NoError(t, err)

	// Prepopulate the file with a disabled module
	moduleName := "module1"
	initialContent := "blacklist " + moduleName + "\nblacklist module2\n"
	err = os.WriteFile(moduleDisableFilePath, []byte(initialContent), 0644)
	assert.NoError(t, err)

	// Test removing an existing module from the disable list
	err = removeModuleFromDisableList(moduleName, moduleDisableFilePath)
	assert.NoError(t, err)

	// Verify the module was removed from the file
	content, err := os.ReadFile(moduleDisableFilePath)
	assert.NoError(t, err)
	assert.NotContains(t, string(content), "blacklist "+moduleName+"\n")
	assert.Contains(t, string(content), "blacklist module2\n")

	// Test removing a module that does not exist in the disable list
	nonExistingModule := "module3"
	err = removeModuleFromDisableList(nonExistingModule, moduleDisableFilePath)
	assert.NoError(t, err)

	// Verify the file content is unchanged
	content, err = os.ReadFile(moduleDisableFilePath)
	assert.NoError(t, err)
	assert.Equal(t, "blacklist module2\n", string(content))
}
