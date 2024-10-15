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

func MarshalYamlFile[ValueType HasIsValid](yamlfilePath string, value ValueType) error {
	yamlString, err := MarshalYaml(value)
	if err != nil {
		return err
	}

	file, err := os.Create(yamlfilePath)
	if err != nil {
		return err
	}
	defer file.Close()

	_, err = file.WriteString(yamlString)
	if err != nil {
		return err
	}

	return nil
}

func MarshalYaml[ValueType HasIsValid](value ValueType) (string, error) {
	yamlData, err := yaml.Marshal(value)
	if err != nil {
		return "", err
	}

	return string(yamlData), nil
}
