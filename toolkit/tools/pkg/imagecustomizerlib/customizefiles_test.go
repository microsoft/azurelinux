// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/ptrutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/stretchr/testify/assert"
)

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

func TestCustomizeImageAdditionalFilesInfiniteFile(t *testing.T) {
	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	testTmpDir := filepath.Join(tmpDir, "TestCustomizeImageAdditionalFilesInfiniteFile")
	buildDir := filepath.Join(testTmpDir, "build")
	configFile := filepath.Join(testDir, "infinite-file-config.yaml")
	outImageFilePath := filepath.Join(testTmpDir, "image.raw")

	// Customize image.
	err := CustomizeImageWithConfigFile(buildDir, configFile, baseImage, nil, outImageFilePath, "raw", "",
		false /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	assert.ErrorContains(t, err, "failed to copy (/dev/zero)")
	assert.ErrorContains(t, err, "No space left on device")
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

func TestCustomizeImageAdditionalDirsInfiniteFile(t *testing.T) {
	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	testTmpDir := filepath.Join(tmpDir, "TestCustomizeImageAdditionalDirsInfiniteFile")
	buildDir := filepath.Join(testTmpDir, "build")
	outImageFilePath := filepath.Join(testTmpDir, "image.raw")

	// Make a directory that contains an infinite file.
	// Specifically, a file that symlinks to /dev/zero, which is a virtual file that contains
	// infinite bytes of 0. This should cause the copy operation to run out of free space on
	// the disk.
	srcDirPath := filepath.Join(testTmpDir, "a")
	infiniteFilePath := filepath.Join(srcDirPath, "zero")

	err := os.MkdirAll(srcDirPath, os.ModePerm)
	if !assert.NoError(t, err) {
		return
	}

	err = os.Symlink("/dev/zero", infiniteFilePath)
	if !assert.NoError(t, err) {
		return
	}

	config := imagecustomizerapi.Config{
		OS: &imagecustomizerapi.OS{
			AdditionalDirs: []imagecustomizerapi.DirConfig{
				{
					SourcePath:      srcDirPath,
					DestinationPath: "/a",
				},
			},
		},
	}

	// Customize image.
	err = CustomizeImage(buildDir, testTmpDir, &config, baseImage, nil, outImageFilePath, "raw", "",
		false /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
	assert.ErrorContains(t, err, "failed to copy directory")
	assert.ErrorContains(t, err, "failed to copy file")
	assert.ErrorContains(t, err, "No space left on device")
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
