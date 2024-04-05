// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import "fmt"

type Config struct {
	Storage *Storage `yaml:"storage"`
	Iso     *Iso     `yaml:"iso"`
	OS      *OS      `yaml:"os"`
	Scripts Scripts  `yaml:"scripts"`
}

func (c *Config) IsValid() (err error) {

	hasStorage := false
	if c.Storage != nil {
		err = c.Storage.IsValid()
		if err != nil {
			return err
		}
		hasStorage = true
	}

	if c.Iso != nil {
		err = c.Iso.IsValid()
		if err != nil {
			return err
		}
	}

	hasResetBootLoader := false
	if c.OS != nil {
		err = c.OS.IsValid()
		if err != nil {
			return err
		}
		hasResetBootLoader = c.OS.ResetBootLoaderType != ResetBootLoaderTypeDefault
	}

	err = c.Scripts.IsValid()
	if err != nil {
		return err
	}

	hasStorage := c.Storage != nil
	hasResetBootLoader := c.OS.ResetBootLoaderType != ResetBootLoaderTypeDefault

	if hasStorage != hasResetBootLoader {
		return fmt.Errorf("os.resetBootLoaderType and storage must be specified together")
	}

	return nil
}
