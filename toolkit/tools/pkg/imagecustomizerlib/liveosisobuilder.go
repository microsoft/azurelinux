// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safeloopback"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safemount"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/isomakerlib"
	"golang.org/x/sys/unix"
)

const (
	bootx64Binary         = "bootx64.efi"
	grubx64Binary         = "grubx64.efi"
	grubx64NoPrefixBinary = "grubx64-noprefix.efi"

	grubCfg = "grub.cfg"

	searchCommandTemplate = "search --label %s --set root"
	rootValueTemplate     = "live:LABEL=%s"

	isoBootDir    = "boot"
	initrdImage   = "initrd.img"
	vmLinuzPrefix = "vmlinuz-"
	isoInitrdPath = "/boot/" + initrdImage
	isoKernelPath = "/boot/vmlinuz"

	// kernel arguments template
	kernelArgsTemplate = " rd.shell rd.live.image rd.live.dir=%s rd.live.squashimg=%s rd.live.overlay=1 rd.live.overlay.nouserconfirmprompt %s"
	liveOSDir          = "liveos"
	liveOSImage        = "rootfs.img"

	dracutConfig = `add_dracutmodules+=" dmsquash-live "
add_drivers+=" overlay "
`
	// the total size of a collection of files is multiplied by the
	// expansionSafetyFactor to estimate a disk size sufficient to hold those
	// files.
	expansionSafetyFactor = 1.5
)

type IsoWorkingDirs struct {
	// 'isoBuildDir' is where intermediate files will be placed during the
	// build.
	isoBuildDir string
	// 'isoArtifactsDir' is where extracted and generated files will be placed
	// during the build.
	isoArtifactsDir string
	// 'isomakerBuildDir' will be deleted/re-created by IsoMaker before it
	// proceeds. It needs to be different from `isoBuildDir`.
	isomakerBuildDir string
}

// `IsoArtifacts` holds the extracted/generated artifacts necessary to build
// a LiveOS ISO image.
type IsoArtifacts struct {
	kernelVersion     string
	bootx64EfiPath    string
	grubx64EfiPath    string
	grubCfgPath       string
	vmlinuzPath       string
	initrdImagePath   string
	squashfsImagePath string
	additionalFiles   map[string]string // local-build-path -> iso-media-path
}

type LiveOSIsoBuilder struct {
	workingDirs IsoWorkingDirs
	artifacts   IsoArtifacts
	cleanupDirs []string
}

func (b *LiveOSIsoBuilder) addCleanupDir(dirName string) {
	b.cleanupDirs = append(b.cleanupDirs, dirName)
}

func (b *LiveOSIsoBuilder) cleanUp() error {
	var err error
	for i := len(b.cleanupDirs) - 1; i >= 0; i-- {
		cleanupErr := os.RemoveAll(b.cleanupDirs[i])
		if cleanupErr != nil {
			if err != nil {
				err = fmt.Errorf("%w:\nfailed to remove (%s): %w", err, b.cleanupDirs[i], cleanupErr)
			} else {
				err = fmt.Errorf("failed to clean-up (%s): %w", b.cleanupDirs[i], cleanupErr)
			}
		}
	}
	return err
}

// populateWriteableRootfsDir
//
//	copies the contents of the rootfs partition unto the build machine.
//
// input:
//   - 'sourceDir'
//     path to full image mount root.
//   - 'writeableRootfsDir'
//     path to the folder where the contents of the rootfsDevice will be
//     copied to.
//
// output:
//   - writeableRootfsDir will hold the contents of sourceDir.
func (b *LiveOSIsoBuilder) populateWriteableRootfsDir(sourceDir, writeableRootfsDir string) error {

	logger.Log.Debugf("Creating writeable rootfs")

	err := os.MkdirAll(writeableRootfsDir, os.ModePerm)
	if err != nil {
		return fmt.Errorf("failed to create folder %s:\n%w", writeableRootfsDir, err)
	}

	err = copyPartitionFiles(sourceDir+"/.", writeableRootfsDir)
	if err != nil {
		return fmt.Errorf("failed to copy rootfs contents to a writeable folder (%s):\n%w", writeableRootfsDir, err)
	}

	return nil
}

// stageIsoMakerInitrdArtifacts
//
//	IsoMaker looks for the vmlinuz/bootloader files inside the initrd image
//	file under specific directory structure.
//	This function stages those artifacts and places them under the same
//	directory structure expected by IsoMaker.
//	Later,  we run 'dracut' which takes this directory structure and embeds
//	it into the initrd image.
//	Finaly, the IsoMaker will read the initrd image and find the artifacts
//	it needs to copy to the final iso media.
//	Something to consider in the future: change IsoMaker so that it can pick
//	those artifacts from the build machine directly.
//
// inputs:
//   - 'writeableRootfsDir':
//     path to an existing folder holding the contents of the rootfs.
//   - 'isoMakerArtifactsStagingDir'
//     path to a folder where the extracted artifacts will stored under.
//
// outputs:
//
//	the artifacts will be stored in 'isoMakerArtifactsStagingDir'.
func (b *LiveOSIsoBuilder) stageIsoMakerInitrdArtifacts(writeableRootfsDir, isoMakerArtifactsStagingDir string) error {

	logger.Log.Debugf("Staging isomaker artifacts into writeable image")

	targetBootloadersInChroot := filepath.Join(isoMakerArtifactsStagingDir, "/efi/EFI/BOOT")
	targetBootloadersDir := filepath.Join(writeableRootfsDir, targetBootloadersInChroot)

	err := os.MkdirAll(targetBootloadersDir, os.ModePerm)
	if err != nil {
		return fmt.Errorf("failed to create %s\n%w", targetBootloadersDir, err)
	}

	sourceBoot64EfiPath := b.artifacts.bootx64EfiPath
	targetBoot64EfiPath := filepath.Join(targetBootloadersDir, bootx64Binary)
	err = file.Copy(sourceBoot64EfiPath, targetBoot64EfiPath)
	if err != nil {
		return fmt.Errorf("failed to stage bootloader file (bootx64.efi):\n%w", err)
	}

	sourceGrub64EfiPath := b.artifacts.grubx64EfiPath
	targetGrub64EfiPath := filepath.Join(targetBootloadersDir, grubx64Binary)
	err = file.Copy(sourceGrub64EfiPath, targetGrub64EfiPath)
	if err != nil {
		return fmt.Errorf("failed to stage bootloader file (grubx64.efi):\n%w", err)
	}

	targetVmlinuzLocalDir := filepath.Join(writeableRootfsDir, isoMakerArtifactsStagingDir)

	sourceVmlinuzPath := b.artifacts.vmlinuzPath
	targetVmlinuzPath := filepath.Join(targetVmlinuzLocalDir, "vmlinuz")
	err = file.Copy(sourceVmlinuzPath, targetVmlinuzPath)
	if err != nil {
		return fmt.Errorf("failed to stage vmlinuz:\n%w", err)
	}

	return nil
}

// prepareRootfsForDracut
//
//	ensures two things:
//	- initrd image build time configuration is in place.
//	- rootfs (squashfs) image contents are compatible with our LiveOS initrd
//	  boot flow.
//	note that the same rootfs is used for both:
//	(1) creating the initrd image and
//	(2) creating the squashfs image.
//
// inputs:
//   - writeableRootfsDir:
//     root directory of existing rootfs content to modify.
//
// outputs:
// - all changes will be applied to the specified rootfs directory in the input.
func (b *LiveOSIsoBuilder) prepareRootfsForDracut(writeableRootfsDir string) error {

	logger.Log.Debugf("Preparing writeable image for dracut")

	fstabFile := filepath.Join(writeableRootfsDir, "/etc/fstab")
	logger.Log.Debugf("Deleting fstab from %s", fstabFile)
	err := os.Remove(fstabFile)
	if err != nil {
		return fmt.Errorf("failed to delete fstab:\n%w", err)
	}

	targetConfigFile := filepath.Join(writeableRootfsDir, "/etc/dracut.conf.d/20-live-cd.conf")
	err = os.WriteFile(targetConfigFile, []byte(dracutConfig), 0o644)
	if err != nil {
		return fmt.Errorf("failed to create %s:\n%w", targetConfigFile, err)
	}

	return nil
}

func (b *LiveOSIsoBuilder) updateGrubCfg(grubCfgFileName string, extraCommandLine string) error {

	inputContentString, err := file.Read(grubCfgFileName)
	if err != nil {
		return err
	}

	grubMkconfigEnabled := isGrubMkconfigConfig(inputContentString)
	if grubMkconfigEnabled {
		return fmt.Errorf("grub-mkconfig enabled images not yet supported for ISO output")
	}

	searchCommand := fmt.Sprintf(searchCommandTemplate, isomakerlib.DefaultVolumeId)
	rootValue := fmt.Sprintf(rootValueTemplate, isomakerlib.DefaultVolumeId)

	inputContentString, err = replaceSearchCommand(inputContentString, searchCommand)
	if err != nil {
		return fmt.Errorf("failed to update the search command in the iso grub.cfg:\n%w", err)
	}

	inputContentString, oldLinuxPath, err := setLinuxPath(inputContentString, isoKernelPath)
	if err != nil {
		return fmt.Errorf("failed to update the kernel file path in the iso grub.cfg:\n%w", err)
	}

	inputContentString, err = replaceToken(inputContentString, oldLinuxPath, isoKernelPath)
	if err != nil {
		return fmt.Errorf("failed to update all the kernel file path occurances in the iso grub.cfg:\n%w", err)
	}

	inputContentString, oldInitrdPath, err := setInitrdPath(inputContentString, isoInitrdPath)
	if err != nil {
		return fmt.Errorf("failed to update the initrd file path in the iso grub.cfg:\n%w", err)
	}

	inputContentString, err = replaceToken(inputContentString, oldInitrdPath, isoInitrdPath)
	if err != nil {
		return fmt.Errorf("failed to update all the initrd file path occurances in the iso grub.cfg:\n%w", err)
	}

	inputContentString, _, err = replaceKernelCommandLineArgValue(inputContentString, "root", rootValue)
	if err != nil {
		return fmt.Errorf("failed to update the root kernel argument in the iso grub.cfg:\n%w", err)
	}

	inputContentString, err = updateSELinuxCommandLineHelper(inputContentString, imagecustomizerapi.SELinuxModeDisabled)
	if err != nil {
		return fmt.Errorf("failed to set SELinux mode:\n%w", err)
	}

	liveosKernelArgs := fmt.Sprintf(kernelArgsTemplate, liveOSDir, liveOSImage, extraCommandLine)

	inputContentString, err = appendKernelCommandLineArgs(inputContentString, liveosKernelArgs)
	if err != nil {
		return fmt.Errorf("failed to update the kernel arguments with the LiveOS configuration and user configuration in the iso grub.cfg:\n%w", err)
	}

	err = os.WriteFile(grubCfgFileName, []byte(inputContentString), 0o644)
	if err != nil {
		return fmt.Errorf("failed to write grub.cfg:\n%w", err)
	}

	return nil
}

// containsGrubNoPrefix
//
// given a list of file path, this function returns true if one of the files
// is named grubx64-noprefix.efi; otherwise it returns false.
//
// inputs:
//   - filePaths:
//     A list of file paths.
//
// outputs:
//   - boolean
//     true if grubx64-noprefix.efi is one of the files.
//     false otherwise.
func containsGrubNoPrefix(filePaths []string) bool {
	for _, filePath := range filePaths {
		if filepath.Base(filePath) == grubx64NoPrefixBinary {
			return true
		}
	}
	return false
}

// extractBootDirFiles
//
// given a rootfs, this function:
// - extracts the files under the /boot folder
//
// inputs:
//   - writeableRootfsDir:
//     A writeable folder where the rootfs content is.
//
// outputs:
//   - copied files and the following are populated:
//     b.artifacts.bootx64EfiPath
//     b.artifacts.grubx64EfiPath
//     b.artifacts.vmlinuzPath
//     b.artifacts.additionalFiles
func (b *LiveOSIsoBuilder) extractBootDirFiles(writeableRootfsDir string) error {

	b.artifacts.additionalFiles = make(map[string]string)

	// the following files will be re-created - no need to copy them only to
	// have them overwritten.
	var exclusions []*regexp.Regexp
	//
	// We will generate a new initrd later. So, we do not copy the initrd.img
	// that comes in the input full disk image.
	//
	exclusions = append(exclusions, regexp.MustCompile(`/boot/initrd\.img.*`))
	//
	// On full disk images (generated by Mariner toolkit), there are two
	// grub.cfg files:
	// - <boot partition>/boot/grub2/grub.cfg:
	//   - mounted at /boot/efi/boot/grub2/grub.cfg.
	//   - empty except for redirection to the other grub.cfg.
	// - <rootfs partition>/boot/grub2/grub.cfg:
	//   - mounted at /boot/grub2/grub.cfg
	//   - has the actual grub configuration.
	//
	// When creating an iso image out of a full disk image, we do not need the
	// redirection mechanism, and hence we can do with only the full grub.cfg.
	//
	// To avoid confusion, we do not copy the redirection grub.cfg to the iso
	// media.
	//
	exclusions = append(exclusions, regexp.MustCompile(`/boot/efi/boot/grub2/grub\.cfg`))

	bootFolderFilePaths, err := file.EnumerateDirFiles(filepath.Join(writeableRootfsDir, "/boot"))
	if err != nil {
		return fmt.Errorf("failed to scan /boot folder:\n%w", err)
	}

	usingGrubNoPrefix := containsGrubNoPrefix(bootFolderFilePaths)

	for _, sourcePath := range bootFolderFilePaths {

		for _, exclusion := range exclusions {
			match := exclusion.FindStringIndex(sourcePath)
			if match != nil {
				logger.Log.Debugf("Not copying %s. File is either unnecessary or will be re-generated.", sourcePath)
				continue
			}
		}

		targetPath := strings.Replace(sourcePath, writeableRootfsDir, b.workingDirs.isoArtifactsDir, -1)
		targetFileName := filepath.Base(targetPath)

		scheduleAdditionalFile := true

		switch targetFileName {
		case bootx64Binary:
			b.artifacts.bootx64EfiPath = targetPath
			// isomaker will extract this from initrd and copy it to include it
			// in the iso media - so no need to schedule it as an additional
			// file.
			scheduleAdditionalFile = false
		case grubx64Binary, grubx64NoPrefixBinary:
			b.artifacts.grubx64EfiPath = targetPath
			// isomaker will extract this from initrd and copy it to include it
			// in the iso media - so no need to schedule it as an additional
			// file.
			scheduleAdditionalFile = false
		case grubCfg:
			if usingGrubNoPrefix {
				// When using the grubx64-noprefix.efi, the 'prefix' grub
				// variable is set to an empty string. When 'prefix' is an
				// empty string, and grubx64-noprefix.efi is run from an iso
				// media, the bootloader defaults to looking for grub.cfg at
				// <boot-media>/EFI/BOOT/grub.cfg.
				// So, below, we ensure that grub.cfg file will be placed where
				// grubx64-nopreifx.efi will be looking for it.
				//
				// Note that this grub.cfg is the only file that needs to be
				// copied to that EFI/BOOT location. The rest of the files (like
				// grubenv, etc) can be left under /boot as usual. This is
				// because grub.cfg still defines 'bootprefix' to be /boot.
				// So, once grubx64.efi loads EFI/BOOT/grub.cfg, it will set
				// bootprefix to the usual location boot/grub2 and will proceed
				// as usual from there.
				targetPath = filepath.Join(b.workingDirs.isoArtifactsDir, "EFI/BOOT", grubCfg)
			}
			b.artifacts.grubCfgPath = targetPath
			// grub.cfg is passed as a parameter to isomaker.
			scheduleAdditionalFile = false
		}
		if strings.HasPrefix(targetFileName, vmLinuzPrefix) {
			targetPath = filepath.Join(filepath.Dir(targetPath), "vmlinuz")
			b.artifacts.vmlinuzPath = targetPath
			// isomaker will extract this from initrd and copy it to include it
			// in the iso media - so no need to schedule it as an additional
			// file.
			scheduleAdditionalFile = false
		}

		err = file.NewFileCopyBuilder(sourcePath, targetPath).
			SetNoDereference().
			Run()
		if err != nil {
			return fmt.Errorf("failed to extract files from under the boot folder:\n%w", err)
		}

		if scheduleAdditionalFile {
			b.artifacts.additionalFiles[targetPath] = strings.TrimPrefix(targetPath, b.workingDirs.isoArtifactsDir)
		}
	}

	if b.artifacts.bootx64EfiPath == "" {
		return fmt.Errorf("failed to find the boot efi file (%s):\n"+
			"this file is provided by the (shim) package",
			bootx64Binary)
	}

	if b.artifacts.grubx64EfiPath == "" {
		return fmt.Errorf("failed to find the grub efi file (%s or %s):\n"+
			"this file is provided by either the (grub2-efi-binary) or the (grub2-efi-binary-noprefix) package",
			grubx64Binary, grubx64NoPrefixBinary)
	}

	return nil
}

// findKernelVersion
//
// given a rootfs, this function:
// - extracts the kernel version, and the files under the boot folder.
//
// inputs:
//   - writeableRootfsDir:
//     A writeable folder where the rootfs content is.
//
// outputs:
//   - the following is populated:
//     b.artifacts.kernelVersion
func (b *LiveOSIsoBuilder) findKernelVersion(writeableRootfsDir string) error {
	const kernelModulesDir = "/usr/lib/modules"

	kernelParentPath := filepath.Join(writeableRootfsDir, kernelModulesDir)
	kernelDirs, err := os.ReadDir(kernelParentPath)
	if err != nil {
		return fmt.Errorf("failed to enumerate kernels under (%s):\n%w", kernelParentPath, err)
	}

	// Filter out directories that are empty.
	// Some versions of Azure Linux 2.0 don't cleanup properly when the kernel package is uninstalled.
	filteredKernelDirs := []fs.DirEntry(nil)
	for _, kernelDir := range kernelDirs {
		kernelPath := filepath.Join(kernelParentPath, kernelDir.Name())
		empty, err := file.IsDirEmpty(kernelPath)
		if err != nil {
			return err
		}

		if !empty {
			filteredKernelDirs = append(filteredKernelDirs, kernelDir)
		}
	}

	if len(filteredKernelDirs) == 0 {
		return fmt.Errorf("did not find any kernels installed under (%s)", kernelModulesDir)
	}
	if len(filteredKernelDirs) > 1 {
		return fmt.Errorf("unsupported scenario: found more than one kernel under (%s)", kernelModulesDir)
	}
	b.artifacts.kernelVersion = filteredKernelDirs[0].Name()
	logger.Log.Debugf("Found installed kernel version (%s)", b.artifacts.kernelVersion)
	return nil
}

// prepareLiveOSDir
//
//	given a rootfs, this function:
//	- extracts the kernel version, and the files under the boot folder.
//	- stages bootloaders and vmlinuz to a specific folder structure.
//	This folder structure is to be included later in the initrd image when
//	it gets generated. IsoMaker extracts those artifacts from the initrd
//	image file and uses them.
//	-prepares the rootfs to run dracut (dracut will generate the initrd later).
//	- creates the squashfs.
//
// inputs:
//   - writeableRootfsDir:
//     A writeable folder where the rootfs content is.
//   - isoMakerArtifactsStagingDir:
//     The folder where the artifacts needed by isoMaker will be staged before
//     'dracut' is run. 'dracut' will include this folder as-is and place it in
//     the initrd image.
//   - 'extraCommandLine':
//     extra kernel command line arguments to add to grub.
//
// outputs
//   - customized writeableRootfsDir (new files, deleted files, etc)
//   - extracted artifacts
func (b *LiveOSIsoBuilder) prepareLiveOSDir(writeableRootfsDir string, isoMakerArtifactsStagingDir string, extraCommandLine string) error {

	logger.Log.Debugf("Creating LiveOS squashfs image")

	err := b.findKernelVersion(writeableRootfsDir)
	if err != nil {
		return err
	}

	err = b.extractBootDirFiles(writeableRootfsDir)
	if err != nil {
		return err
	}

	err = b.updateGrubCfg(b.artifacts.grubCfgPath, extraCommandLine)
	if err != nil {
		return fmt.Errorf("failed to update grub.cfg:\n%w", err)
	}

	err = b.stageIsoMakerInitrdArtifacts(writeableRootfsDir, isoMakerArtifactsStagingDir)
	if err != nil {
		return fmt.Errorf("failed to stage isomaker initrd artifacts:\n%w", err)
	}

	err = b.prepareRootfsForDracut(writeableRootfsDir)
	if err != nil {
		return fmt.Errorf("failed to prepare rootfs for dracut:\n%w", err)
	}

	return nil
}

// createSquashfsImage
//
//	creates a squashfs image based on a given folder.
//
// inputs:
//   - writeableRootfsDir:
//     directory tree root holding the contents to be placed in the squashfs image.
//
// output
//   - creates a squashfs image and stores its path in
//     b.artifacts.squashfsImagePath
func (b *LiveOSIsoBuilder) createSquashfsImage(writeableRootfsDir string) error {

	logger.Log.Debugf("Creating squashfs of %s", writeableRootfsDir)

	squashfsImagePath := filepath.Join(b.workingDirs.isoArtifactsDir, liveOSImage)

	exists, err := file.PathExists(squashfsImagePath)
	if err == nil && exists {
		err = os.Remove(squashfsImagePath)
		if err != nil {
			return fmt.Errorf("failed to delete existing squashfs image (%s):\n%w", squashfsImagePath, err)
		}
	}

	mksquashfsParams := []string{writeableRootfsDir, squashfsImagePath}
	err = shell.ExecuteLive(false, "mksquashfs", mksquashfsParams...)
	if err != nil {
		return fmt.Errorf("failed to create squashfs:\n%w", err)
	}

	b.artifacts.squashfsImagePath = squashfsImagePath

	return nil
}

// generateInitrdImage
//
//	runs dracut against rootfs to create an initrd image file.
//
// inputs:
//   - rootfsSourceDir:
//     local folder (on the build machine) of the rootfs to be used when
//     creating the initrd image.
//   - artifactsSourceDir:
//     source directory (on the build machine) holding an artifacts tree to
//     include in the initrd image.
//   - artifactsTargetDir:
//     target directory (within the initrd image) where the contents of the
//     artifactsSourceDir tree will be copied to.
//
// outputs:
// - creates an initrd.img and stores its path in b.artifacts.initrdImagePath.
func (b *LiveOSIsoBuilder) generateInitrdImage(rootfsSourceDir, artifactsSourceDir, artifactsTargetDir string) error {

	logger.Log.Debugf("Generating initrd")

	chroot := safechroot.NewChroot(rootfsSourceDir, true /*isExistingDir*/)
	if chroot == nil {
		return fmt.Errorf("failed to create a new chroot object for %s.", rootfsSourceDir)
	}
	defer chroot.Close(true /*leaveOnDisk*/)

	err := chroot.Initialize("", nil, nil, true /*includeDefaultMounts*/)
	if err != nil {
		return fmt.Errorf("failed to initialize chroot object for %s:\n%w", rootfsSourceDir, err)
	}

	initrdPathInChroot := "/initrd.img"
	err = chroot.Run(func() error {
		dracutParams := []string{
			initrdPathInChroot,
			"--kver", b.artifacts.kernelVersion,
			"--filesystems", "squashfs",
			"--include", artifactsSourceDir, artifactsTargetDir}

		return shell.ExecuteLive(true /*squashErrors*/, "dracut", dracutParams...)
	})
	if err != nil {
		return fmt.Errorf("failed to run dracut:\n%w", err)
	}

	generatedInitrdPath := filepath.Join(rootfsSourceDir, initrdPathInChroot)
	targetInitrdPath := filepath.Join(b.workingDirs.isoArtifactsDir, initrdImage)
	err = file.Copy(generatedInitrdPath, targetInitrdPath)
	if err != nil {
		return fmt.Errorf("failed to copy generated initrd:\n%w", err)
	}
	b.artifacts.initrdImagePath = targetInitrdPath

	return nil
}

// prepareArtifactsFromFullImage
//
//	extracts and generates all LiveOS Iso artifacts from a given raw full disk
//	image (has boot and rootfs partitions).
//
// inputs:
//   - 'rawImageFile':
//     path to an existing raw full disk image (i.e. image with boot
//     partition and a rootfs partition).
//   - 'extraCommandLine':
//     extra kernel command line arguments to add to grub.
//
// outputs:
//   - all the extracted/generated artifacts will be placed in the
//     `LiveOSIsoBuilder.workingDirs.isoArtifactsDir` folder.
//   - the paths to individual artifaces are found in the
//     `LiveOSIsoBuilder.artifacts` data structure.
func (b *LiveOSIsoBuilder) prepareArtifactsFromFullImage(rawImageFile string, extraCommandLine string) error {

	logger.Log.Infof("Preparing iso artifacts")

	logger.Log.Debugf("Connecting to raw image (%s)", rawImageFile)
	rawImageConnection, err := connectToExistingImage(rawImageFile, b.workingDirs.isoBuildDir, "readonly-rootfs-mount", false /*includeDefaultMounts*/)
	if err != nil {
		return err
	}
	defer rawImageConnection.Close()

	writeableRootfsDir := filepath.Join(b.workingDirs.isoBuildDir, "writeable-rootfs")
	err = b.populateWriteableRootfsDir(rawImageConnection.Chroot().RootDir(), writeableRootfsDir)
	if err != nil {
		return fmt.Errorf("failed to copy the contents of rootfs from image (%s) to local folder (%s):\n%w", rawImageFile, writeableRootfsDir, err)
	}

	isoMakerArtifactsStagingDir := "/boot-staging"
	err = b.prepareLiveOSDir(writeableRootfsDir, isoMakerArtifactsStagingDir, extraCommandLine)
	if err != nil {
		return fmt.Errorf("failed to convert rootfs folder to a LiveOS folder:\n%w", err)
	}

	err = b.createSquashfsImage(writeableRootfsDir)
	if err != nil {
		return fmt.Errorf("failed to create squashfs image:\n%w", err)
	}

	isoMakerArtifactsDirInInitrd := "/boot"
	err = b.generateInitrdImage(writeableRootfsDir, isoMakerArtifactsStagingDir, isoMakerArtifactsDirInInitrd)
	if err != nil {
		return fmt.Errorf("failed to generate initrd image:\n%w", err)
	}

	return nil
}

// createIsoImage
//
//	creates an LiveOS ISO image.
//
// inputs:
//   - additionalIsoFiles:
//     map of addition files to copy to the iso media.
//     sourcePath -> [ targetPath0, targetPath1, ...]
//   - isoOutputDir:
//     path to a folder where the output image will be placed. It does not
//     need to be created before calling this function.
//   - isoOutputBaseName:
//     path to the iso image to be created upon successful copmletion of this
//     function.
//
// ouptuts:
//   - create a LiveOS ISO.
func (b *LiveOSIsoBuilder) createIsoImage(additionalIsoFiles []safechroot.FileToCopy, isoOutputDir, isoOutputBaseName string) error {

	baseDirPath := ""

	// unattended install is where the ISO OS configures a persistent storage
	// and installs RPMs to it. This is different from the LiveOS scenario.
	unattendedInstall := false

	// We are disabling BIOS booloaders because enabling them will requires
	// MIC to take a dependency on binary artifacts stored elsewhere.
	// Should we decide to include the BIOS bootloader, we need to find a
	// reliable and efficient way to pull those binaries.
	enableBiosBoot := false
	isoResourcesDir := ""

	// No stock resources are needed for the LiveOS scenario.
	// No rpms are needed for the LiveOS scenario.
	enableRpmRepo := false
	isoRepoDirPath := ""

	// isoMaker constructs the final image name as follows:
	// {isoOutputDir}/{isoOutputBaseName}{releaseVersion}{imageNameTag}.iso
	releaseVersion := ""
	imageNameTag := ""

	// empty target system config since LiveOS does not install the OS
	// artifacts to the target system.
	targetSystemConfig := configuration.Config{}

	// Add the squashfs file
	squashfsImageToCopy := safechroot.FileToCopy{
		Src:  b.artifacts.squashfsImagePath,
		Dest: filepath.Join(liveOSDir, liveOSImage),
	}
	additionalIsoFiles = append(additionalIsoFiles, squashfsImageToCopy)

	// Add /boot/* files
	for sourceFile, targetFile := range b.artifacts.additionalFiles {
		fileToCopy := safechroot.FileToCopy{
			Src:           sourceFile,
			Dest:          targetFile,
			NoDereference: true,
		}
		additionalIsoFiles = append(additionalIsoFiles, fileToCopy)
	}

	err := os.MkdirAll(isoOutputDir, os.ModePerm)
	if err != nil {
		return err
	}

	isoMaker, err := isomakerlib.NewIsoMakerWithConfig(
		unattendedInstall,
		enableBiosBoot,
		enableRpmRepo,
		baseDirPath,
		b.workingDirs.isomakerBuildDir,
		releaseVersion,
		isoResourcesDir,
		additionalIsoFiles,
		targetSystemConfig,
		isoBootDir,
		b.artifacts.initrdImagePath,
		b.artifacts.grubCfgPath,
		isoRepoDirPath,
		isoOutputDir,
		isoOutputBaseName,
		imageNameTag)
	if err != nil {
		return err
	}

	err = isoMaker.Make()
	if err != nil {
		return err
	}

	return nil
}

// micIsoConfigToIsoMakerConfig
//
//	converts imagecustomizerapi.Iso to isomaker configuration.
//
// inputs:
//
//   - 'baseConfigPath'
//     path to the folder where the mic configuration was loaded from.
//     This path will be used to construct absolute paths for build machine
//     file references defined in the config.
//   - 'isoConfig'
//     user provided configuration for the iso image.
//
// outputs:
//   - 'additionalIsoFiles'
//     list of files to copy from the build machine to the iso media.
func micIsoConfigToIsoMakerConfig(baseConfigPath string, isoConfig *imagecustomizerapi.Iso) (additionalIsoFiles []safechroot.FileToCopy, extraCommandLine string, err error) {

	if isoConfig == nil {
		return
	}

	var cleanedArgs []string
	for _, kernelExtraArgument := range isoConfig.KernelCommandLine.ExtraCommandLine {
		cleanedArg := strings.TrimSpace(string(kernelExtraArgument))
		cleanedArgs = append(cleanedArgs, cleanedArg)
	}

	extraCommandLine = strings.Join(cleanedArgs, " ")

	additionalIsoFiles = []safechroot.FileToCopy{}

	for sourcePath, fileConfigs := range isoConfig.AdditionalFiles {
		absSourcePath := file.GetAbsPathWithBase(baseConfigPath, sourcePath)
		for _, fileConfig := range fileConfigs {
			fileToCopy := safechroot.FileToCopy{
				Src:         absSourcePath,
				Dest:        fileConfig.Path,
				Permissions: (*fs.FileMode)(fileConfig.Permissions),
			}
			additionalIsoFiles = append(additionalIsoFiles, fileToCopy)
		}
	}

	return additionalIsoFiles, extraCommandLine, nil
}

// createLiveOSIsoImage
//
//	main function to create a LiveOS ISO image from a raw full disk image file.
//
// inputs:
//
//   - 'buildDir':
//     path build directory (can be shared with other tools).
//   - 'baseConfigPath'
//     path to the folder where the mic configuration was loaded from.
//     This path will be used to construct absolute paths for file references
//     defined in the config.
//   - 'inputIsoArtifacts'
//     an optional LiveOSIsoBuilder that holds the state of the original input
//     iso if one was provided. If present, this function will copy all files
//     from the inputIsoArtifacts.artifacts.additionalFiles to the new iso
//     if the destination is not already defined (for the new iso).
//     This is used to carry over any files from a previously customized iso
//     to the new one.
//   - 'isoConfig'
//     user provided configuration for the iso image.
//   - 'rawImageFile':
//     path to an existing raw full disk image (has boot + rootfs partitions).
//   - 'outputImageDir':
//     path to a folder where the generated iso will be placed.
//   - 'outputImageBase':
//     base name of the image to generate. The generated name will be on the
//     form: {outputImageDir}/{outputImageBase}.iso
//
// outputs:
//
//	creates a LiveOS ISO image.
func createLiveOSIsoImage(buildDir, baseConfigPath string, inputIsoArtifacts *LiveOSIsoBuilder, isoConfig *imagecustomizerapi.Iso, rawImageFile, outputImageDir, outputImageBase string) (err error) {

	additionalIsoFiles, extraCommandLine, err := micIsoConfigToIsoMakerConfig(baseConfigPath, isoConfig)
	if err != nil {
		return fmt.Errorf("failed to convert iso configuration to isomaker format:\n%w", err)
	}

	isoBuildDir := filepath.Join(buildDir, "tmp")

	isoBuilder := &LiveOSIsoBuilder{
		//
		// buildDir (might be shared with other build tools)
		//  |--tmp   (LiveOSIsoBuilder specific)
		//     |--<various mount points>
		//     |--artifacts        (extracted and generated artifacts)
		//     |--isomaker-tmp     (used exclusively by isomaker)
		//
		workingDirs: IsoWorkingDirs{
			isoBuildDir:     isoBuildDir,
			isoArtifactsDir: filepath.Join(isoBuildDir, "artifacts"),
			// IsoMaker needs its own folder to work in (it starts by deleting and re-creating it).
			isomakerBuildDir: filepath.Join(isoBuildDir, "isomaker-tmp"),
		},
	}
	defer func() {
		cleanupErr := os.RemoveAll(isoBuilder.workingDirs.isoBuildDir)
		if cleanupErr != nil {
			if err != nil {
				err = fmt.Errorf("%w:\nfailed to clean-up (%s): %w", err, isoBuilder.workingDirs.isoBuildDir, cleanupErr)
			} else {
				err = fmt.Errorf("failed to clean-up (%s): %w", isoBuilder.workingDirs.isoBuildDir, cleanupErr)
			}
		}
	}()

	err = isoBuilder.prepareArtifactsFromFullImage(rawImageFile, extraCommandLine)
	if err != nil {
		return err
	}

	// If we started from an input iso (not an input vhd(x)/qcow), then there
	// might be additional files that are not defined in the current user
	// configuration. Below, we loop through the files we have captured so far
	// and append any file that was in the input iso and is not included
	// already. This also ensures that no file from the input iso overwrites
	// a newer version that has just been created.
	if inputIsoArtifacts != nil {
		for inputSourceFile, inputTargetFile := range inputIsoArtifacts.artifacts.additionalFiles {
			found := false
			for _, targetFile := range isoBuilder.artifacts.additionalFiles {
				if inputTargetFile == targetFile {
					found = true
					break
				}
			}
			if !found {
				isoBuilder.artifacts.additionalFiles[inputSourceFile] = inputTargetFile
			}
		}
	}

	err = isoBuilder.createIsoImage(additionalIsoFiles, outputImageDir, outputImageBase)
	if err != nil {
		return err
	}

	return nil
}

// extractIsoImageContents
//
//   - given an iso image, this function extracts its contents into the specified
//     folder.
//
// inputs:
//
//   - 'buildDir':
//     path build directory (can be shared with other tools).
//   - 'isoImageFile'
//     path to iso image file to extract its contents.
//   - 'isoExpansionFolder'
//     folder where the extracts contents will be copied to.
//
// outputs:
//
//   - creates a local folder with the same structure and contents as the provided
//     iso image.
func extractIsoImageContents(buildDir string, isoImageFile string, isoExpansionFolder string) (err error) {

	mountDir, err := os.MkdirTemp(buildDir, "tmp-iso-mount-")
	if err != nil {
		return fmt.Errorf("failed to create temporary mount folder for iso:\n%w", err)
	}
	defer os.RemoveAll(mountDir)

	isoImageLoopDevice, err := safeloopback.NewLoopback(isoImageFile)
	if err != nil {
		return fmt.Errorf("failed to create loop device for (%s):\n%w", isoImageFile, err)
	}
	defer isoImageLoopDevice.Close()

	isoImageMount, err := safemount.NewMount(isoImageLoopDevice.DevicePath(), mountDir,
		"iso9660" /*fstype*/, unix.MS_RDONLY /*flags*/, "" /*data*/, false /*makeAndDelete*/)
	if err != nil {
		return err
	}
	defer isoImageMount.Close()

	err = os.MkdirAll(isoExpansionFolder, os.ModePerm)
	if err != nil {
		return fmt.Errorf("failed to create folder %s:\n%w", isoExpansionFolder, err)
	}

	err = copyPartitionFiles(mountDir+"/.", isoExpansionFolder)
	if err != nil {
		return fmt.Errorf("failed to copy iso image contents to a writeable folder (%s):\n%w", isoExpansionFolder, err)
	}

	err = isoImageMount.CleanClose()
	if err != nil {
		return err
	}

	err = isoImageLoopDevice.CleanClose()
	if err != nil {
		return err
	}

	return nil
}

// createIsoBuilderFromIsoImage
//
//   - given an iso image, this function extracts its contents, scans them, and
//     constructs a LiveOSIsoBuilder object filling out as many of its fields as
//     possible.
//
// inputs:
//
//   - 'buildDir':
//     path build directory (can be shared with other tools).
//   - 'buildDirAbs'
//     the absolute path of 'buildDir'.
//   - 'isoImageFile'
//     the source iso image file to extract/scan.
//
// outputs:
//
//   - returns an instance of LiveOSIsoBuilder populated with all the paths of the
//     extracted contents.
func createIsoBuilderFromIsoImage(buildDir string, buildDirAbs string, isoImageFile string) (isoBuilder *LiveOSIsoBuilder, err error) {

	isoBuildDir := filepath.Join(buildDir, "tmp")
	isoBuilder = &LiveOSIsoBuilder{
		//
		// buildDir (might be shared with other build tools)
		//  |--tmp   (LiveOSIsoBuilder specific)
		//     |--<various mount points>
		//     |--artifacts        (extracted and generated artifacts)
		//     |--isomaker-tmp     (used exclusively by isomaker)
		//
		workingDirs: IsoWorkingDirs{
			isoBuildDir:     isoBuildDir,
			isoArtifactsDir: filepath.Join(isoBuildDir, "artifacts"),
			// IsoMaker needs its own folder to work in (it starts by deleting and re-creating it).
			isomakerBuildDir: filepath.Join(isoBuildDir, "isomaker-tmp"),
		},
	}
	defer func() {
		if err != nil {
			cleanupErr := isoBuilder.cleanUp()
			if cleanupErr != nil {
				err = fmt.Errorf("%w:\nfailed to clean-up:\n%w", err, cleanupErr)
			}
		}
	}()

	// create iso build folder
	err = os.MkdirAll(isoBuildDir, os.ModePerm)
	if err != nil {
		return isoBuilder, fmt.Errorf("failed to create folder %s:\n%w", isoBuildDir, err)
	}
	isoBuilder.addCleanupDir(isoBuildDir)

	// extract iso contents
	isoExpansionFolder, err := os.MkdirTemp(buildDirAbs, "expanded-input-iso-")
	if err != nil {
		return isoBuilder, fmt.Errorf("failed to create a temporary iso expansion folder for iso:\n%w", err)
	}
	isoBuilder.addCleanupDir(isoExpansionFolder)

	err = extractIsoImageContents(buildDir, isoImageFile, isoExpansionFolder)
	if err != nil {
		return isoBuilder, fmt.Errorf("failed to extract iso contents from input iso file:\n%w", err)
	}

	isoFiles, err := file.EnumerateDirFiles(isoExpansionFolder)
	if err != nil {
		return isoBuilder, fmt.Errorf("failed to enumerate expanded iso files under %s:\n%w", isoExpansionFolder, err)
	}

	isoBuilder.artifacts.additionalFiles = make(map[string]string)

	for _, isoFile := range isoFiles {
		fileName := filepath.Base(isoFile)

		scheduleAdditionalFile := true

		switch fileName {
		case bootx64Binary:
			isoBuilder.artifacts.bootx64EfiPath = isoFile
			// isomaker will extract this from initrd and copy it to include it
			// in the iso media - so no need to schedule it as an additional
			// file.
			scheduleAdditionalFile = false
		case grubx64Binary:
			// Note that grubx64NoPrefixBinary is not expected to on an existing
			// iso - and hence we do not look for it here. grubx64NoPrefixBinary
			// may exist only on a vhdx/qcow when the grub-noprefix package is
			// installed. When such images are converted to an iso, we rename
			// the grub binary to its regular name (grubx64.efi).
			isoBuilder.artifacts.grubx64EfiPath = isoFile
			// isomaker will extract this from initrd and copy it to include it
			// in the iso media - so no need to schedule it as an additional
			// file.
			scheduleAdditionalFile = false
		case grubCfg:
			isoBuilder.artifacts.grubCfgPath = isoFile
			// grub.cfg is passed as a parameter to isomaker.
			scheduleAdditionalFile = false
		case liveOSImage:
			isoBuilder.artifacts.squashfsImagePath = isoFile
			// the squashfs image file is added to the additional file list
			// by a different part of the code
			scheduleAdditionalFile = false
		case initrdImage:
			isoBuilder.artifacts.initrdImagePath = isoFile
			// initrd.img is passed as a parameter to isomaker.
			scheduleAdditionalFile = false
		}
		if strings.HasPrefix(fileName, vmLinuzPrefix) {
			isoBuilder.artifacts.vmlinuzPath = isoFile
			// isomaker will extract this from initrd and copy it to include it
			// in the iso media - so no need to schedule it as an additional
			// file.
			scheduleAdditionalFile = false
		}

		if scheduleAdditionalFile {
			isoBuilder.artifacts.additionalFiles[isoFile] = strings.TrimPrefix(isoFile, isoExpansionFolder)
		}
	}

	return isoBuilder, nil
}

// createImageFromUnchangedOS
//
//   - assuming the LiveOSIsoBuilder instance has all its artifacts populated,
//     this function goes straight to updating grub and re-packaging the
//     artifacts into an iso image. It does not re-create the initrd.img or
//     the squashfs.img. This speeds-up customizing iso images when there are
//     no customizations applicable to the OS (i.e. to the squashfs.img).
//
// inputs:
//
//   - 'baseConfigPath':
//     path to where the configuration is loaded from. This is used to resolve
//     relative paths.
//   - 'isoConfig'
//     user provided configuration for the iso image.
//   - 'outputImageDir':
//     path to a folder where the generated iso will be placed.
//   - 'outputImageBase':
//     base name of the image to generate. The generated name will be on the
//     form: {outputImageDir}/{outputImageBase}.iso
//
// outputs:
//
//   - creates an iso image.
func (b *LiveOSIsoBuilder) createImageFromUnchangedOS(baseConfigPath string, isoConfig *imagecustomizerapi.Iso, outputImageDir string, outputImageBase string) error {

	logger.Log.Infof("Creating LiveOS iso image using unchanged OS partitions")

	additionalIsoFiles, extraCommandLine, err := micIsoConfigToIsoMakerConfig(baseConfigPath, isoConfig)
	if err != nil {
		return fmt.Errorf("failed to convert iso configuration to isomaker configuration format:\n%w", err)
	}

	err = b.updateGrubCfg(b.artifacts.grubCfgPath, extraCommandLine)
	if err != nil {
		return fmt.Errorf("failed to update grub.cfg:\n%w", err)
	}

	err = b.createIsoImage(additionalIsoFiles, outputImageDir, outputImageBase)
	if err != nil {
		return fmt.Errorf("failed to create iso image:\n%w", err)
	}

	return nil
}

// getSizeOnDiskInBytes
//
//   - given a folder, it calculates the total size in bytes of its contents.
//
// inputs:
//
//   - 'rootDir':
//     root folder to calculate its size.
//
// outputs:
//
//   - returns the size in bytes.
func getSizeOnDiskInBytes(rootDir string) (size uint64, err error) {
	logger.Log.Debugf("Calculating total size for (%s)", rootDir)

	duStdout, _, err := shell.Execute("du", "-s", rootDir)
	if err != nil {
		return 0, fmt.Errorf("failed find the size of the specified folder using 'du' for (%s):\n%w", rootDir, err)
	}

	// parse and get count and unit
	diskSizeRegex := regexp.MustCompile(`^(\d+)\s+`)
	matches := diskSizeRegex.FindStringSubmatch(duStdout)
	if matches == nil || len(matches) < 2 {
		return 0, fmt.Errorf("failed to parse 'du -s' output (%s).", duStdout)
	}

	sizeInKbsString := matches[1]
	sizeInKbs, err := strconv.ParseUint(sizeInKbsString, 10, 64)
	if err != nil {
		return 0, fmt.Errorf("failed to parse disk size (%d):\n%w", sizeInKbs, err)
	}

	return sizeInKbs * diskutils.KiB, nil
}

// getDiskSizeEstimateInMBs
//
//   - given a folder, it calculates the size of a disk image that can hold
//     all of its contents.
//   - The amount of disk space a file occupies depends on the block size of the
//     host file system. If many files are smaller than a block size, there will
//     be a lot of waste. If files are very large, there will be very little
//     waste. It is hard to predict how much disk space a set of a files will
//     occupy without enumerating the sizes of all the files and knowing the
//     target block size. In this function, we use an optimistic approach which
//     calculates the required disk space by multiplying the total file size by
//     a safety factor - i.e. safe that it will be able t hold all the contents.
//
// inputs:
//
//   - 'rootDir':
//     root folder to calculate its size.
//   - 'safetyFactor':
//     a multiplier used with the total number of bytes calculated.
//
// outputs:
//
//   - returns the size in mega bytes.
func getDiskSizeEstimateInMBs(rootDir string, safetyFactor float64) (size uint64, err error) {

	sizeInBytes, err := getSizeOnDiskInBytes(rootDir)
	if err != nil {
		return 0, fmt.Errorf("failed to get folder size on disk while estimating total disk size:\n%w", err)
	}

	sizeInMBs := sizeInBytes/diskutils.MiB + 1
	estimatedSizeInMBs := uint64(float64(sizeInMBs) * safetyFactor)
	return estimatedSizeInMBs, nil
}

// createWriteableImageFromSquashfs
//
//   - given a squashfs image file, it creates a writeable image with two
//     partitions, and copies the contents of the squashfs unto that writeable
//     image.
//   - the squashfs image file must be extracted from a previously created
//     LiveOS iso and is specified by the LiveOSIsoBuilder.artifacts.squashfsImagePath.
//
// inputs:
//
//   - 'buildDir':
//     path build directory (can be shared with other tools).
//   - 'rawImageFile':
//     the name of the raw image to create and populate with the contents of
//     the squashfs.
//
// outputs:
//
//   - creates the specified writeable image.
func (b *LiveOSIsoBuilder) createWriteableImageFromSquashfs(buildDir, rawImageFile string) error {

	logger.Log.Infof("Creating writeable image from squashfs (%s)", b.artifacts.squashfsImagePath)

	// mount squash fs
	squashMountDir, err := os.MkdirTemp(buildDir, "tmp-squashfs-mount-")
	if err != nil {
		return fmt.Errorf("failed to create temporary mount folder for squashfs:\n%w", err)
	}
	defer os.RemoveAll(squashMountDir)

	squashfsLoopDevice, err := safeloopback.NewLoopback(b.artifacts.squashfsImagePath)
	if err != nil {
		return fmt.Errorf("failed to create loop device for (%s):\n%w", b.artifacts.squashfsImagePath, err)
	}
	defer squashfsLoopDevice.Close()

	isoImageMount, err := safemount.NewMount(squashfsLoopDevice.DevicePath(), squashMountDir,
		"squashfs" /*fstype*/, 0 /*flags*/, "" /*data*/, false /*makeAndDelete*/)
	if err != nil {
		return err
	}
	defer isoImageMount.Close()

	// estimate the new disk size
	safeDiskSizeMB, err := getDiskSizeEstimateInMBs(squashMountDir, expansionSafetyFactor)
	if err != nil {
		return fmt.Errorf("failed to calculate the disk size of %s:\n%w", squashMountDir, err)
	}

	logger.Log.Debugf("safeDiskSizeMB = %d", safeDiskSizeMB)

	// define a disk layout with a boot partition and a rootfs partition
	maxDiskSizeMB := imagecustomizerapi.DiskSize(safeDiskSizeMB * diskutils.MiB)
	var bootPartitionStart imagecustomizerapi.DiskSize
	bootPartitionStart = imagecustomizerapi.DiskSize(1 * diskutils.MiB)
	var bootPartitionEnd imagecustomizerapi.DiskSize
	bootPartitionEnd = imagecustomizerapi.DiskSize(9 * diskutils.MiB)

	diskConfig := imagecustomizerapi.Disk{
		PartitionTableType: imagecustomizerapi.PartitionTableTypeGpt,
		MaxSize:            maxDiskSizeMB,
		Partitions: []imagecustomizerapi.Partition{
			{
				Id:    "esp",
				Start: bootPartitionStart,
				End:   &bootPartitionEnd,
				Type:  imagecustomizerapi.PartitionTypeESP,
			},
			{
				Id:    "rootfs",
				Start: bootPartitionEnd,
			},
		},
	}

	fileSystemConfigs := []imagecustomizerapi.FileSystem{
		{
			DeviceId: "esp",
			Type:     imagecustomizerapi.FileSystemTypeFat32,
			MountPoint: &imagecustomizerapi.MountPoint{
				Path:    "/boot/efi",
				Options: "umask=0077",
			},
		},
		{
			DeviceId: "rootfs",
			Type:     imagecustomizerapi.FileSystemTypeExt4,
			MountPoint: &imagecustomizerapi.MountPoint{
				Path: "/",
			},
		},
	}

	// populate the newly created disk image with content from the squash fs
	installOSFunc := func(imageChroot *safechroot.Chroot) error {
		// At the point when this copy will be executed, both the boot and the
		// root partitions will be mounted, and the files of /boot/efi will
		// land on the the boot partition, while the rest will be on the rootfs
		// partition.
		err := copyPartitionFiles(squashMountDir+"/.", imageChroot.RootDir())
		if err != nil {
			return fmt.Errorf("failed to copy squashfs contents to a writeable disk:\n%w", err)
		}

		// In a vhd(s)/qcow->iso flow, grub.cfg can be modified by the use
		// under the mic's os node, and then again later by the iso node.
		// However, the second modification does not make it back into the
		// squashfs since such customization is specific to the iso (live os
		// configuration). Now, when we are creating a writeable image from an
		// iso, we need to take the grub.cfg that in the iso (not the one in
		// the squashfs), since it will have all previous user modifications
		// and also the one actually used for booting.
		sourceGrubCfgPath := b.artifacts.grubCfgPath
		targetGrubCfgPath := filepath.Join(imageChroot.RootDir(), "boot/grub2/grub.cfg")

		err = file.Copy(sourceGrubCfgPath, targetGrubCfgPath)
		if err != nil {
			return fmt.Errorf("failed to copy the input iso grub.cfg to the writeable image:\n%w", err)
		}

		return err
	}

	// create the new raw disk image
	writeableChrootDir := "writeable-raw-image"
	err = createNewImage(rawImageFile, diskConfig, fileSystemConfigs, buildDir, writeableChrootDir, installOSFunc)
	if err != nil {
		return fmt.Errorf("failed to copy squashfs into new writeable image (%s):\n%w", rawImageFile, err)
	}

	err = isoImageMount.CleanClose()
	if err != nil {
		return err
	}

	err = squashfsLoopDevice.CleanClose()
	if err != nil {
		return err
	}

	return nil
}
