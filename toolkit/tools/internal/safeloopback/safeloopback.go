// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Package that assists with attach and detaching a loopback device cleanly.
package safeloopback

import (
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

type Loopback struct {
	devicePath     string
	diskFilePath   string
	diskIdMaj      string
	diskIdMin      string
	isAttached     bool
	explicitDelete bool
	children       []Loopback
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
	l.explicitDelete = false

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

	logger.Log.Debugf("Processing child devices")
	childBlockDevices, err := diskutils.GetDeviceChildren(l.devicePath)
	if err != nil {
		return err
	}

	for _, childDevice := range childBlockDevices {

		logger.Log.Debugf("  Found child device: (%s %s:%s)", childDevice.Name, childDevice.Maj, childDevice.Min)

		// Add device
		loopbackDevice := Loopback{
			devicePath:     "/dev/" + childDevice.Name,
			diskFilePath:   "",
			diskIdMaj:      childDevice.Maj,
			diskIdMin:      childDevice.Min,
			isAttached:     true,
			explicitDelete: false,
		}

		// call mknod if device file does not exist (when running in a
		// container, udev does not fire correctly)...
		exists, err := file.PathExists(loopbackDevice.devicePath)
		if err != nil {
			return err
		}
		if !exists {
			logger.Log.Debugf("    Block device file for (%s %s:%s) not found. Creating one.", loopbackDevice.devicePath, loopbackDevice.diskIdMaj, loopbackDevice.diskIdMin)
			// mknod /dev/loop23p2 b 259 5
			mknodParams := []string{loopbackDevice.devicePath, "b", loopbackDevice.diskIdMaj, loopbackDevice.diskIdMin}
			err = shell.ExecuteLive(false, "mknod", mknodParams...)
			if err != nil {
				logger.Log.Errorf("failed to create nod file:\n%w", err)
			}
			loopbackDevice.explicitDelete = true
		}

		l.children = append(l.children, loopbackDevice)
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

	logger.Log.Debugf("Closing child block devices if any.")
	for i, _ := range l.children {
		logger.Log.Debugf("  Found child block device (%s %s:%s)", l.children[i].devicePath, l.children[i].diskIdMaj, l.children[i].diskIdMin)
		if l.children[i].explicitDelete {
			logger.Log.Debugf("    Child block devic is marked for explicit deletion.")
			err := file.RemoveFileIfExists(l.children[i].devicePath)
			if err != nil {
				return err
			}
			l.children[i].explicitDelete = false
		}
	}

	return nil
}
