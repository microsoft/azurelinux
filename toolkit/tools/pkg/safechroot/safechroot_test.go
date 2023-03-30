// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package safechroot

import (
	"fmt"
	"os"
	"path/filepath"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/buildpipeline"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/logger"

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
	testDir    string
	tmpDir     string
	workingDir string
)

func TestMain(m *testing.M) {
	var err error

	logger.InitStderrLog()

	workingDir, err = os.Getwd()
	if err != nil {
		logger.Log.Panicf("Failed to get working directory, error: %s", err)
	}

	testDir = filepath.Join(workingDir, "testdata")
	tmpDir = filepath.Join(workingDir, "_tmp")

	retVal := m.Run()

	err = os.RemoveAll(tmpDir)
	if err != nil {
		logger.Log.Warnf("Failed to cleanup tmp dir (%s). Error: %s", tmpDir, err)
	}

	os.Exit(retVal)
}

func TestInitializeShouldCreateRoot(t *testing.T) {
	extraMountPoints := []*MountPoint{}
	extraDirectories := []string{}

	dir := filepath.Join(tmpDir, "TestInitializeShouldCreateRoot")
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

	dir := filepath.Join(tmpDir, "TestCloseShouldRemoveRoot")
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

		dir := filepath.Join(tmpDir, "TestCloseShouldLeaveRootOnRequest")
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
		dir := filepath.Join(tmpDir, "TestRootDirShouldReturnRootDir")
		chroot := NewChroot(dir, isExistingDir)
		assert.Equal(t, dir, chroot.RootDir())
	}
}

func TestRunShouldReturnCorrectError(t *testing.T) {
	extraMountPoints := []*MountPoint{}
	extraDirectories := []string{}

	dir := filepath.Join(tmpDir, "TestRunShouldReturnCorrectError")
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

	dir := filepath.Join(tmpDir, "TestRunShouldChangeCWD")
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

	dir := filepath.Join(tmpDir, "TestShouldRestoreCWD")
	chroot := NewChroot(dir, isExistingDir)

	err := chroot.Initialize(emptyPath, extraDirectories, extraMountPoints)
	assert.NoError(t, err)
	defer chroot.Close(defaultLeaveOnDisk)

	expectedWorkingDirectory := workingDir
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

	dir := filepath.Join(tmpDir, "TestInitializeShouldExtractTar")
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
		extraMountPoints := []*MountPoint{
			NewMountPoint(srcMount, "custom-mount", "", BindMountPointFlags, emptyPath),
		}

		dir := filepath.Join(tmpDir, "TestInitializeShouldCreateCustomMountPoints")
		chroot := NewChroot(dir, isExistingDir)

		err := chroot.Initialize(emptyPath, extraDirectories, extraMountPoints)
		assert.NoError(t, err)
		defer chroot.Close(defaultLeaveOnDisk)

		fullPath := filepath.Join(dir, expectedFile)
		_, err = os.Stat(fullPath)
		assert.True(t, !os.IsNotExist(err))
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

		dir := filepath.Join(tmpDir, "TestInitializeShouldCleanupOnBadMountPoint")
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

	dir := filepath.Join(tmpDir, "TestInitializeShouldCreateExtraDirectories")
	chroot := NewChroot(dir, isExistingDir)

	err := chroot.Initialize(emptyPath, extraDirectories, extraMountPoints)
	assert.NoError(t, err)
	defer chroot.Close(defaultLeaveOnDisk)

	fullPath := filepath.Join(chroot.RootDir(), expectedExtraDirectory)
	_, err = os.Stat(fullPath)
	assert.True(t, !os.IsNotExist(err))
}
