// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Package that assists with mounting and unmounting cleanly.
package safemount

import (
	"fmt"
	"os"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"golang.org/x/sys/unix"
)

type Mount struct {
	target     string
	isMounted  bool
	dirCreated bool
}

// Creates a new system mount.
func NewMount(source, target, fstype string, flags uintptr, data string, makeAndDeleteDir bool) (*Mount, error) {
	var err error

	mount := &Mount{
		target: target,
	}

	// Try to create the mount.
	err = mount.newMountHelper(source, target, fstype, flags, data, makeAndDeleteDir)
	if err != nil {
		// Cleanup anything created during the failed mount.
		cleanupErr := mount.Close()
		if cleanupErr != nil {
			logger.Log.Warnf("failed to cleanup failed mount: %s", cleanupErr)
		}
		return nil, err
	}

	return mount, nil
}

func (m *Mount) newMountHelper(source, target, fstype string, flags uintptr, data string, makeAndDeleteDir bool) error {
	var err error

	logger.Log.Debugf("Mounting: source: (%s), target: (%s), fstype: (%s), flags: (%#x), data: (%s)",
		source, target, fstype, flags, data)

	if makeAndDeleteDir {
		// Create the mount target directory.
		err = os.MkdirAll(target, os.ModePerm)
		if err != nil {
			return fmt.Errorf("failed to create mount directory (%s):\n%w", target, err)
		}

		m.dirCreated = true
	}

	// Create the mount.
	err = unix.Mount(source, target, fstype, flags, data)
	if err != nil {
		return fmt.Errorf("failed to mount (%s) to (%s):\n%w", source, target, err)
	}

	m.isMounted = true
	return nil
}

// Target returns the target directory of the mount.
func (m *Mount) Target() string {
	return m.target
}

// Close removes the system mount.
// This function is safe to call multiple times.
func (m *Mount) Close() error {
	var err error

	logger.Log.Debugf("Unmounting (%s)", m.target)

	if m.isMounted {
		err = unix.Unmount(m.target, 0)
		if err != nil {
			return fmt.Errorf("failed to unmount (%s):\n%w", m.target, err)
		}

		m.isMounted = false
	}

	if m.dirCreated {
		// Note: Do not use `RemoveAll` here in case the unmount silently failed.
		// (This is unlikely. But "belt and braces".)
		err = os.Remove(m.target)
		if err != nil {
			return fmt.Errorf("failed to delete source rpms mount directory (%s):\n%w", m.target, err)
		}

		m.dirCreated = false
	}

	return nil
}
