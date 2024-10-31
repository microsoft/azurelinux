// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"math"
	"os"
	"path/filepath"
	"strconv"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
)

var PxeDracutMinVersion uint32 = 105
var PxeDracutMinPackageRelease uint32 = 1
var PxeDracutMinDistroVersion uint32 = 3

type DracutPackageInformation struct {
	Version        uint32 `yaml:"version"`
	PackageRelease uint32 `yaml:"packageRelease"`
	DistroRelease  string `yaml:"distroRelease"`
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

func getDracutVersion(rootfsSourceDir string) (dracutPackageInfo DracutPackageInformation, err error) {
	chroot := safechroot.NewChroot(rootfsSourceDir, true /*isExistingDir*/)
	if chroot == nil {
		return dracutPackageInfo, fmt.Errorf("failed to create a new chroot object for %s.", rootfsSourceDir)
	}
	defer chroot.Close(true /*leaveOnDisk*/)

	err = chroot.Initialize("", nil, nil, true /*includeDefaultMounts*/)
	if err != nil {
		return dracutPackageInfo, fmt.Errorf("failed to initialize chroot object for %s:\n%w", rootfsSourceDir, err)
	}

	packageName := "dracut"
	packageInfo, err := getPackageInformation(chroot, packageName)
	if err != nil {
		return dracutPackageInfo, fmt.Errorf("failed to get package version for (%s):\n%w", packageName, err)
	}
	versionUint64, err := strconv.ParseUint(packageInfo.version, 10 /*base*/, 64 /*size*/)
	if err != nil {
		return dracutPackageInfo, fmt.Errorf("failed to parse package version (%s) for (%s) into an unsigned integer:\n%w", packageInfo.version, packageName, err)
	}
	if versionUint64 > math.MaxUint32 {
		return dracutPackageInfo, fmt.Errorf("dracut package version (%d) exceeds maximum limit (32bit unsigned integer).", versionUint64)
	}

	dracutPackageInfo.Version = uint32(versionUint64)
	dracutPackageInfo.PackageRelease = packageInfo.packageRelease
	dracutPackageInfo.DistroRelease = packageInfo.distroRelease

	return dracutPackageInfo, nil
}

func verifyDracutPXESupport(packageInfo DracutPackageInformation) error {
	if packageInfo.Version < PxeDracutMinVersion {
		return fmt.Errorf("did not find required Dracut package version (%d-%d) - found (%d-%d)",
			PxeDracutMinVersion, PxeDracutMinPackageRelease, packageInfo.Version, packageInfo.PackageRelease)
	} else if packageInfo.Version > PxeDracutMinVersion {
		return nil
	}
	if packageInfo.PackageRelease < PxeDracutMinPackageRelease {
		return fmt.Errorf("did not find required Dracut package release (%d-%d) - found (%d-%d)",
			PxeDracutMinVersion, PxeDracutMinPackageRelease, packageInfo.Version, packageInfo.PackageRelease)
	}
	return nil
}
