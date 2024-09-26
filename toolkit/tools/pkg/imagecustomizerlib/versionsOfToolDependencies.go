package imagecustomizerlib

import (
	"os/exec"
	"regexp"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

func getVersionsOfToolDeps() {
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
	var pkgVersion string

	// If the package does not have a parameter, we call the package alone and extract the version from the output
	if versionFlagParameter == "none" {
		cmd = exec.Command(pkg)
	} else {
		cmd = exec.Command(pkg, versionFlagParameter)
	}

	output, _ := cmd.CombinedOutput()
	outputLines := strings.Split(string(output), "\n")

	if versionFlagParameter == "none" {
		// Regular expression to match various version formats including num.num.num, num.num, and alphanumeric versions
		re := regexp.MustCompile(`\b\d+(\.\d+){1,3}(-\w+)?\b`)
		for _, line := range outputLines {
			if re.MatchString(line) {
				pkgVersion = line
			}
		}
	} else {
		// Packages with a version parameter will have the version outputted as the first line
		pkgVersion = strings.Split(string(output), "\n")[0]
	}

	return pkgVersion, nil
}
