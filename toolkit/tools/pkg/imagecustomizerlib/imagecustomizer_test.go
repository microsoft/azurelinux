// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"bytes"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/buildpipeline"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/ptrutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/stretchr/testify/assert"
)

const (
	testImageRootDirName = "testimageroot"
)

func TestCustomizeImageEmptyConfig(t *testing.T) {
	var err error

	if testing.Short() {
		t.Skip("Short mode enabled")
	}

	if !buildpipeline.IsRegularBuild() {
		t.Skip("loopback block device not available")
	}

	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses a chroot")
	}

	buildDir := filepath.Join(tmpDir, "TestCustomizeImageEmptyConfig")
	outImageFilePath := filepath.Join(buildDir, "image.vhd")

	// Create fake disk.
	diskFilePath, err := createFakeEfiImage(buildDir)
	if !assert.NoError(t, err) {
		return
	}

	// Customize image.
	err = CustomizeImage(buildDir, buildDir, &imagecustomizerapi.Config{}, diskFilePath, nil, outImageFilePath,
		"vhd", "", false)
	if !assert.NoError(t, err) {
		return
	}

	// Check output file type.
	checkFileType(t, outImageFilePath, "vhd")
}

func TestCustomizeImageCopyFiles(t *testing.T) {
	var err error

	if testing.Short() {
		t.Skip("Short mode enabled")
	}

	if !buildpipeline.IsRegularBuild() {
		t.Skip("loopback block device not available")
	}

	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses a chroot")
	}

	buildDir := filepath.Join(tmpDir, "TestCustomizeImageCopyFiles")
	configFile := filepath.Join(testDir, "addfiles-config.yaml")
	outImageFilePath := filepath.Join(buildDir, "image.qcow2")

	// Create fake disk.
	diskFilePath, err := createFakeEfiImage(buildDir)
	if !assert.NoError(t, err) {
		return
	}

	// Customize image.
	err = CustomizeImageWithConfigFile(buildDir, configFile, diskFilePath, nil, outImageFilePath, "raw", "", false)
	if !assert.NoError(t, err) {
		return
	}

	// Check output file type.
	checkFileType(t, outImageFilePath, "raw")

	// Mount the output disk image so that its contents can be checked.
	imageConnection, err := reconnectToFakeEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Check the contents of the copied file.
	file_contents, err := os.ReadFile(filepath.Join(imageConnection.Chroot().RootDir(), "a.txt"))
	assert.NoError(t, err)
	assert.Equal(t, "abcdefg\n", string(file_contents))
}

func reconnectToFakeEfiImage(buildDir string, imageFilePath string) (*ImageConnection, error) {
	imageConnection := NewImageConnection()
	err := imageConnection.ConnectLoopback(imageFilePath)
	if err != nil {
		imageConnection.Close()
		return nil, err
	}

	rootDir := filepath.Join(buildDir, testImageRootDirName)

	bootPartitionDevPath := fmt.Sprintf("%sp1", imageConnection.Loopback().DevicePath())
	osPartitionDevPath := fmt.Sprintf("%sp2", imageConnection.Loopback().DevicePath())

	mountPoints := []*safechroot.MountPoint{
		safechroot.NewPreDefaultsMountPoint(osPartitionDevPath, "/", "ext4", 0, ""),
		safechroot.NewMountPoint(bootPartitionDevPath, "/boot/efi", "vfat", 0, ""),
	}

	err = imageConnection.ConnectChroot(rootDir, false, []string{}, mountPoints)
	if err != nil {
		imageConnection.Close()
		return nil, err
	}

	return imageConnection, nil
}

func TestValidateConfigValidAdditionalFiles(t *testing.T) {
	err := validateConfig(testDir, &imagecustomizerapi.Config{
		SystemConfig: imagecustomizerapi.SystemConfig{
			AdditionalFiles: map[string]imagecustomizerapi.FileConfigList{
				"files/a.txt": {{Path: "/a.txt"}},
			},
		}}, nil, true)
	assert.NoError(t, err)
}

func TestValidateConfigMissingAdditionalFiles(t *testing.T) {
	err := validateConfig(testDir, &imagecustomizerapi.Config{
		SystemConfig: imagecustomizerapi.SystemConfig{
			AdditionalFiles: map[string]imagecustomizerapi.FileConfigList{
				"files/missing_a.txt": {{Path: "/a.txt"}},
			},
		}}, nil, true)
	assert.Error(t, err)
}

func TestValidateConfigdditionalFilesIsDir(t *testing.T) {
	err := validateConfig(testDir, &imagecustomizerapi.Config{
		SystemConfig: imagecustomizerapi.SystemConfig{
			AdditionalFiles: map[string]imagecustomizerapi.FileConfigList{
				"files": {{Path: "/a.txt"}},
			},
		}}, nil, true)
	assert.Error(t, err)
}

func TestValidateConfigScript(t *testing.T) {
	err := validateConfig(testDir, &imagecustomizerapi.Config{
		SystemConfig: imagecustomizerapi.SystemConfig{
			PostInstallScripts: []imagecustomizerapi.Script{
				{
					Path: "scripts/postinstallscript.sh",
				},
			},
			FinalizeImageScripts: []imagecustomizerapi.Script{
				{
					Path: "scripts/finalizeimagescript.sh",
				},
			},
		}}, nil, true)
	assert.NoError(t, err)
}

func TestValidateConfigScriptNonLocalFile(t *testing.T) {
	err := validateConfig(testDir, &imagecustomizerapi.Config{
		SystemConfig: imagecustomizerapi.SystemConfig{
			PostInstallScripts: []imagecustomizerapi.Script{
				{
					Path: "../a.sh",
				},
			},
		}}, nil, true)
	assert.Error(t, err)
}

func TestValidateConfigScriptNonExecutable(t *testing.T) {
	err := validateConfig(testDir, &imagecustomizerapi.Config{
		SystemConfig: imagecustomizerapi.SystemConfig{
			FinalizeImageScripts: []imagecustomizerapi.Script{
				{
					Path: "files/a.txt",
				},
			},
		}}, nil, true)
	assert.Error(t, err)
}

func TestCustomizeImageKernelCommandLineAdd(t *testing.T) {
	var err error

	if testing.Short() {
		t.Skip("Short mode enabled")
	}

	if !buildpipeline.IsRegularBuild() {
		t.Skip("loopback block device not available")
	}

	if os.Geteuid() != 0 {
		t.Skip("Test must be run as root because it uses a chroot")
	}

	buildDir := filepath.Join(tmpDir, "TestCustomizeImageKernelCommandLine")
	outImageFilePath := filepath.Join(buildDir, "image.vhd")

	// Create fake disk.
	diskFilePath, err := createFakeEfiImage(buildDir)
	if !assert.NoError(t, err) {
		return
	}

	// Customize image.
	config := &imagecustomizerapi.Config{
		SystemConfig: imagecustomizerapi.SystemConfig{
			KernelCommandLine: imagecustomizerapi.KernelCommandLine{
				ExtraCommandLine: "console=tty0 console=ttyS0",
			},
		},
	}

	err = CustomizeImage(buildDir, buildDir, config, diskFilePath, nil, outImageFilePath, "raw", "", false)
	if !assert.NoError(t, err) {
		return
	}

	// Mount the output disk image so that its contents can be checked.
	imageConnection, err := reconnectToFakeEfiImage(buildDir, outImageFilePath)
	if !assert.NoError(t, err) {
		return
	}
	defer imageConnection.Close()

	// Read the grub.cfg file.
	grub2ConfigFilePath := filepath.Join(imageConnection.Chroot().RootDir(), "/boot/grub2/grub.cfg")

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

func createFakeEfiImage(buildDir string) (string, error) {
	var err error

	err = os.MkdirAll(buildDir, os.ModePerm)
	if err != nil {
		return "", fmt.Errorf("failed to make build directory (%s):\n%w", buildDir, err)
	}

	// Use a prototypical Mariner image partition config.
	diskConfig := imagecustomizerapi.Disk{
		PartitionTableType: imagecustomizerapi.PartitionTableTypeGpt,
		MaxSize:            4096,
		Partitions: []imagecustomizerapi.Partition{
			{
				ID:     "boot",
				Flags:  []imagecustomizerapi.PartitionFlag{"esp", "boot"},
				Start:  1,
				End:    ptrutils.PtrTo(uint64(9)),
				FsType: "fat32",
			},
			{
				ID:     "rootfs",
				Start:  9,
				End:    nil,
				FsType: "ext4",
			},
		},
	}

	partitionSettings := []imagecustomizerapi.PartitionSetting{
		{
			ID:              "boot",
			MountPoint:      "/boot/efi",
			MountOptions:    "umask=0077",
			MountIdentifier: imagecustomizerapi.MountIdentifierTypeDefault,
		},
		{
			ID:              "rootfs",
			MountPoint:      "/",
			MountIdentifier: imagecustomizerapi.MountIdentifierTypeDefault,
		},
	}

	rawDisk := filepath.Join(buildDir, "disk.raw")

	installOS := func(imageChroot *safechroot.Chroot) error {
		// Don't write anything for the OS.
		// The createNewImage function will still write the bootloader and fstab file, which will allow the partition
		// discovery logic to work. This allows for a limited set of tests to run without needing any of the RPM files.
		return nil
	}

	imageConnection, err := createNewImage(rawDisk, diskConfig, partitionSettings, "efi",
		imagecustomizerapi.KernelCommandLine{}, buildDir, testImageRootDirName, installOS)
	if err != nil {
		return "", err
	}
	defer imageConnection.Close()

	return rawDisk, nil
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

	// Check for the MBR signature (which exists even on GPT formatted drives).
	case readByteCount >= 512 && bytes.Equal(firstBytes[510:512], []byte{0x55, 0xAA}):
		return "raw", nil
	}

	return "", fmt.Errorf("unknown file type: %s", filePath)
}
