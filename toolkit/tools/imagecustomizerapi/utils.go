// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"bytes"
	"os"

	"gopkg.in/yaml.v3"
)

type HasIsValid interface {
	IsValid() error
}

func UnmarshalYamlFile[ValueType HasIsValid](yamlFilePath string, value ValueType) error {
	var err error

	yamlFile, err := os.ReadFile(yamlFilePath)
	if err != nil {
		return err
	}

	err = UnmarshalYaml(yamlFile, value)
	if err != nil {
		return err
	}

	return nil
}

func UnmarshalYaml[ValueType HasIsValid](yamlData []byte, value ValueType) error {
	var err error

	reader := bytes.NewReader(yamlData)
	decoder := yaml.NewDecoder(reader)

	// Ensure unknown fields result in an error.
	decoder.KnownFields(true)

	err = decoder.Decode(value)
	if err != nil {
		return err
	}

	err = value.IsValid()
	if err != nil {
		return err
	}

	return nil
}
