// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"flag"
	"os"
	"path/filepath"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/buildpipeline"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

type baseImageType string

const (
	baseImageTypeCoreEfi baseImageType = "core-efi"
)

var (
	baseImageCoreEfi = flag.String("base-image-core-efi", "", "A core-efi image to use as a base image.")
)

var (
	testDir    string
	tmpDir     string
	workingDir string
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
func checkSkipForCustomizeImage(t *testing.T, baseImageType baseImageType) string {
	if !buildpipeline.IsRegularBuild() {
		t.Skip("loopback block device not available")
	}

	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses a chroot")
	}

	switch baseImageType {
	case baseImageTypeCoreEfi:
		if baseImageCoreEfi == nil || *baseImageCoreEfi == "" {
			t.Skip("--base-image-core-efi is required for this test")
		}
		return *baseImageCoreEfi
	}

	return ""
}
