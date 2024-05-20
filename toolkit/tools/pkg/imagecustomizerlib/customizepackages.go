// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"regexp"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/sirupsen/logrus"
)

const (
	tdnfInstallPrefix = "Installing/Updating: "
	tdnfRemovePrefix  = "Removing: "
)

var (
	tdnfTransactionError = regexp.MustCompile(`^Found \d+ problems$`)
)

func addRemoveAndUpdatePackages(buildDir string, baseConfigPath string, config *imagecustomizerapi.OS,
	imageChroot *safechroot.Chroot, rpmsSources []string, useBaseImageRpmRepos bool,
) error {
	var err error

	// Note: The 'validatePackageLists' function read the PackageLists files and merged them into the inline package lists.
	needRpmsSources := len(config.Packages.Install) > 0 || len(config.Packages.Update) > 0 ||
		config.Packages.UpdateExistingPackages

	// Mount RPM sources.
	var mounts *rpmSourcesMounts
	if needRpmsSources {
		mounts, err = mountRpmSources(buildDir, imageChroot, rpmsSources, useBaseImageRpmRepos)
		if err != nil {
			return err
		}
		defer mounts.close()
	}

	err = removePackages(config.Packages.Remove, imageChroot)
	if err != nil {
		return err
	}

	if config.Packages.UpdateExistingPackages {
		err = updateAllPackages(imageChroot)
		if err != nil {
			return err
		}
	}

	logger.Log.Infof("Installing packages: %v", config.Packages.Install)
	err = installOrUpdatePackages("install", config.Packages.Install, imageChroot)
	if err != nil {
		return err
	}

	logger.Log.Infof("Updating packages: %v", config.Packages.Update)
	err = installOrUpdatePackages("update", config.Packages.Update, imageChroot)
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
		packageListFilePath := file.GetAbsPathWithBase(baseConfigPath, packageListRelativePath)

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

		err := callTdnf(tnfRemoveArgs, tdnfRemovePrefix, imageChroot)
		if err != nil {
			return fmt.Errorf("failed to remove package (%s):\n%w", packageName, err)
		}
	}

	return nil
}

func updateAllPackages(imageChroot *safechroot.Chroot) error {
	logger.Log.Infof("Updating base image packages")

	tnfUpdateArgs := []string{
		"-v", "update", "--nogpgcheck", "--assumeyes",
		"--setopt", fmt.Sprintf("reposdir=%s", rpmsMountParentDirInChroot),
	}

	err := callTdnf(tnfUpdateArgs, tdnfInstallPrefix, imageChroot)
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

		err := callTdnf(tnfInstallArgs, tdnfInstallPrefix, imageChroot)
		if err != nil {
			return fmt.Errorf("failed to %s package (%s):\n%w", action, packageName, err)
		}
	}

	return nil
}

func callTdnf(tnfArgs []string, tdnfMessagePrefix string, imageChroot *safechroot.Chroot) error {
	seenTransactionErrorMessage := false
	stdoutCallback := func(line string) {
		if !seenTransactionErrorMessage {
			// Check if this line marks the start of a transaction error message.
			seenTransactionErrorMessage = tdnfTransactionError.MatchString(line)
		}

		if seenTransactionErrorMessage {
			// Report all of the transaction error message (i.e. the remainder of stdout) to WARN.
			logger.Log.Warn(line)
		} else if strings.HasPrefix(line, tdnfMessagePrefix) {
			logger.Log.Debug(line)
		} else {
			logger.Log.Trace(line)
		}
	}

	return imageChroot.UnsafeRun(func() error {
		return shell.NewExecBuilder("tdnf", tnfArgs...).
			StdoutCallback(stdoutCallback).
			LogLevel(shell.LogDisabledLevel, logrus.DebugLevel).
			ErrorStderrLines(1).
			Execute()
	})
}
