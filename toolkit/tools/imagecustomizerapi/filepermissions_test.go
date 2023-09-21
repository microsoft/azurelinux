// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/ptrutils"
)

func TestParseFilePermissionsValid1(t *testing.T) {
	testValidYamlValue(t, "\"777\"", ptrutils.PtrTo(FilePermissions(0o777)))
}

func TestParseFilePermissionsValid2(t *testing.T) {
	testValidYamlValue(t, "\"000\"", ptrutils.PtrTo(FilePermissions(0)))
}

func TestParseFilePermissionsValid3(t *testing.T) {
	testValidYamlValue(t, "\"0\"", ptrutils.PtrTo(FilePermissions(0)))
}

func TestParseFilePermissionsInvalidOutOfRange(t *testing.T) {
	// Value out of range.
	testInvalidYamlValue[*FilePermissions](t, "\"1000\"")
}

func TestParseFilePermissionsInvalidType(t *testing.T) {
	// Array value.
	testInvalidYamlValue[*FilePermissions](t, "[]")
}

func TestParseFilePermissionsInvalidNotOctal(t *testing.T) {
	// Not an octal value.
	testInvalidYamlValue[*FilePermissions](t, "\"999\"")
}
