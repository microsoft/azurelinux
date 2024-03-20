// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestOSValidEmpty(t *testing.T) {
	testValidYamlValue[*OS](t, "{ }", &OS{})
}

func TestOSValidHostname(t *testing.T) {
	testValidYamlValue[*OS](t, "{ \"hostname\": \"validhostname\" }", &OS{Hostname: "validhostname"})
}

func TestOSInvalidHostname(t *testing.T) {
	testInvalidYamlValue[*OS](t, "{ \"hostname\": \"invalid_hostname\" }")
}

func TestOSInvalidAdditionalFiles(t *testing.T) {
	testInvalidYamlValue[*OS](t, "{ \"additionalFiles\": { \"a.txt\": [] } }")
}

func TestOSIsValidVerityInValidPartUuid(t *testing.T) {
	invalidVerity := OS{
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

func TestOSIsValidOverlayInvalidLowerDir(t *testing.T) {
	overlayWithInvalidLowerDir := Overlay{
		LowerDir: "",
		UpperDir: "/upper",
		WorkDir:  "/work",
	}

	err := overlayWithInvalidLowerDir.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "path cannot be empty")
}
