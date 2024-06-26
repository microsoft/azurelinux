// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"testing"
	"time"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/ptrutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/stretchr/testify/assert"
)

func TestUpdateHostname(t *testing.T) {
	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses a chroot")
	}

	// Setup environment.
	proposedDir := filepath.Join(tmpDir, "TestUpdateHostname")
	chroot := safechroot.NewChroot(proposedDir, false)
	err := chroot.Initialize("", []string{}, []*safechroot.MountPoint{}, false)
	assert.NoError(t, err)
	defer chroot.Close(false)

	err = os.MkdirAll(filepath.Join(chroot.RootDir(), "etc"), os.ModePerm)
	assert.NoError(t, err)

	// Set hostname.
	expectedHostname := "testhostname"
	err = UpdateHostname(expectedHostname, chroot)
	assert.NoError(t, err)

	// Ensure hostname was correctly set.
	actualHostname, err := os.ReadFile(filepath.Join(chroot.RootDir(), "etc/hostname"))
	assert.NoError(t, err)
	assert.Equal(t, expectedHostname, string(actualHostname))
}

func TestCustomizeImageHostname(t *testing.T) {
	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	testTmpDir := filepath.Join(tmpDir, "TestCustomizeImageHostname")
	buildDir := filepath.Join(testTmpDir, "build")
	configFile := filepath.Join(testDir, "hostname-config.yaml")
	outImageFilePath := filepath.Join(buildDir, "image.qcow2")

	// Customize image.
	err := CustomizeImageWithConfigFile(buildDir, configFile, baseImage, nil, outImageFilePath, "raw", "",
		false /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	// Connect to customized image.
	imageConnection, err := connectToCoreEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Ensure hostname was correctly set.
	actualHostname, err := os.ReadFile(filepath.Join(imageConnection.Chroot().RootDir(), "etc/hostname"))
	assert.NoError(t, err)
	assert.Equal(t, "testname", string(actualHostname))
}

func TestCopyAdditionalFiles(t *testing.T) {
	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses a chroot")
	}

	proposedDir := filepath.Join(tmpDir, "TestCopyAdditionalFiles")
	chroot := safechroot.NewChroot(proposedDir, false)
	baseConfigPath := testDir

	err := chroot.Initialize("", []string{}, []*safechroot.MountPoint{}, false)
	assert.NoError(t, err)
	defer chroot.Close(false)

	copy_2_filemode := os.FileMode(0o777)

	// Copy a file.
	err = copyAdditionalFiles(baseConfigPath, map[string]imagecustomizerapi.FileConfigList{
		"files/a.txt": {
			{Path: "/copy_1.txt"},
			{Path: "/copy_2.txt", Permissions: ptrutils.PtrTo(imagecustomizerapi.FilePermissions(copy_2_filemode))},
		},
	}, chroot)
	assert.NoError(t, err)

	a_orig_path := filepath.Join(baseConfigPath, "files/a.txt")
	copy_1_path := filepath.Join(chroot.RootDir(), "copy_1.txt")
	copy_2_path := filepath.Join(chroot.RootDir(), "copy_2.txt")

	// Make sure the file permissions are the expected values.
	verifyFilePermissionsSame(t, a_orig_path, copy_1_path)
	verifyFilePermissions(t, copy_2_filemode, copy_2_path)

	// Make sure the files' contents are correct.
	verifyFileContentsSame(t, a_orig_path, copy_1_path)
	verifyFileContentsSame(t, a_orig_path, copy_2_path)

	// Copy a different file to the same location.
	err = copyAdditionalFiles(baseConfigPath, map[string]imagecustomizerapi.FileConfigList{
		"files/b.txt": {
			{Path: "/copy_1.txt"},
		},
	}, chroot)
	assert.NoError(t, err)

	b_orig_path := filepath.Join(baseConfigPath, "files/b.txt")

	verifyFileContentsSame(t, b_orig_path, copy_1_path)
	verifyFilePermissionsSame(t, b_orig_path, copy_1_path)
}

func TestCustomizeImageAdditionalFiles(t *testing.T) {
	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	testTmpDir := filepath.Join(tmpDir, "TestCustomizeImageAdditionalFiles")
	buildDir := filepath.Join(testTmpDir, "build")
	configFile := filepath.Join(testDir, "addfiles-config.yaml")
	outImageFilePath := filepath.Join(testTmpDir, "image.raw")

	// Customize image.
	err := CustomizeImageWithConfigFile(buildDir, configFile, baseImage, nil, outImageFilePath, "raw", "",
		false /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	// Connect to customized image.
	imageConnection, err := connectToCoreEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Verify the files were copied correctly.
	a_path := filepath.Join(testDir, "files/a.txt")
	a_copy_path := filepath.Join(imageConnection.Chroot().RootDir(), "/a.txt")

	helloworld_path := filepath.Join(testDir, "files/helloworld.sh")
	helloworld_copy_path := filepath.Join(imageConnection.Chroot().RootDir(), "/usr/local/bin/helloworld.sh")

	verifyFileContentsSame(t, a_path, a_copy_path)
	verifyFileContentsSame(t, helloworld_path, helloworld_copy_path)

	verifyFilePermissions(t, os.FileMode(0o755), helloworld_copy_path)
}

func TestCopyAdditionalDirs(t *testing.T) {
	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses a chroot")
	}

	proposedDir := filepath.Join(tmpDir, "TestCopyAdditionalDirs")
	chroot := safechroot.NewChroot(proposedDir, false)
	baseConfigPath := testDir

	err := chroot.Initialize("", []string{}, []*safechroot.MountPoint{}, false)
	assert.NoError(t, err)
	defer chroot.Close(false)

	// Copy the directory.
	err = copyAdditionalDirs(baseConfigPath,
		imagecustomizerapi.DirConfigList{
			{
				SourcePath:           "dirs/a",
				DestinationPath:      "/",
				ChildFilePermissions: ptrutils.PtrTo(imagecustomizerapi.FilePermissions(0o755)),
				NewDirPermissions:    ptrutils.PtrTo(imagecustomizerapi.FilePermissions(0o750)),
			},
		},
		chroot)
	assert.NoError(t, err)

	animalsFileOrigPath := filepath.Join(baseConfigPath, "dirs/a/usr/local/bin/animals.sh")
	animalsFileNewPath := filepath.Join(chroot.RootDir(), "/usr/local/bin/animals.sh")

	// Verify file and directory contents and permissions.
	verifyFileContentsSame(t, animalsFileOrigPath, animalsFileNewPath)
	verifyFilePermissions(t, os.FileMode(0o755), animalsFileNewPath)

	verifyFilePermissions(t, os.FileMode(0o750), filepath.Join(chroot.RootDir(), "/usr/local/bin"))
	verifyFilePermissions(t, os.FileMode(0o750), filepath.Join(chroot.RootDir(), "/usr/local"))
	verifyFilePermissions(t, os.FileMode(0o750), filepath.Join(chroot.RootDir(), "/usr"))

	// Copy a different directory to the same location but change up the file and directory permissions.
	err = copyAdditionalDirs(baseConfigPath,
		imagecustomizerapi.DirConfigList{
			{
				SourcePath:           "dirs/b",
				DestinationPath:      "/usr/local",
				ChildFilePermissions: ptrutils.PtrTo(imagecustomizerapi.FilePermissions(0o750)),
				MergedDirPermissions: ptrutils.PtrTo(imagecustomizerapi.FilePermissions(0o755)),
			},
		},
		chroot)
	assert.NoError(t, err)

	animalsFileOrigPath = filepath.Join(baseConfigPath, "dirs/b/bin/animals.sh")

	// Verify file and directory contents and permissions.
	verifyFileContentsSame(t, animalsFileOrigPath, animalsFileNewPath)
	verifyFilePermissions(t, os.FileMode(0o750), animalsFileNewPath)

	verifyFilePermissions(t, os.FileMode(0o755), filepath.Join(chroot.RootDir(), "/usr/local/bin"))
	verifyFilePermissions(t, os.FileMode(0o755), filepath.Join(chroot.RootDir(), "/usr/local"))
	verifyFilePermissions(t, os.FileMode(0o750), filepath.Join(chroot.RootDir(), "/usr"))
}

func TestCustomizeImageAdditionalDirs(t *testing.T) {
	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	testTmpDir := filepath.Join(tmpDir, "TestCustomizeImageAdditionalDirs")
	buildDir := filepath.Join(testTmpDir, "build")
	configFile := filepath.Join(testDir, "adddirs-config.yaml")
	outImageFilePath := filepath.Join(testTmpDir, "image.raw")

	// Customize image.
	err := CustomizeImageWithConfigFile(buildDir, configFile, baseImage, nil, outImageFilePath, "raw", "",
		false /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	// Connect to customized image.
	imageConnection, err := connectToCoreEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	animalsFileOrigPath := filepath.Join(testDir, "dirs/a/usr/local/bin/animals.sh")
	animalsFileNewPath := filepath.Join(imageConnection.Chroot().RootDir(), "/usr/local/bin/animals.sh")

	// Verify file and directory contents and permissions.
	verifyFileContentsSame(t, animalsFileOrigPath, animalsFileNewPath)
}

func TestAddCustomizerRelease(t *testing.T) {
	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses a chroot")
	}

	proposedDir := filepath.Join(tmpDir, "TestAddCustomizerRelease")
	chroot := safechroot.NewChroot(proposedDir, false)
	err := chroot.Initialize("", []string{}, []*safechroot.MountPoint{}, false)
	assert.NoError(t, err)
	defer chroot.Close(false)

	err = os.MkdirAll(filepath.Join(chroot.RootDir(), "etc"), os.ModePerm)
	assert.NoError(t, err)

	expectedVersion := "0.1.0"
	expectedDate := time.Now().Format("2006-01-02T15:04:05Z")
	err = addCustomizerRelease(chroot, expectedVersion, expectedDate)
	assert.NoError(t, err)

	releaseFilePath := filepath.Join(chroot.RootDir(), "etc/mariner-customizer-release")

	file, err := os.Open(releaseFilePath)
	if err != nil {
		t.Fatalf("Failed to open file: %v", err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	config := make(map[string]string)
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			continue
		}
		parts := strings.Split(line, "=")
		key := parts[0]
		value := strings.Trim(parts[1], "\"")
		config[key] = value
	}

	assert.Equal(t, expectedVersion, config["TOOL_VERSION"])
	assert.Equal(t, expectedDate, config["BUILD_DATE"])
}

func TestCustomizeImageSELinux(t *testing.T) {
	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	testTmpDir := filepath.Join(tmpDir, "TestCustomizeImageSELinux")
	buildDir := filepath.Join(testTmpDir, "build")
	outImageFilePath := filepath.Join(testTmpDir, "image.raw")

	// Customize image: SELinux enforcing.
	// This tests enabling SELinux on a non-SELinux image.
	configFile := filepath.Join(testDir, "selinux-force-enforcing.yaml")
	err := CustomizeImageWithConfigFile(buildDir, configFile, baseImage, nil, outImageFilePath, "raw", "",
		true /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	// Connect to customized image.
	imageConnection, err := connectToCoreEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Verify bootloader config.
	verifyKernelCommandLine(t, imageConnection, []string{"security=selinux", "selinux=1", "enforcing=1"}, []string{})
	verifySELinuxConfigFile(t, imageConnection, "enforcing")

	// Verify packages are installed.
	ensureFilesExist(t, imageConnection, "/etc/selinux/targeted", "/var/lib/selinux/targeted/active/modules",
		"/usr/bin/seinfo", "/usr/sbin/semanage")

	err = imageConnection.CleanClose()
	if !assert.NoError(t, err) {
		return
	}

	// Customize image: SELinux disabled.
	// This tests disabling (but not removing) SELinux on an SELinux enabled image.
	configFile = filepath.Join(testDir, "selinux-disabled.yaml")
	err = CustomizeImageWithConfigFile(buildDir, configFile, outImageFilePath, nil, outImageFilePath, "raw", "",
		true /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	// Connect to customized image.
	imageConnection, err = connectToCoreEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Verify bootloader config.
	verifyKernelCommandLine(t, imageConnection, []string{}, []string{"security=selinux", "selinux=1", "enforcing=1"})
	verifySELinuxConfigFile(t, imageConnection, "disabled")

	// Verify packages are still installed.
	ensureFilesExist(t, imageConnection, "/etc/selinux/targeted", "/var/lib/selinux/targeted/active/modules",
		"/usr/bin/seinfo", "/usr/sbin/semanage")

	err = imageConnection.CleanClose()
	if !assert.NoError(t, err) {
		return
	}

	// Customize image: SELinux permissive.
	// This tests enabling SELinux on an image with SELinux installed but disabled.
	configFile = filepath.Join(testDir, "selinux-permissive.yaml")
	err = CustomizeImageWithConfigFile(buildDir, configFile, outImageFilePath, nil, outImageFilePath, "raw", "",
		true /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	// Connect to customized image.
	imageConnection, err = connectToCoreEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Verify bootloader config.
	verifyKernelCommandLine(t, imageConnection, []string{"security=selinux", "selinux=1"}, []string{"enforcing=1"})
	verifySELinuxConfigFile(t, imageConnection, "permissive")
}

func TestCustomizeImageSELinuxAndPartitions(t *testing.T) {
	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	testTmpDir := filepath.Join(tmpDir, "TestCustomizeImageSELinuxAndPartitions")
	buildDir := filepath.Join(testTmpDir, "build")
	outImageFilePath := filepath.Join(testTmpDir, "image.raw")

	// Customize image: SELinux enforcing.
	// This tests enabling SELinux on a non-SELinux image.
	configFile := filepath.Join(testDir, "partitions-selinux-enforcing.yaml")
	err := CustomizeImageWithConfigFile(buildDir, configFile, baseImage, nil, outImageFilePath, "raw", "",
		true /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	if !assert.NoError(t, err) {
		return
	}

	// Connect to customized image.
	mountPoints := []mountPoint{
		{
			PartitionNum:   3,
			Path:           "/",
			FileSystemType: "ext4",
		},
		{
			PartitionNum:   2,
			Path:           "/boot",
			FileSystemType: "ext4",
		},
		{
			PartitionNum:   1,
			Path:           "/boot/efi",
			FileSystemType: "vfat",
		},
	}

	imageConnection, err := connectToImage(buildDir, outImageFilePath, mountPoints)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Verify bootloader config.
	verifyKernelCommandLine(t, imageConnection, []string{"security=selinux", "selinux=1"}, []string{"enforcing=1"})
	verifySELinuxConfigFile(t, imageConnection, "enforcing")

	// Verify packages are installed.
	ensureFilesExist(t, imageConnection, "/etc/selinux/targeted", "/var/lib/selinux/targeted/active/modules",
		"/usr/bin/seinfo", "/usr/sbin/semanage")
}

func TestCustomizeImageSELinuxNoPolicy(t *testing.T) {
	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	testTmpDir := filepath.Join(tmpDir, "TestCustomizeImageSELinuxNoPolicy")
	buildDir := filepath.Join(testTmpDir, "build")
	configFile := filepath.Join(testDir, "selinux-enforcing-nopackages.yaml")
	outImageFilePath := filepath.Join(buildDir, "image.qcow2")

	// Customize image.
	err := CustomizeImageWithConfigFile(buildDir, configFile, baseImage, nil, outImageFilePath, "raw", "",
		false /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	assert.ErrorContains(t, err, "SELinux is enabled but the (/etc/selinux/config) file is missing")
	assert.ErrorContains(t, err, "please ensure an SELinux policy is installed")
	assert.ErrorContains(t, err, "the 'selinux-policy' package provides the default policy")
}

func verifyFileContentsSame(t *testing.T, origPath string, newPath string) {
	orignContents, err := os.ReadFile(origPath)
	if !assert.NoErrorf(t, err, "read original file (%s)", origPath) {
		return
	}

	newContents, err := os.ReadFile(newPath)
	if !assert.NoErrorf(t, err, "read new file (%s)", newPath) {
		return
	}

	assert.Equalf(t, orignContents, newContents, "file contents differ (%s) from (%s)", newPath, origPath)
}

func verifyFilePermissions(t *testing.T, expectedPermissions os.FileMode, path string) {
	stat, err := os.Stat(path)
	if assert.NoError(t, err) {
		assert.Equal(t, expectedPermissions&os.ModePerm, stat.Mode()&os.ModePerm)
	}
}

func verifyFilePermissionsSame(t *testing.T, origPath string, newPath string) {
	origStat, err := os.Stat(origPath)
	if assert.NoErrorf(t, err, "stat original file (%s)", origPath) {
		return
	}

	newStat, err := os.Stat(newPath)
	if assert.NoErrorf(t, err, "stat new file (%s)", newPath) {
		return
	}

	assert.Equal(t, origStat.Mode()&os.ModePerm, newStat.Mode()&os.ModePerm)
}

func ensureFilesExist(t *testing.T, imageConnection *ImageConnection, filePaths ...string) {
	for _, filePath := range filePaths {
		// Note: Symbolic links might be broken as we are not checking under the chroot.
		// Hence, the use of lstat instead of stat.
		_, err := os.Lstat(filepath.Join(imageConnection.chroot.RootDir(), filePath))
		assert.NoErrorf(t, err, "check file exists (%s)", filePath)
	}
}

func ensureFilesNotExist(t *testing.T, imageConnection *ImageConnection, filePaths ...string) {
	for _, filePath := range filePaths {
		// Note: Symbolic links might be broken as we are not checking under the chroot.
		// Hence, the use of lstat instead of stat.
		_, err := os.Lstat(filepath.Join(imageConnection.chroot.RootDir(), filePath))
		assert.ErrorIsf(t, err, os.ErrNotExist, "ensure file does not exist (%s)", filePath)
	}
}

func verifyKernelCommandLine(t *testing.T, imageConnection *ImageConnection, existsArgs []string,
	notExistsArgs []string,
) {
	grubCfgFilePath := filepath.Join(imageConnection.Chroot().RootDir(), "/boot/grub2/grub.cfg")
	grubCfgContents, err := file.Read(grubCfgFilePath)
	assert.NoError(t, err, "read grub.cfg file")

	for _, existsArg := range existsArgs {
		assert.Regexpf(t, fmt.Sprintf("linux.* %s ", regexp.QuoteMeta(existsArg)), grubCfgContents,
			"ensure kernel command arg exists (%s)", existsArg)
	}

	for _, notExistsArg := range notExistsArgs {
		assert.NotRegexpf(t, fmt.Sprintf("linux.* %s ", regexp.QuoteMeta(notExistsArg)), grubCfgContents,
			"ensure kernel command arg not exists (%s)", notExistsArg)
	}
}

func verifySELinuxConfigFile(t *testing.T, imageConnection *ImageConnection, mode string) {
	selinuxConfigPath := filepath.Join(imageConnection.Chroot().RootDir(), "/etc/selinux/config")
	selinuxConfigContents, err := file.Read(selinuxConfigPath)
	assert.NoError(t, err, "read SELinux config file")
	assert.Regexp(t, fmt.Sprintf("(?m)^SELINUX=%s$", regexp.QuoteMeta(mode)), selinuxConfigContents)
}
