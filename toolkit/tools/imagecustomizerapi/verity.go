// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type Verity struct {
	VerityTab                string                   `yaml:"VerityTab"`
	VerityDevice             string                   `yaml:"VerityDevice"`
	HashDevice               string                   `yaml:"HashDevice"`
	BootDevice               string                   `yaml:"BootDevice"`
	VerityCorruptionResponse VerityCorruptionResponse `yaml:"VerityCorruptionResponse"`
}

var (
	DefaultVerity = Verity{
		VerityTab:                "",
		VerityDevice:             "",
		HashDevice:               "",
		BootDevice:               "",
		VerityCorruptionResponse: "",
	}
)

func (v *Verity) IsValid() error {
	var err error

	if v.VerityTab == "" {
		return fmt.Errorf("invalid VerityTab value: empty string")
	}

	if v.VerityDevice == "" {
		return fmt.Errorf("invalid VerityDevice value: empty string")
	}

	if v.HashDevice == "" {
		return fmt.Errorf("invalid HashDevice value: empty string")
	}

	if v.BootDevice == "" {
		return fmt.Errorf("invalid BootDevice value: empty string")
	}

	err = v.VerityCorruptionResponse.IsValid()
	if err != nil {
		return err
	}

	return nil
}

// TODO: Implement a new dedicated UnmarshalYAML function.
