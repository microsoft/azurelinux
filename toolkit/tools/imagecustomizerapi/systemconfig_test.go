// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestSystemConfigValidEmpty(t *testing.T) {
	testValidYamlValue[*SystemConfig](t, "{ }", &SystemConfig{})
}

func TestSystemConfigValidHostname(t *testing.T) {
	testValidYamlValue[*SystemConfig](t, "{ \"hostname\": \"validhostname\" }", &SystemConfig{Hostname: "validhostname"})
}

func TestSystemConfigInvalidHostname(t *testing.T) {
	testInvalidYamlValue[*SystemConfig](t, "{ \"hostname\": \"invalid_hostname\" }")
}

func TestSystemConfigInvalidAdditionalFiles(t *testing.T) {
	testInvalidYamlValue[*SystemConfig](t, "{ \"additionalFiles\": { \"a.txt\": [] } }")
}

func TestSystemConfigIsValidDuplicatePartitionID(t *testing.T) {
	value := SystemConfig{
		PartitionSettings: []PartitionSetting{
			{
				ID: "a",
			},
			{
				ID: "a",
			},
		},
	}

	err := value.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "duplicate PartitionSettings ID")
}

func TestSystemConfigIsValidKernelCommandLineInvalidChars(t *testing.T) {
	value := SystemConfig{
		KernelCommandLine: KernelCommandLine{
			ExtraCommandLine: "example=\"example\"",
		},
	}

	err := value.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "ExtraCommandLine")
}
