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

	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/stretchr/testify/assert"
)

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

	releaseFilePath := filepath.Join(chroot.RootDir(), "etc/image-customizer-release")

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
