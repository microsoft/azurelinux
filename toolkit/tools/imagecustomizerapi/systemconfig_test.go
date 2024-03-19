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
	assert.ErrorContains(t, err, "duplicate partitionSettings ID")
}

func TestSystemConfigIsValidVerityInValidPartUuid(t *testing.T) {
	invalidVerity := SystemConfig{
		Verity: &Verity{
			DataPartition: IdentifiedPartition{
				IdType: "part-uuid",
				Id:     "incorrect-uuid-format",
			},
			HashPartition: IdentifiedPartition{
				IdType: "part-label",
				Id:     "hash_partition",
			},
		},
	}

	err := invalidVerity.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid id format")
}

func TestSystemConfigIsValidOverlayInvalidLowerDir(t *testing.T) {
	overlayWithInvalidLowerDir := Overlay{
		LowerDir: "",
		UpperDir: "/upper",
		WorkDir:  "/work",
	}

	err := overlayWithInvalidLowerDir.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "path cannot be empty")
}
