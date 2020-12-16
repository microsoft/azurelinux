// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"encoding/json"
	"fmt"
	"os"
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
	"microsoft.com/pkggen/internal/logger"
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

func TestShouldFailDeviceMapperWithNoRootDisks(t *testing.T) {
	var checkedConfig Config
	testConfig := expectedConfiguration

	// Clear the disks, add one empty one
	testConfig.Disks = []Disk{{}}

	err := testConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "a config in [SystemConfigs] enables a device mapper based root (Encryption or Read-Only), but partitions are miss-configured: can't find a [Disk] [Partition] to match with [PartitionSetting] 'MyRootfs'", err.Error())

	err = remarshalJSON(testConfig, &checkedConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Config]: a config in [SystemConfigs] enables a device mapper based root (Encryption or Read-Only), but partitions are miss-configured: can't find a [Disk] [Partition] to match with [PartitionSetting] 'MyRootfs'", err.Error())
}

func TestShouldFailDeviceMapperWithNoRootPartitions(t *testing.T) {
	var checkedConfig Config
	testConfig := expectedConfiguration

	// Clear the partitions, then add a missmatching one
	testConfig.SystemConfigs = append([]SystemConfig{}, testConfig.SystemConfigs...)
	testConfig.SystemConfigs[0].PartitionSettings = []PartitionSetting{{ID: "NotRoot", MountPoint: "/not/root"}}

	err := testConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "a config in [SystemConfigs] enables a device mapper based root (Encryption or Read-Only), but partitions are miss-configured: can't find a root ('/') [PartitionSetting] to work with either [ReadOnlyVerityRoot] or [Encryption]", err.Error())

	// remarshal runs IsValid() on [SystemConfig] prior to running it on [Config], so we get a different error message here.
	err = remarshalJSON(testConfig, &checkedConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Config]: failed to parse [SystemConfig]: invalid [ReadOnlyVerityRoot] or [Encryption]: must have a partition mounted at '/'", err.Error())

}

func TestShouldFailDeviceMapperWithMultipleRoots(t *testing.T) {
	var checkedConfig Config
	testConfig := expectedConfiguration

	// Copy the root partition settings
	ExtraDmRoot := Partition{
		ID: "MySecondRootfs",
		Flags: []PartitionFlag{
			"dmroot",
		},
		Start:  uint64(1024),
		End:    uint64(2048),
		FsType: "ext4",
	}
	ExtraPartitionSetting := PartitionSetting{
		ID:         "MySecondRootfs",
		MountPoint: "/OtherRoot",
	}

	// Copy the disks, then add the extra partition
	testConfig.Disks = append([]Disk{}, expectedConfiguration.Disks...)
	testConfig.Disks[0].Partitions = append(testConfig.Disks[0].Partitions, ExtraDmRoot)
	// Copy the partition settings, then add the extra partition setting
	testConfig.SystemConfigs = append([]SystemConfig{}, expectedConfiguration.SystemConfigs[0])
	testConfig.SystemConfigs[0].PartitionSettings = append(testConfig.SystemConfigs[0].PartitionSettings, ExtraPartitionSetting)

	err := testConfig.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "a config in [SystemConfigs] enables a device mapper based root (Encryption or Read-Only), but partitions are miss-configured: [SystemConfig] 'SmallerDisk' includes two (or more) device mapper root [PartitionSettings] 'MyRootfs' and 'MySecondRootfs', include only one", err.Error())

	// remarshal runs IsValid() on [SystemConfig] prior to running it on [Config], so we get a different error message here.
	err = remarshalJSON(testConfig, &checkedConfig)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [Config]: a config in [SystemConfigs] enables a device mapper based root (Encryption or Read-Only), but partitions are miss-configured: [SystemConfig] 'SmallerDisk' includes two (or more) device mapper root [PartitionSettings] 'MyRootfs' and 'MySecondRootfs', include only one", err.Error())

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
					ID:           "MyBoot",
					MountPoint:   "/boot",
					MountOptions: "ro,exec",
				},
				{
					ID:         "MyRootfs",
					MountPoint: "/",
					RemoveDocs: true,
				},
			},
			PackageLists: []string{
				"path/to/packages.json",
				"path/to/extraPackages.json",
			},
			KernelOptions: map[string]string{
				"default": "kernel",
				"hyperv":  "kernel-hyperv",
			},
			AdditionalFiles: map[string]string{
				"local/path/file1": "/final/system/path",
				"local/path/file2": "/final/system/path/renamedfile2",
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
			PostInstallScripts: []PostInstallScript{
				{
					Path: "arglessScript.sh",
				},
				{
					Path: "thisOneNeedsArguments.sh",
					Args: "--input abc --output cba",
				},
			},
			Encryption: RootEncryption{
				Enable:   true,
				Password: "EncryptPassphrase123",
			},
			RemoveRpmDb: false,
		},
		{
			Name: "BiggerDiskA",
			PartitionSettings: []PartitionSetting{
				{
					ID:         "MyBootA",
					MountPoint: "/boot",
				},
				{
					ID:         "MyRootfsA",
					MountPoint: "/",
					RemoveDocs: true,
				},
				{
					ID:           "SharedData",
					MountPoint:   "/some/path/to/data",
					MountOptions: "ro,noexec",
				},
			},
			PackageLists: []string{
				"path/to/packages.json",
			},
			KernelOptions: map[string]string{
				"default": "kernel",
				"hyperv":  "kernel-hyperv",
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
					ID:         "MyBootB",
					MountPoint: "/boot",
				},
				{
					ID:         "MyRootfsB",
					MountPoint: "/",
					RemoveDocs: true,
				},
				{
					ID:           "SharedData",
					MountPoint:   "/some/path/to/data",
					MountOptions: "ro,noexec",
				},
			},
			PackageLists: []string{
				"path/to/packages.json",
			},
			KernelOptions: map[string]string{
				"default": "kernel",
				"hyperv":  "kernel-hyperv",
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
