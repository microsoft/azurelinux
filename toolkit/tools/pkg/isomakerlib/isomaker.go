// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package isomakerlib

import (
	"fmt"
	"io"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"syscall"

	"github.com/cavaliercoder/go-cpio"
	"github.com/klauspost/pgzip"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

const (
	efiBootImgPathRelativeToIsoRoot = "boot/grub2/efiboot.img"
	initrdEFIBootDirectoryPath      = "boot/efi/EFI/BOOT"
	isoRootArchDependentDirPath     = "assets/isomaker/iso_root_arch-dependent_files"
	defaultImageNameBase            = "azure-linux"
)

// IsoMaker builds ISO images and populates them with packages and files required by the installer.
type IsoMaker struct {
	enableBiosBoot     bool                 // Flag deciding whether to include BIOS bootloaders or not in the generated ISO image.
	unattendedInstall  bool                 // Flag deciding if the installer should run in unattended mode.
	config             configuration.Config // Configuration for the built ISO image and its installer.
	configSubDirNumber int                  // Current number for the subdirectories storing files mentioned in the config.
	baseDirPath        string               // Base directory for config's relative paths.
	buildDirPath       string               // Path to the temporary build directory.
	efiBootImgPath     string               // Path to the efiboot.img file needed to boot the ISO installer.
	fetchedRepoDirPath string               // Path to the directory containing an RPM repository with all packages required by the ISO installer.
	initrdPath         string               // Path to ISO's initrd file.
	grubCfgPath        string               // Path to ISO's grub.cfg file. If provided, overrides the grub.cfg from the resourcesDirPath location.
	outputDirPath      string               // Path to the output ISO directory.
	releaseVersion     string               // Current Mariner release version.
	resourcesDirPath   string               // Path to the 'resources' directory.
	imageNameBase      string               // Base name of the ISO to generate (no path, and no file extension).
	imageNameTag       string               // Optional user-supplied tag appended to the generated ISO's name.

	isoMakerCleanUpTasks []func() error // List of clean-up tasks to perform at the end of the ISO generation process.
}

// NewIsoMaker returns a new ISO maker.
func NewIsoMaker(unattendedInstall bool, baseDirPath, buildDirPath, releaseVersion, resourcesDirPath, configFilePath, initrdPath, isoRepoDirPath, outputDir, imageNameTag string) (*IsoMaker, error) {
	if baseDirPath == "" {
		baseDirPath = filepath.Dir(configFilePath)
	}

	imageNameBase := strings.TrimSuffix(filepath.Base(configFilePath), ".json")

	config, err := readConfigFile(configFilePath, baseDirPath)
	if err != nil {
		return nil, err
	}
	err = verifyConfig(config, unattendedInstall)
	if err != nil {
		return nil, err
	}

	return &IsoMaker{
		enableBiosBoot:     true,
		unattendedInstall:  unattendedInstall,
		config:             config,
		baseDirPath:        baseDirPath,
		buildDirPath:       buildDirPath,
		initrdPath:         initrdPath,
		releaseVersion:     releaseVersion,
		resourcesDirPath:   resourcesDirPath,
		fetchedRepoDirPath: isoRepoDirPath,
		outputDirPath:      outputDir,
		imageNameBase:      imageNameBase,
		imageNameTag:       imageNameTag,
	}, nil
}

func NewIsoMakerWithConfig(unattendedInstall, enableBiosBoot bool, baseDirPath, buildDirPath, releaseVersion, resourcesDirPath string, config configuration.Config, initrdPath, grubCfgPath, isoRepoDirPath, outputDir, imageNameBase, imageNameTag string) (*IsoMaker, error) {

	if imageNameBase == "" {
		imageNameBase = defaultImageNameBase
	}

	err := verifyConfig(config, unattendedInstall)
	if err != nil {
		return nil, err
	}

	return &IsoMaker{
		enableBiosBoot:     enableBiosBoot,
		unattendedInstall:  unattendedInstall,
		config:             config,
		baseDirPath:        baseDirPath,
		buildDirPath:       buildDirPath,
		initrdPath:         initrdPath,
		grubCfgPath:        grubCfgPath,
		releaseVersion:     releaseVersion,
		resourcesDirPath:   resourcesDirPath,
		fetchedRepoDirPath: isoRepoDirPath,
		outputDirPath:      outputDir,
		imageNameBase:      imageNameBase,
		imageNameTag:       imageNameTag,
	}, nil
}

// Make builds the ISO image to 'buildDirPath' with the packages included in the config JSON.
func (im *IsoMaker) Make() (err error) {
	defer func() {
		cleanupErr := im.isoMakerCleanUp()
		if cleanupErr != nil {
			if err != nil {
				err = fmt.Errorf("%w\n%w", err, cleanupErr)
			} else {
				err = fmt.Errorf("%w", cleanupErr)
			}
		}
	}()

	err = im.initializePaths()
	if err != nil {
		return err
	}

	err = im.prepareWorkDirectory()
	if err != nil {
		return err
	}

	err = im.createIsoRpmsRepo()
	if err != nil {
		return err
	}

	err = im.prepareIsoBootLoaderFilesAndFolders()
	if err != nil {
		return err
	}

	err = im.buildIsoImage()
	if err != nil {
		return err
	}

	return nil
}

func (im *IsoMaker) buildIsoImage() error {
	isoImageFilePath := im.buildIsoImageFilePath()

	logger.Log.Infof("Generating ISO image under '%s'.", isoImageFilePath)

	// For detailed parameter explanation see: https://linux.die.net/man/8/mkisofs.
	// Mkisofs requires all argument paths to be relative to the input directory.
	mkisofsArgs := []string{}

	mkisofsArgs = append(mkisofsArgs,
		// General mkisofs parameters.
		"-R", "-l", "-D", "-o", isoImageFilePath)

	if im.enableBiosBoot {
		mkisofsArgs = append(mkisofsArgs,
			// BIOS bootloader, params suggested by https://wiki.syslinux.org/wiki/index.php?title=ISOLINUX.
			"-b", "isolinux/isolinux.bin", "-c", "isolinux/boot.cat", "-no-emul-boot", "-boot-load-size", "4", "-boot-info-table")
	}

	mkisofsArgs = append(mkisofsArgs,
		// UEFI bootloader.
		"-eltorito-alt-boot", "-e", efiBootImgPathRelativeToIsoRoot, "-no-emul-boot",

		// Directory to convert to an ISO.
		im.buildDirPath)

	err := shell.ExecuteLive(false /*squashErrors*/, "mkisofs", mkisofsArgs...)
	if err != nil {
		return err
	}

	return nil
}

// prepareIsoBootLoaderFilesAndFolders copies the files required by the ISO's bootloader
func (im *IsoMaker) prepareIsoBootLoaderFilesAndFolders() error {
	err := im.setUpIsoGrub2Bootloader()
	if err != nil {
		return err
	}

	err = im.createVmlinuzImage()
	if err != nil {
		return err
	}

	err = im.copyInitrd()
	if err != nil {
		return err
	}

	return nil
}

// copyInitrd copies a pre-built initrd into the isolinux folder.
func (im *IsoMaker) copyInitrd() error {
	initrdDestinationPath := filepath.Join(im.buildDirPath, "isolinux/initrd.img")

	logger.Log.Debugf("Copying initrd from '%s'.", im.initrdPath)

	err := file.Copy(im.initrdPath, initrdDestinationPath)
	if err != nil {
		return err
	}

	return nil
}

// setUpIsoGrub2BootLoader prepares an efiboot.img containing Grub2,
// which is booted in case of an UEFI boot of the ISO image.
func (im *IsoMaker) setUpIsoGrub2Bootloader() (err error) {
	const (
		blockSizeInBytes     = 1024 * 1024
		numberOfBlocksToCopy = 3
	)

	logger.Log.Info("Preparing ISO's bootloaders.")

	ddArgs := []string{
		"if=/dev/zero",                                // Zero device to read a stream of zeroed bytes from.
		fmt.Sprintf("of=%s", im.efiBootImgPath),       // Output file.
		fmt.Sprintf("bs=%d", blockSizeInBytes),        // Size of one copied block. Used together with "count".
		fmt.Sprintf("count=%d", numberOfBlocksToCopy), // Number of blocks to copy to the output file.
	}
	logger.Log.Debugf("Creating an empty '%s' file of %d bytes.", im.efiBootImgPath, blockSizeInBytes*numberOfBlocksToCopy)
	err = shell.ExecuteLive(false /*squashErrors*/, "dd", ddArgs...)
	if err != nil {
		return err
	}

	logger.Log.Debugf("Formatting '%s' as an MS-DOS filesystem.", im.efiBootImgPath)
	err = shell.ExecuteLive(false /*squashErrors*/, "mkdosfs", im.efiBootImgPath)
	if err != nil {
		return err
	}

	efiBootImgTempMountDir := filepath.Join(im.buildDirPath, "efiboot_temp")
	logger.Log.Tracef("Creating temporary mount directory '%s'.", efiBootImgTempMountDir)
	err = os.Mkdir(efiBootImgTempMountDir, os.ModePerm)
	if err != nil {
		return err
	}

	defer func() {
		logger.Log.Debugf("Removing '%s'.", efiBootImgTempMountDir)
		cleanupErr := os.RemoveAll(efiBootImgTempMountDir)
		if cleanupErr != nil {
			if err != nil {
				err = fmt.Errorf("failed to remove temporary mount directory '%s':\n%w\n%w", efiBootImgTempMountDir, err, cleanupErr)
			} else {
				err = fmt.Errorf("failed to remove temporary mount directory '%s':\n%w", efiBootImgTempMountDir, cleanupErr)
			}
		}
	}()

	mountArgs := []string{
		"-o",                   // Indicates we're passing options to "mount". Needed to mount a loop device.
		"loop",                 // Indicates we'd like to mount a loop device. We let the system choose a free /dev/loop* device.
		im.efiBootImgPath,      // Efiboot.img file we'd like to mount to act like a block-based device.
		efiBootImgTempMountDir, // Path to mount the image to.
	}
	logger.Log.Debugf("Mounting '%s' to '%s' to copy EFI modules required to boot grub2.", im.efiBootImgPath, efiBootImgTempMountDir)
	err = shell.ExecuteLive(false /*squashErrors*/, "mount", mountArgs...)
	if err != nil {
		return err
	}

	defer func() {
		logger.Log.Debugf("Unmounting '%s'.", efiBootImgTempMountDir)
		cleanupErr := syscall.Unmount(efiBootImgTempMountDir, 0)
		if cleanupErr != nil {
			if err != nil {
				err = fmt.Errorf("failed to unmount '%s':\n%w\n%w", efiBootImgTempMountDir, err, cleanupErr)
			} else {
				err = fmt.Errorf("failed to unmount '%s':\n%w", efiBootImgTempMountDir, cleanupErr)
			}
		}
	}()

	logger.Log.Debug("Copying EFI modules into efiboot.img.")
	// Copy Shim (boot<arch>64.efi) and grub2 (grub<arch>64.efi)
	if runtime.GOARCH == "arm64" {
		err = im.copyShimFromInitrd(efiBootImgTempMountDir, "bootaa64.efi", "grubaa64.efi")
		if err != nil {
			return err
		}
	} else {
		err = im.copyShimFromInitrd(efiBootImgTempMountDir, "bootx64.efi", "grubx64.efi")
		if err != nil {
			return err
		}
	}

	return nil
}

func (im *IsoMaker) copyShimFromInitrd(efiBootImgTempMountDir, bootBootloaderFile, grubBootloaderFile string) error {
	bootDirPath := filepath.Join(efiBootImgTempMountDir, "EFI", "BOOT")

	initrdBootBootloaderFilePath := filepath.Join(initrdEFIBootDirectoryPath, bootBootloaderFile)
	buildDirBootEFIFilePath := filepath.Join(bootDirPath, bootBootloaderFile)
	err := im.extractFromInitrdAndCopy(initrdBootBootloaderFilePath, buildDirBootEFIFilePath)
	if err != nil {
		return err
	}

	initrdGrubBootloaderFilePath := filepath.Join(initrdEFIBootDirectoryPath, grubBootloaderFile)
	buildDirGrubEFIFilePath := filepath.Join(bootDirPath, grubBootloaderFile)
	err = im.extractFromInitrdAndCopy(initrdGrubBootloaderFilePath, buildDirGrubEFIFilePath)
	if err != nil {
		return err
	}

	err = im.applyRufusWorkaround(bootBootloaderFile, grubBootloaderFile)
	if err != nil {
		return err
	}

	return nil
}

// Rufus ISO-to-USB converter has a limitation where it will only copy the boot<arch>64.efi binary from a given efi*.img
// archive into the standard UEFI EFI/BOOT folder instead of extracting the whole archive as per the El Torito ISO
// specification.
//
// Most distros (including ours) use a 2 stage bootloader flow (shim->grub->kernel). Since the Rufus limitation only
// copies the 1st stage to EFI/BOOT/boot<arch>64.efi, it cannot find the 2nd stage bootloader (grub<arch>64.efi) which should
// be in the same directory: EFI/BOOT/grub<arch>64.efi. This causes the USB installation to fail to boot.
//
// Rufus prioritizes the presence of an EFI folder on the ISO disk over extraction of the efi*.img archive.
// So to workaround the limitation, create an EFI folder and make a duplicate copy of the bootloader files
// in EFI/Boot so Rufus doesn't attempt to extract the efi*.img in the first place.
func (im *IsoMaker) applyRufusWorkaround(bootBootloaderFile, grubBootloaderFile string) error {
	const buildDirBootEFIDirectoryPath = "efi/boot"

	initrdBootloaderFilePath := filepath.Join(initrdEFIBootDirectoryPath, bootBootloaderFile)
	buildDirBootEFIUsbFilePath := filepath.Join(im.buildDirPath, buildDirBootEFIDirectoryPath, bootBootloaderFile)
	err := im.extractFromInitrdAndCopy(initrdBootloaderFilePath, buildDirBootEFIUsbFilePath)
	if err != nil {
		return err
	}

	initrdGrubEFIFilePath := filepath.Join(initrdEFIBootDirectoryPath, grubBootloaderFile)
	buildDirGrubEFIUsbFilePath := filepath.Join(im.buildDirPath, buildDirBootEFIDirectoryPath, grubBootloaderFile)
	err = im.extractFromInitrdAndCopy(initrdGrubEFIFilePath, buildDirGrubEFIUsbFilePath)
	if err != nil {
		return err
	}

	return nil
}

// createVmlinuzImage builds the 'vmlinuz' file containing the Linux kernel
// ran by the ISO bootloader.
func (im *IsoMaker) createVmlinuzImage() error {
	const bootKernelFile = "boot/vmlinuz"

	vmlinuzFilePath := filepath.Join(im.buildDirPath, "isolinux/vmlinuz")

	// In order to select the correct kernel for isolinux, open the initrd archive
	// and extract the vmlinuz file in it. An initrd is a gzip of a cpio archive.
	//
	err := im.extractFromInitrdAndCopy(bootKernelFile, vmlinuzFilePath)
	if err != nil {
		return err
	}

	return nil
}

// createIsoRpmsRepo initializes the RPMs repo on the ISO image
// later accessed by the ISO installer.
func (im *IsoMaker) createIsoRpmsRepo() error {
	isoRpmsRepoDirPath := filepath.Join(im.buildDirPath, "RPMS")

	logger.Log.Debugf("Creating ISO RPMs repo under '%s'.", isoRpmsRepoDirPath)

	err := os.MkdirAll(isoRpmsRepoDirPath, os.ModePerm)
	if err != nil {
		return fmt.Errorf("failed to mkdir '%s'.", isoRpmsRepoDirPath)
	}

	fetchedRepoDirContentsPath := filepath.Join(im.fetchedRepoDirPath, "*")
	err = recursiveCopyDereferencingLinks(fetchedRepoDirContentsPath, isoRpmsRepoDirPath)
	if err != nil {
		return err
	}

	return nil
}

// prepareWorkDirectory makes sure we start with a clean directory
// under "im.buildDirPath". The work directory will contain the contents of the ISO image.
func (im *IsoMaker) prepareWorkDirectory() error {
	logger.Log.Infof("Building ISO under '%s'.", im.buildDirPath)

	exists, err := file.DirExists(im.buildDirPath)
	if err != nil {
		return fmt.Errorf("failed while checking if directory '%s' exists:\n%w", im.buildDirPath, err)
	}
	if exists {
		logger.Log.Warningf("Unexpected: temporary ISO build path '%s' exists. Removing.", im.buildDirPath)
		logger.PanicOnError(os.RemoveAll(im.buildDirPath), "Failed while removing directory '%s'.", im.buildDirPath)
	}

	err = os.Mkdir(im.buildDirPath, os.ModePerm)
	if err != nil {
		return fmt.Errorf("failed while creating directory '%s':\n%w", im.buildDirPath, err)
	}

	im.deferIsoMakerCleanUp(func() error {
		logger.Log.Debugf("Removing '%s'.", im.buildDirPath)
		err := os.RemoveAll(im.buildDirPath)
		if err != nil {
			err = fmt.Errorf("failed to remove '%s':\n%w", im.buildDirPath, err)
		}
		return err
	})

	err = im.copyStaticIsoRootFiles()
	if err != nil {
		return err
	}

	err = im.copyArchitectureDependentIsoRootFiles()
	if err != nil {
		return err
	}

	err = im.copyAndRenameConfigFiles()
	if err != nil {
		return err
	}

	return nil
}

// copyStaticIsoRootFiles copies architecture-independent files from the
// Mariner repo directories.
func (im *IsoMaker) copyStaticIsoRootFiles() error {

	if im.resourcesDirPath == "" && im.grubCfgPath == "" {
		return fmt.Errorf("missing required parameters. Must specify either the resources directory or provide a grub.cfg.")
	}

	if im.resourcesDirPath != "" {
		staticIsoRootFilesPath := filepath.Join(im.resourcesDirPath, "assets/isomaker/iso_root_static_files/*")

		logger.Log.Debugf("Copying static ISO root files from '%s' to '%s'.", staticIsoRootFilesPath, im.buildDirPath)

		err := recursiveCopyDereferencingLinks(staticIsoRootFilesPath, im.buildDirPath)
		if err != nil {
			return err
		}
	}

	// im.grubCfgPath allows the user to overwrite the default grub.cfg that is
	// copied from the resource folder.
	if im.grubCfgPath != "" {
		targetGrubCfg := filepath.Join(im.buildDirPath, "boot/grub2/grub.cfg")
		targetGrubCfgDir := filepath.Dir(targetGrubCfg)
		err := os.MkdirAll(targetGrubCfgDir, os.ModePerm)
		if err != nil {
			return fmt.Errorf("failed while creating directory '%s':\n%w", targetGrubCfgDir, err)
		}

		err = file.Copy(im.grubCfgPath, targetGrubCfg)
		if err != nil {
			return err
		}
	}

	return nil
}

// copyArchitectureDependentIsoRootFiles copies the pre-built BIOS modules required
// to boot the ISO image.
func (im *IsoMaker) copyArchitectureDependentIsoRootFiles() error {
	// If the user does not want the generated ISO to have the BIOS bootloaders
	// (which are copied from the im.resourcesDirPath folder), the user can
	// either set im.resourcesDirPath to an empty string or enableBiosBoot to
	// false. Given that there is nothing else under the 'architecture
	// dependent` resource folder, if either of these two flags is set, we can
	// return immediately.
	// Note that setting resourcesDirPath to an empty string will affect other
	// functions that copy non-architecture dependent files. Setting
	// enableBiosBoot will not affect those on-architecture dependent files
	// though.
	if im.resourcesDirPath == "" || !im.enableBiosBoot {
		return nil
	}

	if im.resourcesDirPath == "" && im.enableBiosBoot {
		logger.Log.Panicf("missing required parameters. Must specify the resources directory if BIOS bootloaders are to be included.")
	}

	architectureDependentFilesDirectory := filepath.Join(im.resourcesDirPath, isoRootArchDependentDirPath, runtime.GOARCH, "*")

	logger.Log.Debugf("Copying architecture-dependent (%s) ISO root files from '%s'.", runtime.GOARCH, architectureDependentFilesDirectory)

	return recursiveCopyDereferencingLinks(architectureDependentFilesDirectory, im.buildDirPath)
}

// copyAndRenameConfigFiles takes care of copying the config JSON along with all the files
// required by the installed system.
func (im *IsoMaker) copyAndRenameConfigFiles() error {
	const configDirName = "config"

	logger.Log.Debugf("Copying the config JSON and required files to the ISO's root.")

	configFilesAbsDirPath := filepath.Join(im.buildDirPath, configDirName)
	err := os.Mkdir(configFilesAbsDirPath, os.ModePerm)
	if err != nil {
		return fmt.Errorf("failed to create ISO's config files directory under '%s':\n%w", configFilesAbsDirPath, err)
	}
	err = im.copyAndRenameAdditionalFiles(configFilesAbsDirPath)
	if err != nil {
		return err
	}
	err = im.copyAndRenamePackagesJSONs(configFilesAbsDirPath)
	if err != nil {
		return err
	}
	err = im.copyAndRenamePreInstallScripts(configFilesAbsDirPath)
	if err != nil {
		return err
	}
	err = im.copyAndRenamePostInstallScripts(configFilesAbsDirPath)
	if err != nil {
		return err
	}
	err = im.copyAndRenameFinalizeImageScripts(configFilesAbsDirPath)
	if err != nil {
		return err
	}
	err = im.copyAndRenameSSHPublicKeys(configFilesAbsDirPath)
	if err != nil {
		return err
	}
	err = im.saveConfigJSON(configFilesAbsDirPath)
	if err != nil {
		return err
	}
	return nil
}

// copyAndRenameAdditionalFiles will copy all additional files into an
// ISO directory to make them available to the installer.
// Each file gets placed in a separate directory to avoid potential name conflicts and
// the config gets updated with the new ISO paths.
func (im *IsoMaker) copyAndRenameAdditionalFiles(configFilesAbsDirPath string) error {
	const additionalFilesSubDirName = "additionalfiles"

	for i := range im.config.SystemConfigs {
		systemConfig := &im.config.SystemConfigs[i]

		absAdditionalFiles := make(map[string]configuration.FileConfigList)
		for localAbsFilePath, installedSystemFileConfigs := range systemConfig.AdditionalFiles {
			isoRelativeFilePath, err := im.copyFileToConfigRoot(configFilesAbsDirPath, additionalFilesSubDirName, localAbsFilePath)
			if err != nil {
				return err
			}
			absAdditionalFiles[isoRelativeFilePath] = installedSystemFileConfigs
		}
		systemConfig.AdditionalFiles = absAdditionalFiles
	}

	return nil
}

// copyAndRenamePackagesJSONs will copy all package list JSONs into an
// ISO directory to make them available to the installer.
// Each file gets placed in a separate directory to avoid potential name conflicts and
// the config gets updated with the new ISO paths.
func (im *IsoMaker) copyAndRenamePackagesJSONs(configFilesAbsDirPath string) error {
	const packagesSubDirName = "packages"

	for _, systemConfig := range im.config.SystemConfigs {
		for i, localPackagesAbsFilePath := range systemConfig.PackageLists {
			isoPackagesRelativeFilePath, err := im.copyFileToConfigRoot(configFilesAbsDirPath, packagesSubDirName, localPackagesAbsFilePath)
			if err != nil {
				return err
			}

			systemConfig.PackageLists[i] = isoPackagesRelativeFilePath
		}
	}

	return nil
}

// copyAndRenamePreInstallScripts will copy all pre-install scripts into an
// ISO directory to make them available to the installer.
// Each file gets placed in a separate directory to avoid potential name conflicts and
// the config gets updated with the new ISO paths.
func (im *IsoMaker) copyAndRenamePreInstallScripts(configFilesAbsDirPath string) error {
	const preInstallScriptsSubDirName = "preinstallscripts"

	for _, systemConfig := range im.config.SystemConfigs {
		for i, localScriptAbsFilePath := range systemConfig.PreInstallScripts {
			isoScriptRelativeFilePath, err := im.copyFileToConfigRoot(configFilesAbsDirPath, preInstallScriptsSubDirName, localScriptAbsFilePath.Path)
			if err != nil {
				return err
			}

			systemConfig.PreInstallScripts[i].Path = isoScriptRelativeFilePath
		}
	}

	return nil
}

// copyAndRenamePostInstallScripts will copy all post-install scripts into an
// ISO directory to make them available to the installer.
// Each file gets placed in a separate directory to avoid potential name conflicts and
// the config gets updated with the new ISO paths.
func (im *IsoMaker) copyAndRenamePostInstallScripts(configFilesAbsDirPath string) error {
	const postInstallScriptsSubDirName = "postinstallscripts"

	for _, systemConfig := range im.config.SystemConfigs {
		for i, localScriptAbsFilePath := range systemConfig.PostInstallScripts {
			isoScriptRelativeFilePath, err := im.copyFileToConfigRoot(configFilesAbsDirPath, postInstallScriptsSubDirName, localScriptAbsFilePath.Path)
			if err != nil {
				return err
			}

			systemConfig.PostInstallScripts[i].Path = isoScriptRelativeFilePath
		}
	}

	return nil
}

// copyAndRenameFinalizeImageScripts will copy all finalize-image scripts into an
// ISO directory to make them available to the installer.
// Each file gets placed in a separate directory to avoid potential name conflicts and
// the config gets updated with the new ISO paths.
func (im *IsoMaker) copyAndRenameFinalizeImageScripts(configFilesAbsDirPath string) error {
	const finalizeImageScriptsSubDirName = "finalizeimagescripts"

	for _, systemConfig := range im.config.SystemConfigs {
		for i, localScriptAbsFilePath := range systemConfig.FinalizeImageScripts {
			isoScriptRelativeFilePath, err := im.copyFileToConfigRoot(configFilesAbsDirPath, finalizeImageScriptsSubDirName, localScriptAbsFilePath.Path)
			if err != nil {
				return err
			}

			systemConfig.FinalizeImageScripts[i].Path = isoScriptRelativeFilePath
		}
	}

	return nil
}

// copyAndRenameSSHPublicKeys will copy all SSH public keys into an
// ISO directory to make them available to the installer.
// Each file gets placed in a separate directory to avoid potential name conflicts and
// the config gets updated with the new ISO paths.
func (im *IsoMaker) copyAndRenameSSHPublicKeys(configFilesAbsDirPath string) error {
	const sshPublicKeysSubDirName = "sshpublickeys"

	for _, systemConfig := range im.config.SystemConfigs {
		for _, user := range systemConfig.Users {
			for i, localSSHPublicKeyAbsPath := range user.SSHPubKeyPaths {
				isoSSHPublicKeyRelativeFilePath, err := im.copyFileToConfigRoot(configFilesAbsDirPath, sshPublicKeysSubDirName, localSSHPublicKeyAbsPath)
				if err != nil {
					return err
				}

				user.SSHPubKeyPaths[i] = isoSSHPublicKeyRelativeFilePath
			}
		}
	}

	return nil
}

// saveConfigJSON will save the modified config JSON into an
// ISO directory to make it available to the installer.
func (im *IsoMaker) saveConfigJSON(configFilesAbsDirPath string) error {
	const (
		attendedInstallConfigFileName   = "attended_config.json"
		unattendedInstallConfigFileName = "unattended_config.json"
	)

	isoConfigFileAbsPath := filepath.Join(configFilesAbsDirPath, attendedInstallConfigFileName)
	if im.unattendedInstall {
		isoConfigFileAbsPath = filepath.Join(configFilesAbsDirPath, unattendedInstallConfigFileName)
	}

	err := jsonutils.WriteJSONFile(isoConfigFileAbsPath, &im.config)
	if err != nil {
		return fmt.Errorf("failed to save config JSON to '%s':\n%w", isoConfigFileAbsPath, err)
	}
	return nil
}

// copyFileToConfigRoot copies a single file to its own, numbered subdirectory to avoid name conflicts
// and returns the relative path to the file for the sake of config updates for the installer.
func (im *IsoMaker) copyFileToConfigRoot(configFilesAbsDirPath, configFilesSubDirName, localAbsFilePath string) (string, error) {
	fileName := filepath.Base(localAbsFilePath)
	configFileSubDirRelativePath := fmt.Sprintf("%s/%d", configFilesSubDirName, im.configSubDirNumber)
	configFileSubDirAbsPath := filepath.Join(configFilesAbsDirPath, configFileSubDirRelativePath)

	err := os.MkdirAll(configFileSubDirAbsPath, os.ModePerm)
	if err != nil {
		return "", fmt.Errorf("failed to create ISO's config subdirectory '%s':\n%w", configFileSubDirAbsPath, err)
	}

	isoRelativeFilePath := filepath.Join(configFileSubDirRelativePath, fileName)
	isoAbsFilePath := filepath.Join(configFilesAbsDirPath, isoRelativeFilePath)

	logger.Log.Tracef("Copying file to ISO's config root '%s' from '%s'.", isoAbsFilePath, localAbsFilePath)

	err = file.Copy(localAbsFilePath, isoAbsFilePath)
	if err != nil {
		return "", fmt.Errorf("failed to copy file to ISO's config root '%s' from '%s':\n%w", isoAbsFilePath, localAbsFilePath, err)
	}

	im.configSubDirNumber++

	return isoRelativeFilePath, nil
}

// initializePaths initializes absolute, global directory paths used by multiple other functions.
func (im *IsoMaker) initializePaths() error {
	var err error
	im.buildDirPath, err = filepath.Abs(im.buildDirPath)
	if err != nil {
		return fmt.Errorf("failed while retrieving absolute path from source root path: '%s':\n%w", im.buildDirPath, err)
	}

	im.efiBootImgPath = filepath.Join(im.buildDirPath, efiBootImgPathRelativeToIsoRoot)

	return nil
}

// buildIsoImageFilePath gets the output ISO file path from the config JSON file name
// and the image build environment.
func (im *IsoMaker) buildIsoImageFilePath() string {
	isoImageFileNameSuffix := ""
	if im.releaseVersion != "" || im.imageNameTag != "" {
		isoImageFileNameSuffix = fmt.Sprintf("-%v%v", im.releaseVersion, im.imageNameTag)
	}
	isoImageFileName := fmt.Sprintf("%v%v.iso", im.imageNameBase, isoImageFileNameSuffix)

	return filepath.Join(im.outputDirPath, isoImageFileName)
}

// deferIsoMakerCleanUp accepts clean-up tasks to be ran when the entire
// build process has finished, NOT at the end of the current scope.
func (im *IsoMaker) deferIsoMakerCleanUp(cleanUpTask func() error) {
	im.isoMakerCleanUpTasks = append(im.isoMakerCleanUpTasks, cleanUpTask)
}

// isoMakerCleanUp runs all clean-up tasks scheduled through "deferIsoMakerCleanUp".
// Tasks are ran in reverse order to how they were scheduled.
func (im *IsoMaker) isoMakerCleanUp() (err error) {
	// We defer again to run the tasks in the correct order AND so that a potential
	// panic from one of these doesn't prevent other ones from running.
	for _, cleanUpTask := range im.isoMakerCleanUpTasks {
		defer func() {
			cleanupErr := cleanUpTask()
			if cleanupErr != nil {
				if err != nil {
					err = fmt.Errorf("%w\n%w", err, cleanupErr)
				} else {
					err = fmt.Errorf("%w", cleanupErr)
				}
			}
		}()
	}
	return err
}

func readConfigFile(configFilePath, baseDirPath string) (configuration.Config, error) {
	config, err := configuration.LoadWithAbsolutePaths(configFilePath, baseDirPath)
	if err != nil {
		return configuration.Config{}, fmt.Errorf("failed while reading config file from '%s' with base directory '%s':\n%w", configFilePath, baseDirPath, err)
	}
	return config, nil
}

func verifyConfig(config configuration.Config, unattendedInstall bool) error {

	// Set IsIsoInstall to true
	for id := range config.SystemConfigs {
		config.SystemConfigs[id].IsIsoInstall = true
	}

	if unattendedInstall && (len(config.SystemConfigs) > 1) && !config.DefaultSystemConfig.IsDefault {
		return fmt.Errorf("for unattended installation with more than one system configuration present you must select a default one with the [IsDefault] field.")
	}
	return nil
}

// recursiveCopyDereferencingLinks simulates the behavior of "cp -r -L".
func recursiveCopyDereferencingLinks(source string, target string) error {
	err := os.MkdirAll(target, os.ModePerm)
	if err != nil {
		return err
	}

	sourceToTarget := make(map[string]string)

	if filepath.Base(source) == "*" {
		filesToCopy, err := filepath.Glob(source)
		if err != nil {
			return err
		}
		for _, file := range filesToCopy {
			sourceToTarget[file] = target
		}
	} else {
		sourceToTarget[source] = target
	}

	for sourcePath, targetPath := range sourceToTarget {
		err := shell.ExecuteLive(false /*squashErrors*/, "cp", "-r", "-L", sourcePath, targetPath)
		if err != nil {
			return err
		}
	}

	return nil
}

func (im *IsoMaker) extractFromInitrdAndCopy(srcFileName, destFilePath string) error {
	// Setup a series of io readers: initrd file -> parallelized gzip -> cpio

	logger.Log.Debugf("Searching for (%s) in initrd (%s) and copying to (%s)", srcFileName, im.initrdPath, destFilePath)

	initrdFile, err := os.Open(im.initrdPath)
	if err != nil {
		return err
	}
	defer initrdFile.Close()

	gzipReader, err := pgzip.NewReader(initrdFile)
	if err != nil {
		return err
	}
	cpioReader := cpio.NewReader(gzipReader)

	for {
		// Search through the headers until the source file is found
		var hdr *cpio.Header
		hdr, err = cpioReader.Next()
		if err == io.EOF {
			return fmt.Errorf("did not find (%s) in initrd (%s)", srcFileName, im.initrdPath)
		}
		if err != nil {
			return err
		}

		if strings.HasPrefix(hdr.Name, srcFileName) {
			logger.Log.Debugf("Found source file (%s) in initrd", srcFileName)
			// Source file found, copy it to destination
			err = os.MkdirAll(filepath.Dir(destFilePath), os.ModePerm)
			if err != nil {
				return err
			}

			dstFile, err := os.Create(destFilePath)
			if err != nil {
				return err
			}
			defer dstFile.Close()

			logger.Log.Debugf("Copying (%s) to (%s)", srcFileName, destFilePath)
			_, err = io.Copy(dstFile, cpioReader)
			if err != nil {
				return err
			}
			break
		}
	}
	return nil
}
