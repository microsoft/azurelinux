// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package installutils

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

// Overlay Struct representing an overlay mount
type Overlay struct {
	DevicePath string
	lowerDir   string
	upperDir   string
	workDir    string
}

func (o Overlay) getMountArgs() string {

	return fmt.Sprintf("lowerdir=%s,upperdir=%s,workdir=%s", o.lowerDir, o.upperDir, o.workDir)
}

func (o Overlay) setupFolders() (err error) {
	err = os.MkdirAll(o.lowerDir, os.ModePerm)
	if err != nil {
		logger.Log.Errorf("Could not create directory (%s)", o.lowerDir)
		return
	}
	err = os.MkdirAll(o.upperDir, os.ModePerm)
	if err != nil {
		logger.Log.Errorf("Could not create directory (%s)", o.upperDir)
		return
	}
	err = os.MkdirAll(o.workDir, os.ModePerm)
	if err != nil {
		logger.Log.Errorf("Could not create directory (%s)", o.workDir)
		return
	}
	err = mount(o.lowerDir, o.DevicePath, "", "")
	if err != nil {
		logger.Log.Errorf("Could not mount %s to %s", o.DevicePath, o.lowerDir)
	}
	return
}

func (o Overlay) getUpperDir() (upperDir string) {
	return o.upperDir
}

func (o Overlay) unmount() (err error) {
	err = umount(o.lowerDir)
	if err != nil {
		logger.Log.Warnf("Unmount of loopback(%s) failed. Still continuing", o.lowerDir)
	}

	temperr := diskutils.DetachLoopbackDevice(o.DevicePath)
	if temperr != nil {
		logger.Log.Warnf("Losetup of loopback(%s) failed. Still continuing", o.lowerDir)
		err = temperr
	}
	return
}

// NewOverlay Creates the overlay struct
func NewOverlay(devicePath string) Overlay {
	_, deviceName := filepath.Split(devicePath)
	lowerDir := "/lowerdir" + deviceName
	upperDir := "/upperdir" + deviceName
	workDir := "/workdir" + deviceName

	o := Overlay{
		devicePath,
		lowerDir,
		upperDir,
		workDir,
	}

	return o
}
