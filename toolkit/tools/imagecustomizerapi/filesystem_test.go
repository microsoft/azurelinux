// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestFileSystemIsValidBadDeviceId(t *testing.T) {
	fileSystem := FileSystem{
		DeviceId: "",
		Type:     FileSystemTypeExt4,
	}

	err := fileSystem.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid deviceId value: must not be empty")
}
