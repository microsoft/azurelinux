// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safeloopback"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safemount"
	"github.com/stretchr/testify/assert"
	"golang.org/x/sys/unix"
)

// Tests:
// - vhdx to ISO, with OS changes.
// - ISO to ISO, with no OS changes.
// - Kernel command-line arg append.
// - .iso.additionalFiles
func TestCustomizeImageLiveCd1(t *testing.T) {
	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	testTempDir := filepath.Join(tmpDir, "TestCustomizeImageLiveCd1")
	buildDir := filepath.Join(testTempDir, "build")
	outImageFilePath := filepath.Join(testTempDir, "image.iso")
	configFile := filepath.Join(testDir, "iso-files-and-args-config.yaml")

	// Customize vhdx to ISO, with OS changes.
	err := CustomizeImageWithConfigFile(buildDir, configFile, baseImage, nil, outImageFilePath, "iso", "", true, false)
	assert.NoError(t, err)

	// Attach ISO.
	isoImageLoopDevice, err := safeloopback.NewLoopback(outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer isoImageLoopDevice.Close()

	isoMountDir := filepath.Join(testTempDir, "iso-mount")
	isoImageMount, err := safemount.NewMount(isoImageLoopDevice.DevicePath(), isoMountDir,
		"iso9660" /*fstype*/, unix.MS_RDONLY /*flags*/, "" /*data*/, true /*makeAndDelete*/)
	if !assert.NoError(t, err) {
		return
	}
	defer isoImageMount.Close()

	// Check for the copied a.txt file.
	aOrigPath := filepath.Join(testDir, "files/a.txt")
	aIsoPath := filepath.Join(isoMountDir, "a.txt")
	verifyFileContentsSame(t, aOrigPath, aIsoPath)

	// Ensure grub.cfg file has the extra kernel command-line args.
	grubCfgFilePath := filepath.Join(isoMountDir, "/boot/grub2/grub.cfg")
	grubCfgContents, err := file.Read(grubCfgFilePath)
	assert.NoError(t, err, "read grub.cfg file")
	assert.Regexp(t, "linux.* rd.info ", grubCfgContents)

	// Check the iso-kernel-args.txt file.
	isoKernelArgsPath := filepath.Join(isoMountDir, savedConfigIsoDir, savedKernelArgsFileName)
	isoKernelArgsContents, err := file.Read(isoKernelArgsPath)
	assert.NoErrorf(t, err, "read (%s) file", savedKernelArgsFileName)
	assert.Equal(t, "rd.info", isoKernelArgsContents)

	err = isoImageMount.CleanClose()
	if !assert.NoError(t, err) {
		return
	}

	err = isoImageLoopDevice.CleanClose()
	if !assert.NoError(t, err) {
		return
	}

	// Customize ISO to ISO, with no OS changes.
	b2FilePerms := imagecustomizerapi.FilePermissions(0o600)
	config := imagecustomizerapi.Config{
		Iso: &imagecustomizerapi.Iso{
			KernelCommandLine: imagecustomizerapi.KernelCommandLine{
				ExtraCommandLine: "rd.debug",
			},
			AdditionalFiles: imagecustomizerapi.AdditionalFilesMap{
				"files/b.txt": []imagecustomizerapi.FileConfig{
					{
						Path: "/b1.txt",
					},
					{
						Path:        "/b2.txt",
						Permissions: &b2FilePerms,
					},
				},
			},
		},
	}
	err = CustomizeImage(buildDir, testDir, &config, outImageFilePath, nil, outImageFilePath, "iso", "", false, false)
	assert.NoError(t, err)

	// Attach ISO.
	isoImageLoopDevice, err = safeloopback.NewLoopback(outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer isoImageLoopDevice.Close()

	isoImageMount, err = safemount.NewMount(isoImageLoopDevice.DevicePath(), isoMountDir,
		"iso9660" /*fstype*/, unix.MS_RDONLY /*flags*/, "" /*data*/, true /*makeAndDelete*/)
	if !assert.NoError(t, err) {
		return
	}
	defer isoImageMount.Close()

	// Check that the a.txt stayed around.
	verifyFileContentsSame(t, aOrigPath, aIsoPath)

	// Check for copied b.txt file.
	bOrigPath := filepath.Join(testDir, "files/b.txt")
	b1IsoPath := filepath.Join(isoMountDir, "b1.txt")
	b2IsoPath := filepath.Join(isoMountDir, "b2.txt")
	verifyFileContentsSame(t, bOrigPath, b1IsoPath)
	verifyFileContentsSame(t, bOrigPath, b2IsoPath)
	verifyFilePermissions(t, os.FileMode(b2FilePerms), b2IsoPath)

	// Ensure grub.cfg file has the extra kernel command-line args from both runs.
	grubCfgContents, err = file.Read(grubCfgFilePath)
	assert.NoError(t, err, "read grub.cfg file")
	assert.Regexp(t, "linux.* rd.info ", grubCfgContents)
	assert.Regexp(t, "linux.* rd.debug ", grubCfgContents)

	// Check the iso-kernel-args.txt file.
	isoKernelArgsContents, err = file.Read(isoKernelArgsPath)
	assert.NoErrorf(t, err, "read (%s) file", savedKernelArgsFileName)
	assert.Equal(t, "rd.info rd.debug", isoKernelArgsContents)
}

// Tests:
// - vhdx to ISO, with no OS changes.
// - ISO to ISO, with OS changes.
func TestCustomizeImageLiveCd2(t *testing.T) {
	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	testTempDir := filepath.Join(tmpDir, "TestCustomizeImageLiveCd2")
	buildDir := filepath.Join(testTempDir, "build")
	outImageFilePath := filepath.Join(testTempDir, "image.raw")
	outIsoFilePath := filepath.Join(testTempDir, "image.iso")

	// Customize vhdx with ISO prereqs.
	configFile := filepath.Join(testDir, "iso-os-prereqs-config.yaml")
	err := CustomizeImageWithConfigFile(buildDir, configFile, baseImage, nil, outImageFilePath, "raw", "", true, false)
	assert.NoError(t, err)

	// Customize image to ISO, with no OS changes.
	config := imagecustomizerapi.Config{
		Iso: &imagecustomizerapi.Iso{},
	}
	err = CustomizeImage(buildDir, testDir, &config, outImageFilePath, nil, outIsoFilePath, "iso", "", false, false)
	assert.NoError(t, err)

	// Customize ISO to ISO, with OS changes.
	configFile = filepath.Join(testDir, "addfiles-config.yaml")
	err = CustomizeImageWithConfigFile(buildDir, configFile, outIsoFilePath, nil, outIsoFilePath, "iso", "", true, false)
	assert.NoError(t, err)

	// Attach ISO.
	isoImageLoopDevice, err := safeloopback.NewLoopback(outIsoFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer isoImageLoopDevice.Close()

	isoMountDir := filepath.Join(testTempDir, "iso-mount")
	isoImageMount, err := safemount.NewMount(isoImageLoopDevice.DevicePath(), isoMountDir,
		"iso9660" /*fstype*/, unix.MS_RDONLY /*flags*/, "" /*data*/, true /*makeAndDelete*/)
	if !assert.NoError(t, err) {
		return
	}
	defer isoImageMount.Close()

	// Attach squashfs file.
	squashfsPath := filepath.Join(isoMountDir, liveOSDir, liveOSImage)
	squashfsLoopDevice, err := safeloopback.NewLoopback(squashfsPath)
	if !assert.NoError(t, err) {
		return
	}
	defer squashfsLoopDevice.Close()

	squashfsMountDir := filepath.Join(testTempDir, "iso-squashfs")
	squashfsMount, err := safemount.NewMount(squashfsLoopDevice.DevicePath(), squashfsMountDir,
		"squashfs" /*fstype*/, unix.MS_RDONLY /*flags*/, "" /*data*/, true /*makeAndDelete*/)
	if !assert.NoError(t, err) {
		return
	}
	defer squashfsMount.Close()

	// Check that a.txt is in the squashfs file.
	aOrigPath := filepath.Join(testDir, "files/a.txt")
	aIsoPath := filepath.Join(squashfsMountDir, "a.txt")
	verifyFileContentsSame(t, aOrigPath, aIsoPath)
}

func TestCustomizeImageLiveCdIsoNoShimEfi(t *testing.T) {
	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	buildDir := filepath.Join(tmpDir, "TestCustomizeImageLiveCdIso")
	outImageFilePath := filepath.Join(buildDir, "image.iso")

	config := &imagecustomizerapi.Config{
		OS: &imagecustomizerapi.OS{
			Packages: imagecustomizerapi.Packages{
				Remove: []string{
					"shim",
				},
			},
		},
	}

	// Customize image.
	err := CustomizeImage(buildDir, testDir, config, baseImage, nil, outImageFilePath, "iso", "", true, false)
	assert.Error(t, err)
	assert.ErrorContains(t, err, "failed to find the boot efi file")
}

func TestCustomizeImageLiveCdIsoNoGrubEfi(t *testing.T) {
	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	buildDir := filepath.Join(tmpDir, "TestCustomizeImageLiveCdIso")
	outImageFilePath := filepath.Join(buildDir, "image.iso")

	config := &imagecustomizerapi.Config{
		OS: &imagecustomizerapi.OS{
			Packages: imagecustomizerapi.Packages{
				Remove: []string{
					"grub2-efi-binary",
				},
			},
		},
	}

	// Customize image.
	err := CustomizeImage(buildDir, testDir, config, baseImage, nil, outImageFilePath, "iso", "", true, false)
	assert.Error(t, err)
	assert.ErrorContains(t, err, "failed to find the grub efi file")
}
