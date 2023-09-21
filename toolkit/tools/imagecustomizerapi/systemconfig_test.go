// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"
)

func TestSystemConfigValidEmpty(t *testing.T) {
	testValidYamlValue[*SystemConfig](t, "{ }", &SystemConfig{})
}

func TestSystemConfigInvalidAdditionalFiles(t *testing.T) {
	testInvalidYamlValue[*SystemConfig](t, "{ \"AdditionalFiles\": { \"a.txt\": [] } }")
}
