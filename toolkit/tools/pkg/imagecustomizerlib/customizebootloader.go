// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"
)

func handleBootLoader(baseConfigPath string, config *imagecustomizerapi.Config, imageConnection *ImageConnection,
) error {

	switch config.OS.ResetBootLoaderType {
	case imagecustomizerapi.ResetBootLoaderTypeHard:
		err := hardResetBootLoader(baseConfigPath, config, imageConnection)
		if err != nil {
			return err
		}

	default:
		// Append the kernel command-line args to the existing grub config.
		err := addKernelCommandLine(config.OS.KernelCommandLine.ExtraCommandLine, imageConnection.Chroot())
		if err != nil {
			return fmt.Errorf("failed to add extra kernel command line:\n%w", err)
		}
	}

	return nil
}

func hardResetBootLoader(baseConfigPath string, config *imagecustomizerapi.Config, imageConnection *ImageConnection,
) error {
	var err error
	logger.Log.Infof("Hard reset bootloader config")

	bootCustomizer, err := NewBootCustomizer(imageConnection.Chroot())
	if err != nil {
		return err
	}

	currentSelinuxMode, err := bootCustomizer.GetSELinuxMode(imageConnection.Chroot())
	if err != nil {
		return fmt.Errorf("failed to get existing SELinux mode:\n%w", err)
	}

	var rootMountIdType imagecustomizerapi.MountIdentifierType
	var bootType imagecustomizerapi.BootType
	if config.CustomizePartitions() {
		rootFileSystem, foundRootFileSystem := sliceutils.FindValueFunc(config.Storage.FileSystems,
			func(fileSystem imagecustomizerapi.FileSystem) bool {
				return fileSystem.MountPoint != nil &&
					fileSystem.MountPoint.Path == "/"
			},
		)
		if !foundRootFileSystem {
			return fmt.Errorf("failed to find root filesystem (i.e. mount equal to '/')")
		}

		rootMountIdType = rootFileSystem.MountPoint.IdType
		bootType = config.Storage.BootType
	} else {
		rootMountIdType, err = findRootMountIdTypeFromFstabFile(imageConnection)
		if err != nil {
			return fmt.Errorf("failed to get image's root mount ID type:\n%w", err)
		}

		bootType, err = getImageBootType(imageConnection)
		if err != nil {
			return fmt.Errorf("failed to get image's boot type:\n%w", err)
		}
	}

	// Hard-reset the grub config.
	err = configureDiskBootLoader(imageConnection, rootMountIdType, bootType, config.OS.SELinux,
		config.OS.KernelCommandLine, currentSelinuxMode)
	if err != nil {
		return fmt.Errorf("failed to configure bootloader:\n%w", err)
	}

	return nil
}

// Inserts new kernel command-line args into the grub config file.
func addKernelCommandLine(kernelExtraArguments imagecustomizerapi.KernelExtraArguments,
	imageChroot *safechroot.Chroot,
) error {
	var err error

	if kernelExtraArguments == "" {
		// Nothing to do.
		return nil
	}

	logger.Log.Infof("Setting KernelCommandLine.ExtraCommandLine")

	bootCustomizer, err := NewBootCustomizer(imageChroot)
	if err != nil {
		return err
	}

	err = bootCustomizer.AddKernelCommandLine(string(kernelExtraArguments))
	if err != nil {
		return err
	}

	err = bootCustomizer.WriteToFile(imageChroot)
	if err != nil {
		return err
	}

	return nil
}
