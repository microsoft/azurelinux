// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package osmodifierlib

import (
	"fmt"
	"path/filepath"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
)

func ModifyOSWithConfigFile(configFile string) error {
	var err error

	var osConfig imagecustomizerapi.OS
	err = imagecustomizerapi.UnmarshalYamlFile(configFile, &osConfig)
	if err != nil {
		return err
	}

	baseConfigPath, _ := filepath.Split(configFile)

	absBaseConfigPath, err := filepath.Abs(baseConfigPath)
	if err != nil {
		return fmt.Errorf("failed to get absolute path of config file directory:\n%w", err)
	}

	err = ModifyOS(absBaseConfigPath, &osConfig)
	if err != nil {
		return err
	}

	return nil
}

func ModifyOS(baseConfigPath string, osConfig *imagecustomizerapi.OS) error {
	err := doModifications(baseConfigPath, osConfig)
	if err != nil {
		return err
	}

	return nil
}

func ModifyOSWithoutConfigFile() error {
	// The case when config file is not needed is when apply verity change in grub.cfg to default grub
	err := doModificationsWithoutConfig()
	if err != nil {
		return err
	}

	return nil
}
