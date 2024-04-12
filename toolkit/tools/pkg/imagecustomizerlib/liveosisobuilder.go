// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"io/fs"
	"io/ioutil"
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
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/isomakerlib"
)

const (
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
	additionalFiles   map[string]string // local-build-path -> iso-media-path
}

type LiveOSIsoBuilder struct {
	workingDirs IsoWorkingDirs
	artifacts   IsoArtifacts
}

func (b *LiveOSIsoBuilder) dump(title string) {
	logger.Log.Debugf("----<><>---- " + title + "----<><>---- ")
	logger.Log.Debugf("- workingDirs")
	logger.Log.Debugf("  |- isoBuildDir      : %s", b.workingDirs.isoBuildDir)
	logger.Log.Debugf("  |- isoArtifactsDir  : %s", b.workingDirs.isoArtifactsDir)
	logger.Log.Debugf("  |- isomakerBuildDir : %s", b.workingDirs.isomakerBuildDir)
	logger.Log.Debugf("- artifacts")
	logger.Log.Debugf("  |- kernelVersion    : %s", b.artifacts.kernelVersion)
	logger.Log.Debugf("  |- bootx64EfiPath   : %s", b.artifacts.bootx64EfiPath)
	logger.Log.Debugf("  |- grubx64EfiPath   : %s", b.artifacts.grubx64EfiPath)
	logger.Log.Debugf("  |- grubCfgPath      : %s", b.artifacts.grubCfgPath)
	logger.Log.Debugf("  |- vmlinuzPath      : %s", b.artifacts.vmlinuzPath)
	logger.Log.Debugf("  |- initrdImagePath  : %s", b.artifacts.initrdImagePath)
	logger.Log.Debugf("  |- squashfsImagePath: %s", b.artifacts.squashfsImagePath)
	logger.Log.Debugf("  |- additionalFiles  : ")
	for source, target := range b.artifacts.additionalFiles {
		logger.Log.Debugf("     |- %s            : %s", source, target)
	}
	logger.Log.Debugf("----<><>---- ----<><>---- ")
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
	targetBoot64EfiPath := filepath.Join(targetBootloadersDir, "bootx64.efi")
	err = file.Copy(sourceBoot64EfiPath, targetBoot64EfiPath)
	if err != nil {
		return fmt.Errorf("failed to stage bootloader file (bootx64.efi):\n%w", err)
	}

	sourceGrub64EfiPath := b.artifacts.grubx64EfiPath
	targetGrub64EfiPath := filepath.Join(targetBootloadersDir, "grubx64.efi")
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

	// empty fstab only...
	touchParams := []string{fstabFile}
	err = shell.ExecuteLive(false, "touch", touchParams...)
	if err != nil {
		return fmt.Errorf("failed to create %s:\n%w", fstabFile, err)
	}
	// ToDo: why create it some where and then copy it?
	//       just create it at the destination...
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

	b.dump("Starting extractBootDirFiles()")

	sourceBootDir := filepath.Join(writeableRootfsDir, "/boot")
	b.artifacts.additionalFiles = make(map[string]string)

	var exclusions []*regexp.Regexp
	// the following files will be re-created - no need to copy them only to
	// have them overwritten.
	exclusions = append(exclusions, regexp.MustCompile(`/boot/initrd\.img.*`))

	err := filepath.Walk(sourceBootDir, func(sourcePath string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if info.IsDir() {
			return nil
		}

		for _, exclusion := range exclusions {
			match := exclusion.FindStringIndex(sourcePath)
			if match != nil {
				return nil
			}
		}

		targetPath := strings.Replace(sourcePath, writeableRootfsDir, b.workingDirs.isoArtifactsDir, -1)
		targetFileName := filepath.Base(targetPath)

		copiedByIsoMaker := false

		switch targetFileName {
		case "bootx64.efi":
			b.artifacts.bootx64EfiPath = targetPath
			copiedByIsoMaker = true
		case "grubx64.efi":
			b.artifacts.grubx64EfiPath = targetPath
			copiedByIsoMaker = true
		case "grub.cfg":
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
			return err
		}

		// If not copied by IsoMaker, add it to the list of files we will copy
		// later. Otherwise, do not do anything and leave it to IsoMaker.
		if !copiedByIsoMaker {
			b.artifacts.additionalFiles[targetPath] = strings.TrimPrefix(targetPath, b.workingDirs.isoArtifactsDir)
		}

		return nil
	})

	if err != nil {
		return fmt.Errorf("failed to extract files from under the boot folder:\n%w", err)
	}

	b.dump("Finished extractBootDirFiles()")

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

	b.dump("Finished createSquashfsImage()")

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

	b.dump("Finished generateInitrdImage()")

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

func expandIso(buildDir, isoImageFile, isoExpandionFolder string) (err error) {
	logger.Log.Debugf("---- dev ---- expandIso() - 1 - isoImageFile=%s", isoImageFile)

	mountDir, err := ioutil.TempDir(buildDir, "tmp-iso-mount-")
	if err != nil {
		return fmt.Errorf("failed to create temporary mount folder for iso:\n%w", err)
	}
	defer os.RemoveAll(mountDir)

	logger.Log.Debugf("---- dev ---- expandIso() - 2 - created mountDir=%s", mountDir)

	mountParams := []string{isoImageFile, mountDir}
	err = shell.ExecuteLive(false, "mount", mountParams...)
	if err != nil {
		return fmt.Errorf("failed to mount iso:\n%w", err)
	}
	defer func() {
		unmountParams := []string{mountDir}
		cleanupErr := shell.ExecuteLive(false, "umount", unmountParams...)
		if cleanupErr != nil {
			err = fmt.Errorf("%w:\nfailed to clean-up (%s): %w", err, mountDir, cleanupErr)
		}
	}()

	logger.Log.Debugf("---- dev ---- expandIso() - 3 - mounted")

	err = os.MkdirAll(isoExpandionFolder, os.ModePerm)
	if err != nil {
		return fmt.Errorf("failed to create folder %s:\n%w", isoExpandionFolder, err)
	}

	logger.Log.Debugf("---- dev ---- expandIso() - 4 - copying %s to %s", mountDir, isoExpandionFolder)

	err = copyPartitionFiles(mountDir+"/.", isoExpandionFolder)
	if err != nil {
		return fmt.Errorf("failed to copy iso image contents to a writeable folder (%s):\n%w", isoExpandionFolder, err)
	}

	return nil
}

func isoBuilderFromLayout(buildDir, isoExpandionFoldr string) (isoBuilder *LiveOSIsoBuilder, err error) {
	logger.Log.Debugf("---- dev ---- fromLayout() - 1")

	isoBuildDir := filepath.Join(buildDir, "tmp")
	err = os.MkdirAll(isoBuildDir, os.ModePerm)
	if err != nil {
		return nil, fmt.Errorf("failed to create folder %s:\n%w", isoBuildDir, err)
	}

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
	/*
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
	*/

	isoFiles, err := file.EnumerateDirFiles(isoExpandionFoldr)
	if err != nil {
		return nil, fmt.Errorf("failed to enumerate expanded iso files under %s:\n%w", isoExpandionFoldr, err)
	}

	isoBuilder.artifacts.additionalFiles = make(map[string]string)

	for _, isoFile := range isoFiles {
		logger.Log.Debugf("---- dev ---- processing %s", isoFile)
		fileName := filepath.Base(isoFile)

		// copiedByIsoMaker is true when isoMaker extracts the file from initrd.
		copiedByIsoMaker := false

		switch fileName {
		case "bootx64.efi", "grubx64.efi":
			copiedByIsoMaker = true
		case "grub.cfg":
			isoBuilder.artifacts.grubCfgPath = isoFile
			copiedByIsoMaker = true
		case "rootfs.img":
			isoBuilder.artifacts.squashfsImagePath = isoFile
			copiedByIsoMaker = true
		case "initrd.img":
			isoBuilder.artifacts.initrdImagePath = isoFile
			copiedByIsoMaker = true
		}
		if strings.HasPrefix(fileName, "vmlinuz-") {
			copiedByIsoMaker = true
		}

		if !copiedByIsoMaker {
			isoBuilder.artifacts.additionalFiles[isoFile] = strings.TrimPrefix(isoFile, isoExpandionFoldr)
		}
	}

	return isoBuilder, nil
}

func (b *LiveOSIsoBuilder) recreateLiveOSIsoImage(baseConfigPath string, isoConfig *imagecustomizerapi.Iso, outputImageDir, outputImageBase string) error {

	additionalIsoFiles, extraCommandLine, err := micIsoConfigToIsoMakerConfig(baseConfigPath, isoConfig)
	if err != nil {
		return fmt.Errorf("failed to convert iso configuration to isomaker format:\n%w", err)
	}

	err = b.updateGrubCfg(b.artifacts.grubCfgPath, extraCommandLine)
	if err != nil {
		return fmt.Errorf("failed to update grub.cfg:\n%w", err)
	}

	err = b.createIsoImage(additionalIsoFiles, outputImageDir, outputImageBase)
	if err != nil {
		return err
	}

	return nil
}

func getDiskSize(rootDir string) (size uint64, err error) {

	duParams := []string{"-sh", rootDir}
	duStdout, _, err := shell.Execute("du", duParams...)
	if err != nil {
		return 0, fmt.Errorf("failed to find the size of the expanded squashfs:\n%w", err)
	}
	duStdoutParts := strings.Split(duStdout, "\t")

	logger.Log.Debugf("du output:\n%s", duStdout)

	diskSizeRegex := regexp.MustCompile(`^(\d+)([KMGT])?.*$`)
	match := diskSizeRegex.FindStringSubmatch(duStdoutParts[0])
	if match == nil {
		return 0, fmt.Errorf("disk size (%s) has incorrect format: <num>[KMGT] (e.g. 100M, 1G)", duStdout)
	}

	numString := match[1]
	logger.Log.Debugf("du output numString=%s", numString)

	num, err := strconv.ParseUint(numString, 0, 10)
	if err != nil {
		return 0, fmt.Errorf("failed to parse disk size:\n%w", err)
	}
	logger.Log.Debugf("du output num=%d", num)

	if len(match) >= 3 {
		unit := match[2]
		multiplier := uint64(1)
		switch unit {
		case "K":
			multiplier = diskutils.KiB
		case "M":
			multiplier = diskutils.MiB
		case "G":
			multiplier = diskutils.GiB
		case "T":
			multiplier = diskutils.TiB
		case "":
			return 0, fmt.Errorf("disk size (%s) must have a suffix (i.e. K, M, G, or T)", numString)
		}

		num *= multiplier
	}
	logger.Log.Debugf("du output num=%d", num)

	// The imager's diskutils works in MiB. So, restrict disk and partition sizes to multiples of 1 MiB.
	if num%diskutils.MiB != 0 {
		return 0, fmt.Errorf("disk size (%d) must be a multiple of 1 MiB", num)
	}

	return num, nil
}

func (b *LiveOSIsoBuilder) createWriteableImage(buildDir, rawImageFile string) error {

	logger.Log.Debugf("---- dev ---- createWriteableImage() - 1 - creating %s", rawImageFile)

	// mount squash fs
	squashMountDir, err := ioutil.TempDir(buildDir, "tmp-squashfs-mount-")
	if err != nil {
		return fmt.Errorf("failed to create temporary mount folder for squashfs:\n%w", err)
	}
	defer os.RemoveAll(squashMountDir)

	logger.Log.Debugf("---- dev ---- createWriteableImage() - 2 - created squashMountDir=%s", squashMountDir)

	squashMountParams := []string{b.artifacts.squashfsImagePath, squashMountDir}
	err = shell.ExecuteLive(false, "mount", squashMountParams...)
	if err != nil {
		return fmt.Errorf("failed to mount squashfs:\n%w", err)
	}
	defer func() {
		unmountParams := []string{squashMountDir}
		cleanupErr := shell.ExecuteLive(false, "umount", unmountParams...)
		if cleanupErr != nil {
			err = fmt.Errorf("%w:\nfailed to clean-up (%s): %w", err, squashMountDir, cleanupErr)
		}
	}()

	logger.Log.Debugf("---- dev ---- createWriteableImage() - 3 - mounted b.artifacts.squashfsImagePath=%s", b.artifacts.squashfsImagePath)

	// get disk space
	diskSizeBytes, err := getDiskSize(squashMountDir)
	if err != nil {
		return fmt.Errorf("failed to calculate the disk size of %s:\n%w", squashMountDir, err)
	}
	diskSizeMB := diskSizeBytes/1024/1024 + 1
	logger.Log.Debugf("------ disk size = %d bytes or %d MB", diskSizeBytes, diskSizeMB)

	// create raw image
	logger.Log.Debugf("---- dev ---- createWriteableImage() - 4 - creating writeable image=%s", rawImageFile)
	var safetyFactor uint64
	safetyFactor = 2
	safeDiskSizeMB := diskSizeMB * safetyFactor

	/*
		#
		# create raw writeable image
		#
		diskSizeMBString := strconv.FormatUint(safeDiskSizeMB, 10)

		createImageParams := []string{"if=/dev/zero", "of=" + rawImageFile, "bs=1M", "count=" + diskSizeMBString}
		err = shell.ExecuteLive(false, "dd", createImageParams...)
		if err != nil {
			return fmt.Errorf("failed to create raw image %s with size %dM", rawImageFile, diskSizeMBString)
		}

		// format raw image
		logger.Log.Debugf("---- dev ---- createWriteableImage() - 5 - formatting writeable image=%s", rawImageFile)
		formatParams := []string{rawImageFile}
		err = shell.ExecuteLive(false, "mkfs.ext4", formatParams...)
		if err != nil {
			return fmt.Errorf("failed to format raw image %s", rawImageFile)
		}

		// mount raw image
		logger.Log.Debugf("---- dev ---- createWriteableImage() - 6 - mounting writeable image=%s", rawImageFile)

		writeableMountDir, err := ioutil.TempDir(buildDir, "tmp-writeable-mount-")
		if err != nil {
			return fmt.Errorf("failed to create temporary mount folder for writeable image:\n%w", err)
		}
		defer os.RemoveAll(writeableMountDir)

		logger.Log.Debugf("---- dev ---- createWriteableImage() - 7 - created writeableMountDir=%s", writeableMountDir)

		writeableMountParams := []string{rawImageFile, writeableMountDir}
		err = shell.ExecuteLive(false, "mount", writeableMountParams...)
		if err != nil {
			return fmt.Errorf("failed to mount writeable image:\n%w", err)
		}
		defer func() {
			unmountParams := []string{writeableMountDir}
			cleanupErr := shell.ExecuteLive(false, "umount", unmountParams...)
			if cleanupErr != nil {
				err = fmt.Errorf("%w:\nfailed to clean-up (%s): %w", err, writeableMountDir, cleanupErr)
			}
		}()

		// copy contents
		err = copyPartitionFiles(squashMountDir+"/.", writeableMountDir)
		if err != nil {
			return fmt.Errorf("failed to copy rootfs contents to a writeable folder (%s):\n%w", writeableMountDir, err)
		}
	*/

	var bootPartitionEnd uint64
	bootPartitionEnd = 9

	diskConfig := imagecustomizerapi.Disk{
		PartitionTableType: imagecustomizerapi.PartitionTableTypeGpt,
		MaxSize:            safeDiskSizeMB,
		Partitions: []imagecustomizerapi.Partition{
			{
				Id:    "esp",
				Start: 1,
				End:   &bootPartitionEnd,
				Flags: []imagecustomizerapi.PartitionFlag{
					imagecustomizerapi.PartitionFlagESP,
					imagecustomizerapi.PartitionFlagBoot,
				},
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

	installOSFunc := func(imageChroot *safechroot.Chroot) error {
		// At the point when this copy will be executed, both the boot and the root
		// partitions will be mounted, and the files of /boot/efi will land on the
		// the boot partition, while the rest will be on the rootfs partition.
		return copyPartitionFiles(squashMountDir+"/.", imageChroot.RootDir())
	}

	fancyRawImage := rawImageFile
	fancyChrootDir := "fancy-raw-image"

	err = createNewImage(fancyRawImage, diskConfig, fileSystemConfigs, buildDir, fancyChrootDir, installOSFunc)
	if err != nil {
		return fmt.Errorf("failed to copy squashfs into new fancy image (%s):\n%w", fancyRawImage, err)
	}

	// unmount raw image and delete mount dir
	// ok - defer

	// unmount squashfs and delete mount dir
	// ok - defer

	return nil
}
