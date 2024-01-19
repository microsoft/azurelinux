// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safeloopback"
)

type ImageConnection struct {
	loopback            *safeloopback.Loopback
	chroot              *safechroot.Chroot
	chrootIsExistingDir bool
}

func NewImageConnection() *ImageConnection {
	return &ImageConnection{}
}

func (c *ImageConnection) ConnectLoopback(diskFilePath string) error {
	if c.loopback != nil {
		return fmt.Errorf("loopback already connected")
	}

	loopback, err := safeloopback.NewLoopback(diskFilePath)
	if err != nil {
		return fmt.Errorf("failed to mount raw disk (%s) as a loopback device:\n%w", diskFilePath, err)
	}
	c.loopback = loopback
	return nil
}

func (c *ImageConnection) ConnectChroot(rootDir string, isExistingDir bool, extraDirectories []string,
	extraMountPoints []*safechroot.MountPoint,
) error {
	if c.chroot != nil {
		return fmt.Errorf("chroot already connected")
	}

	chroot := safechroot.NewChroot(rootDir, isExistingDir)
	err := chroot.Initialize("", extraDirectories, extraMountPoints)
	if err != nil {
		return err
	}
	c.chroot = chroot
	c.chrootIsExistingDir = isExistingDir

	return nil
}

func (c *ImageConnection) Chroot() *safechroot.Chroot {
	return c.chroot
}

func (c *ImageConnection) Loopback() *safeloopback.Loopback {
	return c.loopback
}

func (c *ImageConnection) Close() {
	if c.chroot != nil {
		c.chroot.Close(c.chrootIsExistingDir)
	}

	if c.loopback != nil {
		c.loopback.Close()
	}
}

func (c *ImageConnection) CleanClose() error {
	err := c.chroot.Close(c.chrootIsExistingDir)
	if err != nil {
		return err
	}

	err = c.loopback.CleanClose()
	if err != nil {
		return err
	}

	return nil
}
