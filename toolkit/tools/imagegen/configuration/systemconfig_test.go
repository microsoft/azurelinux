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
	missingPackageListConfig.Packages = []string{}

	err := missingPackageListConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "system configuration must provide at least one package list inside the [PackageLists] or one package in the [Packages] field", err.Error())

	err = remarshalJSON(missingPackageListConfig, &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: system configuration must provide at least one package list inside the [PackageLists] or one package in the [Packages] field", err.Error())
}

func TestShouldSucceedParsingMissingPackageLists_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	//PackageList field is being wiped, Packages field is still non-empty
	missingPackageListConfig := validSystemConfig
	missingPackageListConfig.PackageLists = []string{}

	assert.NoError(t, missingPackageListConfig.IsValid())

	err := remarshalJSON(missingPackageListConfig, &checkedSystemConfig)
	assert.NoError(t, err)
	assert.Equal(t, missingPackageListConfig, checkedSystemConfig)
}

func TestShouldSucceedParsingMissingInlinePackages_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	//Packages field is being wiped, PackageList field is still non-empty
	missingPackagesConfig := validSystemConfig
	missingPackagesConfig.Packages = []string{}

	assert.NoError(t, missingPackagesConfig.IsValid())

	err := remarshalJSON(missingPackagesConfig, &checkedSystemConfig)
	assert.NoError(t, err)
	assert.Equal(t, missingPackagesConfig, checkedSystemConfig)
}

func TestShouldFailParsingMissingDefaultKernel_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	missingDefaultConfig := validSystemConfig
	missingDefaultConfig.KernelOptions = map[string]string{}

	err := missingDefaultConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "system configuration must always provide default kernel inside the [KernelOptions] field; remember that kernels are FORBIDDEN from appearing in any of the [PackageLists] or [Packages]", err.Error())

	err = remarshalJSON(missingDefaultConfig, &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: system configuration must always provide default kernel inside the [KernelOptions] field; remember that kernels are FORBIDDEN from appearing in any of the [PackageLists] or [Packages]", err.Error())
}

func TestShouldFailParsingMissingExtraBlankKernel_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	blankKernelConfig := validSystemConfig
	// Create a new map so we don't affect other tests
	blankKernelConfig.KernelOptions = map[string]string{"default": "kernel", "extra": ""}

	err := blankKernelConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "empty kernel entry found in the [KernelOptions] field (extra); remember that kernels are FORBIDDEN from appearing in any of the [PackageLists] or [Packages]", err.Error())

	err = remarshalJSON(blankKernelConfig, &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: empty kernel entry found in the [KernelOptions] field (extra); remember that kernels are FORBIDDEN from appearing in any of the [PackageLists] or [Packages]", err.Error())
}

func TestShouldSucceedParsingMissingDefaultKernelForRootfs_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	rootfsNoKernelConfig := validSystemConfig
	rootfsNoKernelConfig.KernelOptions = map[string]string{}
	rootfsNoKernelConfig.PartitionSettings = []PartitionSetting{}

	rootfsNoKernelConfig.Encryption = RootEncryption{}

	assert.NoError(t, rootfsNoKernelConfig.IsValid())
	err := remarshalJSON(rootfsNoKernelConfig, &checkedSystemConfig)
	assert.NoError(t, err)
	assert.Equal(t, rootfsNoKernelConfig, checkedSystemConfig)
}

func TestShouldFailParsingInvalidKernelForRootfs_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	invalidBootTypeConfig := validSystemConfig
	invalidBootTypeConfig.KernelOptions = map[string]string{"_comment": "trick the check", "extra": ""}
	invalidBootTypeConfig.PartitionSettings = []PartitionSetting{}

	invalidBootTypeConfig.Encryption = RootEncryption{}

	err := invalidBootTypeConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "empty kernel entry found in the [KernelOptions] field (extra); remember that kernels are FORBIDDEN from appearing in any of the [PackageLists] or [Packages]", err.Error())

	err = remarshalJSON(invalidBootTypeConfig, &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: empty kernel entry found in the [KernelOptions] field (extra); remember that kernels are FORBIDDEN from appearing in any of the [PackageLists] or [Packages]", err.Error())
}

func TestShouldFailParsingBadKernelCommandLine_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	badKernelCommandConfig := validSystemConfig
	badKernelCommandConfig.KernelCommandLine = KernelCommandLine{ExtraCommandLine: invalidExtraCommandLine}

	err := badKernelCommandConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [KernelCommandLine]: the 'ExtraCommandLine' field contains the ` character which is reserved for use by sed", err.Error())

	err = remarshalJSON(badKernelCommandConfig, &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: failed to parse [KernelCommandLine]: the 'ExtraCommandLine' field contains the ` character which is reserved for use by sed", err.Error())
}

func TestShouldFailParsingInvalidHostName_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	badHostnameConfig := validSystemConfig
	badHostnameConfig.Hostname = "abcd_efg"

	err := badHostnameConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [Hostname]: abcd_efg", err.Error())

	err = remarshalJSON(badHostnameConfig, &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: invalid [Hostname]: abcd_efg", err.Error())
}

func TestShouldFailParsingDuplicatePackageRepoNames(t *testing.T) {
	var checkedSystemConfig SystemConfig

	duplicateRepoNameConfig := validSystemConfig
	duplicateRepoNameConfig.PackageRepos = []PackageRepo{
		{Name: "badrepo", BaseUrl: "https://repo1.com", Install: false},
		{Name: "badrepo", BaseUrl: "https://repo2.com", Install: false},
	}

	err := duplicateRepoNameConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [PackageRepos]: duplicate package repo names (badrepo)", err.Error())

	err = remarshalJSON(duplicateRepoNameConfig, &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: invalid [PackageRepos]: duplicate package repo names (badrepo)", err.Error())
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

func TestShouldFailToParsingMultipleSameMounts_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	badPartitionSettingsConfig := validSystemConfig
	badPartitionSettingsConfig.PartitionSettings = []PartitionSetting{
		{MountPoint: "/", MountIdentifier: GetDefaultMountIdentifier()},
		{MountPoint: "/", MountIdentifier: GetDefaultMountIdentifier()},
	}

	err := badPartitionSettingsConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [PartitionSettings]: duplicate mount point found at '/'", err.Error())

	err = remarshalJSON(badPartitionSettingsConfig, &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: invalid [PartitionSettings]: duplicate mount point found at '/'", err.Error())
}

func TestShouldSucceedParsingMultipleSameEmptyMounts_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	emptyPartitionSettingsConfig := validSystemConfig
	emptyPartitionSettingsConfig.PartitionSettings = []PartitionSetting{
		{MountPoint: "", MountIdentifier: GetDefaultMountIdentifier()},
		{MountPoint: "", MountIdentifier: GetDefaultMountIdentifier()},
	}

	err := emptyPartitionSettingsConfig.IsValid()
	assert.NoError(t, err)

	err = remarshalJSON(emptyPartitionSettingsConfig, &checkedSystemConfig)
	assert.NoError(t, err)
	assert.Equal(t, emptyPartitionSettingsConfig, checkedSystemConfig)
}

func TestShouldFailParsingBothVerityAndEncryption_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	badBothEncryptionVerityConfig := validSystemConfig
	badBothEncryptionVerityConfig.ReadOnlyVerityRoot = validSystemConfig.ReadOnlyVerityRoot
	badBothEncryptionVerityConfig.ReadOnlyVerityRoot.Enable = true

	err := badBothEncryptionVerityConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [ReadOnlyVerityRoot] and [Encryption]: verity root currently does not support root encryption", err.Error())

	err = remarshalJSON(badBothEncryptionVerityConfig, &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: invalid [ReadOnlyVerityRoot] and [Encryption]: verity root currently does not support root encryption", err.Error())
}

func TestShouldFailParsingInvalidVerityRoot_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	badPartitionSettingsConfig := validSystemConfig
	badPartitionSettingsConfig.ReadOnlyVerityRoot = ReadOnlyVerityRoot{
		Enable:        true,
		Name:          "test",
		TmpfsOverlays: []string{"/nested", "/nested/folder"},
	}
	// Encryption and Verity currently can't coexist
	badPartitionSettingsConfig.Encryption.Enable = false

	err := badPartitionSettingsConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [ReadOnlyVerityRoot]: failed to validate [TmpfsOverlays], overlays may not overlap each other (/nested)(/nested/folder)", err.Error())

	err = remarshalJSON(badPartitionSettingsConfig, &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: failed to parse [ReadOnlyVerityRoot]: failed to validate [TmpfsOverlays], overlays may not overlap each other (/nested)(/nested/folder)", err.Error())
}

func TestShouldFailParsingVerityRootWithNoRoot_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	badPartitionSettingsConfig := validSystemConfig
	// Take only the boot partition (index 0), drop the root (index 1)
	badPartitionSettingsConfig.PartitionSettings = validSystemConfig.PartitionSettings[0:1]
	badPartitionSettingsConfig.ReadOnlyVerityRoot = ReadOnlyVerityRoot{
		Enable: true,
		Name:   "test",
	}

	err := badPartitionSettingsConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [ReadOnlyVerityRoot] or [Encryption]: must have a partition mounted at '/'", err.Error())

	err = remarshalJSON(badPartitionSettingsConfig, &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: invalid [ReadOnlyVerityRoot] or [Encryption]: must have a partition mounted at '/'", err.Error())
}

func TestShouldFailParsingVerityRootWithNoBoot_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	badPartitionSettingsConfig := validSystemConfig
	// Take only the boot partition (index 0), drop the root (index 1)
	badPartitionSettingsConfig.PartitionSettings = validSystemConfig.PartitionSettings[1:2]
	badPartitionSettingsConfig.ReadOnlyVerityRoot = ReadOnlyVerityRoot{
		Enable: true,
		Name:   "test",
	}
	badPartitionSettingsConfig.Encryption.Enable = false

	err := badPartitionSettingsConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [ReadOnlyVerityRoot]: must have a separate partition mounted at '/boot'", err.Error())

	err = remarshalJSON(badPartitionSettingsConfig, &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: invalid [ReadOnlyVerityRoot]: must have a separate partition mounted at '/boot'", err.Error())
}

func TestShouldFailToFindMissingRootPartitionSetting_SystemConfig(t *testing.T) {
	badPartitionSettingsConfig := validSystemConfig

	// Remove all the partition settings
	badPartitionSettingsConfig.PartitionSettings = []PartitionSetting{}

	var partSetting *PartitionSetting = nil
	partSetting = badPartitionSettingsConfig.GetRootPartitionSetting()
	assert.Nil(t, partSetting)
}

func TestShouldSucceedFindingRootPartitionSetting_SystemConfig(t *testing.T) {
	badPartitionSettingsConfig := validSystemConfig

	partSetting := badPartitionSettingsConfig.GetRootPartitionSetting()
	assert.NotNil(t, partSetting)
	assert.Equal(t, "MyRootfs", partSetting.ID)
}

func TestShouldFailToParseInvalidJSON_SystemConfig(t *testing.T) {
	var checkedSystemConfig SystemConfig

	err := marshalJSONString(invalidSystemConfigJSON, &checkedSystemConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [SystemConfig]: json: cannot unmarshal number into Go struct field IntermediateTypeSystemConfig.IsDefault of type bool", err.Error())

}

func TestShouldSetRemoveRpmDbToFalse(t *testing.T) {
	assert.Equal(t, validSystemConfig.RemoveRpmDb, false)
}

func TestShouldFailParsingUnexpectedBootType_SystemConfig(t *testing.T) {
	invalidBootTypeConfig := validSystemConfig
	invalidBootTypeConfig.BootType = "uefi"

	err := invalidBootTypeConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [BootType]: uefi. Expecting values of either 'efi', 'legacy', 'none' or empty string", err.Error())
}

func TestShouldFaiInvalidAdditionalFiles_SystemConfig(t *testing.T) {
	systemConfig := validSystemConfig
	systemConfig.AdditionalFiles = map[string]FileConfigList{"a.txt": {}}

	err := systemConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [AdditionalFiles]: (a.txt): list is empty", err.Error())
}
