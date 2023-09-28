// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
)

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
