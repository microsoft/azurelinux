// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestMountPointIsValidInvalidIdType(t *testing.T) {
	mountPoint := MountPoint{
		IdType: "bad",
		Path:   "/",
	}

	err := mountPoint.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid")
	assert.ErrorContains(t, err, "idType")
}
