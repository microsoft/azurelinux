// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"

	"gopkg.in/yaml.v3"
)

type Verity struct {
	VerityTab    string `yaml:"VerityTab"`
	VerityDevice string `yaml:"VerityDevice"`
	HashDevice   string `yaml:"HashDevice"`
}

var (
	DefaultVerity = Verity{
		VerityTab:    "",
		VerityDevice: "",
		HashDevice:   "",
	}
)

func (v *Verity) IsValid() (err error) {
	if v.VerityTab == "" {
		return fmt.Errorf("invalid VerityTab value: empty string")
	}

	if v.VerityDevice == "" {
		return fmt.Errorf("invalid VerityDevice value: empty string")
	}

	if v.HashDevice == "" {
		return fmt.Errorf("invalid HashDevice value: empty string")
	}

	return nil
}

func (v *Verity) UnmarshalYAML(value *yaml.Node) error {
	var err error

	if value.Kind == yaml.ScalarNode {
		// Parse as a string.
		*v = Verity{
			VerityTab:    value.Value,
			VerityDevice: value.Value,
			HashDevice:   value.Value,
		}
		return nil
	}

	// Parse as a struct.
	*v = DefaultVerity

	type IntermediateTypeFileConfig Verity
	err = value.Decode((*IntermediateTypeFileConfig)(v))
	if err != nil {
		return fmt.Errorf("failed to parse Verity:\n%w", err)
	}

	return nil
}
