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
	"golang.org/x/sys/unix"
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

	diskFreeWarnThresholdBytes   = 500 * diskutils.MiB
	diskFreeWarnThresholdPercent = 0.05
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
	inputIsIso       bool

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
	outputIsIso           bool
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
	ic.inputImageFormat = strings.TrimLeft(filepath.Ext(inputImageFile), ".")
	ic.inputIsIso = ic.inputImageFormat == ImageFormatIso

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
	ic.outputIsIso = ic.outputImageFormat == ImageFormatIso
	ic.outputImageFile = outputImageFile
	ic.outputImageBase = strings.TrimSuffix(filepath.Base(outputImageFile), filepath.Ext(outputImageFile))
	ic.outputImageDir = filepath.Dir(outputImageFile)

	if ic.outputImageFormat != "" && !ic.outputIsIso {
		ic.qemuOutputImageFormat, err = toQemuImageFormat(ic.outputImageFormat)
		if err != nil {
			return nil, err
		}
	}

	if ic.inputIsIso {
		// When the input is an iso image, there's only one file system: the
		// suqash file system and it has no empty space since it's a read-only
		// file system. So, shrinking it does not make sense.
		if ic.enableShrinkFilesystems {
			return nil, fmt.Errorf("shrinking file systems is not supported when the input image is an iso image")
		}

		// While splitting out the partition for an input iso can mean write
		// the squash file system out to a raw image, we are choosing to
		// not implement this until there is a need.
		if ic.outputSplitPartitionsFormat != "" {
			return nil, fmt.Errorf("extracting partitions is not supported when the input image is an iso image")
		}

		// While re-creating a disk image from the iso is technically possible,
		// we are choosing to not implement it until there is a need.
		if !ic.outputIsIso {
			return nil, fmt.Errorf("generating a non-iso image from an iso image is not supported")
		}

		// While defining a storage configuration can work when the input image is
		// an iso, there is no obvious point of moving content between partitions
		// where all partitions get collapsed into the squashfs at the end.
		if config.Storage != nil {
			return nil, fmt.Errorf("cannot customize storage when the input is an iso")
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
	err := file.RemoveFileIfExists(ic.rawImageFile)
	if err != nil {
		return err
	}

	return nil
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

	inputIsoArtifacts, err := convertInputImageToWriteableFormat(imageCustomizerParameters)
	if err != nil {
		return fmt.Errorf("failed to convert input image to a raw image:\n%w", err)
	}
	defer func() {
		if inputIsoArtifacts != nil {
			cleanupErr := inputIsoArtifacts.cleanUp()
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

	err = convertWriteableFormatToOutputImage(imageCustomizerParameters, inputIsoArtifacts)
	if err != nil {
		return fmt.Errorf("failed to convert customized raw image to output format:\n%w", err)
	}

	logger.Log.Infof("Success!")

	return nil
}

func convertInputImageToWriteableFormat(ic *ImageCustomizerParameters) (*LiveOSIsoBuilder, error) {
	logger.Log.Infof("Converting input image to a writeable format")

	if ic.inputIsIso {
		inputIsoArtifacts, err := createIsoBuilderFromIsoImage(ic.buildDir, ic.buildDirAbs, ic.inputImageFile)
		if err != nil {
			return nil, fmt.Errorf("failed to load input iso artifacts:\n%w", err)
		}

		// If the input is a LiveOS iso and there are OS customizations
		// defined, we create a writeable disk image so that mic can modify
		// it. If no OS customizations are defined, we can skip this step and
		// just re-use the existing squashfs.
		if ic.customizeOSPartitions {
			err = inputIsoArtifacts.createWriteableImageFromSquashfs(ic.buildDir, ic.rawImageFile)
			if err != nil {
				return nil, fmt.Errorf("failed to create writeable image:\n%w", err)
			}
		}

		return inputIsoArtifacts, nil
	} else {
		logger.Log.Infof("Creating raw base image: %s", ic.rawImageFile)
		err := shell.ExecuteLiveWithErr(1, "qemu-img", "convert", "-O", "raw", ic.inputImageFile, ic.rawImageFile)
		if err != nil {
			return nil, fmt.Errorf("failed to convert image file to raw format:\n%w", err)
		}

		return nil, nil
	}
}

func customizeOSContents(ic *ImageCustomizerParameters) error {
	// If there are OS customizations, then we proceed as usual.
	// If there are no OS customizations, and the input is an iso, we just
	// return because this function is mainly about OS customizations.
	// This function also supports shrinking/exporting partitions. While
	// we could support those functions for input isos, we are choosing to
	// not support them until there is an actual need/a future time.
	// We explicitly inform the user of the lack of support earlier during
	// mic parameter validation (see createImageCustomizerParameters()).
	if !ic.customizeOSPartitions && ic.inputIsIso {
		return nil
	}

	// The code beyond this point assumes the OS object is always present. To
	// change the code to check before every usage whether the OS object is
	// present or not will lead to a messy mix of if statements that do not
	// serve the readibility of the code. A simpler solution is to instantiate
	// a default imagecustomizerapi.OS object if the passed in one is absent.
	// Then the code afterwards knows how to handle the default values
	// correctly, and thus it eliminates the need for many if statements.
	if ic.config.OS == nil {
		ic.config.OS = &imagecustomizerapi.OS{}
	}

	// Check if the partition is using DM_verity_hash file system type.
	// The presence of this type indicates that dm-verity has been enabled on the base image. If dm-verity is not enabled,
	// the verity hash device should not be assigned this type. We do not support customization on verity enabled base
	// images at this time because such modifications would compromise the integrity and security mechanisms enforced by dm-verity.
	err := checkDmVerityEnabled(ic.rawImageFile)
	if err != nil {
		return err
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

func convertWriteableFormatToOutputImage(ic *ImageCustomizerParameters, inputIsoArtifacts *LiveOSIsoBuilder) error {
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
		if ic.customizeOSPartitions || inputIsoArtifacts == nil {
			err := createLiveOSIsoImage(ic.buildDir, ic.configPath, inputIsoArtifacts, ic.config.Iso, ic.rawImageFile, ic.outputImageDir, ic.outputImageBase)
			if err != nil {
				return fmt.Errorf("failed to create LiveOS iso image:\n%w", err)
			}
		} else {
			err := inputIsoArtifacts.createImageFromUnchangedOS(ic.configPath, ic.config.Iso, ic.outputImageDir, ic.outputImageBase)
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

	// Out of disk space errors can be difficult to diagnose.
	// So, warn about any partitions with low free space.
	warnOnLowFreeSpace(buildDir, imageConnection)

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

func warnOnLowFreeSpace(buildDir string, imageConnection *ImageConnection) {
	logger.Log.Debugf("Checking disk space")

	imageChroot := imageConnection.Chroot()

	// Check all of the customized OS's partitions.
	for _, mountPoint := range getNonSpecialChrootMountPoints(imageConnection.Chroot()) {
		fullPath := filepath.Join(imageChroot.RootDir(), mountPoint.GetTarget())
		warnOnPathLowFreeSpace(fullPath, mountPoint.GetTarget())
	}

	// Check the partition that contains the build directory.
	warnOnPathLowFreeSpace(buildDir, "host:"+buildDir)
}

func warnOnPathLowFreeSpace(path string, name string) {
	var stat unix.Statfs_t
	err := unix.Statfs(path, &stat)
	if err != nil {
		logger.Log.Warnf("Failed to read disk space usage (%s)", path)
		return
	}

	totalBytes := stat.Frsize * int64(stat.Blocks)
	freeBytes := stat.Frsize * int64(stat.Bfree)
	usedBytes := totalBytes - freeBytes
	percentUsed := float64(usedBytes) / float64(totalBytes)
	percentFree := 1 - percentUsed

	logger.Log.Debugf("Disk space %.f%% (%s) on (%s)", percentUsed*100,
		humanReadableDiskSizeRatio(usedBytes, totalBytes), name)

	if percentFree <= diskFreeWarnThresholdPercent && freeBytes <= diskFreeWarnThresholdBytes {
		logger.Log.Warnf("Low free disk space %.f%% (%s) on (%s)", percentFree*100,
			humanReadableDiskSize(freeBytes), name)
	}
}

func humanReadableDiskSize(size int64) string {
	unitSize, unitName := humanReadableUnitSizeAndName(size)
	return fmt.Sprintf("%.f %s", float64(size)/float64(unitSize), unitName)
}

func humanReadableDiskSizeRatio(size int64, total int64) string {
	unitSize, unitName := humanReadableUnitSizeAndName(total)
	return fmt.Sprintf("%.f/%.f %s", float64(size)/float64(unitSize), float64(total)/float64(unitSize), unitName)
}

func humanReadableUnitSizeAndName(size int64) (int64, string) {
	switch {
	case size >= diskutils.TiB:
		return diskutils.TiB, "TiB"

	case size >= diskutils.GiB:
		return diskutils.GiB, "GiB"

	case size >= diskutils.MiB:
		return diskutils.MiB, "MiB"

	case size >= diskutils.KiB:
		return diskutils.KiB, "KiB"

	default:
		return 1, "B"
	}
}
