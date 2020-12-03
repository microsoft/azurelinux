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
					Flags: []string{
						"esp",
						"boot",
					},
					Start:  uint64(3),
					End:    uint64(9),
					FsType: "fat32",
				},
				{
					ID:     "MyRootfs",
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
					Flags: []string{
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
				},
				{
					ID: "MyBootB",
					Flags: []string{
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
