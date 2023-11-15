// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/ptrutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/stretchr/testify/assert"
)

func TestUpdateHostname(t *testing.T) {
	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses a chroot")
	}

	// Setup environment.
	proposedDir := filepath.Join(tmpDir, "TestUpdateHostname")
	chroot := safechroot.NewChroot(proposedDir, false)
	err := chroot.Initialize("", []string{}, []*safechroot.MountPoint{})
	assert.NoError(t, err)
	defer chroot.Close(false)

	err = os.MkdirAll(filepath.Join(chroot.RootDir(), "etc"), os.ModePerm)
	assert.NoError(t, err)

	// Set hostname.
	expectedHostname := "testhostname"
	err = updateHostname(expectedHostname, chroot)
	assert.NoError(t, err)

	// Ensure hostname was correctly set.
	actualHostname, err := os.ReadFile(filepath.Join(chroot.RootDir(), "etc/hostname"))
	assert.NoError(t, err)
	assert.Equal(t, expectedHostname, string(actualHostname))
}

func TestCopyAdditionalFiles(t *testing.T) {
	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses a chroot")
	}

	proposedDir := filepath.Join(tmpDir, "TestCopyAdditionalFiles")
	chroot := safechroot.NewChroot(proposedDir, false)
	baseConfigPath := testDir

	err := chroot.Initialize("", []string{}, []*safechroot.MountPoint{})
	assert.NoError(t, err)
	defer chroot.Close(false)

	copy_2_filemode := os.FileMode(0o777)

	err = copyAdditionalFiles(baseConfigPath, map[string]imagecustomizerapi.FileConfigList{
		"files/a.txt": {
			{Path: "/a_copy_1.txt"},
			{Path: "/a_copy_2.txt", Permissions: ptrutils.PtrTo(imagecustomizerapi.FilePermissions(copy_2_filemode))},
		},
	}, chroot)
	assert.NoError(t, err)

	orig_path := filepath.Join(baseConfigPath, "files/a.txt")
	copy_1_path := filepath.Join(chroot.RootDir(), "a_copy_1.txt")
	copy_2_path := filepath.Join(chroot.RootDir(), "a_copy_2.txt")

	// Make sure the files exist.
	orig_stat, err := os.Stat(orig_path)
	assert.NoError(t, err)

	copy_1_stat, err := os.Stat(copy_1_path)
	assert.NoError(t, err)

	copy_2_stat, err := os.Stat(copy_2_path)
	assert.NoError(t, err)

	// Make sure the filemode of the original file is different from the target filemode,
	// as otherwise it would defeat the purpose of the test.
	assert.NotEqual(t, copy_2_filemode, orig_stat.Mode()&os.ModePerm)

	// Make sure the file permissions are the expected values.
	assert.Equal(t, orig_stat.Mode()&os.ModePerm, copy_1_stat.Mode()&os.ModePerm)
	assert.Equal(t, copy_2_filemode, copy_2_stat.Mode()&os.ModePerm)

	// Make sure the files' contents are correct.
	orig_contents, err := os.ReadFile(orig_path)
	assert.NoError(t, err)

	copy_1_contents, err := os.ReadFile(copy_1_path)
	assert.NoError(t, err)

	copy_2_contents, err := os.ReadFile(copy_2_path)
	assert.NoError(t, err)

	assert.Equal(t, orig_contents, copy_1_contents)
	assert.Equal(t, orig_contents, copy_2_contents)
}
