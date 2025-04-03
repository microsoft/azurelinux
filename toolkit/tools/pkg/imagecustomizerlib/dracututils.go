// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"os"
	"path/filepath"
	"strconv"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
)

const (
	PxeDracutMinVersion        = 102
	PxeDracutMinPackageRelease = 7
	PxeDracutDistroName        = "azl"
	PxeDracutMinDistroVersion  = 3
)

type DracutPackageInformation struct {
	PackageVersion uint32 `yaml:"packageVersion"`
	PackageRelease uint32 `yaml:"packageRelease"`
	DistroName     string `yaml:"distroName"`
	DistroVersion  uint32 `yaml:"distroVersion"`
}

func addDracutConfig(dracutConfigFile string, lines []string) error {
	if _, err := os.Stat(dracutConfigFile); os.IsNotExist(err) {
		err := file.WriteLines(lines, dracutConfigFile)
		if err != nil {
			return fmt.Errorf("failed to write to dracut config file (%s): %w", dracutConfigFile, err)
		}
	} else {
		return fmt.Errorf("dracut config file (%s) already exists", dracutConfigFile)
	}
	return nil
}

func addDracutModuleAndDriver(dracutModuleName string, dracutDriverName string, imageChroot *safechroot.Chroot) error {
	dracutConfigFile := filepath.Join(imageChroot.RootDir(), "etc", "dracut.conf.d", dracutModuleName+".conf")
	lines := []string{
		"add_dracutmodules+=\" " + dracutModuleName + " \"",
		"add_drivers+=\" " + dracutDriverName + " \"",
	}
	return addDracutConfig(dracutConfigFile, lines)
}

func addDracutModule(dracutModuleName string, imageChroot *safechroot.Chroot) error {
	dracutConfigFile := filepath.Join(imageChroot.RootDir(), "etc", "dracut.conf.d", dracutModuleName+".conf")
	lines := []string{
		"add_dracutmodules+=\" " + dracutModuleName + " \"",
	}
	return addDracutConfig(dracutConfigFile, lines)
}

func addDracutDriver(dracutDriverName string, imageChroot *safechroot.Chroot) error {
	dracutConfigFile := filepath.Join(imageChroot.RootDir(), "etc", "dracut.conf.d", dracutDriverName+".conf")
	lines := []string{
		"add_drivers+=\" " + dracutDriverName + " \"",
	}
	return addDracutConfig(dracutConfigFile, lines)
}

func getDracutVersion(rootfsSourceDir string) (dracutPackageInfo *DracutPackageInformation, err error) {
	chroot := safechroot.NewChroot(rootfsSourceDir, true /*isExistingDir*/)
	if chroot == nil {
		return nil, fmt.Errorf("failed to create a new chroot object for %s.", rootfsSourceDir)
	}
	defer chroot.Close(true /*leaveOnDisk*/)

	err = chroot.Initialize("", nil, nil, true /*includeDefaultMounts*/)
	if err != nil {
		return nil, fmt.Errorf("failed to initialize chroot object for %s:\n%w", rootfsSourceDir, err)
	}

	packageName := "dracut"
	packageInfo, err := getPackageInformation(chroot, packageName)
	if err != nil {
		return nil, fmt.Errorf("failed to get package version for (%s):\n%w", packageName, err)
	}
	versionUint64, err := strconv.ParseUint(packageInfo.packageVersion, 10 /*base*/, 32 /*size*/)
	if err != nil {
		return nil, fmt.Errorf("failed to parse package version (%s) for (%s) into an unsigned integer:\n%w", packageInfo.packageVersion, packageName, err)
	}

	dracutPackageInfo = &DracutPackageInformation{
		PackageVersion: uint32(versionUint64),
		PackageRelease: packageInfo.packageRelease,
		DistroName:     packageInfo.distroName,
		DistroVersion:  packageInfo.distroVersion,
	}

	return dracutPackageInfo, nil
}

func verifyDracutPXESupport(packageInfo *DracutPackageInformation) error {
	if packageInfo == nil {
		return fmt.Errorf("no dracut package information provided")
	}

	if packageInfo.DistroName != PxeDracutDistroName {
		return fmt.Errorf("did not find required Azure Linux distro (%s) - found (%s)", PxeDracutDistroName, packageInfo.DistroName)
	}

	if packageInfo.DistroVersion < PxeDracutMinDistroVersion {
		return fmt.Errorf("did not find required Azure Linux distro version (%d) - found (%d)", PxeDracutMinDistroVersion, packageInfo.DistroVersion)
	}

	// Note that, theoretically, an new distro version could still have an older package version.
	// So, it is not sufficient to check that packageInfo.DistroVersion > PxeDracutMinDistroVersion.
	// We need to check the package version number.

	if packageInfo.PackageVersion < PxeDracutMinVersion {
		return fmt.Errorf("did not find required Dracut package version (%d-%d) - found (%d-%d)",
			PxeDracutMinVersion, PxeDracutMinPackageRelease, packageInfo.PackageVersion, packageInfo.PackageRelease)
	} else if packageInfo.PackageVersion > PxeDracutMinVersion {
		return nil
	}

	if packageInfo.PackageRelease < PxeDracutMinPackageRelease {
		return fmt.Errorf("did not find required Dracut package release (%d-%d) - found (%d-%d)",
			PxeDracutMinVersion, PxeDracutMinPackageRelease, packageInfo.PackageVersion, packageInfo.PackageRelease)
	}
	return nil
}
