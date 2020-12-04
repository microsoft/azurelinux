// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

//TestMain found in configuration_test.go.

var (
	validSystemConfig       SystemConfig = expectedConfiguration.SystemConfigs[0]
	invalidSystemConfigJSON              = `{"IsDefault": 1234}`
)

func TestShouldFailParsingDefaultSystemConfig_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig
	err := marshalJSONString("{}", &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: missing [Name] field", err.Error())
}

func TestShouldSucceedParseValidSystemConfig_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	assert.NoError(t, validSystemConfig.IsValid())
	err := remarshalJSON(validSystemConfig, &checkedSystemConfig)
	assert.NoError(t, err)
	assert.Equal(t, validSystemConfig, checkedSystemConfig)
}

func TestShouldFailParsingMissingName_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	missingNameConfig := validSystemConfig
	missingNameConfig.Name = ""

	err := missingNameConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "missing [Name] field", err.Error())

	err = remarshalJSON(missingNameConfig, &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: missing [Name] field", err.Error())
}

func TestShouldFailParsingMissingPackages_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	missingPackageListConfig := validSystemConfig
	missingPackageListConfig.PackageLists = []string{}

	err := missingPackageListConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "system configuration must provide at least one package list inside the [PackageLists] field", err.Error())

	err = remarshalJSON(missingPackageListConfig, &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: system configuration must provide at least one package list inside the [PackageLists] field", err.Error())
}

func TestShouldFailParsingMissingDefaultKernel_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	missingDefaultConfig := validSystemConfig
	missingDefaultConfig.KernelOptions = map[string]string{}

	err := missingDefaultConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "system configuration must always provide default kernel inside the [KernelOptions] field; remember that kernels are FORBIDDEN from appearing in any of the [PackageLists]", err.Error())

	err = remarshalJSON(missingDefaultConfig, &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: system configuration must always provide default kernel inside the [KernelOptions] field; remember that kernels are FORBIDDEN from appearing in any of the [PackageLists]", err.Error())
}

func TestShouldFailParsingMissingExtraBlankKernel_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	blankKernelConfig := validSystemConfig
	// Create a new map so we don't affect other tests
	blankKernelConfig.KernelOptions = map[string]string{"default": "kernel", "extra": ""}

	err := blankKernelConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "empty kernel entry found in the [KernelOptions] field (extra); remember that kernels are FORBIDDEN from appearing in any of the [PackageLists]", err.Error())

	err = remarshalJSON(blankKernelConfig, &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: empty kernel entry found in the [KernelOptions] field (extra); remember that kernels are FORBIDDEN from appearing in any of the [PackageLists]", err.Error())
}

func TestShouldSucceedParsingMissingDefaultKernelForRootfs_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	rootfsNoKernelConfig := validSystemConfig
	rootfsNoKernelConfig.KernelOptions = map[string]string{}
	rootfsNoKernelConfig.PartitionSettings = []PartitionSetting{}

	assert.NoError(t, rootfsNoKernelConfig.IsValid())
	err := remarshalJSON(rootfsNoKernelConfig, &checkedSystemConfig)
	assert.NoError(t, err)
	assert.Equal(t, rootfsNoKernelConfig, checkedSystemConfig)
}

func TestShouldFailParsingBadKernelCommandLine_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	badKernelCommandConfig := validSystemConfig
	badKernelCommandConfig.KernelCommandLine = KernelCommandLine{ExtraCommandLine: invalidExtraCommandLine}

	err := badKernelCommandConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [KernelCommandLine]: ExtraCommandLine contains character ` which is reserved for use by sed", err.Error())

	err = remarshalJSON(badKernelCommandConfig, &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: failed to parse [KernelCommandLine]: ExtraCommandLine contains character ` which is reserved for use by sed", err.Error())
}

func TestShouldFailParsingBadUserUID_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig
	badUserConfig := validSystemConfig

	// Copy the current users (via append to get a copy), then mangle one
	badUsers := append([]User{}, validSystemConfig.Users...)
	badUsers[1].UID = "-2"
	badUserConfig.Users = badUsers

	err := badUserConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [User]: invalid value for UID (-2), not within [0, 60000]", err.Error())

	err = remarshalJSON(badUserConfig, &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: failed to parse [User]: invalid value for UID (-2), not within [0, 60000]", err.Error())
}

func TestShouldFailToParseInvalidJSON_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	err := marshalJSONString(invalidSystemConfigJSON, &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: json: cannot unmarshal number into Go struct field IntermediateTypeSystemConfig.IsDefault of type bool", err.Error())

}
