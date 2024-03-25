// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import "fmt"

type Config struct {
	Storage *Storage `yaml:"storage"`
	Iso     *Iso     `yaml:"iso"`
	OS      OS       `yaml:"os"`
}

func (c *Config) IsValid() (err error) {
	if c.Storage != nil {
		err = c.Storage.IsValid()
		if err != nil {
			return err
		}
	}

	if c.Iso != nil {
		err = c.Iso.IsValid()
		if err != nil {
			return err
		}
	}

	err = c.OS.IsValid()
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
