package configvalidator

import (
	"fmt"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/imagegen/configuration"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/imagegen/installutils"
)

// ValidateConfiguration will run sanity checks on a configuration structure
func ValidateConfiguration(config configuration.Config) (err error) {
	err = config.IsValid()
	if err != nil {
		return
	}
	err = validatePackages(config)
	return
}

func validatePackages(config configuration.Config) (err error) {
	const (
		selinuxPkgName     = "selinux-policy"
		validateError      = "failed to validate package lists in config"
		verityPkgName      = "verity-read-only-root"
		verityDebugPkgName = "verity-read-only-root-debug-tools"
		dracutFipsPkgName  = "dracut-fips"
		fipsKernelCmdLine  = "fips=1"
	)
	for _, systemConfig := range config.SystemConfigs {
		packageList, err := installutils.PackageNamesFromSingleSystemConfig(systemConfig)
		if err != nil {
			return fmt.Errorf("%s: %w", validateError, err)
		}
		foundSELinuxPackage := false
		foundVerityInitramfsPackage := false
		foundVerityInitramfsDebugPackage := false
		foundDracutFipsPackage := false
		kernelCmdLineString := systemConfig.KernelCommandLine.ExtraCommandLine
		for _, pkg := range packageList {
			if pkg == "kernel" {
				return fmt.Errorf("%s: kernel should not be included in a package list, add via config file's [KernelOptions] entry", validateError)
			}
			if pkg == verityPkgName {
				foundVerityInitramfsPackage = true
			}
			if pkg == verityDebugPkgName {
				foundVerityInitramfsDebugPackage = true
			}
			if pkg == dracutFipsPkgName {
				foundDracutFipsPackage = true
			}
			if pkg == selinuxPkgName {
				foundSELinuxPackage = true
			}
		}
		if systemConfig.ReadOnlyVerityRoot.Enable {
			if !foundVerityInitramfsPackage {
				return fmt.Errorf("%s: [ReadOnlyVerityRoot] selected, but '%s' package is not included in the package lists", validateError, verityPkgName)
			}
			if systemConfig.ReadOnlyVerityRoot.TmpfsOverlayDebugEnabled && !foundVerityInitramfsDebugPackage {
				return fmt.Errorf("%s: [ReadOnlyVerityRoot] and [TmpfsOverlayDebugEnabled] selected, but '%s' package is not included in the package lists", validateError, verityDebugPkgName)
			}
		}
		if strings.Contains(kernelCmdLineString, fipsKernelCmdLine) {
			if !foundDracutFipsPackage {
				return fmt.Errorf("%s: 'fips=1' provided on kernel cmdline, but '%s' package is not included in the package lists", validateError, dracutFipsPkgName)
			}
		}
		if systemConfig.KernelCommandLine.SELinux != configuration.SELinuxOff {
			if !foundSELinuxPackage {
				return fmt.Errorf("%s: [SELinux] selected, but '%s' package is not included in the package lists", validateError, selinuxPkgName)
			}
		}
	}
	return
}
