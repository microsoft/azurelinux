// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package safeloopback

import (
	"os"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/buildpipeline"
	"github.com/stretchr/testify/assert"
)

func TestLoopbackCloseWithOpenFileHandle(t *testing.T) {
	if testing.Short() {
		t.Skip("Short mode enabled")
	}

	if !buildpipeline.IsRegularBuild() {
		t.Skip("loopback block device not available")
	}

	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses loopback devices")
	}

	// Create raw disk image file.
	rawDisk, err := diskutils.CreateEmptyDisk(tmpDir, "disk.raw", 4096)
	assert.NoErrorf(t, err, "create empty disk file")

	// Attach image file.
	loopback, err := NewLoopback(rawDisk)
	assert.NoErrorf(t, err, "attach disk file")
	defer loopback.Close()

	// Open a file handle to the disk.
	// If we wanted to do this properly, we could create partitions, mount those partitions, and then create a
	// file on the partition. But just opening the disk file itself is easier.
	diskFile, err := os.OpenFile(loopback.DevicePath(), os.O_RDWR, 0)
	assert.NoErrorf(t, err, "open disk file")
	defer diskFile.Close()

	// Attempt to close the loopback with the file handle open.
	// This should fail since loopback devices won't detach until they are no longer in use.
	err = loopback.CleanClose()
	assert.Error(t, err)

	// Now close the disk file.
	diskFile.Close()

	// Loopback should now detach.
	err = loopback.CleanClose()
	assert.NoError(t, err)
}
