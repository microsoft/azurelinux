// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"path"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

func addRemoveAndUpdatePackages(buildDir string, baseConfigPath string, config *imagecustomizerapi.SystemConfig,
	imageChroot *safechroot.Chroot, rpmsSources []string, useBaseImageRpmRepos bool, partitionsCustomized bool,
) error {
	var err error

	// Note: The 'validatePackageLists' function read the PackageLists files and merged them into the inline package lists.
	needRpmsSources := len(config.PackagesInstall) > 0 || len(config.PackagesUpdate) > 0 ||
		config.UpdateBaseImagePackages || partitionsCustomized

	// Mount RPM sources.
	var mounts *rpmSourcesMounts
	if needRpmsSources {
		mounts, err = mountRpmSources(buildDir, imageChroot, rpmsSources, useBaseImageRpmRepos)
		if err != nil {
			return err
		}
		defer mounts.close()
	}

	if partitionsCustomized {
		logger.Log.Infof("Updating initrd file")

		err = installOrUpdatePackages("reinstall", []string{"initramfs"}, imageChroot)
		if err != nil {
			return err
		}
	}

	err = removePackages(config.PackagesRemove, imageChroot)
	if err != nil {
		return err
	}

	if config.UpdateBaseImagePackages {
		err = updateAllPackages(imageChroot)
		if err != nil {
			return err
		}
	}

	logger.Log.Infof("Installing packages: %v", config.PackagesInstall)
	err = installOrUpdatePackages("install", config.PackagesInstall, imageChroot)
	if err != nil {
		return err
	}

	logger.Log.Infof("Updating packages: %v", config.PackagesUpdate)
	err = installOrUpdatePackages("update", config.PackagesUpdate, imageChroot)
	if err != nil {
		return err
	}

	// Unmount RPM sources.
	if mounts != nil {
		err = mounts.close()
		if err != nil {
			return err
		}
	}

	return nil
}

func collectPackagesList(baseConfigPath string, packageLists []string, packages []string) ([]string, error) {
	var err error

	// Read in the packages from the package list files.
	var allPackages []string
	for _, packageListRelativePath := range packageLists {
		packageListFilePath := path.Join(baseConfigPath, packageListRelativePath)

		var packageList imagecustomizerapi.PackageList
		err = imagecustomizerapi.UnmarshalYamlFile(packageListFilePath, &packageList)
		if err != nil {
			return nil, fmt.Errorf("failed to read package list file (%s):\n%w", packageListFilePath, err)
		}

		allPackages = append(allPackages, packageList.Packages...)
	}

	allPackages = append(allPackages, packages...)
	return allPackages, nil
}

func removePackages(allPackagesToRemove []string, imageChroot *safechroot.Chroot) error {
	logger.Log.Infof("Removing packages: %v", allPackagesToRemove)

	tnfRemoveArgs := []string{
		"-v", "remove", "--assumeyes", "--disablerepo", "*",
		// Placeholder for package name.
		"",
	}

	// Remove packages.
	// Do this one at a time, to avoid running out of memory.
	for _, packageName := range allPackagesToRemove {
		tnfRemoveArgs[len(tnfRemoveArgs)-1] = packageName

		err := imageChroot.Run(func() error {
			return shell.ExecuteLiveWithCallback(tdnfRemoveStdoutFilter, logger.Log.Debug, false, "tdnf",
				tnfRemoveArgs...)
		})
		if err != nil {
			return fmt.Errorf("failed to remove package (%s):\n%w", packageName, err)
		}
	}

	return nil
}

// Process the stdout of a `tdnf install -v` call and send the list of installed packages to the debug log.
func tdnfRemoveStdoutFilter(args ...interface{}) {
	const tdnfInstallPrefix = "Removing: "

	if len(args) == 0 {
		return
	}

	line := args[0].(string)
	if !strings.HasPrefix(line, tdnfInstallPrefix) {
		return
	}

	logger.Log.Debug(line)
}

func updateAllPackages(imageChroot *safechroot.Chroot) error {
	logger.Log.Infof("Updating base image packages")

	tnfUpdateArgs := []string{
		"-v", "update", "--nogpgcheck", "--assumeyes",
		"--setopt", fmt.Sprintf("reposdir=%s", rpmsMountParentDirInChroot),
	}

	err := imageChroot.Run(func() error {
		return shell.ExecuteLiveWithCallback(tdnfInstallOrUpdateStdoutFilter, logger.Log.Debug, false, "tdnf",
			tnfUpdateArgs...)
	})
	if err != nil {
		return fmt.Errorf("failed to update packages:\n%w", err)
	}

	return nil
}

func installOrUpdatePackages(action string, allPackagesToAdd []string, imageChroot *safechroot.Chroot) error {
	// Create tdnf command args.
	// Note: When using `--repofromdir`, tdnf will not use any default repos and will only use the last
	// `--repofromdir` specified.
	tnfInstallArgs := []string{
		"-v", action, "--nogpgcheck", "--assumeyes",
		"--setopt", fmt.Sprintf("reposdir=%s", rpmsMountParentDirInChroot),
		// Placeholder for package name.
		"",
	}

	// Install packages.
	// Do this one at a time, to avoid running out of memory.
	for _, packageName := range allPackagesToAdd {
		tnfInstallArgs[len(tnfInstallArgs)-1] = packageName

		err := imageChroot.Run(func() error {
			return shell.ExecuteLiveWithCallback(tdnfInstallOrUpdateStdoutFilter, logger.Log.Debug, false, "tdnf",
				tnfInstallArgs...)
		})
		if err != nil {
			return fmt.Errorf("failed to %s package (%s):\n%w", action, packageName, err)
		}
	}

	return nil
}

// Process the stdout of a `tdnf install -v` call and send the list of installed packages to the debug log.
func tdnfInstallOrUpdateStdoutFilter(args ...interface{}) {
	const tdnfInstallPrefix = "Installing/Updating: "

	if len(args) == 0 {
		return
	}

	line := args[0].(string)
	if !strings.HasPrefix(line, tdnfInstallPrefix) {
		return
	}

	logger.Log.Debug(line)
}
