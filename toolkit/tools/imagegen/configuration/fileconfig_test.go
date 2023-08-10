// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

//

package configuration

import (
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/ptrutils"
	"github.com/stretchr/testify/assert"
)

func TestParseFileConfigValid1(t *testing.T) {
	// Simple string path
	testValidFileConfigList(t, "\"/a.txt\"", FileConfigList{{Path: "/a.txt"}})
}

func TestParseFileConfigValid2(t *testing.T) {
	// Simple string path in an array.
	testValidFileConfigList(t, "[ \"/a.txt\" ]", FileConfigList{{Path: "/a.txt"}})
}

func TestParseFileConfigValid3(t *testing.T) {
	// Simple struct.
	testValidFileConfigList(t, "{ \"Path\": \"/b.txt\" }", FileConfigList{{Path: "/b.txt"}})
}

func TestParseFileConfigValid4(t *testing.T) {
	// Full struct.
	testValidFileConfigList(t, "{ \"Path\": \"/b.txt\", \"Permissions\": \"770\" }",
		FileConfigList{{Path: "/b.txt", Permissions: ptrutils.PtrTo(FilePermissions(0o770))}},
	)
}

func TestParseFileConfigValid5(t *testing.T) {
	// Mixed struct and string array.
	testValidFileConfigList(t, "[ { \"Path\": \"/b.txt\" }, \"/c.txt\" ]",
		FileConfigList{
			{Path: "/b.txt"},
			{Path: "/c.txt"},
		},
	)
}

func TestParseFileConfigInvalid1(t *testing.T) {
	// Empty array.
	testInvalidFileConfigList(t, "[ ]")
}

func TestParseFileConfigInvalid2(t *testing.T) {
	// Number.
	testInvalidFileConfigList(t, "1.2")
}

func TestParseFileConfigInvalid3(t *testing.T) {
	// Empty string.
	testInvalidFileConfigList(t, "\"\"")
}

func testValidFileConfigList(t *testing.T, json string, expectedValue FileConfigList) {
	var value FileConfigList
	err := marshalJSONString(json, &value)
	assert.NoError(t, err)
	assert.Equal(t, expectedValue, value)
}

func testInvalidFileConfigList(t *testing.T, json string) {
	var value FileConfigList
	err := marshalJSONString(json, &value)
	assert.Error(t, err)
}
