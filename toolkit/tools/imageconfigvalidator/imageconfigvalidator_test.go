// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"microsoft.com/pkggen/imagegen/configuration"
	"microsoft.com/pkggen/internal/logger"
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
	configFiles, err := ioutil.ReadDir(configDirectory)
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
	assert.Equal(t, "invalid [SystemConfigs]: missing [Name] field", err.Error())
}

func TestShouldFailDeeplyNestedParsingError(t *testing.T) {
	const (
		configDirectory string = "../../imageconfigs/"
		targetPackage          = "core-efi.json"
	)
	configFiles, err := ioutil.ReadDir(configDirectory)
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
			assert.Equal(t, "invalid [Disks]: invalid [PartitionTableType]: invalid value for PartitionTableType (not_a_real_partition_type)", err.Error())

			return
		}
	}
	assert.Failf(t, "Could not find config", "Could not find image config file '%s' to test", filepath.Join(configDirectory, targetPackage))
}

func TestShouldFailMissingVerityPackageWithVerityRoot(t *testing.T) {
	const (
		configDirectory       string = "../../imageconfigs/"
		targetPackage                = "read-only-root-efi.json"
		roRootPackageListFile        = "read-only-root-packages.json"
	)
	configFiles, err := ioutil.ReadDir(configDirectory)
	assert.NoError(t, err)

	// Pick the read-only-root config file, but remove the dm-verity dracut package list
	for _, file := range configFiles {
		if !file.IsDir() && strings.Contains(file.Name(), targetPackage) {
			configPath := filepath.Join(configDirectory, file.Name())

			fmt.Println("Corrupting ", configPath)

			config, err := configuration.LoadWithAbsolutePaths(configPath, configDirectory)
			assert.NoError(t, err)

			newPackageList := []string{}
			for _, pl := range config.SystemConfigs[0].PackageLists {
				if !strings.Contains(pl, roRootPackageListFile) {
					newPackageList = append(newPackageList, pl)
				}
			}

			config.SystemConfigs[0].PackageLists = newPackageList

			err = ValidateConfiguration(config)
			assert.Error(t, err)
			assert.Equal(t, "failed to validate package lists in config: [ReadOnlyVerityRoot] selected, but 'verity-read-only-root' package is not included in the package lists", err.Error())

			return
		}
	}
	assert.Fail(t, "Could not find "+targetPackage+" to test")
}

func TestShouldFailMissingVerityDebugPackageWithVerityDebug(t *testing.T) {
	const (
		configDirectory string = "../../imageconfigs/"
		targetPackage          = "read-only-root-efi.json"
	)
	configFiles, err := ioutil.ReadDir(configDirectory)
	assert.NoError(t, err)

	// Find the read-only root image config
	for _, file := range configFiles {
		if !file.IsDir() && strings.Contains(file.Name(), targetPackage) {
			configPath := filepath.Join(configDirectory, file.Name())

			fmt.Println("Corrupting ", configPath)

			config, err := configuration.LoadWithAbsolutePaths(configPath, configDirectory)
			assert.NoError(t, err)

			// Turn on the debug flag
			config.SystemConfigs[0].ReadOnlyVerityRoot.TmpfsOverlayDebugEnabled = true

			err = ValidateConfiguration(config)
			assert.Error(t, err)
			assert.Equal(t, "failed to validate package lists in config: [ReadOnlyVerityRoot] and [TmpfsOverlayDebugEnabled] selected, but 'verity-read-only-root-debug-mount' package is not included in the package lists", err.Error())

			return
		}
	}
	assert.Fail(t, "Could not find "+targetPackage+" to test")
}
