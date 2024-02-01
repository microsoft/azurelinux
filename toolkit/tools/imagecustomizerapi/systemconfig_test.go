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
	testValidYamlValue[*SystemConfig](t, "{ \"Hostname\": \"validhostname\" }", &SystemConfig{Hostname: "validhostname"})
}

func TestSystemConfigInvalidHostname(t *testing.T) {
	testInvalidYamlValue[*SystemConfig](t, "{ \"Hostname\": \"invalid_hostname\" }")
}

func TestSystemConfigInvalidAdditionalFiles(t *testing.T) {
	testInvalidYamlValue[*SystemConfig](t, "{ \"AdditionalFiles\": { \"a.txt\": [] } }")
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

func TestSystemConfigIsValidVerityInvalidPartLabel(t *testing.T) {
	validVerity := SystemConfig{
		Verity: &Verity{
			DataPartition: VerityPartition{
				IdType: "PartUuid",
				Id:     "0f2884c0-8fe0-4a19-87bf-286b7fe9d6f2",
			},
			HashPartition: VerityPartition{
				IdType: "PartLabel",
				Id:     "",
			},
		},
	}

	err := validVerity.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid Id: empty string")
}

func TestSystemConfigIsValidVerityInValidPartUuid(t *testing.T) {
	invalidVerity := SystemConfig{
		Verity: &Verity{
			DataPartition: VerityPartition{
				IdType: "PartUuid",
				Id:     "incorrect-uuid-format",
			},
			HashPartition: VerityPartition{
				IdType: "PartLabel",
				Id:     "hash_partition",
			},
		},
	}

	err := invalidVerity.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid Id format")
}
