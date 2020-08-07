// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"os"
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
		Disk{
			PartitionTableType: "gpt",
			MaxSize:            uint64(1024),
			TargetDisk: TargetDisk{
				Type:  "path",
				Value: "/dev/sda",
			},
			Artifacts: []Artifact{
				Artifact{
					Name:        "CompressedVHD",
					Type:        "vhd",
					Compression: "gz",
				},
				Artifact{
					Name: "UncompressedVHD",
					Type: "vhd",
				},
			},
			RawBinaries: []RawBinary{
				RawBinary{
					BinPath:   "binaries/1.bin",
					BlockSize: uint64(1024),
					Seek:      uint64(1),
				},
				RawBinary{
					BinPath:   "binaries/2.bin",
					BlockSize: uint64(1024),
					Seek:      uint64(2),
				},
			},
			Partitions: []Partition{
				Partition{
					ID: "MyBoot",
					Flags: []string{
						"esp",
						"boot",
					},
					Start:  uint64(3),
					End:    uint64(9),
					FsType: "fat32",
				},
				Partition{
					ID:     "MyRootfs",
					Start:  uint64(9),
					End:    uint64(1024),
					FsType: "ext4",
				},
			},
		},
		Disk{
			PartitionTableType: "mbr",
			MaxSize:            uint64(4096),
			TargetDisk: TargetDisk{
				Type:  "path",
				Value: "/dev/sdb",
			},
			Partitions: []Partition{
				Partition{
					ID: "MyBootA",
					Flags: []string{
						"boot",
					},
					Start:  uint64(3),
					FsType: "fat32",
				},
				Partition{
					ID:     "MyRootfsA",
					Start:  uint64(9),
					End:    uint64(1024),
					FsType: "ext4",
				},
				Partition{
					ID: "MyBootB",
					Flags: []string{
						"boot",
					},
					Start:  uint64(1024),
					FsType: "fat32",
				},
				Partition{
					ID:     "MyRootfsB",
					Start:  uint64(1033),
					End:    uint64(2048),
					FsType: "ext4",
				},
				Partition{
					ID:     "SharedData",
					Start:  uint64(2048),
					End:    uint64(0),
					FsType: "ext4",
				},
			},
		},
	},
	SystemConfigs: []SystemConfig{
		SystemConfig{
			Name:      "SmallerDisk",
			IsDefault: true,
			PartitionSettings: []PartitionSetting{
				PartitionSetting{
					ID:           "MyBoot",
					MountPoint:   "/boot",
					MountOptions: "ro,exec",
				},
				PartitionSetting{
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
				Group{
					Name: "groupa",
				},
				Group{
					Name: "groupb",
				},
				Group{
					Name: "testgroup",
					GID:  "109",
				},
			},
			Users: []User{
				User{
					Name:     "basicuser",
					Password: "abc",
				},
				User{
					Name:                "advancedSecureCoolUser",
					Password:            "$6$7oFZAqiJ$EqnWLXsSLwX.wrIHDH8iDGou3BgFXxx0NgMJgJ5LSYjGA09BIUwjTNO31LrS2C9890P8SzYkyU6FYsYNihEgp0",
					PasswordHashed:      true,
					PasswordExpiresDays: uint64(99999),
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
				PostInstallScript{
					Path: "arglessScript.sh",
				},
				PostInstallScript{
					Path: "thisOneNeedsArguments.sh",
					Args: "--input abc --output cba",
				},
			},
			Encryption: RootEncryption{
				Enable:   true,
				Password: "EncryptPassphrase123",
			},
		},
		SystemConfig{
			Name: "BiggerDiskA",
			PartitionSettings: []PartitionSetting{
				PartitionSetting{
					ID:         "MyBootA",
					MountPoint: "/boot",
				},
				PartitionSetting{
					ID:         "MyRootfsA",
					MountPoint: "/",
					RemoveDocs: true,
				},
				PartitionSetting{
					ID:           "SharedData",
					MountPoint:   "/some/path/to/data",
					MountOptions: "ro,noexec",
				},
			},
			PackageLists: []string{
				"path/to/packages.json",
			},
			Hostname: "Mariner-TestA",
			Users: []User{
				User{
					Name:     "basicuser",
					Password: "abc",
				},
			},
		},
		SystemConfig{
			Name: "BiggerDiskB",
			PartitionSettings: []PartitionSetting{
				PartitionSetting{
					ID:         "MyBootB",
					MountPoint: "/boot",
				},
				PartitionSetting{
					ID:         "MyRootfsB",
					MountPoint: "/",
					RemoveDocs: true,
				},
				PartitionSetting{
					ID:           "SharedData",
					MountPoint:   "/some/path/to/data",
					MountOptions: "ro,noexec",
				},
			},
			PackageLists: []string{
				"path/to/packages.json",
			},
			Hostname: "Mariner-TestB",
			Users: []User{
				User{
					Name:     "basicuser",
					Password: "abc",
				},
			},
		},
	},
}
