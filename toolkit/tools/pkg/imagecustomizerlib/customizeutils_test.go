// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"bufio"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
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
