// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
)

// 'SavedConfigs' is a subset of the Image Customizer input configurations that
// needs to be saved on the output media so that it can be used in subsequent
// runs of the Image Customizer against that same output media.
//
// This preservation of input configuration is necessary for subsequent runs if
// the configuration does not result in updating root file system.
//
// For example, if the user specifies a kernel argument that is specific to the
// ISO image, it will not be present in any of the grub config files on the
// root file system - only in the final ISO image grub.cfg. When that ISO image
// is further customized, the root file system grub.cfg might get re-generated
// and we need to remember to add the ISO specific arguments from the previous
// runs. SavedConfigs is the place where we can store such arguments so we can
// re-apply them.

type IsoSavedConfigs struct {
	KernelCommandLine imagecustomizerapi.KernelCommandLine  `yaml:"kernelCommandLine"`
}

func (i *IsoSavedConfigs) IsValid() error {
	err := i.KernelCommandLine.IsValid()
	if err != nil {
		return fmt.Errorf("invalid kernelCommandLine: %w", err)
	}

	return nil
}

type SavedConfigs struct {
	Iso IsoSavedConfigs `yaml:"iso"`
}

func (c *SavedConfigs) IsValid() (err error) {
	err = c.Iso.IsValid()
	if err != nil {
		return fmt.Errorf("invalid 'iso' field:\n%w", err)
	}

	return nil
}

func (c *SavedConfigs) IsEmpty() bool {
	isoConfigEmpty := c.Iso.KernelCommandLine.ExtraCommandLine == ""
	return isoConfigEmpty
}

func (c *SavedConfigs) persistSavedConfigs(savedConfigsFilePath string) (err error) {
	if c.IsEmpty() {
		return nil
	}

	err = os.MkdirAll(filepath.Dir(savedConfigsFilePath), os.ModePerm)
	if err != nil {
		return fmt.Errorf("failed to create directory for (%s):\n%w", savedConfigsFilePath, err)
	}

	err = imagecustomizerapi.MarshalYamlFile(savedConfigsFilePath, c)
	if err != nil {
		return fmt.Errorf("failed to persist saved configs file to (%s):\n%w", savedConfigsFilePath, err)
	}

	return nil
}

func loadSavedConfigs(savedConfigsFilePath string) (savedConfigs *SavedConfigs, err error) {
	exists, err := file.PathExists(savedConfigsFilePath)
	if err != nil {
		return nil, fmt.Errorf("failed to check if (%s) exists:\n%w", savedConfigsFilePath, err)
	}

	if !exists {
		return nil, nil
	}

	savedConfigs = &SavedConfigs{}
	err = imagecustomizerapi.UnmarshalYamlFile(savedConfigsFilePath, savedConfigs)
	if err != nil {
		return nil, fmt.Errorf("failed to load saved configs file (%s):\n%w", savedConfigsFilePath, err)
	}

	return savedConfigs, nil
}
