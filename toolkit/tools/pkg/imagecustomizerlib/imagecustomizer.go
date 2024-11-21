// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safeloopback"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safemount"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

const (
	tmpParitionDirName = "tmppartition"

	// supported input formats
	ImageFormatVhd   = "vhd"
	ImageFormatVhdx  = "vhdx"
	ImageFormatQCow2 = "qcow2"
	ImageFormatIso   = "iso"
	ImageFormatRaw   = "raw"

	// qemu-specific formats
	QemuFormatVpc = "vpc"

	BaseImageName                = "image.raw"
	PartitionCustomizedImageName = "image2.raw"
)

var (
	// Version specifies the version of the Mariner Image Customizer tool.
	// The value of this string is inserted during compilation via a linker flag.
	ToolVersion = ""
)

func CustomizeImageWithConfigFile(buildDir string, configFile string, imageFile string,
	rpmsSources []string, outputImageFile string, outputImageFormat string,
	outputSplitPartitionsFormat string, useBaseImageRpmRepos bool, enableShrinkFilesystems bool,
) error {
	var err error

	var config imagecustomizerapi.Config
	err = imagecustomizerapi.UnmarshalYamlFile(configFile, &config)
	if err != nil {
		return err
	}

	baseConfigPath, _ := filepath.Split(configFile)

	absBaseConfigPath, err := filepath.Abs(baseConfigPath)
	if err != nil {
		return fmt.Errorf("failed to get absolute path of config file directory:\n%w", err)
	}

	err = CustomizeImage(buildDir, absBaseConfigPath, &config, imageFile, rpmsSources, outputImageFile, outputImageFormat,
		outputSplitPartitionsFormat, useBaseImageRpmRepos, enableShrinkFilesystems)
	if err != nil {
		return err
	}

	return nil
}

func CustomizeImage(buildDir string, baseConfigPath string, config *imagecustomizerapi.Config, imageFile string,
	rpmsSources []string, outputImageFile string, outputImageFormat string, outputSplitPartitionsFormat string,
	useBaseImageRpmRepos bool, enableShrinkFilesystems bool,
) error {
	var err error
	var qemuOutputImageFormat string

	outputImageBase := strings.TrimSuffix(filepath.Base(outputImageFile), filepath.Ext(outputImageFile))
	outputImageDir := filepath.Dir(outputImageFile)

	// Validate 'outputImageFormat' value if specified.
	if outputImageFormat != "" && outputImageFormat != ImageFormatIso {
		qemuOutputImageFormat, err = toQemuImageFormat(outputImageFormat)
		if err != nil {
			return err
		}
	}

	// Validate config.
	err = validateConfig(baseConfigPath, config, rpmsSources, useBaseImageRpmRepos)
	if err != nil {
		return fmt.Errorf("invalid image config:\n%w", err)
	}

	// Normalize 'buildDir' path.
	buildDirAbs, err := filepath.Abs(buildDir)
	if err != nil {
		return err
	}

	// Create 'buildDir' directory.
	err = os.MkdirAll(buildDirAbs, os.ModePerm)
	if err != nil {
		return err
	}

	// Convert image file to raw format, so that a kernel loop device can be used to make changes to the image.
	rawImageFile := filepath.Join(buildDirAbs, BaseImageName)
	defer func() {
		cleanupErr := file.RemoveFileIfExists(rawImageFile)
		if cleanupErr != nil {
			if err != nil {
				err = fmt.Errorf("%w:\nfailed to clean-up (%s): %w", err, rawImageFile, cleanupErr)
			} else {
				err = fmt.Errorf("failed to clean-up (%s): %w", rawImageFile, cleanupErr)
			}
		}
	}()

	logger.Log.Infof("Creating raw base image: %s", rawImageFile)
	err = shell.ExecuteLiveWithErr(1, "qemu-img", "convert", "-O", "raw", imageFile, rawImageFile)
	if err != nil {
		return fmt.Errorf("failed to convert image file to raw format:\n%w", err)
	}

	// Customize the partitions.
	partitionsCustomized, rawImageFile, err := customizePartitions(buildDirAbs, baseConfigPath, config, rawImageFile)
	if err != nil {
		return err
	}

	// Customize the raw image file.
	err = customizeImageHelper(buildDirAbs, baseConfigPath, config, rawImageFile, rpmsSources, useBaseImageRpmRepos,
		partitionsCustomized)
	if err != nil {
		return err
	}

	// Shrink the filesystems.
	if enableShrinkFilesystems {
		err = shrinkFilesystemsHelper(rawImageFile)
		if err != nil {
			return fmt.Errorf("failed to shrink filesystems:\n%w", err)
		}
	}

	if config.SystemConfig.Verity != nil {
		// Customize image for dm-verity, setting up verity metadata and security features.
		err = customizeVerityImageHelper(buildDirAbs, baseConfigPath, config, rawImageFile, rpmsSources, useBaseImageRpmRepos)
		if err != nil {
			return err
		}
	}

	// Create final output image file if requested.
	switch outputImageFormat {
	case ImageFormatVhd, ImageFormatVhdx, ImageFormatQCow2, ImageFormatRaw:
		logger.Log.Infof("Writing: %s", outputImageFile)

		os.MkdirAll(outputImageDir, os.ModePerm)
		err = shell.ExecuteLiveWithErr(1, "qemu-img", "convert", "-O", qemuOutputImageFormat, rawImageFile, outputImageFile)
		if err != nil {
			return fmt.Errorf("failed to convert image file to format: %s:\n%w", outputImageFormat, err)
		}
	case ImageFormatIso:
		err = createLiveOSIsoImage(buildDir, baseConfigPath, config.Iso, rawImageFile, outputImageDir, outputImageBase)
		if err != nil {
			return err
		}
	}

	// If outputSplitPartitionsFormat is specified, extract the partition files.
	if outputSplitPartitionsFormat != "" {
		logger.Log.Infof("Extracting partition files")
		err = extractPartitionsHelper(rawImageFile, outputImageDir, outputImageBase, outputSplitPartitionsFormat)
		if err != nil {
			return err
		}
	}

	logger.Log.Infof("Success!")

	return nil
}

func toQemuImageFormat(imageFormat string) (string, error) {
	switch imageFormat {
	case ImageFormatVhd:
		return QemuFormatVpc, nil

	case ImageFormatVhdx, ImageFormatRaw, ImageFormatQCow2:
		return imageFormat, nil

	default:
		return "", fmt.Errorf("unsupported image format (supported: vhd, vhdx, raw, qcow2): %s", imageFormat)
	}
}

func validateConfig(baseConfigPath string, config *imagecustomizerapi.Config, rpmsSources []string,
	useBaseImageRpmRepos bool,
) error {
	// Note: This IsValid() check does duplicate the one in UnmarshalYamlFile().
	// But it is useful for functions that call CustomizeImage() directly. For example, test code.
	err := config.IsValid()
	if err != nil {
		return err
	}

	partitionsCustomized := hasPartitionCustomizations(config)

	err = validateIsoConfig(baseConfigPath, config.Iso)
	if err != nil {
		return err
	}

	err = validateSystemConfig(baseConfigPath, &config.SystemConfig, rpmsSources, useBaseImageRpmRepos,
		partitionsCustomized)
	if err != nil {
		return err
	}

	return nil
}

func hasPartitionCustomizations(config *imagecustomizerapi.Config) bool {
	return config.Disks != nil
}

func validateAdditionalFiles(baseConfigPath string, additionalFiles imagecustomizerapi.AdditionalFilesMap) error {
	var aggregateErr error
	for sourceFile := range additionalFiles {
		sourceFileFullPath := filepath.Join(baseConfigPath, sourceFile)
		isFile, err := file.IsFile(sourceFileFullPath)
		if err != nil {
			aggregateErr = errors.Join(aggregateErr, fmt.Errorf("invalid AdditionalFiles source file (%s):\n%w", sourceFile, err))
		}

		if !isFile {
			aggregateErr = errors.Join(aggregateErr, fmt.Errorf("invalid AdditionalFiles source file (%s): not a file", sourceFile))
		}
	}
	return aggregateErr
}

func validateIsoConfig(baseConfigPath string, config *imagecustomizerapi.Iso) error {
	if config == nil {
		return nil
	}

	err := validateIsoKernelCommandline(config.KernelCommandLine)
	if err != nil {
		return err
	}

	err = validateAdditionalFiles(baseConfigPath, config.AdditionalFiles)
	if err != nil {
		return err
	}

	return nil
}

func validateIsoKernelCommandline(kernelCommandLine imagecustomizerapi.KernelCommandLine) error {
	if kernelCommandLine.SELinux != imagecustomizerapi.SELinuxDefault {
		return fmt.Errorf("unsupported SELinux configuration for the output ISO image.")
	}
	return nil
}

func validateSystemConfig(baseConfigPath string, config *imagecustomizerapi.SystemConfig,
	rpmsSources []string, useBaseImageRpmRepos bool, partitionsCustomized bool,
) error {
	var err error

	err = validatePackageLists(baseConfigPath, config, rpmsSources, useBaseImageRpmRepos, partitionsCustomized)
	if err != nil {
		return err
	}

	err = validateAdditionalFiles(baseConfigPath, config.AdditionalFiles)
	if err != nil {
		return err
	}

	for i, script := range config.PostInstallScripts {
		err = validateScript(baseConfigPath, &script)
		if err != nil {
			return fmt.Errorf("invalid PostInstallScripts item at index %d: %w", i, err)
		}
	}

	for i, script := range config.FinalizeImageScripts {
		err = validateScript(baseConfigPath, &script)
		if err != nil {
			return fmt.Errorf("invalid FinalizeImageScripts item at index %d: %w", i, err)
		}
	}

	return nil
}

func validateScript(baseConfigPath string, script *imagecustomizerapi.Script) error {
	// Ensure that install scripts sit under the config file's parent directory.
	// This allows the install script to be run in the chroot environment by bind mounting the config directory.
	if !filepath.IsLocal(script.Path) {
		return fmt.Errorf("install script (%s) is not under config directory (%s)", script.Path, baseConfigPath)
	}

	// Verify that the file exists.
	fullPath := filepath.Join(baseConfigPath, script.Path)

	scriptStat, err := os.Stat(fullPath)
	if err != nil {
		return fmt.Errorf("couldn't read install script (%s):\n%w", script.Path, err)
	}

	// Verify that the file has an executable bit set.
	if scriptStat.Mode()&0111 == 0 {
		return fmt.Errorf("install script (%s) does not have executable bit set", script.Path)
	}

	return nil
}

func validatePackageLists(baseConfigPath string, config *imagecustomizerapi.SystemConfig, rpmsSources []string,
	useBaseImageRpmRepos bool, partitionsCustomized bool,
) error {
	allPackagesRemove, err := collectPackagesList(baseConfigPath, config.PackageListsRemove, config.PackagesRemove)
	if err != nil {
		return err
	}

	allPackagesInstall, err := collectPackagesList(baseConfigPath, config.PackageListsInstall, config.PackagesInstall)
	if err != nil {
		return err
	}

	allPackagesUpdate, err := collectPackagesList(baseConfigPath, config.PackageListsUpdate, config.PackagesUpdate)
	if err != nil {
		return err
	}

	hasRpmSources := len(rpmsSources) > 0 || useBaseImageRpmRepos

	if !hasRpmSources {
		needRpmsSources := len(allPackagesInstall) > 0 || len(allPackagesUpdate) > 0 || config.UpdateBaseImagePackages

		if needRpmsSources {
			return fmt.Errorf("have packages to install or update but no RPM sources were specified")
		} else if partitionsCustomized {
			return fmt.Errorf("partitions were customized so the initramfs package needs to be reinstalled but no RPM sources were specified")
		}
	}

	config.PackagesRemove = allPackagesRemove
	config.PackagesInstall = allPackagesInstall
	config.PackagesUpdate = allPackagesUpdate

	config.PackageListsRemove = nil
	config.PackageListsInstall = nil
	config.PackageListsUpdate = nil

	return nil
}

func customizeImageHelper(buildDir string, baseConfigPath string, config *imagecustomizerapi.Config,
	rawImageFile string, rpmsSources []string, useBaseImageRpmRepos bool, partitionsCustomized bool,
) error {
	imageConnection, err := connectToExistingImage(rawImageFile, buildDir, "imageroot", true)
	if err != nil {
		return err
	}
	defer imageConnection.Close()

	// Do the actual customizations.
	err = doCustomizations(buildDir, baseConfigPath, config, imageConnection.Chroot(), rpmsSources,
		useBaseImageRpmRepos, partitionsCustomized)
	if err != nil {
		return err
	}

	err = imageConnection.CleanClose()
	if err != nil {
		return err
	}

	return nil
}

func extractPartitionsHelper(rawImageFile string, outputDir string, outputBasename string, outputSplitPartitionsFormat string) error {
	imageLoopback, err := safeloopback.NewLoopback(rawImageFile)
	if err != nil {
		return err
	}
	defer imageLoopback.Close()

	// Extract the partitions as files.
	err = extractPartitions(imageLoopback.DevicePath(), outputDir, outputBasename, outputSplitPartitionsFormat)
	if err != nil {
		return err
	}

	err = imageLoopback.CleanClose()
	if err != nil {
		return err
	}

	return nil
}

func shrinkFilesystemsHelper(buildImageFile string) error {
	imageLoopback, err := safeloopback.NewLoopback(buildImageFile)
	if err != nil {
		return err
	}
	defer imageLoopback.Close()

	// Shrink the filesystems.
	err = shrinkFilesystems(imageLoopback.DevicePath())
	if err != nil {
		return err
	}

	err = imageLoopback.CleanClose()
	if err != nil {
		return err
	}

	return nil
}

func customizeVerityImageHelper(buildDir string, baseConfigPath string, config *imagecustomizerapi.Config,
	buildImageFile string, rpmsSources []string, useBaseImageRpmRepos bool,
) error {
	var err error

	// Connect the disk image to an NBD device using qemu-nbd
	// Find a free NBD device
	nbdDevice, err := findFreeNBDDevice()
	if err != nil {
		return fmt.Errorf("failed to find a free nbd device: %v", err)
	}

	err = shell.ExecuteLiveWithErr(1, "qemu-nbd", "-c", nbdDevice, "-f", "raw", buildImageFile)
	if err != nil {
		return fmt.Errorf("failed to connect nbd %s to image %s: %s", nbdDevice, buildImageFile, err)
	}
	defer func() {
		// Disconnect the NBD device when the function returns
		err = shell.ExecuteLiveWithErr(1, "qemu-nbd", "-d", nbdDevice)
		if err != nil {
			return
		}
	}()

	diskPartitions, err := diskutils.GetDiskPartitions(nbdDevice)
	if err != nil {
		return err
	}

	// Extract the partition block device path.
	dataPartition, err := idToPartitionBlockDevicePath(config.SystemConfig.Verity.DataPartition.IdType, config.SystemConfig.Verity.DataPartition.Id, nbdDevice, diskPartitions)
	if err != nil {
		return err
	}
	hashPartition, err := idToPartitionBlockDevicePath(config.SystemConfig.Verity.HashPartition.IdType, config.SystemConfig.Verity.HashPartition.Id, nbdDevice, diskPartitions)
	if err != nil {
		return err
	}

	// Extract root hash using regular expressions.
	verityOutput, _, err := shell.Execute("veritysetup", "format", dataPartition, hashPartition)
	if err != nil {
		return fmt.Errorf("failed to calculate root hash:\n%w", err)
	}

	var rootHash string
	rootHashRegex, err := regexp.Compile(`Root hash:\s+([0-9a-fA-F]+)`)
	if err != nil {
		// handle the error appropriately, for example:
		return fmt.Errorf("failed to compile root hash regex: %w", err)
	}

	rootHashMatches := rootHashRegex.FindStringSubmatch(verityOutput)
	if len(rootHashMatches) <= 1 {
		return fmt.Errorf("failed to parse root hash from veritysetup output")
	}
	rootHash = rootHashMatches[1]

	systemBootPartition, err := findSystemBootPartition(diskPartitions)
	if err != nil {
		return err
	}
	bootPartition, err := findBootPartitionFromEsp(systemBootPartition, diskPartitions, buildDir)
	if err != nil {
		return err
	}

	bootPartitionTmpDir := filepath.Join(buildDir, tmpParitionDirName)
	// Temporarily mount the partition.
	bootPartitionMount, err := safemount.NewMount(bootPartition.Path, bootPartitionTmpDir, bootPartition.FileSystemType, 0, "", true)
	if err != nil {
		return fmt.Errorf("failed to mount partition (%s):\n%w", bootPartition.Path, err)
	}
	defer bootPartitionMount.Close()

	grubCfgFullPath := filepath.Join(bootPartitionTmpDir, "grub2/grub.cfg")
	if err != nil {
		return fmt.Errorf("failed to stat file (%s):\n%w", grubCfgFullPath, err)
	}

	err = updateGrubConfig(config.SystemConfig.Verity.DataPartition.IdType, config.SystemConfig.Verity.DataPartition.Id,
		config.SystemConfig.Verity.HashPartition.IdType, config.SystemConfig.Verity.HashPartition.Id, rootHash, grubCfgFullPath)
	if err != nil {
		return err
	}

	err = bootPartitionMount.CleanClose()
	if err != nil {
		return err
	}

	return nil
}
