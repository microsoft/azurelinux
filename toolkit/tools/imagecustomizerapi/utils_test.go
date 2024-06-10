// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"path/filepath"
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestUnmarshalYamlFile(t *testing.T) {
	var config Config
	err := UnmarshalYamlFile(filepath.Join(workingDir, "../pkg/imagecustomizerlib/testdata/nochange-config.yaml"),
		&config)
	assert.NoError(t, err)
}

func TestUnmarshalYamlFileDoesNotExist(t *testing.T) {
	var config Config
	err := UnmarshalYamlFile(filepath.Join(workingDir, "../pkg/imagecustomizerlib/testdata/no-such-file.yaml"),
		&config)
	assert.ErrorContains(t, err, "no such file or directory")
}

func TestUnmarshalYamlInvalidFile(t *testing.T) {
	var config Config
	err := UnmarshalYamlFile(filepath.Join(workingDir, "../pkg/imagecustomizerlib/testdata/lists/dracut-fips.yaml"),
		&config)
	assert.ErrorContains(t, err, "yaml: unmarshal errors")
}

func testValidYamlValue[DataType HasIsValid](t *testing.T, yamlString string, expectedValue DataType) {
	value := makeValue[DataType]()

	err := UnmarshalYaml([]byte(yamlString), value)
	assert.NoError(t, err)
	assert.Equal(t, expectedValue, value)
}

func testInvalidYamlValue[DataType HasIsValid](t *testing.T, yamlString string) {
	value := makeValue[DataType]()
	err := UnmarshalYaml([]byte(yamlString), value)
	assert.Errorf(t, err, "value: %v", value)
}

func makeValue[DataType any]() DataType {
	// When DataType is a pointer, there is no built-in way to create a new value
	// of the underlying type. So, use reflection to do this.
	var placeholder DataType
	return reflect.New(reflect.TypeOf(placeholder).Elem()).Interface().(DataType)
}
