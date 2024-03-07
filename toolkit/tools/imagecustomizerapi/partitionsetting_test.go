// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestPartitionIsValidInvalidMountIdentifier(t *testing.T) {
	partition := PartitionSetting{
		ID:              "a",
		MountIdentifier: "bad",
	}

	err := partition.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid")
	assert.ErrorContains(t, err, "MountIdentifierType")
}
