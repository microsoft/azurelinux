// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"errors"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

type resolvConfType int

const (
	resolvConfTypeNone resolvConfType = iota
	resolvConfTypeSymlink
	resolvConfTypeFile
)

type resolvConfInfo struct {
	existingType resolvConfType
	fileContents string
	symlinkPath  string
}

const (
	resolvConfPath        = "/etc/resolv.conf"
	resolvSystemdStubPath = "../run/systemd/resolve/stub-resolv.conf"
)

// Override the resolv.conf file, so that in-chroot processes can access the network.
// For example, to install packages from packages.microsoft.com.
func overrideResolvConf(imageChroot *safechroot.Chroot) (resolvConfInfo, error) {
	logger.Log.Infof("Overriding resolv.conf file")

	imageResolveConfPath := filepath.Join(imageChroot.RootDir(), resolvConfPath)

	existing := resolvConfInfo{}

	stat, err := os.Lstat(imageResolveConfPath)
	if err != nil {
		if !os.IsNotExist(err) {
			return resolvConfInfo{}, fmt.Errorf("failed to stat resolv.conf file:\n%w", err)
		}
		existing.existingType = resolvConfTypeNone
	} else if stat.Mode()&os.ModeSymlink != 0 {
		symlinkPath, err := os.Readlink(imageResolveConfPath)
		if err != nil {
			return resolvConfInfo{}, fmt.Errorf("failed to read resolv.conf symlink's path:\n%w", err)
		}
		existing.existingType = resolvConfTypeSymlink
		existing.symlinkPath = symlinkPath
	} else {
		fileContents, err := file.Read(imageResolveConfPath)
		if err != nil {
			return resolvConfInfo{}, fmt.Errorf("failed to read resolv.conf file:\n%w", err)
		}
		existing.existingType = resolvConfTypeFile
		existing.fileContents = fileContents
	}

	// Remove the existing resolv.conf file, if it exists.
	// Note: It is assumed that the image will have a process that runs on boot that will override the resolv.conf
	// file. For example, systemd-resolved. So, it isn't neccessary to make a back-up of the existing file.
	err = os.RemoveAll(imageResolveConfPath)
	if err != nil {
		return resolvConfInfo{}, fmt.Errorf("failed to delete existing resolv.conf file:\n%w", err)
	}

	err = file.Copy(resolvConfPath, imageResolveConfPath)
	if err != nil {
		return resolvConfInfo{}, fmt.Errorf("failed to override resolv.conf file with host's resolv.conf:\n%w", err)
	}

	return existing, nil
}

func restoreResolvConf(existing resolvConfInfo, imageChroot *safechroot.Chroot) error {
	imageResolveConfPath := filepath.Join(imageChroot.RootDir(), resolvConfPath)

	// Delete the overridden resolv.conf file.
	err := os.RemoveAll(imageResolveConfPath)
	if err != nil {
		return fmt.Errorf("failed to delete overridden resolv.conf file: %w", err)
	}

	switch existing.existingType {
	case resolvConfTypeNone:
		// Check if systemd-resolved is enabled.
		resolvedEnabled := true
		err := imageChroot.UnsafeRun(func() error {
			err := shell.ExecuteLive(true, "systemctl", "is-enabled", "systemd-resolved.service")

			var exitError *exec.ExitError
			if errors.As(err, &exitError) && exitError.ExitCode() == 1 {
				resolvedEnabled = false
				return nil
			}
			return err
		})
		if err != nil {
			return fmt.Errorf("failed to check if systemd-resolved service is enabled:\n%w", err)
		}

		if resolvedEnabled {
			// The systemd-resolved.service is enabled.
			// So, create the symlink for the resolv.conf file.
			// While technically this symlink will be automatically created on first boot, doing it now is helpful for
			// verity images where the root filesystem is readonly.
			err := os.Symlink(resolvSystemdStubPath, imageResolveConfPath)
			if err != nil {
				return fmt.Errorf("failed to create resolv.conf symlink:\n%w", err)
			}
		}

	case resolvConfTypeFile:
		// Restore the resolv.conf file.
		err := file.WriteWithPerm(existing.fileContents, imageResolveConfPath, 0o644)
		if err != nil {
			return fmt.Errorf("failed to restore resolv.conf file:\n%w", err)
		}

	case resolvConfTypeSymlink:
		// Restore the resolv.conf symlink.
		err := os.Symlink(existing.symlinkPath, imageResolveConfPath)
		if err != nil {
			return fmt.Errorf("failed to restore resolv.conf file:\n%w", err)
		}

	default:
		panic(fmt.Sprintf("unexpected imagecustomizerlib.resolvConfType: %#v", existing.existingType))
	}

	return nil
}
