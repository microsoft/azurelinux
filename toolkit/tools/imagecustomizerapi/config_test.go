// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestConfigIsValid(t *testing.T) {
	config := &Config{
		Disks: &[]Disk{{
			PartitionTableType: "gpt",
			MaxSize:            2,
			Partitions: []Partition{
				{
					ID:             "esp",
					FileSystemType: "fat32",
					Start:          1,
					Flags: []PartitionFlag{
						"esp",
						"boot",
					},
				},
			},
		}},
		OS: OS{
			BootType:            "efi",
			ResetBootLoaderType: "hard-reset",
			Hostname:            "test",
			PartitionSettings: []PartitionSetting{
				{
					ID:         "esp",
					MountPoint: "/boot/efi",
				},
			},
		},
	}

	err := config.IsValid()
	assert.NoError(t, err)
}

func TestConfigIsValidLegacy(t *testing.T) {
	config := &Config{
		Disks: &[]Disk{{
			PartitionTableType: "gpt",
			MaxSize:            2,
			Partitions: []Partition{
				{
					ID:             "boot",
					FileSystemType: "fat32",
					Start:          1,
					Flags: []PartitionFlag{
						"bios-grub",
					},
				},
			},
		}},
		OS: OS{
			BootType:            "legacy",
			ResetBootLoaderType: "hard-reset",
			Hostname:            "test",
		},
	}

	err := config.IsValid()
	assert.NoError(t, err)
}

func TestConfigIsValidNoBootType(t *testing.T) {
	config := &Config{
		Disks: &[]Disk{{
			PartitionTableType: "gpt",
			MaxSize:            2,
			Partitions: []Partition{
				{
					ID:             "a",
					FileSystemType: "ext4",
					Start:          1,
				},
			},
		}},
		OS: OS{
			Hostname:            "test",
			ResetBootLoaderType: "hard-reset",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "bootType")
	assert.ErrorContains(t, err, "disks")
}

func TestConfigIsValidMissingBootLoaderReset(t *testing.T) {
	config := &Config{
		Disks: &[]Disk{{
			PartitionTableType: "gpt",
			MaxSize:            2,
			Partitions: []Partition{
				{
					ID:             "a",
					FileSystemType: "ext4",
					Start:          1,
				},
			},
		}},
		OS: OS{
			Hostname: "test",
			BootType: "efi",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "resetBootLoaderType")
	assert.ErrorContains(t, err, "disks")
}

func TestConfigIsValidMultipleDisks(t *testing.T) {
	config := &Config{
		Disks: &[]Disk{
			{
				PartitionTableType: "gpt",
				MaxSize:            1,
			},
			{
				PartitionTableType: "gpt",
				MaxSize:            1,
			},
		},
		OS: OS{
			BootType:            "legacy",
			ResetBootLoaderType: "hard-reset",
			Hostname:            "test",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "multiple disks")
}

func TestConfigIsValidZeroDisks(t *testing.T) {
	config := &Config{
		Disks: &[]Disk{},
		OS: OS{
			Hostname: "test",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "1 disk")
}

func TestConfigIsValidBadHostname(t *testing.T) {
	config := &Config{
		OS: OS{
			Hostname: "test_",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid hostname")
}

func TestConfigIsValidBadDisk(t *testing.T) {
	config := &Config{
		Disks: &[]Disk{{
			PartitionTableType: PartitionTableTypeGpt,
			MaxSize:            0,
		}},
		OS: OS{
			Hostname: "test",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "maxSize")
}

func TestConfigIsValidMissingEsp(t *testing.T) {
	config := &Config{
		Disks: &[]Disk{{
			PartitionTableType: "gpt",
			MaxSize:            2,
			Partitions:         []Partition{},
		}},
		OS: OS{
			BootType:            "efi",
			ResetBootLoaderType: "hard-reset",
			Hostname:            "test",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "esp")
	assert.ErrorContains(t, err, "efi")
}

func TestConfigIsValidMissingBiosBoot(t *testing.T) {
	config := &Config{
		Disks: &[]Disk{{
			PartitionTableType: "gpt",
			MaxSize:            2,
			Partitions:         []Partition{},
		}},
		OS: OS{
			BootType:            "legacy",
			ResetBootLoaderType: "hard-reset",
			Hostname:            "test",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "bios-grub")
	assert.ErrorContains(t, err, "legacy")
}

func TestConfigIsValidInvalidMountPoint(t *testing.T) {
	config := &Config{
		Disks: &[]Disk{{
			PartitionTableType: "gpt",
			MaxSize:            2,
			Partitions: []Partition{
				{
					ID:             "esp",
					FileSystemType: "fat32",
					Start:          1,
					Flags: []PartitionFlag{
						"esp",
						"boot",
					},
				},
			},
		}},
		OS: OS{
			BootType:            "efi",
			ResetBootLoaderType: "hard-reset",
			Hostname:            "test",
			PartitionSettings: []PartitionSetting{
				{
					ID:         "esp",
					MountPoint: "boot/efi",
				},
			},
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "mountPoint")
	assert.ErrorContains(t, err, "absolute path")
}

func TestConfigIsValidInvalidPartitionId(t *testing.T) {
	config := &Config{
		Disks: &[]Disk{{
			PartitionTableType: "gpt",
			MaxSize:            2,
			Partitions: []Partition{
				{
					ID:             "esp",
					FileSystemType: "fat32",
					Start:          1,
					Flags: []PartitionFlag{
						"esp",
						"boot",
					},
				},
			},
		}},
		OS: OS{
			BootType:            "efi",
			ResetBootLoaderType: "hard-reset",
			Hostname:            "test",
			PartitionSettings: []PartitionSetting{
				{
					ID:         "boot",
					MountPoint: "/boot/efi",
				},
			},
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "partition")
	assert.ErrorContains(t, err, "id")
}

func TestConfigIsValidPartitionSettingsMissingDisks(t *testing.T) {
	config := &Config{
		OS: OS{
			Hostname: "test",
			PartitionSettings: []PartitionSetting{
				{
					ID:         "esp",
					MountPoint: "/boot/efi",
				},
			},
		},
	}
	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "disks")
	assert.ErrorContains(t, err, "bootType")
	assert.ErrorContains(t, err, "partitionSettings")
}

func TestConfigIsValidBootTypeMissingDisks(t *testing.T) {
	config := &Config{
		OS: OS{
			Hostname:            "test",
			BootType:            BootTypeEfi,
			ResetBootLoaderType: "hard-reset",
			KernelCommandLine: KernelCommandLine{
				ExtraCommandLine: "console=ttyS0",
			},
		},
	}
	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "os.bootType and disks must be specified together")
}

func TestConfigIsValidKernelCLI(t *testing.T) {
	config := &Config{
		Disks: &[]Disk{{
			PartitionTableType: "gpt",
			MaxSize:            2,
			Partitions: []Partition{
				{
					ID:             "esp",
					FileSystemType: "fat32",
					Start:          1,
					Flags: []PartitionFlag{
						"esp",
						"boot",
					},
				},
			},
		}},
		OS: OS{
			BootType:            "efi",
			ResetBootLoaderType: "hard-reset",
			Hostname:            "test",
			PartitionSettings: []PartitionSetting{
				{
					ID:         "esp",
					MountPoint: "/boot/efi",
				},
			},
			KernelCommandLine: KernelCommandLine{
				ExtraCommandLine: "console=ttyS0",
			},
		},
	}
	err := config.IsValid()
	assert.NoError(t, err)
}
