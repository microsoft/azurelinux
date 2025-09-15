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
	assert.ErrorContains(t, err, "invalid idType value")
	assert.ErrorContains(t, err, "invalid value (bad)")
}

func TestMountPointIsValidInvalidPath(t *testing.T) {
	mountPoint := MountPoint{
		IdType: MountIdentifierTypeDefault,
		Path:   "",
	}

	err := mountPoint.IsValid()
	assert.ErrorContains(t, err, "invalid path:\npath cannot be empty")
}

func TestMountPointIsValidInvalidOptions(t *testing.T) {
	mountPoint := MountPoint{
		IdType:  MountIdentifierTypeDefault,
		Path:    "/mnt",
		Options: "invalid\toptions",
	}

	err := mountPoint.IsValid()
	assert.ErrorContains(t, err, "options (invalid\toptions) contain spaces, tabs, or newlines and are invalid")
}
