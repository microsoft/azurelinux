// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/sirupsen/logrus"
)

const (
	azureLinuxPackagePrefix = "azl"
	tdnfInstallPrefix       = "Installing/Updating: "
	tdnfRemovePrefix        = "Removing: "
)

var (
	tdnfTransactionError = regexp.MustCompile(`^Found \d+ problems$`)
)

type packageInformation struct {
	packageVersion string
	packageRelease uint32
	distroName     string
	distroVersion  uint32
}

func addRemoveAndUpdatePackages(buildDir string, baseConfigPath string, config *imagecustomizerapi.OS,
	imageChroot *safechroot.Chroot, rpmsSources []string, useBaseImageRpmRepos bool,
) error {
	var err error

	// Note: The 'validatePackageLists' function read the PackageLists files and merged them into the inline package lists.
	needRpmsSources := len(config.Packages.Install) > 0 || len(config.Packages.Update) > 0 ||
		config.Packages.UpdateExistingPackages

	var mounts *rpmSourcesMounts
	if needRpmsSources {
		// Mount RPM sources.
		mounts, err = mountRpmSources(buildDir, imageChroot, rpmsSources, useBaseImageRpmRepos)
		if err != nil {
			return err
		}
		defer mounts.close()

		// Refresh metadata.
		err = refreshTdnfMetadata(imageChroot)
		if err != nil {
			return err
		}
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

	if needRpmsSources {
		err = cleanTdnfCache(imageChroot)
		if err != nil {
			return err
		}
	}

	return nil
}

func refreshTdnfMetadata(imageChroot *safechroot.Chroot) error {
	tdnfArgs := []string{
		"-v", "check-update", "--refresh", "--nogpgcheck", "--assumeyes",
		"--setopt", fmt.Sprintf("reposdir=%s", rpmsMountParentDirInChroot),
	}

	err := imageChroot.UnsafeRun(func() error {
		return shell.NewExecBuilder("tdnf", tdnfArgs...).
			LogLevel(logrus.DebugLevel, logrus.DebugLevel).
			ErrorStderrLines(1).
			Execute()
	})
	if err != nil {
		return fmt.Errorf("failed to refresh tdnf repo metadata:\n%w", err)
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

	tdnfRemoveArgs := []string{
		"-v", "remove", "--assumeyes", "--disablerepo", "*",
		// Placeholder for package name.
		"",
	}

	// Remove packages.
	// Do this one at a time, to avoid running out of memory.
	for _, packageName := range allPackagesToRemove {
		tdnfRemoveArgs[len(tdnfRemoveArgs)-1] = packageName

		err := callTdnf(tdnfRemoveArgs, tdnfRemovePrefix, imageChroot)
		if err != nil {
			return fmt.Errorf("failed to remove package (%s):\n%w", packageName, err)
		}
	}

	return nil
}

func updateAllPackages(imageChroot *safechroot.Chroot) error {
	logger.Log.Infof("Updating base image packages")

	tdnfUpdateArgs := []string{
		"-v", "update", "--nogpgcheck", "--assumeyes", "--cacheonly",
		"--setopt", fmt.Sprintf("reposdir=%s", rpmsMountParentDirInChroot),
	}

	err := callTdnf(tdnfUpdateArgs, tdnfInstallPrefix, imageChroot)
	if err != nil {
		return fmt.Errorf("failed to update packages:\n%w", err)
	}

	return nil
}

func installOrUpdatePackages(action string, allPackagesToAdd []string, imageChroot *safechroot.Chroot) error {
	// Create tdnf command args.
	// Note: When using `--repofromdir`, tdnf will not use any default repos and will only use the last
	// `--repofromdir` specified.
	tdnfInstallArgs := []string{
		"-v", action, "--nogpgcheck", "--assumeyes", "--cacheonly",
		"--setopt", fmt.Sprintf("reposdir=%s", rpmsMountParentDirInChroot),
		// Placeholder for package name.
		"",
	}

	// Install packages.
	// Do this one at a time, to avoid running out of memory.
	for _, packageName := range allPackagesToAdd {
		tdnfInstallArgs[len(tdnfInstallArgs)-1] = packageName

		err := callTdnf(tdnfInstallArgs, tdnfInstallPrefix, imageChroot)
		if err != nil {
			return fmt.Errorf("failed to %s package (%s):\n%w", action, packageName, err)
		}
	}

	return nil
}

func callTdnf(tdnfArgs []string, tdnfMessagePrefix string, imageChroot *safechroot.Chroot) error {
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
		return shell.NewExecBuilder("tdnf", tdnfArgs...).
			StdoutCallback(stdoutCallback).
			LogLevel(shell.LogDisabledLevel, logrus.DebugLevel).
			ErrorStderrLines(1).
			Execute()
	})
}

func isPackageInstalled(imageChroot *safechroot.Chroot, packageName string) bool {
	err := imageChroot.UnsafeRun(func() error {
		return shell.ExecuteLive(true /*squashErrors*/, "rpm", "-qi", packageName)
	})
	if err != nil {
		return false
	}
	return true
}

func getPackageInformation(imageChroot *safechroot.Chroot, packageName string) (info packageInformation, err error) {
	var packageVersion string
	err = imageChroot.UnsafeRun(func() error {
		packageVersion, _, err = shell.Execute("rpm", "-q", "--queryformat", "%{VERSION}", packageName)
		return err
	})
	if err != nil {
		return info, err
	}

	releaseInfo := ""
	err = imageChroot.UnsafeRun(func() error {
		releaseInfo, _, err = shell.Execute("rpm", "-q", "--queryformat", "%{RELEASE}", packageName)
		return err
	})
	if err != nil {
		return info, err
	}

	parts := strings.Split(releaseInfo, ".")
	if len(parts) != 2 {
		return info, fmt.Errorf("unexpected package release information format. Missing '.' in (%s)", releaseInfo)
	}

	// Extract package release
	packageReleaseUint64, err := strconv.ParseUint(parts[0], 10 /*base*/, 32 /*size*/)
	if err != nil {
		return info, fmt.Errorf("failed to parse package version (%s) for (%s) into an unsigned integer:\n%w", parts[0], packageName, err)
	}
	packageRelease := uint32(packageReleaseUint64)

	// Extrack package distro and version
	distroName := ""
	distroVersion := uint32(0)
	if strings.HasPrefix(parts[1], azureLinuxPackagePrefix) {
		distroName = azureLinuxPackagePrefix
		distroVersionString := parts[1][len(azureLinuxPackagePrefix):]
		distroVersionUint64, err := strconv.ParseUint(distroVersionString, 10 /*base*/, 32 /*size*/)
		if err != nil {
			return info, fmt.Errorf("failed to parse distro version (%s) for (%s) into an unsigned integer:\n%w", distroVersionString, packageName, err)
		}
		distroVersion = uint32(distroVersionUint64)
	}

	// Set return values
	info.packageVersion = packageVersion
	info.packageRelease = packageRelease
	info.distroName = distroName
	info.distroVersion = distroVersion

	return info, nil
}

func cleanTdnfCache(imageChroot *safechroot.Chroot) error {
	logger.Log.Infof("Cleaning up RPM cache")
	// Run all cleanup tasks inside the chroot environment
	return imageChroot.UnsafeRun(func() error {
		tdnfArgs := []string{
			"-v", "clean", "all",
		}
		err := shell.NewExecBuilder("tdnf", tdnfArgs...).
			LogLevel(logrus.TraceLevel, logrus.DebugLevel).
			ErrorStderrLines(1).
			Execute()
		if err != nil {
			return fmt.Errorf("Failed to clean tdnf cache: %w", err)
		}
		return nil
	})
}
