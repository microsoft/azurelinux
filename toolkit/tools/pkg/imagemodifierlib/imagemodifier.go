// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagemodifierlib

import (
	"fmt"
	"path/filepath"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerapi"
)

func ModifyImageWithConfigFile(configFile string) error {
	var err error

	var config imagecustomizerapi.Config
	err = imagecustomizerapi.UnmarshalYamlFile(configFile, &config.SystemConfig)
	if err != nil {
		return err
	}

	baseConfigPath, _ := filepath.Split(configFile)

	absBaseConfigPath, err := filepath.Abs(baseConfigPath)
	if err != nil {
		return fmt.Errorf("failed to get absolute path of config file directory:\n%w", err)
	}

	err = ModifyImage(absBaseConfigPath, &config)
	if err != nil {
		return err
	}

	return nil
}

func ModifyImage(baseConfigPath string, config *imagecustomizerapi.Config) error {
	err := doModifications(baseConfigPath, config)
	if err != nil {
		return err
	}

	return nil
}
