// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/ptrutils"
	"github.com/stretchr/testify/assert"
)

func TestDirConfigListIsValidEmpty(t *testing.T) {
	list := DirConfigList{}
	err := list.IsValid()
	assert.NoError(t, err)
}

func TestDirConfigListIsValidValidItem(t *testing.T) {
	list := DirConfigList{
		DirConfig{
			Source:      "a.txt",
			Destination: "/a.txt",
		},
	}
	err := list.IsValid()
	assert.NoError(t, err)
}

func TestDirConfigListIsValidValidItemWithPermissions(t *testing.T) {
	list := DirConfigList{
		DirConfig{
			Source:               "a.txt",
			Destination:          "/a.txt",
			NewDirPermissions:    ptrutils.PtrTo(FilePermissions(0o777)),
			MergedDirPermissions: ptrutils.PtrTo(FilePermissions(0o777)),
			ChildFilePermissions: ptrutils.PtrTo(FilePermissions(0o777)),
		},
	}
	err := list.IsValid()
	assert.NoError(t, err)
}

func TestDirConfigListIsValidEmptySource(t *testing.T) {
	list := DirConfigList{
		DirConfig{
			Source:      "",
			Destination: "/a.txt",
		},
	}
	err := list.IsValid()
	assert.ErrorContains(t, err, "invalid value at index 0")
	assert.ErrorContains(t, err, "invalid 'source' value: empty string")
}

func TestDirConfigListIsValidEmptyDestination(t *testing.T) {
	list := DirConfigList{
		DirConfig{
			Source:      "a.txt",
			Destination: "",
		},
	}
	err := list.IsValid()
	assert.ErrorContains(t, err, "invalid value at index 0")
	assert.ErrorContains(t, err, "invalid 'destination' value: empty string")
}

func TestDirConfigListIsValidInvalidNewDirPermissions(t *testing.T) {
	list := DirConfigList{
		DirConfig{
			Source:            "a.txt",
			Destination:       "/a.txt",
			NewDirPermissions: ptrutils.PtrTo(FilePermissions(0o1000)),
		},
	}
	err := list.IsValid()
	assert.ErrorContains(t, err, "invalid value at index 0")
	assert.ErrorContains(t, err, "invalid newDirPermissions value")
	assert.ErrorContains(t, err, "0o1000 contains non-permission bits")
}

func TestDirConfigListIsValidInvalidMergedDirPermissions(t *testing.T) {
	list := DirConfigList{
		DirConfig{
			Source:               "a.txt",
			Destination:          "/a.txt",
			MergedDirPermissions: ptrutils.PtrTo(FilePermissions(0o1000)),
		},
	}
	err := list.IsValid()
	assert.ErrorContains(t, err, "invalid value at index 0")
	assert.ErrorContains(t, err, "invalid mergedDirPermissions value")
	assert.ErrorContains(t, err, "0o1000 contains non-permission bits")
}

func TestDirConfigListIsValidInvalidChildFilePermissions(t *testing.T) {
	list := DirConfigList{
		DirConfig{
			Source:               "a.txt",
			Destination:          "/a.txt",
			ChildFilePermissions: ptrutils.PtrTo(FilePermissions(0o1000)),
		},
	}
	err := list.IsValid()
	assert.ErrorContains(t, err, "invalid value at index 0")
	assert.ErrorContains(t, err, "invalid childFilePermissions value")
	assert.ErrorContains(t, err, "0o1000 contains non-permission bits")
}
