// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"

	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	os.Exit(m.Run())
}

func TestShouldSucceedValidatingDefaultConfigs(t *testing.T) {
	const (
		configDirectory = "../../imageconfigs/"
	)
	checkedConfigs := 0
	configFiles, err := os.ReadDir(configDirectory)
	assert.NoError(t, err)

	for _, file := range configFiles {
		if !file.IsDir() && strings.Contains(file.Name(), ".json") {
			configPath := filepath.Join(configDirectory, file.Name())

			fmt.Println("Validating ", configPath)

			config, err := configuration.LoadWithAbsolutePaths(configPath, configDirectory)
			assert.NoError(t, err)

			if err != nil {
				// It can be hard to figure out which config failed from the printed output, explicitly print
				// an error message listed the failed configs.
				fmt.Printf("Failed to validate %s\n", configPath)
			}

			err = ValidateConfiguration(config)
			assert.NoError(t, err)
			if err != nil {
				fmt.Printf("Failed to validate %s\n", configPath)
			}
			checkedConfigs++
		}
	}
	// Make sure we found at least one config to validate
	assert.GreaterOrEqual(t, checkedConfigs, 1)
}

func TestShouldFailEmptyConfig(t *testing.T) {
	config := configuration.Config{}

	err := ValidateConfiguration(config)
	assert.Error(t, err)
	assert.Equal(t, "config file must provide at least one system configuration inside the [SystemConfigs] field", err.Error())
}

func TestShouldFailEmptySystemConfig(t *testing.T) {
	config := configuration.Config{}
	config.SystemConfigs = []configuration.SystemConfig{{}}

	err := ValidateConfiguration(config)
	assert.Error(t, err)
	assert.Equal(t, "invalid [SystemConfigs]:\nmissing [Name] field", err.Error())
}

func TestShouldFailDeeplyNestedParsingError(t *testing.T) {
	const (
		configDirectory string = "../../imageconfigs/"
		targetPackage          = "core-efi.json"
	)
	configFiles, err := os.ReadDir(configDirectory)
	assert.NoError(t, err)

	// Pick the first config file and mess something up which is deeply
	// nested inside the json
	for _, file := range configFiles {
		if !file.IsDir() && strings.Contains(file.Name(), targetPackage) {
			configPath := filepath.Join(configDirectory, file.Name())

			fmt.Println("Corrupting ", configPath)

			config, err := configuration.LoadWithAbsolutePaths(configPath, configDirectory)
			assert.NoError(t, err)

			config.Disks[0].PartitionTableType = configuration.PartitionTableType("not_a_real_partition_type")
			err = ValidateConfiguration(config)
			assert.Error(t, err)
			assert.Equal(t, "invalid [Disks]:\ninvalid [PartitionTableType]: invalid value for PartitionTableType (not_a_real_partition_type)", err.Error())

			return
		}
	}
	assert.Failf(t, "Could not find config", "Could not find image config file '%s' to test", filepath.Join(configDirectory, targetPackage))
}

func TestShouldFailMissingFipsPackageWithFipsCmdLine(t *testing.T) {
	const (
		configDirectory     string = "../../imageconfigs/"
		targetPackage              = "core-fips.json"
		fipsPackageListFile        = "fips-packages.json"
	)
	configFiles, err := os.ReadDir(configDirectory)
	assert.NoError(t, err)

	// Pick the core-fips config file, but remove the fips package list
	for _, file := range configFiles {
		if !file.IsDir() && strings.Contains(file.Name(), targetPackage) {
			configPath := filepath.Join(configDirectory, file.Name())

			fmt.Println("Corrupting ", configPath)

			config, err := configuration.LoadWithAbsolutePaths(configPath, configDirectory)
			assert.NoError(t, err)

			newPackageList := []string{}
			for _, pl := range config.SystemConfigs[0].PackageLists {
				if !strings.Contains(pl, fipsPackageListFile) {
					newPackageList = append(newPackageList, pl)
				}
			}

			config.SystemConfigs[0].PackageLists = newPackageList

			err = ValidateConfiguration(config)
			assert.Error(t, err)
			assert.Equal(t, "failed to validate package lists in config: 'fips=1' provided on kernel cmdline, but 'dracut-fips' package is not included in the package lists", err.Error())

			return
		}
	}
	assert.Fail(t, "Could not find "+targetPackage+" to test")
}

func TestShouldFailMissingSELinuxPackageWithSELinux(t *testing.T) {
	const (
		configDirectory   = "../../imageconfigs/"
		targetPackage     = "core-efi.json"
		targetPackageList = "selinux.json"
	)
	configFiles, err := os.ReadDir(configDirectory)
	assert.NoError(t, err)

	// Pick the core-efi config file, then enable SELinux
	for _, file := range configFiles {
		if !file.IsDir() && strings.Contains(file.Name(), targetPackage) {
			configPath := filepath.Join(configDirectory, file.Name())

			fmt.Println("Corrupting ", configPath)

			config, err := configuration.LoadWithAbsolutePaths(configPath, configDirectory)
			for i, list := range config.SystemConfigs[0].PackageLists {
				// Delete the packagelist from the config
				if strings.Contains(list, targetPackageList) {
					config.SystemConfigs[0].PackageLists = append(config.SystemConfigs[0].PackageLists[:i], config.SystemConfigs[0].PackageLists[i+1:]...)
				}
			}
			assert.NoError(t, err)

			config.SystemConfigs[0].KernelCommandLine.SELinux = "enforcing"

			err = ValidateConfiguration(config)
			assert.Error(t, err)
			assert.Equal(t, "failed to validate package lists in config: [SELinux] selected, but 'selinux-policy' package is not included in the package lists", err.Error())

			return
		}
	}
	assert.Fail(t, "Could not find "+targetPackage+" to test")
}

func TestShouldSucceedSELinuxPackageDefinedInline(t *testing.T) {
	const (
		configDirectory   = "../../imageconfigs/"
		targetPackage     = "core-efi.json"
		targetPackageList = "selinux.json"
		selinuxPkgName    = "selinux-policy"
	)
	configFiles, err := os.ReadDir(configDirectory)
	assert.NoError(t, err)

	// Pick the core-efi config file, then enable SELinux
	for _, file := range configFiles {
		if !file.IsDir() && strings.Contains(file.Name(), targetPackage) {
			configPath := filepath.Join(configDirectory, file.Name())

			fmt.Println("Corrupting ", configPath)

			config, err := configuration.LoadWithAbsolutePaths(configPath, configDirectory)
			for i, list := range config.SystemConfigs[0].PackageLists {
				// Delete the packagelist from the config
				if strings.Contains(list, targetPackageList) {
					config.SystemConfigs[0].PackageLists = append(config.SystemConfigs[0].PackageLists[:i], config.SystemConfigs[0].PackageLists[i+1:]...)
				}
			}
			assert.NoError(t, err)

			//Add required SELinux package in the inline package definition
			newPackagesField := []string{selinuxPkgName}
			config.SystemConfigs[0].Packages = newPackagesField

			config.SystemConfigs[0].KernelCommandLine.SELinux = "enforcing"

			err = ValidateConfiguration(config)
			assert.NoError(t, err)
			return
		}
	}
	assert.Fail(t, "Could not find "+targetPackage+" to test")
}
