// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"encoding/json"
	"fmt"
	"os"
	"reflect"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/ptrutils"

	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	testResult := 0

	expectedConfiguration.DefaultSystemConfig = &expectedConfiguration.SystemConfigs[0]

	logger.InitStderrLog()
	testResult = m.Run()

	os.Exit(testResult)
}

// remarshalJSON takes a struct, marshals it into a JSON format, then
// unmarshals it back into a structure.
func remarshalJSON(structIn interface{}, structOut interface{}) (err error) {
	tIn := reflect.TypeOf(structIn)
	tOut := reflect.TypeOf(structOut)
	if tOut.Kind() != reflect.Ptr {
		return fmt.Errorf("can't remarshal JSON, structOut must be a pointer to a struct")
	}

	if !tIn.ConvertibleTo(tOut.Elem()) {
		return fmt.Errorf("can't remarshal JSON, types are incorrect (%v, %v). Should be (myStruct, *myStruct)", tIn, tOut)
	}
	jsonData, err := json.Marshal(structIn)
	if err != nil {
		return
	}
	err = json.Unmarshal(jsonData, structOut)
	return
}

// marshalJSONString coverts a JSON string into a struct
func marshalJSONString(jsonString string, structOut interface{}) (err error) {
	err = json.Unmarshal([]byte(jsonString), structOut)
	return
}

func TestConfigurationShouldContainExpectedFields(t *testing.T) {
	actualConfiguration, err := Load("testdata/test_configuration.json")
	assert.NoError(t, err)

	logger.Log.Infof("Actual: %v", actualConfiguration)

	assert.Equal(t, expectedConfiguration, actualConfiguration)
}

func TestShouldErrorForMissingFile(t *testing.T) {
	_, err := Load("missing_file.json")
	assert.Error(t, err)
}

func TestShouldSucceedReturnNilDiskForBadPartition(t *testing.T) {
	badPartition := Partition{ID: "NOT_A_REAL_ID"}
	diskPart := expectedConfiguration.GetDiskContainingPartition(&badPartition)
	assert.Nil(t, diskPart)
}

func TestShouldFailForUntaggedEncryptionDeviceMapperRoot(t *testing.T) {
	var checkedConfig Config
	testConfig := expectedConfiguration

	// Copy the current disks, then mangle one by removing the expected dmroot flag
	badDisks := append([]Disk{}, testConfig.Disks...)
	badDiskParts := append([]Partition{}, badDisks[0].Partitions...)
	badDisks[0].Partitions = badDiskParts
	testConfig.Disks = badDisks

	// Clear the flags for the root
	testConfig.GetDiskPartByID(testConfig.SystemConfigs[0].GetRootPartitionSetting().ID).Flags = []PartitionFlag{}

	err := testConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "a config in [SystemConfigs] enables a device mapper based root (Encryption or Read-Only), but partitions are miss-configured: [Partition] 'MyRootfs' must include 'dmroot' device mapper root flag in [Flags] for [SystemConfig] 'SmallerDisk's root partition since it uses [ReadOnlyVerityRoot] or [Encryption]", err.Error())

	err = remarshalJSON(testConfig, &checkedConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Config]: a config in [SystemConfigs] enables a device mapper based root (Encryption or Read-Only), but partitions are miss-configured: [Partition] 'MyRootfs' must include 'dmroot' device mapper root flag in [Flags] for [SystemConfig] 'SmallerDisk's root partition since it uses [ReadOnlyVerityRoot] or [Encryption]", err.Error())
}

func TestShouldFailDeviceMapperWithNoRootPartitions(t *testing.T) {
	var checkedConfig Config
	testConfig := expectedConfiguration

	// Clear the partitions, then add a new non-root partition back
	testConfig.SystemConfigs = append([]SystemConfig{}, testConfig.SystemConfigs...)
	testConfig.Disks = append([]Disk{}, expectedConfiguration.Disks...)
	testConfig.Disks[0].Partitions = []Partition{
		{
			ID: "NotRoot",
			Flags: []PartitionFlag{
				"dmroot",
			},
			Start:  uint64(0),
			End:    uint64(1024),
			FsType: "ext4",
		},
	}
	testConfig.SystemConfigs[0].PartitionSettings = []PartitionSetting{{ID: "NotRoot", MountPoint: "/not/root", MountIdentifier: GetDefaultMountIdentifier()}}

	err := testConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "a config in [SystemConfigs] enables a device mapper based root (Encryption or Read-Only), but partitions are miss-configured: can't find a root ('/') [PartitionSetting] to work with either [ReadOnlyVerityRoot] or [Encryption]", err.Error())

	err = remarshalJSON(testConfig, &checkedConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Config]: failed to parse [SystemConfig]: invalid [ReadOnlyVerityRoot] or [Encryption]: must have a partition mounted at '/'", err.Error())

}

func TestShouldFailDeviceMapperWithMultipleRoots(t *testing.T) {
	var checkedConfig Config
	testConfig := expectedConfiguration

	// Copy the root partition settings
	ExtraDmRoots := []Partition{
		{
			ID: "MyRootfs",
			Flags: []PartitionFlag{
				"dmroot",
			},
			Start:  uint64(0),
			End:    uint64(512),
			FsType: "ext4",
		}, {
			ID: "MySecondRootfs",
			Flags: []PartitionFlag{
				"dmroot",
			},
			Start:  uint64(512),
			End:    uint64(1024),
			FsType: "ext4",
		},
	}
	ExtraPartitionSettings := []PartitionSetting{
		{
			ID:              "MyRootfs",
			MountPoint:      "/",
			MountIdentifier: GetDefaultMountIdentifier(),
		}, {
			ID:              "MySecondRootfs",
			MountPoint:      "/OtherRoot",
			MountIdentifier: GetDefaultMountIdentifier(),
		},
	}

	// Copy the disks, then add the extra partition
	testConfig.Disks = append([]Disk{}, expectedConfiguration.Disks...)
	testConfig.Disks[0].Partitions = ExtraDmRoots
	// Copy the partition settings, then add the extra partition setting
	testConfig.SystemConfigs = append([]SystemConfig{}, expectedConfiguration.SystemConfigs[0])
	testConfig.SystemConfigs[0].PartitionSettings = ExtraPartitionSettings

	err := testConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "a config in [SystemConfigs] enables a device mapper based root (Encryption or Read-Only), but partitions are miss-configured: [SystemConfig] 'SmallerDisk' includes two (or more) device mapper root [PartitionSettings] 'MyRootfs' and 'MySecondRootfs', include only one", err.Error())

	// remarshal runs IsValid() on [SystemConfig] prior to running it on [Config], so we get a different error message here.
	err = remarshalJSON(testConfig, &checkedConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Config]: a config in [SystemConfigs] enables a device mapper based root (Encryption or Read-Only), but partitions are miss-configured: [SystemConfig] 'SmallerDisk' includes two (or more) device mapper root [PartitionSettings] 'MyRootfs' and 'MySecondRootfs', include only one", err.Error())

}

func TestShouldFailDuplicatedIDs(t *testing.T) {
	var checkedConfig Config
	testConfig := expectedConfiguration

	// Copy the disks, then add some duplicate IDs
	// First on the same disk
	testConfig.Disks = append([]Disk{}, expectedConfiguration.Disks...)
	testConfig.Disks[0].Partitions = append([]Partition{}, expectedConfiguration.Disks[0].Partitions...)
	testConfig.Disks[0].Partitions = append(testConfig.Disks[0].Partitions, Partition{ID: "duplicatedID"})
	testConfig.Disks[0].Partitions = append(testConfig.Disks[0].Partitions, Partition{ID: "duplicatedID"})

	err := testConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [Config]: a [Partition] on a [Disk] '0' shares an ID 'duplicatedID' with another partition (on disk '0')", err.Error())

	err = remarshalJSON(testConfig, &checkedConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Config]: invalid [Config]: a [Partition] on a [Disk] '0' shares an ID 'duplicatedID' with another partition (on disk '0')", err.Error())

	// Reset the config, then try across disks
	testConfig.Disks = append([]Disk{}, expectedConfiguration.Disks...)
	testConfig.Disks[0].Partitions = append([]Partition{}, expectedConfiguration.Disks[0].Partitions...)
	testConfig.Disks[1].Partitions = append([]Partition{}, expectedConfiguration.Disks[1].Partitions...)
	testConfig.Disks[0].Partitions = append(testConfig.Disks[0].Partitions, Partition{ID: "duplicatedID"})
	testConfig.Disks[1].Partitions = append(testConfig.Disks[1].Partitions, Partition{ID: "duplicatedID"})

	err = testConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [Config]: a [Partition] on a [Disk] '0' shares an ID 'duplicatedID' with another partition (on disk '1')", err.Error())

	err = remarshalJSON(testConfig, &checkedConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Config]: invalid [Config]: a [Partition] on a [Disk] '0' shares an ID 'duplicatedID' with another partition (on disk '1')", err.Error())
}

func TestShouldFailMissingPartition(t *testing.T) {
	var checkedConfig Config
	testConfig := expectedConfiguration

	testConfig.Disks = append([]Disk{}, expectedConfiguration.Disks...)
	testConfig.SystemConfigs = append([]SystemConfig{}, expectedConfiguration.SystemConfigs...)
	testConfig.SystemConfigs[0].PartitionSettings = append([]PartitionSetting{}, expectedConfiguration.SystemConfigs[0].PartitionSettings...)
	testConfig.SystemConfigs[0].PartitionSettings[0].ID = "NOT_AN_ID"

	err := testConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [Config]: [SystemConfig] 'SmallerDisk' mounts a [Partition] 'NOT_AN_ID' which has no corresponding partition on a [Disk]", err.Error())

	err = remarshalJSON(testConfig, &checkedConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Config]: invalid [Config]: [SystemConfig] 'SmallerDisk' mounts a [Partition] 'NOT_AN_ID' which has no corresponding partition on a [Disk]", err.Error())
}

func TestShouldFailMissmatchedGPTMountsWithNonMBRDisk(t *testing.T) {
	var checkedConfig Config
	testConfig := expectedConfiguration

	testConfig.Disks = append([]Disk{}, expectedConfiguration.Disks...)
	testConfig.Disks[0].PartitionTableType = PartitionTableTypeMbr
	testConfig.Disks[0].Partitions = append([]Partition{}, expectedConfiguration.Disks[0].Partitions...)
	testConfig.Disks[0].Partitions[0].Name = "LABEL_NAME"

	testConfig.SystemConfigs = append([]SystemConfig{}, expectedConfiguration.SystemConfigs...)
	testConfig.SystemConfigs[0].PartitionSettings = append([]PartitionSetting{}, expectedConfiguration.SystemConfigs[0].PartitionSettings...)
	testConfig.SystemConfigs[0].PartitionSettings[0].MountIdentifier = MountIdentifierPartLabel

	err := testConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [Config]: [SystemConfig] 'SmallerDisk' mounts a [Partition] 'MyBoot' via PARTLABEL, but that partition is on an MBR disk which does not support PARTLABEL", err.Error())

	err = remarshalJSON(testConfig, &checkedConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Config]: invalid [Config]: [SystemConfig] 'SmallerDisk' mounts a [Partition] 'MyBoot' via PARTLABEL, but that partition is on an MBR disk which does not support PARTLABEL", err.Error())
}

func TestShouldFailPartLabelWithNoName(t *testing.T) {
	var checkedConfig Config
	testConfig := expectedConfiguration

	testConfig.SystemConfigs = append([]SystemConfig{}, expectedConfiguration.SystemConfigs...)
	testConfig.SystemConfigs[0].PartitionSettings = append([]PartitionSetting{}, expectedConfiguration.SystemConfigs[0].PartitionSettings...)
	testConfig.SystemConfigs[0].PartitionSettings[0].MountIdentifier = MountIdentifierPartLabel

	err := testConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid [Config]: [SystemConfig] 'SmallerDisk' mounts a [Partition] 'MyBoot' via PARTLABEL, but it has no [Name]", err.Error())

	err = remarshalJSON(testConfig, &checkedConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Config]: invalid [Config]: [SystemConfig] 'SmallerDisk' mounts a [Partition] 'MyBoot' via PARTLABEL, but it has no [Name]", err.Error())
}

func TestShouldSucceedReturnPartitionIndexAndObjectForBootPartition(t *testing.T) {
	actualConfiguration, err := Load("testdata/test_configuration.json")
	assert.NoError(t, err)
	bootIndex, bootPartition := actualConfiguration.GetBootPartition()
	assert.ObjectsAreEqualValues(expectedConfiguration.Disks[0].Partitions[0], bootPartition)
	assert.Equal(t, 0, bootIndex)
}

var expectedConfiguration Config = Config{
	Disks: []Disk{
		{
			PartitionTableType: "gpt",
			MaxSize:            uint64(1024),
			TargetDisk: TargetDisk{
				Type:  "path",
				Value: "/dev/sda",
			},
			Artifacts: []Artifact{
				{
					Name:        "CompressedVHD",
					Type:        "vhd",
					Compression: "gz",
				},
				{
					Name: "UncompressedVHD",
					Type: "vhd",
				},
			},
			RawBinaries: []RawBinary{
				{
					BinPath:   "binaries/1.bin",
					BlockSize: uint64(1024),
					Seek:      uint64(1),
				},
				{
					BinPath:   "binaries/2.bin",
					BlockSize: uint64(1024),
					Seek:      uint64(2),
				},
			},
			Partitions: []Partition{
				{
					ID: "MyBoot",
					Flags: []PartitionFlag{
						"esp",
						"boot",
					},
					Start:  uint64(3),
					End:    uint64(9),
					FsType: "fat32",
				},
				{
					ID: "MyRootfs",
					Flags: []PartitionFlag{
						"dmroot",
					},
					Start:  uint64(9),
					End:    uint64(1024),
					FsType: "ext4",
				},
			},
		},
		{
			PartitionTableType: "mbr",
			MaxSize:            uint64(4096),
			TargetDisk: TargetDisk{
				Type:  "path",
				Value: "/dev/sdb",
			},
			Partitions: []Partition{
				{
					ID: "MyBootA",
					Flags: []PartitionFlag{
						"boot",
					},
					Start:  uint64(3),
					FsType: "fat32",
				},
				{
					ID:     "MyRootfsA",
					Start:  uint64(9),
					End:    uint64(1024),
					FsType: "ext4",
					Flags: []PartitionFlag{
						"dmroot",
					},
				},
				{
					ID: "MyBootB",
					Flags: []PartitionFlag{
						"boot",
					},
					Start:  uint64(1024),
					FsType: "fat32",
				},
				{
					ID:     "MyRootfsB",
					Start:  uint64(1033),
					End:    uint64(2048),
					FsType: "ext4",
					Flags: []PartitionFlag{
						"dmroot",
					},
				},
				{
					ID:     "SharedData",
					Start:  uint64(2048),
					End:    uint64(0),
					FsType: "ext4",
				},
			},
		},
	},
	SystemConfigs: []SystemConfig{
		{
			Name:      "SmallerDisk",
			IsDefault: true,
			PartitionSettings: []PartitionSetting{
				{
					ID:              "MyBoot",
					MountPoint:      "/boot",
					MountIdentifier: "partuuid",
					MountOptions:    "ro,exec",
					RdiffBaseImage:  "../out/images/core-efi/core-efi-1.0.20200918.1751.ext4",
				},
				{
					ID:               "MyRootfs",
					MountPoint:       "/",
					MountIdentifier:  "partuuid",
					RemoveDocs:       true,
					OverlayBaseImage: "../out/images/core-efi/core-efi-1.0.20200918.1751.ext4",
				},
			},
			PackageLists: []string{
				"path/to/packages.json",
				"path/to/extraPackages.json",
			},
			Packages: []string{
				"additionalPkgName",
			},
			KernelOptions: map[string]string{
				"default": "kernel",
			},
			AdditionalFiles: map[string]FileConfigList{
				"local/path/file1": {{Path: "/final/system/path"}},
				"local/path/file2": {{Path: "/final/system/path/renamedfile2"}},
				"local/path/file3": {{Path: "/final/system/path/file3"}},
				"local/path/file4": {{Path: "/final/system/path/file4", Permissions: ptrutils.PtrTo(FilePermissions(0o664))}},
				"local/path/file5": {{Path: "/final/system/path/file5"}},
				"local/path/file6": {{Path: "/final/system/path/file6"}, {Path: "/final/system/path/file6_copy"}},
			},
			Hostname: "Mariner-Test",
			BootType: "efi",
			Groups: []Group{
				{
					Name: "groupa",
				},
				{
					Name: "groupb",
				},
				{
					Name: "testgroup",
					GID:  "109",
				},
			},
			Users: []User{
				{
					Name:     "basicuser",
					Password: "abc",
				},
				{
					Name:                "advancedSecureCoolUser",
					Password:            "$6$7oFZAqiJ$EqnWLXsSLwX.wrIHDH8iDGou3BgFXxx0NgMJgJ5LSYjGA09BIUwjTNO31LrS2C9890P8SzYkyU6FYsYNihEgp0",
					PasswordHashed:      true,
					PasswordExpiresDays: int64(99999),
					UID:                 "105",
					PrimaryGroup:        "testgroup",
					SecondaryGroups: []string{
						"groupa",
						"groupb",
					},
					SSHPubKeyPaths: []string{
						"firstSSHKey.pub",
						"secondSSHKey.pub",
					},
					StartupCommand: "/usr/bin/somescript",
				},
			},
			PackageRepos: []PackageRepo{
				{
					Name:         "repo1",
					BaseUrl:      "https://repo1.com",
					Install:      true,
					GPGCheck:     true,
					RepoGPGCheck: true,
					GPGKeys:      "file:///etc/pki/rpm-gpg/MY-CUSTOM-KEY",
				},
				{
					Name:         "repo2",
					BaseUrl:      "https://repo2.com",
					Install:      false,
					GPGCheck:     false,
					RepoGPGCheck: false,
					GPGKeys:      "file:///etc/pki/rpm-gpg/MICROSOFT-RPM-GPG-KEY file:///etc/pki/rpm-gpg/MICROSOFT-METADATA-GPG-KEY",
				},
			},
			PreInstallScripts: []InstallScript{
				{
					Path: "arglessPreScript.sh",
				},
				{
					Path: "PreScriptWithArguments.sh",
					Args: "--input abc --output cba",
				},
			},
			PostInstallScripts: []InstallScript{
				{
					Path: "arglessScript.sh",
				},
				{
					Path: "thisOneNeedsArguments.sh",
					Args: "--input abc --output cba",
				},
			},
			FinalizeImageScripts: []InstallScript{
				{
					Path: "arglessScript.sh",
				},
				{
					Path: "thisOneNeedsArguments.sh",
					Args: "--input abc --output cba",
				},
			},
			Networks: []Network{
				{
					BootProto: "dhcp",
					GateWay:   "192.168.20.4",
					Ip:        "192.169.20.148",
					NetMask:   "255.255.255.0",
					OnBoot:    false,
					NameServers: []string{
						"192.168.30.23",
					},
					Device: "eth0",
				},
			},
			Encryption: RootEncryption{
				Enable:   true,
				Password: "EncryptPassphrase123",
			},
			RemoveRpmDb: false,
			ReadOnlyVerityRoot: ReadOnlyVerityRoot{
				Enable:                       false,
				Name:                         "verity_root_fs",
				ErrorCorrectionEnable:        true,
				ErrorCorrectionEncodingRoots: 2,
				RootHashSignatureEnable:      false,
				VerityErrorBehavior:          "",
				TmpfsOverlays:                nil,
				TmpfsOverlaySize:             "20%",
			},
			EnableHidepid: true,
		},
		{
			Name: "BiggerDiskA",
			PartitionSettings: []PartitionSetting{
				{
					ID:              "MyBootA",
					MountPoint:      "/boot",
					MountIdentifier: "uuid",
				},
				{
					ID:              "MyRootfsA",
					MountPoint:      "/",
					MountIdentifier: "uuid",
					RemoveDocs:      true,
				},
				{
					ID:              "SharedData",
					MountPoint:      "/some/path/to/data",
					MountIdentifier: "partuuid",
					MountOptions:    "ro,noexec",
				},
			},
			PackageLists: []string{
				"path/to/packages.json",
			},
			KernelOptions: map[string]string{
				"default": "kernel",
			},
			Hostname: "Mariner-TestA",
			Users: []User{
				{
					Name:     "basicuser",
					Password: "abc",
				},
			},
		},
		{
			Name: "BiggerDiskB",
			PartitionSettings: []PartitionSetting{
				{
					ID:              "MyBootB",
					MountPoint:      "/boot",
					MountIdentifier: "partuuid",
				},
				{
					ID:              "MyRootfsB",
					MountPoint:      "/",
					MountIdentifier: "partuuid",
					RemoveDocs:      true,
				},
				{
					ID:              "SharedData",
					MountPoint:      "/some/path/to/data",
					MountIdentifier: "partuuid",
					MountOptions:    "ro,noexec",
				},
			},
			PackageLists: []string{
				"path/to/packages.json",
			},
			KernelOptions: map[string]string{
				"default": "kernel",
			},
			Hostname: "Mariner-TestB",
			Users: []User{
				{
					Name:     "basicuser",
					Password: "abc",
				},
			},
		},
	},
}
