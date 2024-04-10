// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package installutils

import (
	"os"
	"path/filepath"
	"runtime"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/ptrutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"

	"github.com/stretchr/testify/assert"
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

func TestShouldReturnCorrectRequiredPackagesForArch(t *testing.T) {
	arm64RequiredPackages := []*pkgjson.PackageVer{}
	amd64RequiredPackages := []*pkgjson.PackageVer{{Name: "grub2-pc"}}

	requiredPackages := GetRequiredPackagesForInstall()

	switch arch := runtime.GOARCH; arch {
	case "arm64":
		assert.Equal(t, arm64RequiredPackages, requiredPackages)
	case "amd64":
		assert.Equal(t, amd64RequiredPackages, requiredPackages)
	default:
		assert.Fail(t, "unknown GOARCH detected: "+arch)
	}
}

func TestCopyAdditionalFiles(t *testing.T) {
	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses a chroot")
	}

	proposedDir := filepath.Join(tmpDir, "TestCopyAdditionalFiles")
	chroot := safechroot.NewChroot(proposedDir, false)

	err := chroot.Initialize("", []string{}, []*safechroot.MountPoint{}, true)
	assert.NoError(t, err)

	defer chroot.Close(false)

	copy_2_filemode := os.FileMode(0o777)

	err = copyAdditionalFilesHelper(chroot, map[string]configuration.FileConfigList{
		"testdata/a.txt": {
			{Path: "/a_copy_1.txt"},
			{Path: "/a_copy_2.txt", Permissions: ptrutils.PtrTo(configuration.FilePermissions(copy_2_filemode))},
		},
	})
	assert.NoError(t, err)

	copy_1_path := filepath.Join(chroot.RootDir(), "a_copy_1.txt")
	copy_2_path := filepath.Join(chroot.RootDir(), "a_copy_2.txt")

	// Make sure the files exist.
	orig_stat, err := os.Stat("testdata/a.txt")
	assert.NoError(t, err)

	copy_1_stat, err := os.Stat(copy_1_path)
	assert.NoError(t, err)

	copy_2_stat, err := os.Stat(copy_2_path)
	assert.NoError(t, err)

	// Make sure the filemode of the original file is different from the target filemode,
	// as otherwise it would defeat the purpose of the test.
	assert.NotEqual(t, copy_2_filemode, orig_stat.Mode()&os.ModePerm)

	// Make sure the file permissions are the expected values.
	assert.Equal(t, orig_stat.Mode()&os.ModePerm, copy_1_stat.Mode()&os.ModePerm)
	assert.Equal(t, copy_2_filemode, copy_2_stat.Mode()&os.ModePerm)

	// Make sure the files' contents are correct.
	orig_contents, err := os.ReadFile("testdata/a.txt")
	assert.NoError(t, err)

	copy_1_contents, err := os.ReadFile(copy_1_path)
	assert.NoError(t, err)

	copy_2_contents, err := os.ReadFile(copy_2_path)
	assert.NoError(t, err)

	assert.Equal(t, orig_contents, copy_1_contents)
	assert.Equal(t, orig_contents, copy_2_contents)
}

// Test AddImageIDFile function in installutils.go
func TestAddImageIDFile(t *testing.T) {
	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses a chroot")
	}

	proposedDir := filepath.Join(tmpDir, "TestAddImageIDFile")
	chroot := safechroot.NewChroot(proposedDir, false)

	err := chroot.Initialize("", []string{}, []*safechroot.MountPoint{}, true)
	assert.NoError(t, err)

	defer chroot.Close(false)

	buildNumber := "build-1234"
	imageIDFilePath := "/etc/image-id"

	etcPath := filepath.Join(chroot.RootDir(), "etc")
	os.Mkdir(etcPath, os.ModePerm)
	err = AddImageIDFile(chroot.RootDir(), buildNumber)
	assert.NoError(t, err)

	imageIDFileContents, err := os.ReadFile(filepath.Join(chroot.RootDir(), imageIDFilePath))
	assert.NoError(t, err)

	// assert that file has BUILD_NUMBER and the build number
	assert.Contains(t, string(imageIDFileContents), "BUILD_NUMBER="+buildNumber)
	// assert that file has IMAGE_BUILD_DATE and a timestamp in the format of YYYYMMDDHHMMSS
	assert.Regexp(t, "IMAGE_BUILD_DATE=[0-9]{14}", string(imageIDFileContents))
	// assert that file has IMAGE_UUID and a UUID
	assert.Regexp(t, "IMAGE_UUID=[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", string(imageIDFileContents))
}

func TestAddImageIDFileEmptyBuildNumber(t *testing.T) {
	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses a chroot")
	}

	proposedDir := filepath.Join(tmpDir, "TestAddImageIDFile")
	chroot := safechroot.NewChroot(proposedDir, false)

	err := chroot.Initialize("", []string{}, []*safechroot.MountPoint{}, true)
	assert.NoError(t, err)

	defer chroot.Close(false)

	buildNumber := ""
	expectedBuildNumber := "local"
	imageIDFilePath := "/etc/image-id"

	etcPath := filepath.Join(chroot.RootDir(), "etc")
	os.Mkdir(etcPath, os.ModePerm)
	err = AddImageIDFile(chroot.RootDir(), buildNumber)
	assert.NoError(t, err)

	imageIDFileContents, err := os.ReadFile(filepath.Join(chroot.RootDir(), imageIDFilePath))
	assert.NoError(t, err)
	assert.Contains(t, string(imageIDFileContents), expectedBuildNumber)
}

func TestAddImageIDFileGuardClause(t *testing.T) {
	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses a chroot")
	}

	proposedDir := filepath.Join(tmpDir, "TestAddImageIDFileGuardClause")
	chroot := safechroot.NewChroot(proposedDir, false)

	err := chroot.Initialize("", []string{}, []*safechroot.MountPoint{}, true)
	assert.NoError(t, err)

	defer chroot.Close(false)

	err = AddImageIDFile(chroot.RootDir(), "")
	assert.Error(t, err)
}
