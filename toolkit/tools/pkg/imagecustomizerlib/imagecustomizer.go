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

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safeloopback"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safemount"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
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
	// Version specifies the version of the Azure Linux Image Customizer tool.
	// The value of this string is inserted during compilation via a linker flag.
	ToolVersion = ""
)

type ImageCustomizerParameters struct {
	// build dirs
	buildDir    string
	buildDirAbs string

	// input image
	inputImageFile   string
	inputImageFormat string

	// configurations
	configPath                  string
	config                      *imagecustomizerapi.Config
	customizeOSPartitions       bool
	useBaseImageRpmRepos        bool
	rpmsSources                 []string
	enableShrinkFilesystems     bool
	outputSplitPartitionsFormat string

	// intermediate writeable image
	rawImageFile string

	// output image
	outputImageFormat     string
	qemuOutputImageFormat string
	outputImageFile       string
	outputImageDir        string
	outputImageBase       string
}

func createImageCustomizerParameters(buildDir string,
	inputImageFile string,
	configPath string, config *imagecustomizerapi.Config,
	useBaseImageRpmRepos bool, rpmsSources []string, enableShrinkFilesystems bool, outputSplitPartitionsFormat string,
	outputImageFormat string, outputImageFile string) (*ImageCustomizerParameters, error) {

	ic := &ImageCustomizerParameters{}

	// working directories
	ic.buildDir = buildDir

	buildDirAbs, err := filepath.Abs(buildDir)
	if err != nil {
		return nil, err
	}

	ic.buildDirAbs = buildDirAbs

	// input image
	ic.inputImageFile = inputImageFile
	ic.inputImageFormat = filepath.Ext(inputImageFile)

	// configuration
	ic.configPath = configPath
	ic.config = config
	ic.customizeOSPartitions = (config.Storage != nil) || (config.OS != nil) || (config.Scripts != nil)

	ic.useBaseImageRpmRepos = useBaseImageRpmRepos
	ic.rpmsSources = rpmsSources

	ic.enableShrinkFilesystems = enableShrinkFilesystems
	ic.outputSplitPartitionsFormat = outputSplitPartitionsFormat

	// intermediate writeable image
	ic.rawImageFile = filepath.Join(buildDirAbs, BaseImageName)

	// output image
	ic.outputImageFormat = outputImageFormat
	ic.outputImageFile = outputImageFile
	ic.outputImageBase = strings.TrimSuffix(filepath.Base(outputImageFile), filepath.Ext(outputImageFile))
	ic.outputImageDir = filepath.Dir(outputImageFile)

	if ic.outputImageFormat != "" && ic.outputImageFormat != ImageFormatIso {
		ic.qemuOutputImageFormat, err = toQemuImageFormat(ic.outputImageFormat)
		if err != nil {
			return nil, err
		}
	}

	return ic, nil
}

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

func cleanUp(ic *ImageCustomizerParameters) error {

	var allErrors error

	err := file.RemoveFileIfExists(ic.rawImageFile)
	if err != nil {
		allErrors = fmt.Errorf("failed to clean-up raw image file:\n%w", err)
	}

	return allErrors
}

func CustomizeImage(buildDir string, baseConfigPath string, config *imagecustomizerapi.Config, imageFile string,
	rpmsSources []string, outputImageFile string, outputImageFormat string, outputSplitPartitionsFormat string,
	useBaseImageRpmRepos bool, enableShrinkFilesystems bool,
) error {
	err := validateConfig(baseConfigPath, config, rpmsSources, useBaseImageRpmRepos)
	if err != nil {
		return fmt.Errorf("invalid image config:\n%w", err)
	}

	imageCustomizerParameters, err := createImageCustomizerParameters(buildDir, imageFile,
		baseConfigPath, config,
		useBaseImageRpmRepos, rpmsSources, enableShrinkFilesystems, outputSplitPartitionsFormat,
		outputImageFormat, outputImageFile)
	if err != nil {
		return fmt.Errorf("failed to create image customizer parameters object:\n%w", err)
	}
	defer func() {
		cleanupErr := cleanUp(imageCustomizerParameters)
		if cleanupErr != nil {
			if err != nil {
				err = fmt.Errorf("%w:\nfailed to clean-up:\n%w", err, cleanupErr)
			} else {
				err = fmt.Errorf("failed to clean-up:\n%w", cleanupErr)
			}
		}
	}()

	// ensure build and output folders are created up front
	err = os.MkdirAll(imageCustomizerParameters.buildDirAbs, os.ModePerm)
	if err != nil {
		return err
	}

	err = os.MkdirAll(imageCustomizerParameters.outputImageDir, os.ModePerm)
	if err != nil {
		return err
	}

	isoBuilder, err := convertInputImageToWriteableFormat(imageCustomizerParameters)
	if err != nil {
		return fmt.Errorf("failed to convert input image to a raw image:\n%w", err)
	}
	defer func() {
		if isoBuilder != nil {
			cleanupErr := isoBuilder.cleanUp()
			if cleanupErr != nil {
				if err != nil {
					err = fmt.Errorf("%w:\nfailed to clean-up iso builder state:\n%w", err, cleanupErr)
				} else {
					err = fmt.Errorf("failed to clean-up iso builder state:\n%w", cleanupErr)
				}
			}
		}
	}()

	err = customizeOSContents(imageCustomizerParameters)
	if err != nil {
		return fmt.Errorf("failed to customize raw image:\n%w", err)
	}

	err = convertWriteableFormatToOutputImage(imageCustomizerParameters, isoBuilder)
	if err != nil {
		return fmt.Errorf("failed to convert customized raw image to output format:\n%w", err)
	}

	logger.Log.Infof("Success!")

	return nil
}

func convertInputImageToWriteableFormat(ic *ImageCustomizerParameters) (*LiveOSIsoBuilder, error) {
	logger.Log.Infof("Converting input image to a writeable format")

	if ic.inputImageFormat == ".iso" {

		isoBuilder, err := createIsoBuilderFromIsoImage(ic.buildDir, ic.buildDirAbs, ic.inputImageFile)
		if err != nil {
			var cleanUpError error
			if isoBuilder != nil {
				cleanUpError = isoBuilder.cleanUp()
			}
			if cleanUpError == nil {
				return nil, fmt.Errorf("failed to load input iso artifacts:\n%w", err)
			} else {
				return nil, fmt.Errorf("failed to load input iso artifacts:\n%w\nclean-up error:\n%w", err, cleanUpError)
			}
		}

		// If the input is a LiveOS iso and there are OS customizations
		// defined, we create a writeable disk image so that mic can modify
		// it. If no OS customizations are defined, we can skip this step and
		// just re-use the existing squashfs.
		if ic.customizeOSPartitions {
			var aggregateErr error

			err = isoBuilder.createWriteableImageFromSquashfs(ic.buildDir, ic.rawImageFile)
			if err != nil {
				aggregateErr = errors.Join(aggregateErr, fmt.Errorf("failed to create writeable image:\n%w", err))
			}

			// From this point on, the customization code will do its job
			// without even knowning that the writeable image came from an iso
			// and all iso artifacts will need to be regenerated - so, no need
			// to keep the state of the input iso around.
			cleanUpError := isoBuilder.cleanUp()
			if cleanUpError != nil {
				aggregateErr = errors.Join(aggregateErr, fmt.Errorf("failed to clean-up iso builder object:\n%w", cleanUpError))
			}

			// delete the isoBuilder object
			isoBuilder = nil

			return nil, aggregateErr
		} else {
			return isoBuilder, nil
		}
	} else {
		logger.Log.Infof("Creating raw base image: %s", ic.rawImageFile)
		err := shell.ExecuteLiveWithErr(1, "qemu-img", "convert", "-O", "raw", ic.inputImageFile, ic.rawImageFile)
		if err != nil {
			return nil, fmt.Errorf("failed to convert image file to raw format:\n%w", err)
		}
	}

	return nil, nil
}

func customizeOSContents(ic *ImageCustomizerParameters) error {

	// If the user has defined customizations, then should proceed as usual.
	// However, there are no customizations, and the input is an iso, we
	// should just return - but call out any command line switches that might
	// have requested unsupported changes.
	if !ic.customizeOSPartitions && ic.inputImageFormat == ".iso" {

		if ic.enableShrinkFilesystems {
			return fmt.Errorf("shrinking file systems is not supported when the input image is an iso.")
		}

		if ic.outputSplitPartitionsFormat != "" {
			return fmt.Errorf("extracting partitions is not support when the input image is an iso.")
		}

		return nil
	}

	// Check if the partition is using DM_verity_hash file system type.
	// The presence of this type indicates that dm-verity has been enabled on the base image. If dm-verity is not enabled,
	// the verity hash device should not be assigned this type. We do not support customization on verity enabled base
	// images at this time because such modifications would compromise the integrity and security mechanisms enforced by dm-verity.
	err = checkDmVerityEnabled(ic.rawImageFile)
	if err != nil {
		return err
	}

	if ic.config.OS == nil {
		ic.config.OS = &imagecustomizerapi.OS{}
	}

	// Customize the partitions.
	partitionsCustomized, newRawImageFile, err := customizePartitions(ic.buildDirAbs, ic.configPath, ic.config, ic.rawImageFile)
	if err != nil {
		return err
	}
	ic.rawImageFile = newRawImageFile

	// Customize the raw image file.
	err = customizeImageHelper(ic.buildDirAbs, ic.configPath, ic.config, ic.rawImageFile, ic.rpmsSources, ic.useBaseImageRpmRepos,
		partitionsCustomized)
	if err != nil {
		return err
	}

	// Shrink the filesystems.
	if ic.enableShrinkFilesystems {
		err = shrinkFilesystemsHelper(ic.rawImageFile)
		if err != nil {
			return fmt.Errorf("failed to shrink filesystems:\n%w", err)
		}
	}

	if ic.config.OS.Verity != nil {
		// Customize image for dm-verity, setting up verity metadata and security features.
		err = customizeVerityImageHelper(ic.buildDirAbs, ic.configPath, ic.config, ic.rawImageFile, ic.rpmsSources, ic.useBaseImageRpmRepos)
		if err != nil {
			return err
		}
	}

	// Check file systems for corruption.
	err = checkFileSystems(ic.rawImageFile)
	if err != nil {
		return fmt.Errorf("failed to check filesystems:\n%w", err)
	}

	// If outputSplitPartitionsFormat is specified, extract the partition files.
	if ic.outputSplitPartitionsFormat != "" {
		logger.Log.Infof("Extracting partition files")
		err = extractPartitionsHelper(ic.rawImageFile, ic.outputImageDir, ic.outputImageBase, ic.outputSplitPartitionsFormat)
		if err != nil {
			return err
		}
	}

	return nil
}

func convertWriteableFormatToOutputImage(ic *ImageCustomizerParameters, isoBuilder *LiveOSIsoBuilder) error {

	logger.Log.Infof("Converting customized OS partitions into the final image")

	// Create final output image file if requested.
	switch ic.outputImageFormat {
	case ImageFormatVhd, ImageFormatVhdx, ImageFormatQCow2, ImageFormatRaw:
		logger.Log.Infof("Writing: %s", ic.outputImageFile)

		err := shell.ExecuteLiveWithErr(1, "qemu-img", "convert", "-O", ic.qemuOutputImageFormat, ic.rawImageFile, ic.outputImageFile)
		if err != nil {
			return fmt.Errorf("failed to convert image file to format: %s:\n%w", ic.outputImageFormat, err)
		}
	case ImageFormatIso:
		if ic.customizeOSPartitions {
			err := createLiveOSIsoImage(ic.buildDir, ic.configPath, ic.config.Iso, ic.rawImageFile, ic.outputImageDir, ic.outputImageBase)
			if err != nil {
				return fmt.Errorf("failed to create LiveOS iso image:\n%w", err)
			}
		} else {
			if isoBuilder == nil {
				return fmt.Errorf("internal error: isoBuilder cannot be nil when the output format is .iso and there are no OS customizations.")
			}
			err := isoBuilder.createImageFromUnchangedOS(ic.configPath, ic.config.Iso, ic.outputImageDir, ic.outputImageBase)
			if err != nil {
				return fmt.Errorf("failed to create LiveOS iso image:\n%w", err)
			}
		}
	}

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

	err = validateIsoConfig(baseConfigPath, config.Iso)
	if err != nil {
		return err
	}

	err = validateSystemConfig(baseConfigPath, config.OS, rpmsSources, useBaseImageRpmRepos)
	if err != nil {
		return err
	}

	err = validateScripts(baseConfigPath, config.Scripts)
	if err != nil {
		return err
	}

	return nil
}

func hasPartitionCustomizations(config *imagecustomizerapi.Config) bool {
	return config.Storage != nil
}

func validateAdditionalFiles(baseConfigPath string, additionalFiles imagecustomizerapi.AdditionalFilesMap) error {
	var aggregateErr error
	for sourceFile := range additionalFiles {
		sourceFileFullPath := file.GetAbsPathWithBase(baseConfigPath, sourceFile)
		isFile, err := file.IsFile(sourceFileFullPath)
		if err != nil {
			aggregateErr = errors.Join(aggregateErr, fmt.Errorf("invalid additionalFiles source file (%s):\n%w", sourceFile, err))
		}

		if !isFile {
			aggregateErr = errors.Join(aggregateErr, fmt.Errorf("invalid additionalFiles source file (%s): not a file", sourceFile))
		}
	}
	return aggregateErr
}

func validateIsoConfig(baseConfigPath string, config *imagecustomizerapi.Iso) error {
	if config == nil {
		return nil
	}

	err := validateAdditionalFiles(baseConfigPath, config.AdditionalFiles)
	if err != nil {
		return err
	}

	return nil
}

func validateSystemConfig(baseConfigPath string, config *imagecustomizerapi.OS,
	rpmsSources []string, useBaseImageRpmRepos bool,
) error {

	if config == nil {
		return nil
	}

	var err error

	err = validatePackageLists(baseConfigPath, config, rpmsSources, useBaseImageRpmRepos)
	if err != nil {
		return err
	}

	err = validateAdditionalFiles(baseConfigPath, config.AdditionalFiles)
	if err != nil {
		return err
	}

	return nil
}

func validateScripts(baseConfigPath string, scripts *imagecustomizerapi.Scripts) error {

	if scripts == nil {
		return nil
	}

	for i, script := range scripts.PostCustomization {
		err := validateScript(baseConfigPath, &script)
		if err != nil {
			return fmt.Errorf("invalid postCustomization item at index %d:\n%w", i, err)
		}
	}

	for i, script := range scripts.FinalizeCustomization {
		err := validateScript(baseConfigPath, &script)
		if err != nil {
			return fmt.Errorf("invalid finalizeCustomization item at index %d:\n%w", i, err)
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

func validatePackageLists(baseConfigPath string, config *imagecustomizerapi.OS, rpmsSources []string,
	useBaseImageRpmRepos bool,
) error {

	if config == nil {
		return nil
	}

	allPackagesRemove, err := collectPackagesList(baseConfigPath, config.Packages.RemoveLists, config.Packages.Remove)
	if err != nil {
		return err
	}

	allPackagesInstall, err := collectPackagesList(baseConfigPath, config.Packages.InstallLists, config.Packages.Install)
	if err != nil {
		return err
	}

	allPackagesUpdate, err := collectPackagesList(baseConfigPath, config.Packages.UpdateLists, config.Packages.Update)
	if err != nil {
		return err
	}

	hasRpmSources := len(rpmsSources) > 0 || useBaseImageRpmRepos

	if !hasRpmSources {
		needRpmsSources := len(allPackagesInstall) > 0 || len(allPackagesUpdate) > 0 ||
			config.Packages.UpdateExistingPackages

		if needRpmsSources {
			return fmt.Errorf("have packages to install or update but no RPM sources were specified")
		}
	}

	config.Packages.Remove = allPackagesRemove
	config.Packages.Install = allPackagesInstall
	config.Packages.Update = allPackagesUpdate

	config.Packages.RemoveLists = nil
	config.Packages.InstallLists = nil
	config.Packages.UpdateLists = nil

	return nil
}

func customizeImageHelper(buildDir string, baseConfigPath string, config *imagecustomizerapi.Config,
	rawImageFile string, rpmsSources []string, useBaseImageRpmRepos bool, partitionsCustomized bool,
) error {
	logger.Log.Debugf("Customizing OS")

	imageConnection, err := connectToExistingImage(rawImageFile, buildDir, "imageroot", true)
	if err != nil {
		return err
	}
	defer imageConnection.Close()

	// Do the actual customizations.
	err = doCustomizations(buildDir, baseConfigPath, config, imageConnection, rpmsSources,
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
	dataPartition, err := idToPartitionBlockDevicePath(config.OS.Verity.DataPartition.IdType, config.OS.Verity.DataPartition.Id, nbdDevice, diskPartitions)
	if err != nil {
		return err
	}
	hashPartition, err := idToPartitionBlockDevicePath(config.OS.Verity.HashPartition.IdType, config.OS.Verity.HashPartition.Id, nbdDevice, diskPartitions)
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

	err = updateGrubConfig(config.OS.Verity.DataPartition.IdType, config.OS.Verity.DataPartition.Id,
		config.OS.Verity.HashPartition.IdType, config.OS.Verity.HashPartition.Id, config.OS.Verity.CorruptionOption,
		rootHash, grubCfgFullPath)
	if err != nil {
		return err
	}

	err = bootPartitionMount.CleanClose()
	if err != nil {
		return err
	}

	return nil
}

func checkDmVerityEnabled(rawImageFile string) error {
	logger.Log.Debugf("Check if dm-verity is enabled in base image")

	loopback, err := safeloopback.NewLoopback(rawImageFile)
	if err != nil {
		return fmt.Errorf("failed to check if dm-verity is enabled in base image:\n%w", err)
	}
	defer loopback.Close()

	diskPartitions, err := diskutils.GetDiskPartitions(loopback.DevicePath())
	if err != nil {
		return err
	}

	for i := range diskPartitions {
		diskPartition := diskPartitions[i]

		if diskPartition.FileSystemType == "DM_verity_hash" {
			return fmt.Errorf("cannot customize base image that has dm-verity enabled")
		}
	}

	err = loopback.CleanClose()
	if err != nil {
		return fmt.Errorf("failed to check if dm-verity is enabled in base image:\n%w", err)
	}

	return nil
}
