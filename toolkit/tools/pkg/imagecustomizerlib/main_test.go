// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/buildpipeline"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/stretchr/testify/assert"
)

type baseImageType string

const (
	baseImageTypeCoreEfi    baseImageType = "core-efi"
	baseImageTypeCoreLegacy baseImageType = "core-legacy"
)

type baseImageVersion string

const (
	baseImageVersionAzl2 baseImageVersion = "2.0"
	baseImageVersionAzl3 baseImageVersion = "3.0"

	// Most features don't have version Azure Linux version specific behavior.
	// So, there is only minimal value in duplicating the tests across versions for such features.
	baseImageVersionDefault = baseImageVersionAzl2
)

var (
	baseImageCoreEfiAzl2    = flag.String("base-image-core-efi-azl2", "", "A core-efi 2.0 image to use as a base image.")
	baseImageCoreEfiAzl3    = flag.String("base-image-core-efi-azl3", "", "A core-efi 3.0 image to use as a base image.")
	baseImageCoreLegacyAzl2 = flag.String("base-image-core-legacy-azl2", "", "A core-legacy 2.0 image to use as a base image.")
	baseImageCoreLegacyAzl3 = flag.String("base-image-core-legacy-azl3", "", "A core-legacy 3.0 image to use as a base image.")
)

var (
	testDir    string
	tmpDir     string
	workingDir string

	supportedAzureLinuxVersions = []baseImageVersion{
		baseImageVersionAzl2,
		baseImageVersionAzl3,
	}
)

func TestMain(m *testing.M) {
	var err error

	logger.InitStderrLog()

	flag.Parse()

	workingDir, err = os.Getwd()
	if err != nil {
		logger.Log.Panicf("Failed to get working directory, error: %s", err)
	}

	testDir = filepath.Join(workingDir, "testdata")
	tmpDir = filepath.Join(workingDir, "_tmp")

	err = os.MkdirAll(tmpDir, os.ModePerm)
	if err != nil {
		logger.Log.Panicf("Failed to create tmp directory, error: %s", err)
	}

	retVal := m.Run()

	err = os.RemoveAll(tmpDir)
	if err != nil {
		logger.Log.Warnf("Failed to cleanup tmp dir (%s). Error: %s", tmpDir, err)
	}

	os.Exit(retVal)
}

// Skip the test if requirements for testing CustomizeImage() are not met.
func checkSkipForCustomizeImage(t *testing.T, baseImageType baseImageType, baseImageVersion baseImageVersion) string {
	if !buildpipeline.IsRegularBuild() {
		t.Skip("loopback block device not available")
	}

	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses a chroot")
	}

	param, paramName := getImageParamAndName(baseImageType, baseImageVersion)
	if param == nil || *param == "" {
		t.Skipf("--%s is required for this test", paramName)
	}

	return *param
}

func getImageParamAndName(baseImageType baseImageType, baseImageVersion baseImageVersion) (*string, string) {
	switch baseImageType {
	case baseImageTypeCoreEfi:
		switch baseImageVersion {
		case baseImageVersionAzl2:
			return baseImageCoreEfiAzl2, "base-image-core-efi-azl2"

		case baseImageVersionAzl3:
			return baseImageCoreEfiAzl3, "base-image-core-efi-azl3"
		}

	case baseImageTypeCoreLegacy:
		switch baseImageVersion {
		case baseImageVersionAzl2:
			return baseImageCoreLegacyAzl2, "base-image-core-legacy-azl2"

		case baseImageVersionAzl3:
			return baseImageCoreLegacyAzl3, "base-image-core-legacy-azl3"
		}
	}

	return nil, ""
}

func getDownloadedRpmsDir(t *testing.T, azureLinuxVersion string) string {
	downloadedRpmsDir := filepath.Join(testDir, "testrpms/downloadedrpms", azureLinuxVersion)
	dirExists, err := file.DirExists(downloadedRpmsDir)
	if !assert.NoErrorf(t, err, "cannot access downloaded RPMs dir (%s)", downloadedRpmsDir) {
		t.FailNow()
	}
	if !assert.True(t, dirExists) {
		t.Logf("test requires offline RPMs")
		t.Logf("please run toolkit/tools/pkg/imagecustomizerlib/testdata/testrpms/download-test-rpms.sh -t %s",
			azureLinuxVersion)
		t.FailNow()
	}

	return downloadedRpmsDir
}

func getDownloadedRpmsRepoFile(t *testing.T, azureLinuxVersion string) string {
	dir := getDownloadedRpmsDir(t, azureLinuxVersion)
	repoFile := filepath.Join(dir, "../", fmt.Sprintf("rpms-%s.repo", azureLinuxVersion))
	return repoFile
}
