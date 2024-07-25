// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/stretchr/testify/assert"
)

func TestConfigIsValid(t *testing.T) {
	config := &Config{
		Storage: &Storage{
			Disks: []Disk{{
				PartitionTableType: "gpt",
				MaxSize:            2 * diskutils.MiB,
				Partitions: []Partition{
					{
						Id:    "esp",
						Start: 1 * diskutils.MiB,
						Type:  PartitionTypeESP,
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
		OS: &OS{
			ResetBootLoaderType: "hard-reset",
			Hostname:            "test",
		},
		Scripts: &Scripts{},
		Iso:     &Iso{},
	}

	err := config.IsValid()
	assert.NoError(t, err)
}

func TestConfigIsValidLegacy(t *testing.T) {
	config := &Config{
		Storage: &Storage{
			Disks: []Disk{{
				PartitionTableType: "gpt",
				MaxSize:            2 * diskutils.MiB,
				Partitions: []Partition{
					{
						Id:    "boot",
						Start: 1 * diskutils.MiB,
						Type:  PartitionTypeBiosGrub,
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
		OS: &OS{
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
				MaxSize:            2 * diskutils.MiB,
				Partitions: []Partition{
					{
						Id:    "a",
						Start: 1 * diskutils.MiB,
					},
				},
			}},
		},
		OS: &OS{
			Hostname:            "test",
			ResetBootLoaderType: "hard-reset",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid bootType value ()")
}

func TestConfigIsValidMissingBootLoaderReset(t *testing.T) {
	config := &Config{
		Storage: &Storage{
			Disks: []Disk{{
				PartitionTableType: "gpt",
				MaxSize:            2 * diskutils.MiB,
				Partitions: []Partition{
					{
						Id:    "esp",
						Start: 1 * diskutils.MiB,
						Type:  PartitionTypeESP,
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
		OS: &OS{
			Hostname: "test",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "os.resetBootLoaderType must be specified if storage is specified")
}

func TestConfigIsValidMultipleDisks(t *testing.T) {
	config := &Config{
		Storage: &Storage{
			Disks: []Disk{
				{
					PartitionTableType: "gpt",
					MaxSize:            1 * diskutils.MiB,
				},
				{
					PartitionTableType: "gpt",
					MaxSize:            1 * diskutils.MiB,
				},
			},
			BootType: "legacy",
		},
		OS: &OS{
			ResetBootLoaderType: "hard-reset",
			Hostname:            "test",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "defining multiple disks is not currently supported")
}

func TestConfigIsValidZeroDisks(t *testing.T) {
	config := &Config{
		Storage: &Storage{
			BootType: BootTypeEfi,
			Disks:    []Disk{},
		},
		OS: &OS{
			Hostname: "test",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "at least 1 disk must be specified")
}

func TestConfigIsValidBadHostname(t *testing.T) {
	config := &Config{
		OS: &OS{
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
		OS: &OS{
			Hostname: "test",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid disk at index 0")
	assert.ErrorContains(t, err, "a disk's maxSize value (0) must be a positive non-zero number")
}

func TestConfigIsValidMissingEsp(t *testing.T) {
	config := &Config{
		Storage: &Storage{
			Disks: []Disk{{
				PartitionTableType: "gpt",
				MaxSize:            2 * diskutils.MiB,
				Partitions:         []Partition{},
			}},
			BootType: "efi",
		},
		OS: &OS{
			ResetBootLoaderType: "hard-reset",
			Hostname:            "test",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "'esp' partition must be provided for 'efi' boot type")
}

func TestConfigIsValidMissingBiosBoot(t *testing.T) {
	config := &Config{
		Storage: &Storage{
			Disks: []Disk{{
				PartitionTableType: "gpt",
				MaxSize:            2 * diskutils.MiB,
				Partitions:         []Partition{},
			}},
			BootType: "legacy",
		},
		OS: &OS{
			ResetBootLoaderType: "hard-reset",
			Hostname:            "test",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "'bios-grub' partition must be provided for 'legacy' boot type")
}

func TestConfigIsValidInvalidMountPoint(t *testing.T) {
	config := &Config{
		Storage: &Storage{
			Disks: []Disk{{
				PartitionTableType: "gpt",
				MaxSize:            2 * diskutils.MiB,
				Partitions: []Partition{
					{
						Id:    "esp",
						Start: 1 * diskutils.MiB,
						Type:  PartitionTypeESP,
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
		OS: &OS{
			ResetBootLoaderType: "hard-reset",
			Hostname:            "test",
		},
	}

	err := config.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid fileSystems item at index 0")
	assert.ErrorContains(t, err, "invalid mountPoint value")
	assert.ErrorContains(t, err, "invalid path (boot/efi): must be an absolute path")
}

func TestConfigIsValidKernelCLI(t *testing.T) {
	config := &Config{
		Storage: &Storage{
			Disks: []Disk{{
				PartitionTableType: "gpt",
				MaxSize:            2 * diskutils.MiB,
				Partitions: []Partition{
					{
						Id:    "esp",
						Start: 1 * diskutils.MiB,
						Type:  PartitionTypeESP,
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
		OS: &OS{
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

func TestConfigIsValidInvalidIso(t *testing.T) {
	config := &Config{
		Iso: &Iso{
			AdditionalFiles: AdditionalFilesMap{
				"": FileConfigList{},
			},
		},
	}
	err := config.IsValid()
	assert.ErrorContains(t, err, "invalid 'iso' field")
	assert.ErrorContains(t, err, "invalid additionalFiles")
}

func TestConfigIsValidInvalidScripts(t *testing.T) {
	config := &Config{
		Scripts: &Scripts{
			PostCustomization: []Script{
				{
					Path: "",
				},
			},
		},
	}
	err := config.IsValid()
	assert.ErrorContains(t, err, "invalid postCustomization script at index 0")
	assert.ErrorContains(t, err, "either path or content must have a value")
}
