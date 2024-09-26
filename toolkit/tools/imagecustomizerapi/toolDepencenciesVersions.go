package imagecustomizerapi

import (
	"os/exec"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

func getToolDependencenciesVersions() {
	// Map of version flags with corresponding packages
	versionFlags := map[string][]string{
		"--version": {
			"qemu-img", "rpm", "dd", "lsblk", "losetup", "sfdisk", "udevadm",
			"flock", "blkid", "sed", "createrepo", "genisoimage", "parted", "mkfs",
			"fsck", "fatlabel", "zstd", "veritysetup", "grub-install",
		},
		"-version": {
			"mksquashfs",
		},
		"version": {
			"openssl",
		},
		"-V": {
			"mkfs.ext4", "mkfs.xfs", "e2fsck", "xfs_repair", "xfs_admin",
		},
		"none": {
			"mkfs.vfat", "resize2fs", "tune2fs",
		},
	}

	// Get distro and version
	distro, version := getDistroAndVersion()
	logger.Log.Debugf("Distro: %s, Version: %s\n", distro, version)

	// Get versions of packages
	logger.Log.Debugf("Tool Dependencies:")
	for versionFlag, pkgList := range versionFlags {
		for _, pkg := range pkgList {
			version, err := getPackageVersion(pkg, versionFlag)
			if err != nil {
				logger.Log.Debugf("%s: not installed or error retrieving version\n", pkg)
			} else {
				logger.Log.Debugf("%s: %s", pkg, version)
			}
		}
	}
}

// Function to get the distribution and version of host machine
func getDistroAndVersion() (string, string) {
	output, err := exec.Command("lsb_release", "-si").Output()
	if err != nil {
		output = []byte("Unknown Distro")
	}
	distro := strings.TrimSpace(string(output))

	output, err = exec.Command("lsb_release", "-sr").Output()
	if err != nil {
		output = []byte("Unknown Version")
	}
	version := strings.TrimSpace(string(output))

	return distro, version
}

// Function to get the version of a package
func getPackageVersion(pkg string, versionFlagParameter string) (string, error) {
	var cmd *exec.Cmd
	// shell.ExecuteLive()
	if versionFlagParameter == "none" {
		// logger.Log.Debugf("in none case")
		cmd = exec.Command(pkg)
	} else {
		// logger.Log.Debugf("%s %s", pkg, versionFlagParameter)
		cmd = exec.Command(pkg, versionFlagParameter)
	}

	output, _ := cmd.Output()

	return parsePackageVersion(string(output)), nil
}

// Function to parse the version from the output
func parsePackageVersion(output string) string {
	lines := strings.Split(output, "\n")
	return lines[0]
}
