// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestParseFilePermissionsValid1(t *testing.T) {
	testValidFilePermission(t, "\"777\"", FilePermissions(0o777))
}

func TestParseFilePermissionsValid2(t *testing.T) {
	testValidFilePermission(t, "\"000\"", FilePermissions(0))
}

func TestParseFilePermissionsValid3(t *testing.T) {
	testValidFilePermission(t, "\"0\"", FilePermissions(0))
}

func TestParseFilePermissionsInvalid1(t *testing.T) {
	// Value out of range.
	testInvalidFilePermission(t, "\"1000\"")
}

func TestParseFilePermissionsInvalid2(t *testing.T) {
	// Decimal number.
	testInvalidFilePermission(t, "0")
}

func TestParseFilePermissionsInvalid3(t *testing.T) {
	// Array value.
	testInvalidFilePermission(t, "[]")
}

func TestParseFilePermissionsInvalid4(t *testing.T) {
	// Not an octal value.
	testInvalidFilePermission(t, "\"999\"")
}

func testValidFilePermission(t *testing.T, json string, expectedValue FilePermissions) {
	var value FilePermissions
	err := marshalJSONString(json, &value)
	assert.NoError(t, err)
	assert.Equal(t, expectedValue, value)
}

func testInvalidFilePermission(t *testing.T, json string) {
	var value FilePermissions
	err := marshalJSONString(json, &value)
	assert.Error(t, err)
}
