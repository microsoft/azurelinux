// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"
)

func TestSystemConfigValidEmpty(t *testing.T) {
	testValidYamlValue[*SystemConfig](t, "{ }", &SystemConfig{})
}

func TestSystemConfigValidHostname(t *testing.T) {
	testValidYamlValue[*SystemConfig](t, "{ \"Hostname\": \"validhostname\" }", &SystemConfig{Hostname: "validhostname"})
}

func TestSystemConfigInvalidHostname(t *testing.T) {
	testInvalidYamlValue[*SystemConfig](t, "{ \"Hostname\": \"invalid_hostname\" }")
}

func TestSystemConfigInvalidAdditionalFiles(t *testing.T) {
	testInvalidYamlValue[*SystemConfig](t, "{ \"AdditionalFiles\": { \"a.txt\": [] } }")
}
