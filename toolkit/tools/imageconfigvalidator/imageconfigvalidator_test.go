// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"fmt"
	"os"
	"path"
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

func TestSELinuxRequiresSELinuxPacakgeInline(t *testing.T) {
	const (
		configDirectory = "./testdata/"
		targetConfig    = "test-config.json"
		selinuxPkgName  = "selinux-policy"
	)
	configPath := filepath.Join(configDirectory, targetConfig)

	config, err := configuration.LoadWithAbsolutePaths(configPath, configDirectory)
	assert.NoError(t, err)

	config.SystemConfigs[0].KernelCommandLine.SELinux = "enforcing"

	err = ValidateConfiguration(config)
	assert.Error(t, err)
	assert.Equal(t, "failed to validate package lists in config: [SELinux] selected, but 'selinux-policy' package is not included in the package lists", err.Error())

	//Add required SELinux package in the inline package definition
	newPackagesField := []string{selinuxPkgName}
	config.SystemConfigs[0].Packages = newPackagesField

	err = ValidateConfiguration(config)
	assert.NoError(t, err)
}

func TestValidationAgainstTestConfig(t *testing.T) {
	confiDirAbsPath, err := filepath.Abs("./testdata/")
	assert.NoError(t, err)

	tests := []struct {
		name           string
		extraListPath  string
		configModifier func(*configuration.Config)
		expectedError1 string
		expectedError2 string
	}{
		{
			name:          "Deeply nested parsing error",
			extraListPath: "",
			configModifier: func(config *configuration.Config) {
				config.Disks[0].PartitionTableType = configuration.PartitionTableType("not_a_real_partition_type")
			},
			expectedError1: "invalid [Disks]:\ninvalid [PartitionTableType]: invalid value for PartitionTableType (not_a_real_partition_type)",
			// No action is taken to fix the error, so it will still be present
			expectedError2: "invalid [Disks]:\ninvalid [PartitionTableType]: invalid value for PartitionTableType (not_a_real_partition_type)",
		},
		{
			name:          "fips with  dracut-fips",
			extraListPath: "./testdata/fips-list.json",
			configModifier: func(config *configuration.Config) {
				config.SystemConfigs[0].KernelCommandLine.EnableFIPS = true
			},
			expectedError1: "failed to validate package lists in config: 'fips=1' provided on kernel cmdline, but 'dracut-fips' package is not included in the package lists",
			expectedError2: "",
		},
		{
			name:          "selinux with selinux-policy",
			extraListPath: "./testdata/selinux-policy-list.json",
			configModifier: func(config *configuration.Config) {
				config.SystemConfigs[0].KernelCommandLine.SELinux = "enforcing"
			},
			expectedError1: "failed to validate package lists in config: [SELinux] selected, but 'selinux-policy' package is not included in the package lists",
			expectedError2: "",
		},
		{
			name:          "user with shadowutils",
			extraListPath: "./testdata/shadowutils-list.json",
			configModifier: func(config *configuration.Config) {
				config.SystemConfigs[0].Users = []configuration.User{
					{
						Name: "testuser",
					},
				}
			},
			expectedError1: "failed to validate package lists in config: the 'shadow-utils' package must be included in the package lists when the image is configured to add users or groups",
			expectedError2: "",
		},
		{
			name:          "Shadowutils pinned version",
			extraListPath: "./testdata/pinned-shadowutils-list.json",
			configModifier: func(config *configuration.Config) {
				config.SystemConfigs[0].Users = []configuration.User{
					{
						Name: "testuser",
					},
				}
			},
			expectedError1: "failed to validate package lists in config: the 'shadow-utils' package must be included in the package lists when the image is configured to add users or groups",
			expectedError2: "",
		},
		{
			name:           "missing package list",
			extraListPath:  "./testdata/not-a-real-list.json",
			configModifier: func(config *configuration.Config) {},
			expectedError1: "",
			expectedError2: "failed to validate package lists in config: open " + path.Join(confiDirAbsPath, "not-a-real-list.json") + ": no such file or directory",
		},
		{
			name:           "bad package name",
			extraListPath:  "./testdata/bogus-list.json",
			configModifier: func(config *configuration.Config) {},
			expectedError1: "",
			expectedError2: `failed to validate package lists in config: packages list entry "bad package = bad < version" does not match the '[name][optional_condition][optional_version]' format`,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			configPath := filepath.Join("./testdata/", "test-config.json")
			config, err := configuration.LoadWithAbsolutePaths(configPath, "./testdata/")
			assert.NoError(t, err)

			// Break the config
			tt.configModifier(&config)

			// Ensure the validation detects the expected failure
			err = ValidateConfiguration(config)
			if tt.expectedError1 != "" {
				assert.Error(t, err)
				assert.Equal(t, tt.expectedError1, err.Error())
			} else {
				assert.NoError(t, err)
			}

			// Fix the config by adding the package list if provided
			if tt.extraListPath != "" {
				replacementPackageListAbsPath, err := filepath.Abs(tt.extraListPath)
				assert.NoError(t, err)
				config.SystemConfigs[0].PackageLists = append(config.SystemConfigs[0].PackageLists, replacementPackageListAbsPath)
			}

			// Validate again
			err = ValidateConfiguration(config)
			if tt.expectedError2 != "" {
				assert.Error(t, err)
				assert.Equal(t, tt.expectedError2, err.Error())
			} else {
				assert.NoError(t, err)
			}
		})
	}
}
