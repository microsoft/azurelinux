// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/isomakerlib"
)

const (
	bootx64Binary         = "bootx64.efi"
	grubx64Binary         = "grubx64.efi"
	grubx64NoPrefixBinary = "grubx64-noprefix.efi"
	grubCfg               = "grub.cfg"

	searchCommandTemplate = "search --label %s --set root"
	rootValueTemplate     = "live:LABEL=%s"
	// The names initrd.img and vmlinuz are expected by isomaker.
	isoBootDir    = "boot"
	isoInitrdPath = "/boot/initrd.img"
	isoKernelPath = "/boot/vmlinuz"

	// kernel arguments template
	kernelArgsTemplate = " rd.shell rd.live.image rd.live.dir=%s rd.live.squashimg=%s rd.live.overlay=1 rd.live.overlay.nouserconfirmprompt %s"
	liveOSDir          = "liveos"
	liveOSImage        = "rootfs.img"

	dracutConfig = `add_dracutmodules+=" dmsquash-live "
add_drivers+=" overlay "
`
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
	bootDirFiles      map[string]string // local-build-path -> iso-media-path
}

type LiveOSIsoBuilder struct {
	workingDirs IsoWorkingDirs
	artifacts   IsoArtifacts
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

	sourceConfigFile := filepath.Join(b.workingDirs.isoArtifactsDir, "20-live-cd.conf")
	err = os.WriteFile(sourceConfigFile, []byte(dracutConfig), 0o644)
	if err != nil {
		return fmt.Errorf("failed to create %s:\n%w", sourceConfigFile, err)
	}

	targetConfigFile := filepath.Join(writeableRootfsDir, "/etc/dracut.conf.d/20-live-cd.conf")
	err = file.Copy(sourceConfigFile, targetConfigFile)
	if err != nil {
		return fmt.Errorf("failed to copy dracut config at %s:\n%w", targetConfigFile, err)
	}

	return nil
}

func (b *LiveOSIsoBuilder) updateGrubCfg(grubCfgFileName string, extraCommandLine string) error {

	inputContentString, err := file.Read(grubCfgFileName)
	if err != nil {
		return err
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

	inputContentString, _, err = replaceKernelCommandLineArgumentValue(inputContentString, "root", rootValue)
	if err != nil {
		return fmt.Errorf("failed to update the root kernel argument in the iso grub.cfg:\n%w", err)
	}

	inputContentString, err = updateSELinuxCommandLineHelper(inputContentString, imagecustomizerapi.SELinuxModeDisabled)
	if err != nil {
		return fmt.Errorf("failed to set SELinux mode:\n%w", err)
	}

	liveosKernelArgs := fmt.Sprintf(kernelArgsTemplate, liveOSDir, liveOSImage, extraCommandLine)

	inputContentString, err = appendKernelCommandLineArguments(inputContentString, liveosKernelArgs)
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
//     b.artifacts.bootDirFiles
func (b *LiveOSIsoBuilder) extractBootDirFiles(writeableRootfsDir string) error {

	b.artifacts.bootDirFiles = make(map[string]string)

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

		copiedByIsoMaker := false

		switch targetFileName {
		case bootx64Binary:
			b.artifacts.bootx64EfiPath = targetPath
			copiedByIsoMaker = true
		case grubx64Binary, grubx64NoPrefixBinary:
			b.artifacts.grubx64EfiPath = targetPath
			copiedByIsoMaker = true
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
		}
		if strings.HasPrefix(targetFileName, "vmlinuz-") {
			targetPath = filepath.Join(filepath.Dir(targetPath), "vmlinuz")
			b.artifacts.vmlinuzPath = targetPath
			copiedByIsoMaker = true
		}

		err = file.NewFileCopyBuilder(sourcePath, targetPath).
			SetNoDereference().
			Run()
		if err != nil {
			return fmt.Errorf("failed to extract files from under the boot folder:\n%w", err)
		}

		// If not copied by IsoMaker, add it to the list of files we will copy
		// later. Otherwise, do not do anything and leave it to IsoMaker.
		if !copiedByIsoMaker {
			b.artifacts.bootDirFiles[targetPath] = strings.TrimPrefix(targetPath, b.workingDirs.isoArtifactsDir)
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

	squashfsImagePath := filepath.Join(b.workingDirs.isoArtifactsDir, "rootfs.img")

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
	targetInitrdPath := filepath.Join(b.workingDirs.isoArtifactsDir, "initrd.img")
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
	for sourceFile, targetFile := range b.artifacts.bootDirFiles {
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

	extraCommandLine = strings.TrimSpace(string(isoConfig.KernelCommandLine.ExtraCommandLine))

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
func createLiveOSIsoImage(buildDir, baseConfigPath string, isoConfig *imagecustomizerapi.Iso, rawImageFile, outputImageDir, outputImageBase string) (err error) {

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

	err = isoBuilder.createIsoImage(additionalIsoFiles, outputImageDir, outputImageBase)
	if err != nil {
		return err
	}

	return nil
}
