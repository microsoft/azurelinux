// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package installutils

import (
	"fmt"
	"os"
	"path/filepath"

	"microsoft.com/pkggen/imagegen/diskutils"
	"microsoft.com/pkggen/internal/logger"
)

// Overlay Struct representing an overlay mount
type Overlay struct {
	DevicePath string
}

func (o Overlay) getMountArgs() string {

	_, deviceName := filepath.Split(o.DevicePath)
	lowerDir := "/lowerdir" + deviceName
	upperDir := "/upperdir" + deviceName
	workDir := "/workdir" + deviceName
	return fmt.Sprintf("lowerdir=%s,upperdir=%s,workdir=%s", lowerDir, upperDir, workDir)
}

func (o Overlay) setupFolders() (err error) {
	_, deviceName := filepath.Split(o.DevicePath)
	lowerDir := "/lowerdir" + deviceName
	upperDir := "/upperdir" + deviceName
	workDir := "/workdir" + deviceName
	err = os.MkdirAll(lowerDir, os.ModePerm)
	if err != nil {
		logger.Log.Errorf("Could not create directory (%s)", lowerDir)
		return
	}
	err = os.MkdirAll(upperDir, os.ModePerm)
	if err != nil {
		logger.Log.Errorf("Could not create directory (%s)", upperDir)
		return
	}
	err = os.MkdirAll(workDir, os.ModePerm)
	if err != nil {
		logger.Log.Errorf("Could not create directory (%s)", workDir)
		return
	}
	err = mount(lowerDir, o.DevicePath, "", "")
	if err != nil {
		logger.Log.Errorf("Could not mount %s to %s", o.DevicePath, lowerDir)
	}
	return
}

func (o Overlay) getUpperDir() (upperDir string) {

	_, deviceName := filepath.Split(o.DevicePath)
	upperDir = "/upperdir" + deviceName
	return
}

func (o Overlay) unmount() (err error) {
	_, deviceName := filepath.Split(o.DevicePath)
	lowerDir := "/lowerdir" + deviceName
	err = umount(lowerDir)
	if err != nil {
		logger.Log.Warnf("Unmount of loopback(%s) failed. Still continuing", lowerDir)
	}

	err = diskutils.DetachLoopbackDevice(o.DevicePath)
	if err != nil {
		logger.Log.Warnf("Losetup of loopback(%s) failed. Still continuing", lowerDir)
	}
	return
}
