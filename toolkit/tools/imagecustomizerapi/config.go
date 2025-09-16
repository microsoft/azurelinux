// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import "fmt"

type Config struct {
	Storage Storage `yaml:"storage"`
	Iso     *Iso    `yaml:"iso"`
	Pxe     *Pxe    `yaml:"pxe"`
	OS      *OS     `yaml:"os"`
	Scripts Scripts `yaml:"scripts"`
}

func (c *Config) IsValid() (err error) {
	err = c.Storage.IsValid()
	if err != nil {
		return err
	}

	hasResetPartitionsUuids := c.Storage.ResetPartitionsUuidsType != ResetPartitionsUuidsTypeDefault

	if c.Iso != nil {
		err = c.Iso.IsValid()
		if err != nil {
			return fmt.Errorf("invalid 'iso' field:\n%w", err)
		}
	}

	if c.Pxe != nil {
		err = c.Pxe.IsValid()
		if err != nil {
			return fmt.Errorf("invalid 'pxe' field:\n%w", err)
		}
	}

	hasResetBootLoader := false
	if c.OS != nil {
		err = c.OS.IsValid()
		if err != nil {
			return fmt.Errorf("invalid 'os' field:\n%w", err)
		}
		hasResetBootLoader = c.OS.BootLoader.Reset != ResetBootLoaderTypeDefault

		if c.OS.Uki != nil {
			// Temporary limitation: We currently require 'os.bootloader.reset' to be 'hard-reset' when 'os.uki' is enabled.
			// In the future, as we design and develop the bootloader further, this hard-reset limitation may be lifted.
			// However, 'systemd-boot' is expected to remain tightly coupled with the 'uki' feature for the foreseeable future.
			if c.OS.BootLoader.Type != BootLoaderTypeSystemdBoot || c.OS.BootLoader.Reset != ResetBootLoaderTypeHard {
				return fmt.Errorf(
					"'os.bootloader.type' must be 'systemd-boot' and 'os.bootloader.reset' must be 'hard-reset' when 'os.uki' is enabled",
				)
			}
		}
	}

	err = c.Scripts.IsValid()
	if err != nil {
		return err
	}

	if c.CustomizePartitions() && !hasResetBootLoader {
		return fmt.Errorf("'os.bootloader.reset' must be specified if 'storage.disks' is specified")
	}

	if hasResetPartitionsUuids && !hasResetBootLoader {
		return fmt.Errorf("'os.bootloader.reset' must be specified if 'storage.resetPartitionsUuidsType' is specified")
	}

	return nil
}

func (c *Config) CustomizePartitions() bool {
	return c.Storage.CustomizePartitions()
}
