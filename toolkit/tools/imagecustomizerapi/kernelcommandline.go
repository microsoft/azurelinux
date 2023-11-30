// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
	"strings"
)

type KernelCommandLine struct {
	// Command line args added during partition customiztion.
	ExtraCommandLine string `yaml:"ExtraCommandLine"`
	// Command line args added during OS customization.
	CommandLineAdd string `yaml:"CommandLineAdd"`
}

func (s *KernelCommandLine) IsValid() error {
	err := commandLineIsValid(s.ExtraCommandLine, "ExtraCommandLine")
	if err != nil {
		return err
	}

	err = commandLineIsValid(s.CommandLineAdd, "CommandLineAdd")
	if err != nil {
		return err
	}

	return nil
}

func commandLineIsValid(commandLine string, fieldName string) error {
	// Disallow special characters to avoid breaking the grub.cfg file.
	// In addition, disallow the "`" character, since it is used as the sed escape character by
	// `installutils.setGrubCfgAdditionalCmdLine()`.
	if strings.ContainsAny(commandLine, "\n'\"\\$`") {
		return fmt.Errorf("the %s value contains invalid characters", fieldName)
	}

	return nil
}
