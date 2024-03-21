// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestConfigIsValid(t *testing.T) {
	config := &Config{
		Storage: &Storage{
			Disks: []Disk{{
				PartitionTableType: "gpt",
				MaxSize:            2,
				Partitions: []Partition{
					{
						Id:    "esp",
						Start: 1,
						Flags: []PartitionFlag{
							"esp",
							"boot",
						},
					},
				},
			}},
			BootType: "efi",
			FileSystems: []FileSystem{
				{
					DeviceId: "esp",
					Type:     "fat32",
					MountPoint: &MountPoint{
						Path: "/boot/efi",
					},
				},
			},
		},
		OS: OS{
			ResetBootLoaderType: "hard-reset",
			Hostname:            "test",
		},
	}

	err := config.IsValid()
	assert.NoError(t, err)
}

func TestConfigIsValidLegacy(t *testing.T) {
	config := &Config{
		Storage: &Storage{
			Disks: []Disk{{
				PartitionTableType: "gpt",
				MaxSize:            2,
				Partitions: []Partition{
					{
						Id:    "boot",
						Start: 1,
						Flags: []PartitionFlag{
							"bios-grub",
						},
					},
				},
			}},
			BootType: "legacy",
			FileSystems: []FileSystem{
				{
					DeviceId: "boot",
					Type:     "fat32",
				},
			},
		},
		OS: OS{
			ResetBootLoaderType: "hard-reset",
			Hostname:            "test",
		},
	}

	err := config.IsValid()
	assert.NoError(t, err)
}

func TestConfigIsValidNoBootType(t *testing.T) {
	config := &Config{
		Storage: &Storage{
			Disks: []Disk{{
				PartitionTableType: "gpt",
				MaxSize:            2,
				Partitions: []Partition{
					{
						Id:    "a",
						Start: 1,
					},
				},
			}},
		},
		OS: OS{
			Hostname:            "test",
			ResetBootLoaderType: "hard-reset",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "bootType")
}

func TestConfigIsValidMissingBootLoaderReset(t *testing.T) {
	config := &Config{
		Storage: &Storage{
			Disks: []Disk{{
				PartitionTableType: "gpt",
				MaxSize:            2,
				Partitions: []Partition{
					{
						Id:    "esp",
						Start: 1,
						Flags: []PartitionFlag{
							"esp",
							"boot",
						},
					},
				},
			}},
			BootType: "efi",
			FileSystems: []FileSystem{
				{
					DeviceId: "esp",
					Type:     "fat32",
					MountPoint: &MountPoint{
						Path: "/boot/efi",
					},
				},
			},
		},
		OS: OS{
			Hostname: "test",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "os.resetBootLoaderType and storage must be specified together")
}

func TestConfigIsValidMultipleDisks(t *testing.T) {
	config := &Config{
		Storage: &Storage{
			Disks: []Disk{
				{
					PartitionTableType: "gpt",
					MaxSize:            1,
				},
				{
					PartitionTableType: "gpt",
					MaxSize:            1,
				},
			},
			BootType: "legacy",
		},
		OS: OS{
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
		Storage: &Storage{
			BootType: BootTypeEfi,
			Disks:    []Disk{},
		},
		OS: OS{
			Hostname: "test",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "at least 1 disk must be specified")
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
		Storage: &Storage{
			BootType: BootTypeEfi,
			Disks: []Disk{{
				PartitionTableType: PartitionTableTypeGpt,
				MaxSize:            0,
			}},
		},
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
		Storage: &Storage{
			Disks: []Disk{{
				PartitionTableType: "gpt",
				MaxSize:            2,
				Partitions:         []Partition{},
			}},
			BootType: "efi",
		},
		OS: OS{
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
		Storage: &Storage{
			Disks: []Disk{{
				PartitionTableType: "gpt",
				MaxSize:            2,
				Partitions:         []Partition{},
			}},
			BootType: "legacy",
		},
		OS: OS{
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
		Storage: &Storage{
			Disks: []Disk{{
				PartitionTableType: "gpt",
				MaxSize:            2,
				Partitions: []Partition{
					{
						Id:    "esp",
						Start: 1,
						Flags: []PartitionFlag{
							"esp",
							"boot",
						},
					},
				},
			}},
			BootType: "efi",
			FileSystems: []FileSystem{
				{
					DeviceId: "esp",
					Type:     "fat32",
					MountPoint: &MountPoint{
						Path: "boot/efi",
					},
				},
			},
		},
		OS: OS{
			ResetBootLoaderType: "hard-reset",
			Hostname:            "test",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "mountPoint")
	assert.ErrorContains(t, err, "absolute path")
}

func TestConfigIsValidKernelCLI(t *testing.T) {
	config := &Config{
		Storage: &Storage{
			Disks: []Disk{{
				PartitionTableType: "gpt",
				MaxSize:            2,
				Partitions: []Partition{
					{
						Id:    "esp",
						Start: 1,
						Flags: []PartitionFlag{
							"esp",
							"boot",
						},
					},
				},
			}},
			BootType: "efi",
			FileSystems: []FileSystem{
				{
					DeviceId: "esp",
					Type:     "fat32",
					MountPoint: &MountPoint{
						Path: "/boot/efi",
					},
				},
			},
		},
		OS: OS{
			ResetBootLoaderType: "hard-reset",
			Hostname:            "test",
			KernelCommandLine: KernelCommandLine{
				ExtraCommandLine: "console=ttyS0",
			},
		},
	}
	err := config.IsValid()
	assert.NoError(t, err)
}
