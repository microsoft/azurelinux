// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package safechroot

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/buildpipeline"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/moby/sys/mountinfo"
	"golang.org/x/sys/unix"

	"github.com/stretchr/testify/assert"
)

const (
	testTar            = "testchroot.tar.gz"
	emptyPath          = ""
	emptyFlags         = 0
	isExistingDir      = false
	defaultLeaveOnDisk = false
)

var (
	testDir string
)

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	logger.InitBestEffort("", "debug")

	var retVal int
	if os.Geteuid() != 0 {
		// We're not running as root; we need to skip all tests in this file.
		logger.Log.Warn("safechroot tests must be run as root; skipping...")
		retVal = 0
	} else {
		// We're running as root; let's proceed with test setup and testing.
		var err error
		testDir, err = filepath.Abs("testdata")
		if err != nil {
			logger.Log.Panicf("Failed to get path to test data, error: %s", err)
		}

		retVal = m.Run()
	}

	os.Exit(retVal)
}

func TestInitializeShouldCreateRoot(t *testing.T) {
	extraMountPoints := []*MountPoint{}
	extraDirectories := []string{}

	dir := filepath.Join(t.TempDir(), "TestInitializeShouldCreateRoot")
	chroot := NewChroot(dir, isExistingDir)

	err := chroot.Initialize(emptyPath, extraDirectories, extraMountPoints)
	assert.NoError(t, err)

	defer chroot.Close(defaultLeaveOnDisk)

	_, err = os.Stat(chroot.RootDir())
	assert.True(t, !os.IsNotExist(err))
}

func TestCloseShouldRemoveRoot(t *testing.T) {
	extraMountPoints := []*MountPoint{}
	extraDirectories := []string{}

	dir := filepath.Join(t.TempDir(), "TestCloseShouldRemoveRoot")
	chroot := NewChroot(dir, isExistingDir)

	err := chroot.Initialize(emptyPath, extraDirectories, extraMountPoints)
	assert.NoError(t, err)

	// save away chroot location and close
	chrootDir := chroot.RootDir()
	err = chroot.Close(defaultLeaveOnDisk)
	assert.NoError(t, err)

	// when Docker based pipeline:
	// - chroot name are static and pre-defined
	// - chroot folders are re-cycled
	_, err = os.Stat(chrootDir)
	if buildpipeline.IsRegularBuild() {
		assert.True(t, os.IsNotExist(err))
	} else {
		assert.True(t, !os.IsNotExist(err))
	}
}

func TestCloseShouldLeaveRootOnRequest(t *testing.T) {
	if buildpipeline.IsRegularBuild() {
		// this test only apply to "regular build" pipeline
		const leaveOnDisk = true

		extraMountPoints := []*MountPoint{}
		extraDirectories := []string{}

		dir := filepath.Join(t.TempDir(), "TestCloseShouldLeaveRootOnRequest")
		chroot := NewChroot(dir, isExistingDir)

		err := chroot.Initialize(emptyPath, extraDirectories, extraMountPoints)
		assert.NoError(t, err)

		err = chroot.Close(leaveOnDisk)
		assert.NoError(t, err)

		_, err = os.Stat(dir)
		assert.True(t, !os.IsNotExist(err))

		// Since the chroot dir will be left on disk but unmounted,
		// manually clean it up.
		err = os.RemoveAll(dir)
		assert.NoError(t, err)
	}
}

func TestRootDirShouldReturnRootDir(t *testing.T) {
	if buildpipeline.IsRegularBuild() {
		// this test only apply to "regular build" pipeline
		dir := filepath.Join(t.TempDir(), "TestRootDirShouldReturnRootDir")
		chroot := NewChroot(dir, isExistingDir)
		assert.Equal(t, dir, chroot.RootDir())
	}
}

func TestRunShouldReturnCorrectError(t *testing.T) {
	extraMountPoints := []*MountPoint{}
	extraDirectories := []string{}

	dir := filepath.Join(t.TempDir(), "TestRunShouldReturnCorrectError")
	chroot := NewChroot(dir, isExistingDir)

	err := chroot.Initialize(emptyPath, extraDirectories, extraMountPoints)
	assert.NoError(t, err)
	defer chroot.Close(defaultLeaveOnDisk)

	expectedErr := fmt.Errorf("expected returned error")
	actualErr := chroot.Run(func() error {
		return expectedErr
	})

	assert.Equal(t, expectedErr, actualErr)
}

func TestRunShouldChangeCWD(t *testing.T) {
	extraMountPoints := []*MountPoint{}
	extraDirectories := []string{}

	dir := filepath.Join(t.TempDir(), "TestRunShouldChangeCWD")
	chroot := NewChroot(dir, isExistingDir)

	err := chroot.Initialize(emptyPath, extraDirectories, extraMountPoints)
	assert.NoError(t, err)
	defer chroot.Close(defaultLeaveOnDisk)

	var (
		expectedWorkingDirectory = "/"
		actualWorkingDirectory   string
	)

	err = chroot.Run(func() (err error) {
		actualWorkingDirectory, err = os.Getwd()
		return
	})

	assert.NoError(t, err)
	assert.Equal(t, expectedWorkingDirectory, actualWorkingDirectory)
}

func TestShouldRestoreCWD(t *testing.T) {
	extraMountPoints := []*MountPoint{}
	extraDirectories := []string{}

	dir := filepath.Join(t.TempDir(), "TestShouldRestoreCWD")
	chroot := NewChroot(dir, isExistingDir)

	err := chroot.Initialize(emptyPath, extraDirectories, extraMountPoints)
	assert.NoError(t, err)
	defer chroot.Close(defaultLeaveOnDisk)

	expectedWorkingDirectory, err := os.Getwd()
	assert.NoError(t, err)

	err = chroot.Run(func() (err error) {
		return nil
	})
	assert.NoError(t, err)

	actualWorkingDirectory, err := os.Getwd()
	assert.NoError(t, err)
	assert.Equal(t, expectedWorkingDirectory, actualWorkingDirectory)
}

func TestInitializeShouldExtractTar(t *testing.T) {
	const expectedFile = "/test/testfile.txt"

	tarPath := filepath.Join(testDir, testTar)
	extraMountPoints := []*MountPoint{}
	extraDirectories := []string{}

	dir := filepath.Join(t.TempDir(), "TestInitializeShouldExtractTar")
	chroot := NewChroot(dir, isExistingDir)

	err := chroot.Initialize(tarPath, extraDirectories, extraMountPoints)
	assert.NoError(t, err)
	defer chroot.Close(defaultLeaveOnDisk)

	fullPath := filepath.Join(chroot.RootDir(), expectedFile)
	_, err = os.Stat(fullPath)
	assert.True(t, !os.IsNotExist(err))
}

func TestInitializeShouldCreateCustomMountPoints(t *testing.T) {
	if buildpipeline.IsRegularBuild() {
		// this test only apply to "regular build" pipeline
		const expectedFile = "/custom-mount/testfile.txt"

		extraDirectories := []string{}
		srcMount := filepath.Join(testDir, "testmount")
		logger.Log.Warnf("srcMount: %s", srcMount)
		extraMountPoints := []*MountPoint{
			NewMountPoint(srcMount, "custom-mount", "", BindMountPointFlags, emptyPath),
		}

		dir := filepath.Join(t.TempDir(), "TestInitializeShouldCreateCustomMountPoints")
		chroot := NewChroot(dir, isExistingDir)

		err := chroot.Initialize(emptyPath, extraDirectories, extraMountPoints)
		logger.Log.Infof("Done init")
		assert.NoError(t, err)
		defer chroot.Close(defaultLeaveOnDisk)

		fullPath := filepath.Join(dir, expectedFile)
		logger.Log.Infof("Checking... %s", fullPath)
		_, err = os.Stat(fullPath)
		assert.True(t, !os.IsNotExist(err))
		logger.Log.Infof("Done checking")
	}
}

func TestInitializeShouldCleanupOnBadMountPoint(t *testing.T) {
	if buildpipeline.IsRegularBuild() {
		// this test only apply to "regular build" pipeline
		const invalidMountPointSource = "@"

		extraDirectories := []string{}
		extraMountPoints := []*MountPoint{
			NewMountPoint(invalidMountPointSource, "custom-mount", "", emptyFlags, emptyPath),
		}

		dir := filepath.Join(t.TempDir(), "TestInitializeShouldCleanupOnBadMountPoint")
		chroot := NewChroot(dir, isExistingDir)

		err := chroot.Initialize(emptyPath, extraDirectories, extraMountPoints)
		assert.Error(t, err)

		_, err = os.Stat(dir)
		assert.True(t, os.IsNotExist(err))
	}
}

func TestInitializeShouldCreateExtraDirectories(t *testing.T) {
	const expectedExtraDirectory = "/testdir"

	extraDirectories := []string{expectedExtraDirectory}
	extraMountPoints := []*MountPoint{}

	dir := filepath.Join(t.TempDir(), "TestInitializeShouldCreateExtraDirectories")
	chroot := NewChroot(dir, isExistingDir)

	err := chroot.Initialize(emptyPath, extraDirectories, extraMountPoints)
	assert.NoError(t, err)
	defer chroot.Close(defaultLeaveOnDisk)

	fullPath := filepath.Join(chroot.RootDir(), expectedExtraDirectory)
	_, err = os.Stat(fullPath)
	assert.True(t, !os.IsNotExist(err))
}

func TestUnsafeUnmounts(t *testing.T) {
	// create a temporary directory to use as the mount directory
	rootDir := t.TempDir()

	// create some nested directories and mount them
	nestedDir1 := filepath.Join(rootDir, "nested1")
	assert.NoError(t, os.Mkdir(nestedDir1, 0755))
	assert.NoError(t, unix.Mount("tmpfs", nestedDir1, "tmpfs", 0, ""))

	isMounted, err := mountinfo.Mounted(nestedDir1)
	assert.NoError(t, err)
	if !assert.True(t, isMounted) {
		t.FailNow()
	}

	nestedDir2 := filepath.Join(nestedDir1, "nested2")
	assert.NoError(t, os.Mkdir(nestedDir2, 0755))
	assert.NoError(t, unix.Mount("tmpfs", nestedDir2, "tmpfs", 0, ""))

	isMounted, err = mountinfo.Mounted(nestedDir2)
	assert.NoError(t, err)
	if !assert.True(t, isMounted) {
		t.FailNow()
	}

	nestedDir3 := filepath.Join(nestedDir2, "nested3")
	assert.NoError(t, os.Mkdir(nestedDir3, 0755))
	assert.NoError(t, unix.Mount("tmpfs", nestedDir3, "tmpfs", 0, ""))

	isMounted, err = mountinfo.Mounted(nestedDir3)
	assert.NoError(t, err)
	if !assert.True(t, isMounted) {
		t.FailNow()
	}

	anyFailed := CleanupUnsafeMounts([]string{rootDir, nestedDir1, nestedDir2, nestedDir3})
	assert.False(t, anyFailed)

	// check that all directories are unmounted from the mounts in /proc/mounts
	// They will look similar to '/tmp/TestUnsafeUnmount3846658289/001/nested1/nested2/nested3', just search for the
	// rootDir to find them.
	mountsList, err := file.ReadLines("/proc/mounts")
	assert.NoError(t, err)

	foundBadUnmount := false
	for _, mount := range mountsList {
		if strings.Contains(mount, rootDir) {
			path := strings.Fields(mount)[1]
			t.Logf("**** Consider running 'sudo umount --lazy %s' to clean up ****", path)
			foundBadUnmount = true
		}
	}
	if foundBadUnmount {
		// Test is in a bad state, but since we are just using tmpfs mounts in a tempdir it isn't the end of the world.
		// We will fail out and print instructions to fix the issue but the mounts will get cleaned up on a reboot at worst.
		t.FailNow()
	}
}
