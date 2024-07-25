// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/installutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/stretchr/testify/assert"
)

const (
	testImageRootDirName = "testimageroot"
)

var (
	coreEfiMountPoints = []mountPoint{
		{
			PartitionNum:   2,
			Path:           "/",
			FileSystemType: "ext4",
		},
		{
			PartitionNum:   1,
			Path:           "/boot/efi",
			FileSystemType: "vfat",
		},
	}
)

func TestCustomizeImageEmptyConfig(t *testing.T) {
	var err error

	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	buildDir := filepath.Join(tmpDir, "TestCustomizeImageEmptyConfig")
	outImageFilePath := filepath.Join(buildDir, "image.vhd")

	// Customize image.
	err = CustomizeImage(buildDir, buildDir, &imagecustomizerapi.Config{}, baseImage, nil, outImageFilePath,
		"vhd", "", false, false)
	if !assert.NoError(t, err) {
		return
	}

	// Check output file type.
	checkFileType(t, outImageFilePath, "vhd")
}

func TestCustomizeImageCopyFiles(t *testing.T) {
	var err error

	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	buildDir := filepath.Join(tmpDir, "TestCustomizeImageCopyFiles")
	configFile := filepath.Join(testDir, "addfiles-config.yaml")
	outImageFilePath := filepath.Join(buildDir, "image.qcow2")

	// Customize image.
	err = CustomizeImageWithConfigFile(buildDir, configFile, baseImage, nil, outImageFilePath, "raw", "", false, false)
	if !assert.NoError(t, err) {
		return
	}

	// Check output file type.
	checkFileType(t, outImageFilePath, "raw")

	// Mount the output disk image so that its contents can be checked.
	imageConnection, err := connectToCoreEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Check the contents of the copied file.
	file_contents, err := os.ReadFile(filepath.Join(imageConnection.Chroot().RootDir(), "a.txt"))
	assert.NoError(t, err)
	assert.Equal(t, "abcdefg\n", string(file_contents))
}

func connectToCoreEfiImage(buildDir string, imageFilePath string) (*ImageConnection, error) {
	return connectToImage(buildDir, imageFilePath, coreEfiMountPoints)
}

type mountPoint struct {
	PartitionNum   int
	Path           string
	FileSystemType string
	Flags          uintptr
}

func connectToImage(buildDir string, imageFilePath string, mounts []mountPoint) (*ImageConnection, error) {
	imageConnection := NewImageConnection()
	err := imageConnection.ConnectLoopback(imageFilePath)
	if err != nil {
		imageConnection.Close()
		return nil, err
	}

	rootDir := filepath.Join(buildDir, testImageRootDirName)

	mountPoints := []*safechroot.MountPoint(nil)
	for _, mount := range mounts {
		devPath := partitionDevPath(imageConnection, mount.PartitionNum)

		var mountPoint *safechroot.MountPoint
		if mount.Path == "/" {
			mountPoint = safechroot.NewPreDefaultsMountPoint(devPath, mount.Path, mount.FileSystemType, mount.Flags,
				"")
		} else {
			mountPoint = safechroot.NewMountPoint(devPath, mount.Path, mount.FileSystemType, mount.Flags, "")
		}

		mountPoints = append(mountPoints, mountPoint)
	}

	err = imageConnection.ConnectChroot(rootDir, false, []string{}, mountPoints, false)
	if err != nil {
		imageConnection.Close()
		return nil, err
	}

	return imageConnection, nil
}

func partitionDevPath(imageConnection *ImageConnection, partitionNum int) string {
	devPath := fmt.Sprintf("%sp%d", imageConnection.Loopback().DevicePath(), partitionNum)
	return devPath
}

func TestValidateConfigValidAdditionalFiles(t *testing.T) {
	err := validateConfig(testDir, &imagecustomizerapi.Config{
		OS: &imagecustomizerapi.OS{
			AdditionalFiles: imagecustomizerapi.AdditionalFilesMap{
				"files/a.txt": {{Path: "/a.txt"}},
			},
		}}, nil, true)
	assert.NoError(t, err)
}

func TestValidateConfigMissingAdditionalFiles(t *testing.T) {
	err := validateConfig(testDir, &imagecustomizerapi.Config{
		OS: &imagecustomizerapi.OS{
			AdditionalFiles: imagecustomizerapi.AdditionalFilesMap{
				"files/missing_a.txt": {{Path: "/a.txt"}},
			},
		}}, nil, true)
	assert.Error(t, err)
}

func TestValidateConfigdditionalFilesIsDir(t *testing.T) {
	err := validateConfig(testDir, &imagecustomizerapi.Config{
		OS: &imagecustomizerapi.OS{
			AdditionalFiles: imagecustomizerapi.AdditionalFilesMap{
				"files": {{Path: "/a.txt"}},
			},
		}}, nil, true)
	assert.Error(t, err)
}

func TestValidateConfigScript(t *testing.T) {
	err := validateScripts(testDir, &imagecustomizerapi.Scripts{
		PostCustomization: []imagecustomizerapi.Script{
			{
				Path: "scripts/postcustomizationscript.sh",
			},
		},
		FinalizeCustomization: []imagecustomizerapi.Script{
			{
				Path: "scripts/finalizecustomizationscript.sh",
			},
		},
	})
	assert.NoError(t, err)
}

func TestValidateConfigScriptNonLocalFile(t *testing.T) {
	err := validateScripts(testDir, &imagecustomizerapi.Scripts{
		FinalizeCustomization: []imagecustomizerapi.Script{
			{
				Path: "../a.sh",
			},
		},
	})
	assert.Error(t, err)
}

func TestCustomizeImageKernelCommandLineAdd(t *testing.T) {
	var err error

	baseImage := checkSkipForCustomizeImage(t, baseImageTypeCoreEfi)

	buildDir := filepath.Join(tmpDir, "TestCustomizeImageKernelCommandLine")
	outImageFilePath := filepath.Join(buildDir, "image.vhd")

	// Customize image.
	config := &imagecustomizerapi.Config{
		OS: &imagecustomizerapi.OS{
			KernelCommandLine: imagecustomizerapi.KernelCommandLine{
				ExtraCommandLine: "console=tty0 console=ttyS0",
			},
		},
	}

	err = CustomizeImage(buildDir, buildDir, config, baseImage, nil, outImageFilePath, "raw", "", false, false)
	if !assert.NoError(t, err) {
		return
	}

	// Mount the output disk image so that its contents can be checked.
	imageConnection, err := connectToCoreEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Read the grub.cfg file.
	grub2ConfigFilePath := filepath.Join(imageConnection.Chroot().RootDir(), installutils.GrubCfgFile)

	grub2ConfigFile, err := os.ReadFile(grub2ConfigFilePath)
	if !assert.NoError(t, err) {
		return
	}

	t.Logf("%s", grub2ConfigFile)

	linuxCommandLineRegex, err := regexp.Compile(`linux .* console=tty0 console=ttyS0 `)
	if !assert.NoError(t, err) {
		return
	}

	assert.True(t, linuxCommandLineRegex.Match(grub2ConfigFile))
}

func checkFileType(t *testing.T, filePath string, expectedFileType string) {
	fileType, err := getImageFileType(filePath)
	assert.NoError(t, err)
	assert.Equal(t, expectedFileType, fileType)
}

func getImageFileType(filePath string) (string, error) {
	file, err := os.OpenFile(filePath, os.O_RDONLY, 0)
	if err != nil {
		return "", err
	}
	defer file.Close()

	firstBytes := make([]byte, 512)
	readByteCount, err := file.Read(firstBytes)
	if err != nil {
		return "", err
	}

	switch {
	case readByteCount >= 8 && bytes.Equal(firstBytes[:8], []byte("conectix")):
		return "vhd", nil

	case readByteCount >= 8 && bytes.Equal(firstBytes[:8], []byte("vhdxfile")):
		return "vhdx", nil

	case isZstFile(firstBytes):
		return "zst", nil

	// Check for the MBR signature (which exists even on GPT formatted drives).
	case readByteCount >= 512 && bytes.Equal(firstBytes[510:512], []byte{0x55, 0xAA}):
		return "raw", nil
	}

	return "", fmt.Errorf("unknown file type: %s", filePath)
}

func isZstFile(firstBytes []byte) bool {
	if len(firstBytes) < 4 {
		return false
	}

	magicNumber := binary.LittleEndian.Uint32(firstBytes[:4])

	// 0xFD2FB528 is a zst frame.
	// 0x184D2A50-0x184D2A5F are skippable ztd frames.
	return magicNumber == 0xFD2FB528 || (magicNumber >= 0x184D2A50 && magicNumber <= 0x184D2A5F)
}
