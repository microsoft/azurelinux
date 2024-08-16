// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestOverlayValidConfiguration(t *testing.T) {
	overlay := Overlay{
		LowerDir:          "/lower",
		UpperDir:          "/upper",
		WorkDir:           "/work",
		MountPoint:        "/mnt",
		IsRootfsOverlay:   false,
		MountDependencies: []string{"/var"},
		MountOptions:      "noatime",
	}

	err := overlay.IsValid()
	assert.NoError(t, err)
}

func TestOverlayInvalidEmptyLowerDir(t *testing.T) {
	overlay := Overlay{
		LowerDir:          "",
		UpperDir:          "/upper",
		WorkDir:           "/work",
		MountPoint:        "/mnt",
		IsRootfsOverlay:   false,
		MountDependencies: []string{"/var"},
		MountOptions:      "noatime",
	}

	err := overlay.IsValid()
	assert.ErrorContains(t, err, "invalid lowerDir ()")
	assert.ErrorContains(t, err, "path cannot be empty")
}

func TestOverlayInvalidInvalidWorkDir(t *testing.T) {
	overlay := Overlay{
		LowerDir:          "/lower",
		UpperDir:          "/upper",
		WorkDir:           " ",
		MountPoint:        "/mnt",
		IsRootfsOverlay:   false,
		MountDependencies: []string{"/var"},
		MountOptions:      "noatime",
	}

	err := overlay.IsValid()
	assert.ErrorContains(t, err, "invalid workDir ( )")
	assert.ErrorContains(t, err, "path ( ) contains spaces and is invalid")
}

func TestOverlayInvalidSameUpperAndWorkDir(t *testing.T) {
	overlay := Overlay{
		LowerDir:          "/lower",
		UpperDir:          "/invalid/same",
		WorkDir:           "/invalid/same",
		MountPoint:        "/mnt",
		IsRootfsOverlay:   false,
		MountDependencies: []string{"/var"},
		MountOptions:      "noatime",
	}

	err := overlay.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "upperDir and workDir must be distinct")
}

func TestOverlayInvalidWorkDirSubsUpperDir(t *testing.T) {
	overlay := Overlay{
		LowerDir:          "/lower",
		UpperDir:          "/invalid",
		WorkDir:           "/invalid/same",
		MountPoint:        "/mnt",
		IsRootfsOverlay:   false,
		MountDependencies: []string{"/var"},
		MountOptions:      "noatime",
	}

	err := overlay.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "upperDir (/invalid) should not be a subdirectory of workDir (/invalid/same)")
}

func TestOverlayInvalidUpperDirSubsWorkDir(t *testing.T) {
	overlay := Overlay{
		LowerDir:          "/lower",
		UpperDir:          "/invalid/same",
		WorkDir:           "/invalid",
		MountPoint:        "/mnt",
		IsRootfsOverlay:   false,
		MountDependencies: []string{"/var"},
		MountOptions:      "noatime",
	}

	err := overlay.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "workDir (/invalid) should not be a subdirectory of upperDir (/invalid/same)")
}

func TestOverlayInvalidMountDependencyPath(t *testing.T) {
	overlay := Overlay{
		LowerDir:          "/lower",
		UpperDir:          "/upper",
		WorkDir:           "/work",
		MountPoint:        "/mnt",
		IsRootfsOverlay:   false,
		MountDependencies: []string{"invalid/path"},
		MountOptions:      "noatime",
	}

	err := overlay.IsValid()
	assert.ErrorContains(t, err, "invalid mountDependencies (invalid/path)")
	assert.ErrorContains(t, err, "must be an absolute path")
}

func TestOverlayValidEmptyMountDependencies(t *testing.T) {
	overlay := Overlay{
		LowerDir:          "/lower",
		UpperDir:          "/upper",
		WorkDir:           "/work",
		MountPoint:        "/mnt",
		IsRootfsOverlay:   false,
		MountDependencies: []string{},
		MountOptions:      "noatime",
	}

	err := overlay.IsValid()
	assert.NoError(t, err)
}

func TestOverlayInvalidMountOptions(t *testing.T) {
	overlay := Overlay{
		LowerDir:          "/lower",
		UpperDir:          "/upper",
		WorkDir:           "/work",
		MountPoint:        "/mnt",
		IsRootfsOverlay:   false,
		MountDependencies: []string{"/var"},
		MountOptions:      "invalid option with spaces",
	}

	err := overlay.IsValid()
	assert.ErrorContains(t, err, "mountOptions (invalid option with spaces) contains spaces and is invalid")
}
