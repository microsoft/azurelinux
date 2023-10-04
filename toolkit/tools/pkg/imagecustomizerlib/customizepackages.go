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

func updatePackages(buildDir string, baseConfigPath string, packagesToAddLists []string, packagesToAdd []string,
	packagesToRemoveLists []string, packagesToRemove []string, imageChroot *safechroot.Chroot, rpmsSources []string,
	useBaseImageRpmRepos bool,
) error {
	var err error

	allPackagesToRemove, err := collectPackagesList(baseConfigPath, packagesToRemoveLists, packagesToRemove)
	if err != nil {
		return err
	}

	allPackagesToAdd, err := collectPackagesList(baseConfigPath, packagesToAddLists, packagesToAdd)
	if err != nil {
		return err
	}

	err = removePackages(buildDir, allPackagesToRemove, imageChroot)
	if err != nil {
		return err
	}

	err = installPackages(buildDir, allPackagesToAdd, imageChroot, rpmsSources, useBaseImageRpmRepos)
	if err != nil {
		return err
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

func removePackages(buildDir string, allPackagesToRemove []string, imageChroot *safechroot.Chroot) error {
	var err error

	tnfRemoveArgs := []string{
		"-v", "remove", "--assumeyes", "--disablerepo", "*",
		// Placeholder for package name.
		"",
	}

	// Remove packages.
	// Do this one at a time, to avoid running out of memory.
	for _, packageName := range allPackagesToRemove {
		tnfRemoveArgs[len(tnfRemoveArgs)-1] = packageName

		err = imageChroot.Run(func() error {
			err := shell.ExecuteLiveWithCallback(tdnfRemoveStdoutFilter, logger.Log.Warn, false, "tdnf",
				tnfRemoveArgs...)
			return err
		})
		if err != nil {
			return fmt.Errorf("failed to install package (%s):\n%w", packageName, err)
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

func installPackages(buildDir string, allPackagesToAdd []string, imageChroot *safechroot.Chroot, rpmsSources []string,
	useBaseImageRpmRepos bool,
) error {
	var err error

	if len(allPackagesToAdd) <= 0 {
		return nil
	}

	if len(rpmsSources) <= 0 && !useBaseImageRpmRepos {
		return fmt.Errorf("have %d packages to install but no RPM sources were specified", len(allPackagesToAdd))
	}

	// Mount RPM sources.
	mounts, err := mountRpmSources(buildDir, imageChroot, rpmsSources, useBaseImageRpmRepos)
	if err != nil {
		return err
	}
	defer mounts.close()

	// Create tdnf command args.
	// Note: When using `--repofromdir`, tdnf will not use any default repos and will only use the last
	// `--repofromdir` specified.
	tnfInstallArgs := []string{
		"-v", "install", "--nogpgcheck", "--assumeyes",
		"--setopt", fmt.Sprintf("reposdir=%s", rpmsMountParentDirInChroot),
		// Placeholder for package name.
		"",
	}

	// Install packages.
	// Do this one at a time, to avoid running out of memory.
	for _, packageName := range allPackagesToAdd {
		tnfInstallArgs[len(tnfInstallArgs)-1] = packageName

		err = imageChroot.Run(func() error {
			err := shell.ExecuteLiveWithCallback(tdnfInstallStdoutFilter, logger.Log.Warn, false, "tdnf",
				tnfInstallArgs...)
			return err
		})
		if err != nil {
			return fmt.Errorf("failed to install package (%s):\n%w", packageName, err)
		}
	}

	// Unmount RPM sources.
	err = mounts.close()
	if err != nil {
		return err
	}

	return nil
}

// Process the stdout of a `tdnf install -v` call and send the list of installed packages to the debug log.
func tdnfInstallStdoutFilter(args ...interface{}) {
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
