// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/ptrutils"
)

func TestParseFileConfigValidString(t *testing.T) {
	testValidYamlValue(t, "\"/a.txt\"", &FileConfigList{{Path: "/a.txt"}})
}

func TestParseFileConfigValidStringInArray(t *testing.T) {
	testValidYamlValue(t, "[ \"/a.txt\" ]", &FileConfigList{{Path: "/a.txt"}})
}

func TestParseFileConfigValidBasicStruct(t *testing.T) {
	testValidYamlValue(t, "{ \"Path\": \"/b.txt\" }", &FileConfigList{{Path: "/b.txt"}})
}

func TestParseFileConfigValidFullStruct(t *testing.T) {
	testValidYamlValue(t, "{ \"Path\": \"/b.txt\", \"Permissions\": \"770\" }",
		&FileConfigList{{Path: "/b.txt", Permissions: ptrutils.PtrTo(FilePermissions(0o770))}},
	)
}

func TestParseFileConfigValidMixedArray(t *testing.T) {
	testValidYamlValue(t, "[ { \"Path\": \"/b.txt\" }, \"/c.txt\" ]",
		&FileConfigList{
			{Path: "/b.txt"},
			{Path: "/c.txt"},
		},
	)
}

func TestParseFileConfigInvalidEmptyArray(t *testing.T) {
	// Empty array.
	testInvalidYamlValue[*FileConfigList](t, "[ ]")
}

func TestParseFileConfigInvalidArrayArray(t *testing.T) {
	// Empty array.
	testInvalidYamlValue[*FileConfigList](t, "[ [ ] ]")
}

func TestParseFileConfigInvalidEmptyString(t *testing.T) {
	// Empty string.
	testInvalidYamlValue[*FileConfigList](t, "\"\"")
}

func TestParseFileConfigInvalidFilePermissions(t *testing.T) {
	// Empty string.
	testInvalidYamlValue[*FileConfigList](t, "{ \"Path\": \"/b.txt\", \"Permissions\": \"7777\" }")
}
