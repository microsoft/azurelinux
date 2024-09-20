// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/ptrutils"
	"github.com/stretchr/testify/assert"
)

func TestAdditionalFilesIsValidNoDestination(t *testing.T) {
	additionalFiles := AdditionalFileList{
		{
			Destination: "",
			Source:      "a.txt",
		},
	}
	err := additionalFiles.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid value at index 0")
	assert.ErrorContains(t, err, "detination path must not be empty")
}

func TestAdditionalFilesIsValidNoSourceOrContent(t *testing.T) {
	additionalFiles := AdditionalFileList{
		{
			Destination: "/a.txt",
		},
	}
	err := additionalFiles.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid value at index 0")
	assert.ErrorContains(t, err, "must specify either 'path' or 'content'")
}

func TestAdditionalFilesIsValidBothSourceAndContent(t *testing.T) {
	additionalFiles := AdditionalFileList{
		{
			Destination: "/a.txt",
			Source:      "a.txt",
			Content:     ptrutils.PtrTo("abc"),
		},
	}
	err := additionalFiles.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid value at index 0")
	assert.ErrorContains(t, err, "cannot specify both 'path' and 'content'")
}

func TestAdditionalFilesIsValidBadPermissions(t *testing.T) {
	additionalFiles := AdditionalFileList{
		{
			Destination: "/a.txt",
			Source:      "a.txt",
			Permissions: ptrutils.PtrTo(FilePermissions(0o7000)),
		},
	}
	err := additionalFiles.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid value at index 0")
	assert.ErrorContains(t, err, "invalid permissions value")
	assert.ErrorContains(t, err, "0o7000 contains non-permission bits")
}
