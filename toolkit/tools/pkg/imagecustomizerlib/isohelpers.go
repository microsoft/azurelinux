// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safemount"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/isomakerlib"
)

var (
	grubCfgTemplate = `set default="0"
set timeout=0

menuentry "Mariner Baremetal Iso" {

	search --label CDROM --set root
	linux /isolinux/vmlinuz \
			overlay-size=70% \
			selinux=0 \
			console=tty0 \
			apparmor=0 \
			root=live:LABEL=CDROM \
			rd.shell \
			rd.live.image \
			rd.live.dir=config/additionalfiles/0 \
			rd.live.squashimg=rootfs.img \
			rd.live.overlay=1 \
			rd.live.overlay.nouserconfirmprompt

	initrd /isolinux/initrd.img
}	
`
	dracutConfig = `add_dracutmodules+=" dmsquash-live "
add_drivers+=" overlay "
`
)

type IsoWorkingDirs struct {
	buildDir       string
	tmpDir         string
	isomakerTmpDir string
	outDir 	       string
}

type IsoArtifacts struct {
	bootx64EfiPath string
	grubx64EfiPath string
	grubCfgPath    string
	vmlinuzPath    string
	kernelVersion  string
	initrdPath     string
	squashfsPath   string
}

// IsoMaker builds ISO images and populates them with packages and files required by the installer.
type IsoArtifactExtractor struct {
	workingDirs    IsoWorkingDirs
	artifacts      IsoArtifacts
}

// runs dracut against a modified rootfs to create the initrd file.
func (iae* IsoArtifactExtractor) generateInitrd(writeableRootfsDir string, isoMakerArtifactsDirInChroot string) error {

	logger.Log.Infof("generating initrd...")

	initrdPathInChroot := "/initrd.img"
	initrdPath := filepath.Join(writeableRootfsDir, initrdPathInChroot)
	isoMakerArtifactsDirInInitrd := "/boot"

	chroot := safechroot.NewChroot(writeableRootfsDir, true /*isExistingDir*/)
	if chroot == nil {
		return fmt.Errorf("failed to create a new chroot object for %s.", writeableRootfsDir)
	}
	defer chroot.Close(true /*leaveOnDisk*/)

	err := chroot.Initialize("", nil, nil, true /*includeDefaultMounts*/)
	if err != nil {
		return fmt.Errorf("failed to initialize chroot object for %s.\n%w", writeableRootfsDir, err)
	}

	err = chroot.Run(func() error {
		dracutParams := []string{
			initrdPathInChroot,
			"--kver", iae.artifacts.kernelVersion,
			"--filesystems", "squashfs",
			"--include", isoMakerArtifactsDirInChroot, isoMakerArtifactsDirInInitrd }

		return shell.ExecuteLive(false /*squashErrors*/, "dracut", dracutParams...)
	})
	if err != nil {
		return fmt.Errorf("failed to run dracut.\n%w", err)
	}

	artifactsInitrdPath := filepath.Join(iae.workingDirs.outDir, "initrd.img")
	err = copyFile(initrdPath, artifactsInitrdPath)
	if err != nil {
		return fmt.Errorf("failed to copy generated initrd.\n%w", err)
	}
	iae.artifacts.initrdPath = artifactsInitrdPath

	return nil
}

func createIsoConfig(isoRootfsPath string) (configuration.Config, error) {

	config := configuration.Config{
		SystemConfigs: []configuration.SystemConfig{
			{
				Name: "dummy-name",
				AdditionalFiles: map[string]configuration.FileConfigList{
					isoRootfsPath: {{Path: "/dummy-name"}},
				},
			},
		},
	}

	return config, nil
}

// invokes the iso maker library to create an iso image.
func createIso(buildDir, isoGrubFile, isoInitrdFile, isoRootfsFile, isoOutputDir, isoOutputBaseName string) error {

	logger.Log.Infof("--isohelpers.go - creating iso...")
	logger.Log.Infof("--isohelpers.go - - buildDir          = %s", buildDir)
	logger.Log.Infof("--isohelpers.go - - isoGrubFile       = %s", isoGrubFile)
	logger.Log.Infof("--isohelpers.go - - isoInitrdFile     = %s", isoInitrdFile)
	logger.Log.Infof("--isohelpers.go - - isoRootfsFile     = %s", isoRootfsFile)
	logger.Log.Infof("--isohelpers.go - - isoOutputDir      = %s", isoOutputDir)
	logger.Log.Infof("--isohelpers.go - - isoOutputBaseName = %s", isoOutputBaseName)

	unattendedInstall := false
	enableBiosBoot := false // if true, the bios bootloaders needs to be downloaded.
	baseDirPath := ""
	releaseVersion := ""
	isoResourcesDir := ""
	isoRepoDirPath := ""
	imageNameTag := ""

	config, err := createIsoConfig(isoRootfsFile)
	if err != nil {
		return err
	}

	err = os.MkdirAll(isoOutputDir, os.ModePerm)
	if err != nil {
		return err
	}

	// isoMaker constructs the final image name as follows:
	// {isoOutputDir}/{isoOutputBaseName}{releaseVersion}{imageNameTag}.iso

	isoMaker := isomakerlib.NewIsoMakerWithConfig(
		unattendedInstall,
		enableBiosBoot,
		baseDirPath,
		buildDir,
		releaseVersion,
		isoResourcesDir,
		config,
		isoInitrdFile,
		isoGrubFile,
		isoRepoDirPath,
		isoOutputDir,
		isoOutputBaseName,
		imageNameTag)

	isoMaker.Make()

	return nil
}

func (iae* IsoArtifactExtractor) extractIsoArtifactsFromBoot(bootDevicePath string, bootfsType string) (error) {

	logger.Log.Infof("extracting artifacts from the boot partition...")

	loopDevMountFullDir := filepath.Join(iae.workingDirs.buildDir, "readonly-boot-mount")
	logger.Log.Infof("--isohelpers.go - mounting %s(%s) to %s", bootDevicePath, bootfsType, loopDevMountFullDir)

	fullDiskBootMount, err := safemount.NewMount(bootDevicePath, loopDevMountFullDir, bootfsType, 0, "", true)
	if err != nil {
		return fmt.Errorf("failed to mount boot partition (%s):\n%w", bootDevicePath, err)
	}
	defer fullDiskBootMount.Close()

	sourceBootx64EfiPath := filepath.Join(loopDevMountFullDir, "/EFI/BOOT/bootx64.efi")
	iae.artifacts.bootx64EfiPath = filepath.Join(iae.workingDirs.outDir, "bootx64.efi")
	err = copyFile(sourceBootx64EfiPath, iae.artifacts.bootx64EfiPath)
	if err != nil {
		logger.Log.Infof("--isohelpers.go - extractIsoArtifactsFromBoot() - failed to copy %w", sourceBootx64EfiPath)
		return err
	}

	sourceGrubx64EfiPath := filepath.Join(loopDevMountFullDir, "/EFI/BOOT/grubx64.efi")
	iae.artifacts.grubx64EfiPath = filepath.Join(iae.workingDirs.outDir, "grubx64.efi")
	err = copyFile(sourceGrubx64EfiPath, iae.artifacts.grubx64EfiPath)
	if err != nil {
		logger.Log.Infof("--isohelpers.go - extractIsoArtifactsFromBoot() - failed to copy %w", sourceGrubx64EfiPath)
		return err
	}

	return nil
}

func (iae* IsoArtifactExtractor) populateWriteableRootfs(rootfsDevicePath, rootfsType, writeableRootfsDir string) (error) {

	logger.Log.Infof("creating writeable rootfs...")

	// -- mount .vhdx ---------------------------------------------------------

	srcLoopDevMountFullDir := filepath.Join(iae.workingDirs.buildDir, "readonly-rootfs-mount")
	logger.Log.Infof("--isohelpers.go - mounting %s(%s) to %s", rootfsDevicePath, rootfsType, srcLoopDevMountFullDir)

	srcLoopDevMount, err := safemount.NewMount(rootfsDevicePath, srcLoopDevMountFullDir, rootfsType, 0, "", true)
	if err != nil {
		return fmt.Errorf("failed to mount rootfs partition (%s):\n%w", rootfsDevicePath, err)
	}
	defer srcLoopDevMount.Close()

	err = os.MkdirAll(writeableRootfsDir, os.ModePerm)
	if err != nil {
		logger.Log.Infof("--isohelpers.go - failed to create folder %s", writeableRootfsDir)
		return err
	}

	logger.Log.Infof("--isohelpers.go - copying from %w to %w", srcLoopDevMountFullDir, writeableRootfsDir)
	cpParams := []string{"-aT", srcLoopDevMountFullDir, writeableRootfsDir}
	err = shell.ExecuteLive(false, "cp", cpParams...)
	if err != nil {
		logger.Log.Infof("--isohelpers.go - failed to copy rootfs contents to the writeable image.")
		return err
	}

	return nil
}

func (iae* IsoArtifactExtractor) stageIsoMakerInitrdArtifacts(writeableRootfsDir, isoMakerArtifactsDirInChroot string) (error) {

	logger.Log.Infof("staging isomaker artifacts into writeable image...")

	targetBootloadersRWImageDir:=filepath.Join(isoMakerArtifactsDirInChroot, "/efi/EFI/BOOT")
	targetBootloadersLocalDir := filepath.Join(writeableRootfsDir, targetBootloadersRWImageDir)

	err := os.MkdirAll(targetBootloadersLocalDir, os.ModePerm)
	if err != nil {
		logger.Log.Infof("--isohelpers.go - failed to create %w", targetBootloadersLocalDir)
		return err
	}

	sourceBoot64EfiFile := filepath.Join(iae.workingDirs.outDir, "bootx64.efi")
	targetBoot64EfiFile := filepath.Join(targetBootloadersLocalDir, "bootx64.efi")
	err = copyFile(sourceBoot64EfiFile, targetBoot64EfiFile)
	if err != nil {
		logger.Log.Infof("--isohelpers.go - failed to copy boot64.efi")
		return err
	}

	sourceGrub64EfiFile := filepath.Join(iae.workingDirs.outDir, "grubx64.efi")
	targetGrub64EfiFile := filepath.Join(targetBootloadersLocalDir, "grubx64.efi")
	err = copyFile(sourceGrub64EfiFile, targetGrub64EfiFile)
	if err != nil {
		logger.Log.Infof("--isohelpers.go - failed to copy grub64.efi")
		return err
	}

	targetVmlinuzRWImageDir := isoMakerArtifactsDirInChroot
	targetVmlinuzLocalDir := filepath.Join(writeableRootfsDir, targetVmlinuzRWImageDir)

	sourceVmlinuzFile := iae.artifacts.vmlinuzPath
	targetVmlinuzFile := filepath.Join(targetVmlinuzLocalDir, "vmlinuz")
	err = copyFile(sourceVmlinuzFile, targetVmlinuzFile)
	if err != nil {
		logger.Log.Infof("--isohelpers.go - failed to copy vmlinuz")
		return err
	}

	return nil
}

func (iae* IsoArtifactExtractor) prepareImageForDracut(writeableRootfsDir string) (error) {

	logger.Log.Infof("preparing writeable image for dracut...")

	fstabFile := filepath.Join(writeableRootfsDir, "/etc/fstab")
	logger.Log.Infof("--isohelpers.go - deleting fstab from %w", fstabFile)
	err := os.Remove(fstabFile)
	if err != nil {
		logger.Log.Infof("--isohelpers.go - failed to delete fstab. Error=%w", err)
		return err
	}

	sourceConfigFile := filepath.Join(iae.workingDirs.tmpDir, "20-live-cd.conf")

	logger.Log.Infof("--isohelpers.go - creating %s", sourceConfigFile)
	err = ioutil.WriteFile(sourceConfigFile, []byte(dracutConfig), 0644)
	if err != nil {
		logger.Log.Infof("--isohelpers.go - failed to create %s. Error:\n%w", sourceConfigFile, err)
		return err
	}

	targetConfigFile := filepath.Join(writeableRootfsDir, "/etc/dracut.conf.d/20-live-cd.conf")
	err = copyFile(sourceConfigFile, targetConfigFile)
	if err != nil {
		logger.Log.Infof("--isohelpers.go - failed to copy dracut config")
		return err
	}

	return nil
}

func (iae* IsoArtifactExtractor) createSquashfs(writeableRootfsDir string) (error) {

	logger.Log.Infof("creating squashfs of %w", writeableRootfsDir)

	generatedSquashfsFile := filepath.Join(iae.workingDirs.outDir, "rootfs.img")

	oldFileExists, err := fileExists(generatedSquashfsFile)
	if err == nil && oldFileExists {
		err = os.Remove(generatedSquashfsFile)
		if err != nil {
			logger.Log.Infof("--isohelpers.go - failed to delete squashfs")
			return err
		}
	}

	mksquashfsParams := []string{writeableRootfsDir, generatedSquashfsFile}
	err = shell.ExecuteLive(false, "mksquashfs", mksquashfsParams...)
	if err != nil {
		logger.Log.Infof("--isohelpers.go - failed to create squashfs")
		return err
	}

	iae.artifacts.squashfsPath = generatedSquashfsFile

	return nil
}

func (iae* IsoArtifactExtractor) convertToLiveOSImage(writeableRootfsDir, isoMakerArtifactsDirInChroot string) (error) {

	logger.Log.Infof("converting writeable image to be a LiveOS file system...")

	// -- determine kernel version --------------------------------------------

	kernelParentPath := filepath.Join(writeableRootfsDir, "/usr/lib/modules")
	logger.Log.Infof("--isohelpers.go - enumerating kernels under %w", kernelParentPath)
	kernelPaths, err := os.ReadDir(kernelParentPath)
	if err != nil {
		logger.Log.Infof("--isohelpers.go - failed to enumerate kernels.")
		return err
	}
	if len(kernelPaths) == 0 {
		logger.Log.Infof("--isohelpers.go - found 0 kernels.")
		return fmt.Errorf("found 0 kernels!")
	}
	// do we need to sort this?
	iae.artifacts.kernelVersion = kernelPaths[len(kernelPaths)-1].Name()
	logger.Log.Infof("--isohelpers.go - found kernel version (%s)", iae.artifacts.kernelVersion)	

	// -- extract grub.cfg and vmlinuz ----------------------------------------

	sourceGrubCfgPath := filepath.Join(writeableRootfsDir, "/boot/grub2/grub.cfg")
	targetGrubCfgPath := filepath.Join(iae.workingDirs.outDir, "grub.cfg")

	err = createGrubCfg(sourceGrubCfgPath, grubCfgTemplate, targetGrubCfgPath)
	if err != nil {
		logger.Log.Infof("--isohelpers.go - failed to create grub.cfg")
		return err
	}

	iae.artifacts.grubCfgPath = targetGrubCfgPath

	sourceVmlinuzPath := filepath.Join(writeableRootfsDir, "/boot/vmlinuz-" + iae.artifacts.kernelVersion)
	iae.artifacts.vmlinuzPath = filepath.Join(iae.workingDirs.outDir, "vmlinuz")
	err = copyFile(sourceVmlinuzPath, iae.artifacts.vmlinuzPath)
	if err != nil {
		logger.Log.Infof("--isohelpers.go - failed to copy vmlinuz")
		return err
	}

	// -- upload bootloaders and vmlinuz to make isomaker happy ---------------

	err = iae.stageIsoMakerInitrdArtifacts(writeableRootfsDir, isoMakerArtifactsDirInChroot)
	if err != nil {
		logger.Log.Infof("--isohelpers.go - failed to embed iso maker artifacts.")
		return err
	}

	// -- configure dracut ----------------------------------------------------

	err = iae.prepareImageForDracut(writeableRootfsDir)
	if err != nil {
		logger.Log.Infof("--isohelpers.go - failed to embed iso maker artifacts.")
		return err
	}
	// -- generate squashfs ---------------------------------------------------

	err = iae.createSquashfs(writeableRootfsDir)
	if err != nil {
		logger.Log.Infof("--isohelpers.go - failed to squashfs.")
		return err
	}

	return nil
}

func createGrubCfg(sourceGrubCfgPath, grubCfgTemplate, targetGrubCfgPath string) error {

	logger.Log.Infof("--isohelpers.go - using %s to create %s", sourceGrubCfgPath, targetGrubCfgPath)

	// ToDo: we should merge sourceGrubCfgPath with grubCfgTemplate
	err := ioutil.WriteFile(targetGrubCfgPath, []byte(grubCfgTemplate), 0644)
	if err != nil {
		return err
	}

	return nil
}

func copyFile(src, dst string) error {

	logger.Log.Infof("--isohelpers.go - copying %s to %s", src, dst)

	err := os.MkdirAll(filepath.Dir(dst), os.ModePerm)
	if err != nil {
		return err
	}

	return file.Copy(src, dst)
}

func fileExists(filePath string) (bool, error) {
	_, err := os.Stat(filePath)

	if err == nil {
		// File exists
		return true, nil
	} else if os.IsNotExist(err) {
		// File does not exist
		return false, nil
	} else {
		// An error occurred (other than file not existing)
		return false, err
	}
}