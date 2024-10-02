// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"path/filepath"
	"strings"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/stretchr/testify/assert"
)

func TestCustomizeImageOverlays(t *testing.T) {
	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi, baseImageVersionDefault)

	testTempDir := filepath.Join(tmpDir, "TestCustomizeImageOverlays")
	buildDir := filepath.Join(testTempDir, "build")
	outImageFilePath := filepath.Join(testTempDir, "image.raw")
	configFile := filepath.Join(testDir, "overlays-config.yaml")

	// Customize image.
	err := CustomizeImageWithConfigFile(buildDir, configFile, baseImage, nil, outImageFilePath, "raw", "",
		"" /*outputPXEArtifactsDir*/, true /*useBaseImageRpmRepos*/, false /*enableShrinkFilesystems*/)
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
		{
			PartitionNum:   4,
			Path:           "/var",
			FileSystemType: "ext4",
		},
	}

	// Connect to customized image.
	imageConnection, err := connectToImage(buildDir, outImageFilePath, false /*includeDefaultMounts*/, mountPoints)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	verifyOverlays(t, imageConnection.chroot.RootDir())
	verifyOverlaysEquivalencyRules(t, imageConnection.chroot.RootDir())
}

func verifyOverlays(t *testing.T, rootPath string) {
	// Verify fstab for Overlays.
	fstabPath := filepath.Join(rootPath, "etc/fstab")
	fstabContents, err := file.Read(fstabPath)
	if !assert.NoError(t, err) {
		return
	}

	// Check for specific overlay configurations in fstab
	assert.Contains(t, fstabContents,
		"overlay /etc overlay lowerdir=/sysroot/etc,"+
			"upperdir=/sysroot/var/overlays/etc/upper,workdir=/sysroot/var/overlays/etc/work,"+
			"x-systemd.requires=/sysroot/var,x-initrd.mount,x-systemd.wanted-by=initrd-fs.target 0 0")

	assert.Contains(t, fstabContents,
		"overlay /media overlay lowerdir=/media:/home,"+
			"upperdir=/overlays/media/upper,workdir=/overlays/media/work 0 0")
}

func verifyOverlaysEquivalencyRules(t *testing.T, rootPath string) {
	mntPoints := map[string]string{
		"/etc":   "/var/overlays/etc/upper",
		"/media": "/overlays/media/upper",
	}

	for mntPoint, upperDir := range mntPoints {
		mntPointFullPath := filepath.Join(rootPath, mntPoint)
		upperDirFullPath := filepath.Join(rootPath, upperDir)

		mntPointLabel, _, err := shell.Execute("ls", "-Zd", mntPointFullPath)
		if !assert.NoError(t, err, "Failed to get SELinux label for %s", mntPointFullPath) {
			return
		}
		upperDirLabel, _, err := shell.Execute("ls", "-Zd", upperDirFullPath)
		if !assert.NoError(t, err, "Failed to get SELinux label for %s", upperDirFullPath) {
			return
		}

		// Modify the labels to remove the first section (before the first colon) and path.
		mntPointLabel = strings.Fields(mntPointLabel[strings.Index(mntPointLabel, ":")+1:])[0]
		upperDirLabel = strings.Fields(upperDirLabel[strings.Index(upperDirLabel, ":")+1:])[0]
		assert.Equal(t, mntPointLabel, upperDirLabel,
			"SELinux label mismatch between %s and %s", mntPointFullPath, upperDirFullPath)
	}
}
