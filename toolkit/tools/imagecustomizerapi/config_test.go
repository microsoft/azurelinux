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
					ID:     "esp",
					FsType: "fat32",
					Start:  1,
					Flags: []PartitionFlag{
						"esp",
						"boot",
					},
				},
			},
		}},
		SystemConfig: SystemConfig{
			BootType: "efi",
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
	assert.NoError(t, err)
}

func TestConfigIsValidLegacy(t *testing.T) {
	config := &Config{
		Disks: &[]Disk{{
			PartitionTableType: "gpt",
			MaxSize:            2,
			Partitions: []Partition{
				{
					ID:     "boot",
					FsType: "fat32",
					Start:  1,
					Flags: []PartitionFlag{
						"bios_grub",
					},
				},
			},
		}},
		SystemConfig: SystemConfig{
			BootType: "legacy",
			Hostname: "test",
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
					ID:     "a",
					FsType: "ext4",
					Start:  1,
				},
			},
		}},
		SystemConfig: SystemConfig{
			Hostname: "test",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "BootType")
	assert.ErrorContains(t, err, "Disks")
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
		SystemConfig: SystemConfig{
			Hostname: "test",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "multiple disks")
}

func TestConfigIsValidZeroDisks(t *testing.T) {
	config := &Config{
		Disks: &[]Disk{},
		SystemConfig: SystemConfig{
			Hostname: "test",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "1 disk")
}

func TestConfigIsValidBadHostname(t *testing.T) {
	config := &Config{
		SystemConfig: SystemConfig{
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
		SystemConfig: SystemConfig{
			Hostname: "test",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "MaxSize")
}

func TestConfigIsValidMissingEsp(t *testing.T) {
	config := &Config{
		Disks: &[]Disk{{
			PartitionTableType: "gpt",
			MaxSize:            2,
			Partitions:         []Partition{},
		}},
		SystemConfig: SystemConfig{
			BootType: "efi",
			Hostname: "test",
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
		SystemConfig: SystemConfig{
			BootType: "legacy",
			Hostname: "test",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "bios_grub")
	assert.ErrorContains(t, err, "legacy")
}

func TestConfigIsValidInvalidMountPoint(t *testing.T) {
	config := &Config{
		Disks: &[]Disk{{
			PartitionTableType: "gpt",
			MaxSize:            2,
			Partitions: []Partition{
				{
					ID:     "esp",
					FsType: "fat32",
					Start:  1,
					Flags: []PartitionFlag{
						"esp",
						"boot",
					},
				},
			},
		}},
		SystemConfig: SystemConfig{
			BootType: "efi",
			Hostname: "test",
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
	assert.ErrorContains(t, err, "MountPoint")
	assert.ErrorContains(t, err, "absolute path")
}

func TestConfigIsValidInvalidPartitionId(t *testing.T) {
	config := &Config{
		Disks: &[]Disk{{
			PartitionTableType: "gpt",
			MaxSize:            2,
			Partitions: []Partition{
				{
					ID:     "esp",
					FsType: "fat32",
					Start:  1,
					Flags: []PartitionFlag{
						"esp",
						"boot",
					},
				},
			},
		}},
		SystemConfig: SystemConfig{
			BootType: "efi",
			Hostname: "test",
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
	assert.ErrorContains(t, err, "ID")
}

func TestConfigIsValidPartitionSettingsMissingDisks(t *testing.T) {
	config := &Config{
		SystemConfig: SystemConfig{
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
	assert.ErrorContains(t, err, "Disks")
	assert.ErrorContains(t, err, "BootType")
	assert.ErrorContains(t, err, "PartitionSettings")
}

func TestConfigIsValidBootTypeMissingDisks(t *testing.T) {
	config := &Config{
		SystemConfig: SystemConfig{
			Hostname: "test",
			BootType: BootTypeEfi,
			KernelCommandLine: KernelCommandLine{
				ExtraCommandLine: "console=ttyS0",
			},
		},
	}
	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "SystemConfig.BootType and Disks must be specified together")
}

func TestConfigIsValidKernelCLI(t *testing.T) {
	config := &Config{
		Disks: &[]Disk{{
			PartitionTableType: "gpt",
			MaxSize:            2,
			Partitions: []Partition{
				{
					ID:     "esp",
					FsType: "fat32",
					Start:  1,
					Flags: []PartitionFlag{
						"esp",
						"boot",
					},
				},
			},
		}},
		SystemConfig: SystemConfig{
			BootType: "efi",
			Hostname: "test",
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
