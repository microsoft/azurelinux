// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import "fmt"

type Config struct {
	Storage Storage `yaml:"storage"`
	Iso     *Iso    `yaml:"iso"`
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

	hasResetBootLoader := false
	if c.OS != nil {
		err = c.OS.IsValid()
		if err != nil {
			return fmt.Errorf("invalid 'os' field:\n%w", err)
		}
		hasResetBootLoader = c.OS.ResetBootLoaderType != ResetBootLoaderTypeDefault
	}

	err = c.Scripts.IsValid()
	if err != nil {
		return err
	}

	if c.CustomizePartitions() && !hasResetBootLoader {
		return fmt.Errorf("'os.resetBootLoaderType' must be specified if 'storage.disks' is specified")
	}

	if hasResetPartitionsUuids && !hasResetBootLoader {
		return fmt.Errorf("'os.resetBootLoaderType' must be specified if 'storage.resetPartitionsUuidsType' is specified")
	}

	return nil
}

func (c *Config) CustomizePartitions() bool {
	return c.Storage.CustomizePartitions()
}
