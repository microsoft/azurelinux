// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Package that assists with attach and detaching a loopback device cleanly.
package safeloopback

import (
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
)

type Loopback struct {
	devicePath   string
	diskFilePath string
	diskIdMaj    string
	diskIdMin    string
	isAttached   bool
}

func NewLoopback(diskFilePath string) (*Loopback, error) {
	loopback := &Loopback{
		diskFilePath: diskFilePath,
	}

	err := loopback.newLoopbackHelper()
	if err != nil {
		loopback.Close()
		return nil, err
	}

	return loopback, nil
}

func (l *Loopback) newLoopbackHelper() error {
	// Try to create the mount.
	devicePath, err := diskutils.SetupLoopbackDevice(l.diskFilePath)
	if err != nil {
		return err
	}

	l.devicePath = devicePath
	l.isAttached = true

	// Get the disk's IDs.
	maj, min, err := diskutils.GetDiskIds(l.devicePath)
	if err != nil {
		return err
	}

	l.diskIdMaj = maj
	l.diskIdMin = min

	// Ensure all the partitions have finished populating.
	err = diskutils.WaitForDevicesToSettle()
	if err != nil {
		return err
	}

	return nil
}

func (l *Loopback) DevicePath() string {
	return l.devicePath
}

func (l *Loopback) DiskFilePath() string {
	return l.diskFilePath
}

func (l *Loopback) Close() {
	err := l.close( /*async*/ true)
	if err != nil {
		logger.Log.Warnf("failed to close loopback: %s", err)
	}
}

func (l *Loopback) CleanClose() error {
	return l.close( /*async*/ false)
}

func (l *Loopback) close(async bool) error {
	if l.isAttached {
		err := diskutils.DetachLoopbackDevice(l.devicePath)
		if err != nil {
			return err
		}

		l.isAttached = false
	}

	if !async {
		// The `losetup --detach` call happens asynchronously.
		// So, need to wait for it to complete.
		err := diskutils.WaitForLoopbackToDetach(l.devicePath, l.diskFilePath)
		if err != nil {
			return err
		}

		err = diskutils.BlockOnDiskIOByIds(l.devicePath, l.diskIdMaj, l.diskIdMin)
		if err != nil {
			return err
		}
	}

	return nil
}
