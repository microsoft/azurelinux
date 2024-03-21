// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/stretchr/testify/assert"
)

func TestEnsureModulesLoaded(t *testing.T) {
	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses a chroot")
	}

	// Setup environment.
	proposedDir := filepath.Join(tmpDir, "TestEnsureModulesLoaded")
	chroot := safechroot.NewChroot(proposedDir, false)
	err := chroot.Initialize("", []string{}, []*safechroot.MountPoint{}, false)
	assert.NoError(t, err)
	defer chroot.Close(false)

	modulesLoadPath := filepath.Join(chroot.RootDir(), "etc/modules-load.d")
	moduleLoadFilePath := filepath.Join(modulesLoadPath, "modules.conf")

	// Only create parent directory. Test case where the file does not exist
	err = os.MkdirAll(modulesLoadPath, os.ModePerm)
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
	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses a chroot")
	}

	// Setup environment.
	proposedDir := filepath.Join(tmpDir, "TestEnsureModulesDisabled")
	chroot := safechroot.NewChroot(proposedDir, false)
	err := chroot.Initialize("", []string{}, []*safechroot.MountPoint{}, false)
	assert.NoError(t, err)
	defer chroot.Close(false)

	modprobePath := filepath.Join(chroot.RootDir(), "etc/modprobe.d")
	moduleDisableFilePath := filepath.Join(modprobePath, "blacklist.conf")
	err = os.MkdirAll(modprobePath, os.ModePerm)
	assert.NoError(t, err)

	// Prepopulate the file with a blacklisted module
	initialContent := "blacklist module1\n"
	err = os.WriteFile(moduleDisableFilePath, []byte(initialContent), 0644)
	assert.NoError(t, err)

	// Test case where the module is already blacklisted
	err = ensureModulesDisabled([]string{"module1"}, moduleDisableFilePath)
	assert.NoError(t, err)

	// Verify the file content is unchanged
	content, err := os.ReadFile(moduleDisableFilePath)
	assert.NoError(t, err)
	assert.Equal(t, initialContent, string(content))

	// Test case where a new module needs to be blacklisted
	err = ensureModulesDisabled([]string{"module2"}, moduleDisableFilePath)
	assert.NoError(t, err)

	// Verify the file now contains both modules
	expectedContent := initialContent + "blacklist module2\n"
	content, err = os.ReadFile(moduleDisableFilePath)
	assert.NoError(t, err)
	assert.Equal(t, expectedContent, string(content))
}

func TestRemoveModuleFromDisableList(t *testing.T) {
	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses a chroot")
	}

	// Setup environment.
	proposedDir := filepath.Join(tmpDir, "TestRemoveModuleFromDisableList")
	chroot := safechroot.NewChroot(proposedDir, false)
	err := chroot.Initialize("", []string{}, []*safechroot.MountPoint{}, false)
	assert.NoError(t, err)
	defer chroot.Close(false)

	modprobePath := filepath.Join(chroot.RootDir(), "etc/modprobe.d")
	moduleDisableFilePath := filepath.Join(modprobePath, "blacklist.conf")
	err = os.MkdirAll(modprobePath, os.ModePerm)
	assert.NoError(t, err)

	// Prepopulate the file with a blacklisted module
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

func TestUpdateModulesOptions(t *testing.T) {
	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses a chroot")
	}

	// Setup environment.
	proposedDir := filepath.Join(tmpDir, "TestAggregateModuleOptions")
	chroot := safechroot.NewChroot(proposedDir, false)
	err := chroot.Initialize("", []string{}, []*safechroot.MountPoint{}, false)
	assert.NoError(t, err)
	defer chroot.Close(false)

	modprobePath := filepath.Join(chroot.RootDir(), "etc/modprobe.d")
	moduleOptionsFilePath := filepath.Join(modprobePath, "options.conf")
	err = os.MkdirAll(modprobePath, os.ModePerm)
	assert.NoError(t, err)

	moduleOptionsUpdates := map[string]map[string]string{
		"module1": {
			"option1": "value1",
			"option2": "value2",
		},
		"module2": {
			"option3": "value3",
		},
	}

	err = updateModulesOptions(moduleOptionsUpdates, moduleOptionsFilePath)
	assert.NoError(t, err)

	content, err := os.ReadFile(moduleOptionsFilePath)
	assert.NoError(t, err)

	expectedContent := "options module1 option1=value1\noptions module1 option2=value2\noptions module2 option3=value3\n"
	assert.Equal(t, expectedContent, string(content))

	// Update existing module option
	_, err = aggregateModuleOptions([]string{}, moduleOptionsFilePath, "module1", "option2", "new_value2")
	assert.NoError(t, err)

	_, err = aggregateModuleOptions([]string{}, moduleOptionsFilePath, "module3", "option3", "new_value3")
	assert.NoError(t, err)

	content, _ = os.ReadFile(moduleOptionsFilePath)
	expectedContent = "options module1 option1=value1\noptions module1 option2=new_value\noptions module2 option3=new_value3\n"
	assert.Equal(t, expectedContent, string(content))

	// Add new module option
	_, err = aggregateModuleOptions([]string{}, moduleOptionsFilePath, "module4", "option4", "value4")
	assert.NoError(t, err)
	content, _ = os.ReadFile(moduleOptionsFilePath)
	assert.Contains(t, string(content), "options module4 option4=value4")
}
