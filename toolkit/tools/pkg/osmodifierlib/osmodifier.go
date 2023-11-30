// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package osmodifierlib

import (
	"fmt"
	"path/filepath"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerapi"
)

func ModifyOSWithConfigFile(configFile string) error {
	var err error

	var systemConfig imagecustomizerapi.SystemConfig
	err = imagecustomizerapi.UnmarshalYamlFile(configFile, &systemConfig)
	if err != nil {
		return err
	}

	baseConfigPath, _ := filepath.Split(configFile)

	absBaseConfigPath, err := filepath.Abs(baseConfigPath)
	if err != nil {
		return fmt.Errorf("failed to get absolute path of config file directory:\n%w", err)
	}

	err = ModifyOS(absBaseConfigPath, &systemConfig)
	if err != nil {
		return err
	}

	return nil
}

func ModifyOS(baseConfigPath string, systemConfig *imagecustomizerapi.SystemConfig) error {
	err := doModifications(baseConfigPath, systemConfig)
	if err != nil {
		return err
	}

	return nil
}
