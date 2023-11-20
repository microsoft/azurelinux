// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

type Config struct {
	SystemConfig SystemConfig `yaml:"SystemConfig"`
}

func (c *Config) IsValid() error {
	err := c.SystemConfig.IsValid()
	if err != nil {
		return err
	}

	return nil
}
