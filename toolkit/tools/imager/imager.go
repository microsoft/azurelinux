// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Tool to create and install images

package main

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/installutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/customizationmacros"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/exe"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/timestamp"
	"github.com/microsoft/azurelinux/toolkit/tools/pkg/profile"

	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app             = kingpin.New("imager", "Tool to create and install images.")
	buildDir        = app.Flag("build-dir", "Directory to store temporary files while building.").ExistingDir()
	configFile      = exe.InputFlag(app, "Path to the image config file.")
	localRepo       = app.Flag("local-repo", "Path to local RPM repo").ExistingDir()
	tdnfTar         = app.Flag("tdnf-worker", "Path to tdnf worker tarball").ExistingFile()
	repoFile        = app.Flag("repo-file", "Full path to local.repo.").ExistingFile()
	assets          = app.Flag("assets", "Path to assets directory.").ExistingDir()
	baseDirPath     = app.Flag("base-dir", "Base directory for relative file paths from the config. Defaults to config's directory.").ExistingDir()
	outputDir       = app.Flag("output-dir", "Path to directory to place final image.").ExistingDir()
	imgContentFile  = app.Flag("output-image-contents", "File that stores list of packages used to compose the image.").String()
	liveInstallFlag = app.Flag("live-install", "Enable to perform a live install to the disk specified in config file.").Bool()
	emitProgress    = app.Flag("emit-progress", "Write progress updates to stdout, such as percent complete and current action.").Bool()
	timestampFile   = app.Flag("timestamp-file", "File that stores timestamps for this program.").String()
	buildNumber     = app.Flag("build-number", "Build number to be used in the image.").String()
	logFlags        = exe.SetupLogFlags(app)
	profFlags       = exe.SetupProfileFlags(app)
)

const (
	// additionalFilesTempDirectory is the location where installutils expects to pick up any additional files
	// to add to the install directory
	additionalFilesTempDirectory = "/tmp/additionalfiles"

	// postInstallScriptTempDirectory is the directory where installutils expects to pick up any post install scripts
	// to run inside the install directory environment
	postInstallScriptTempDirectory = "/tmp/postinstall"

	// finalizeImageScriptTempDirectory is the directory where installutils expects to pick up any finalize image scripts
	// to run inside the install directory environment
	finalizeImageScriptTempDirectory = "/tmp/finalizeimage"

	// sshPubKeysTempDirectory is the directory where installutils expects to pick up ssh public key files to add into
	// the install directory
	sshPubKeysTempDirectory = "/tmp/sshpubkeys"

	// kickstartPartitionFile is the file that includes the partitioning schema used by
	// kickstart installation
	kickstartPartitionFile = "/tmp/part-include"
)

func main() {
	const defaultSystemConfig = 0

	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(logFlags)

	prof, err := profile.StartProfiling(profFlags)
	if err != nil {
		logger.Log.Warnf("Could not start profiling: %s", err)
	}
	defer prof.StopProfiler()

	timestamp.BeginTiming("imager", *timestampFile)
	defer timestamp.CompleteTiming()

	if *emitProgress {
		installutils.EnableEmittingProgress()
	}

	// Parse Config
	config, err := configuration.LoadWithAbsolutePaths(*configFile, *baseDirPath)
	logger.PanicOnError(err, "Failed to load configuration file (%s) with base directory (%s)", *configFile, *baseDirPath)
	// Currently only process 1 system config
	systemConfig := config.SystemConfigs[defaultSystemConfig]

	// Execute preinstall scripts and parse partitioning when performing kickstart installation
	if systemConfig.IsKickStartBoot {
		timestamp.StartEvent("applying kickstart", nil)
		err = installutils.RunPreInstallScripts(systemConfig)
		logger.PanicOnError(err, "Failed to preinstall scripts")

		disks, partitionSettings, err := configuration.ParseKickStartPartitionScheme(kickstartPartitionFile)
		logger.PanicOnError(err, "Failed to parse partition schema")

		config.Disks = disks
		systemConfig.PartitionSettings = partitionSettings

		err = config.IsValid()
		if err != nil {
			logger.PanicOnError(err, "Invalid image configuration: %s", err)
		}
		timestamp.StopEvent(nil) // applying kickstart
	}

	err = buildSystemConfig(systemConfig, config.Disks, *outputDir, *buildDir, *imgContentFile)
	logger.PanicOnError(err, "Failed to build system configuration")
}

func buildSystemConfig(systemConfig configuration.SystemConfig, disks []configuration.Disk, outputDir, buildDir string, imgContentFile string) (err error) {
	logger.Log.Infof("Building system configuration (%s)", systemConfig.Name)
	timestamp.StartEvent("building system config", nil)
	defer timestamp.StopEvent(nil)

	const (
		localRepoMountPoint  = "/mnt/cdrom/RPMS"
		repoFileMountPoint   = "/etc/yum.repos.d"
		setupRoot            = "/setuproot"
		installRoot          = "/installroot"
		rootID               = "rootfs"
		defaultDiskIndex     = 0
		defaultTempDiskName  = "disk.raw"
		existingChrootDir    = false
		leaveChrootOnDisk    = false
		grub2Package         = "grub2"
		distroReleasePackage = "azurelinux-release"
	)

	var (
		isLoopDevice           bool
		isOfflineInstall       bool
		diskDevPath            string
		kernelPkg              string
		encryptedRoot          diskutils.EncryptedRootDevice
		readOnlyRoot           diskutils.VerityDevice
		partIDToDevPathMap     map[string]string
		partIDToFsTypeMap      map[string]string
		mountPointToOverlayMap map[string]*installutils.Overlay
		extraMountPoints       []*safechroot.MountPoint
		extraDirectories       []string
	)

	// Get list of packages to install into image
	packagesToInstall, err := installutils.PackageNamesFromSingleSystemConfig(systemConfig)
	if err != nil {
		err = fmt.Errorf("failed to import packages from package lists in config file:\n%w", err)
		return
	}

	// Azure Linux images don't work appropriately when azurelinux-release is not installed.
	// As a stopgap to this, azurelinux-release will now be added to all images regardless
	// of presence in the CONFIG_FILE
	packagesToInstall = append([]string{distroReleasePackage}, packagesToInstall...)

	if systemConfig.IsRootFS() {
		logger.Log.Infof("Creating rootfs")
		timestamp.StartEvent("creating rootfs", nil)
		defer timestamp.StopEvent(nil)
		additionalExtraMountPoints, additionalExtraDirectories, err := setupRootFS(outputDir, installRoot)
		if err != nil {
			return err
		}

		extraDirectories = append(extraDirectories, additionalExtraDirectories...)
		extraMountPoints = append(extraMountPoints, additionalExtraMountPoints...)
		isOfflineInstall = true

		// Select the best kernel package for this environment.
		kernelPkg, err = installutils.SelectKernelPackage(systemConfig, *liveInstallFlag)
		// Rootfs images will usually not set a kernel, ignore errors
		if err != nil {
			logger.Log.Debugf("Rootfs did not find a kernel, this is normal: '%s'", err.Error())
		} else {
			logger.Log.Infof("Rootfs is including a kernel (%s)", kernelPkg)
			packagesToInstall = append([]string{kernelPkg}, packagesToInstall...)
		}
	} else {
		timestamp.StartEvent("creating raw disk", nil)

		diskConfig := disks[defaultDiskIndex]
		diskDevPath, partIDToDevPathMap, partIDToFsTypeMap, isLoopDevice, encryptedRoot, readOnlyRoot, err = setupDisk(buildDir, defaultTempDiskName, *liveInstallFlag, diskConfig, systemConfig.Encryption, systemConfig.ReadOnlyVerityRoot)
		if err != nil {
			return
		}

		if isLoopDevice {
			isOfflineInstall = true
			defer diskutils.DetachLoopbackDevice(diskDevPath)
			defer diskutils.BlockOnDiskIO(diskDevPath)
		}

		if systemConfig.ReadOnlyVerityRoot.Enable {
			defer readOnlyRoot.CleanupVerityDevice()
		}

		// Add additional system settings for root encryption
		err = setupDiskEncryption(&systemConfig, &encryptedRoot, buildDir)
		if err != nil {
			return
		}

		// Select the best kernel package for this environment
		kernelPkg, err = installutils.SelectKernelPackage(systemConfig, *liveInstallFlag)
		if err != nil {
			err = fmt.Errorf("failed to select a suitable kernel to install in config (%s):\n%w", systemConfig.Name, err)
			return
		}

		logger.Log.Infof("Selected (%s) for the kernel", kernelPkg)
		packagesToInstall = append([]string{kernelPkg}, packagesToInstall...)
		timestamp.StopEvent(nil) // creating raw disk
	}

	setupChrootDir := filepath.Join(buildDir, setupRoot)

	// Create Parition to Mountpoint map
	mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap, diffDiskBuild := installutils.CreateMountPointPartitionMap(partIDToDevPathMap, partIDToFsTypeMap, systemConfig.PartitionSettings)
	if diffDiskBuild {
		timestamp.StartEvent("creating delta disk", nil)
		mountPointToOverlayMap, err = installutils.UpdatePartitionMapWithOverlays(partIDToDevPathMap, partIDToFsTypeMap, mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap, systemConfig)
		// Schedule unmount of overlays after the upper layers are unmounted.
		defer installutils.OverlayUnmount(mountPointToOverlayMap)
		if err != nil {
			err = fmt.Errorf("failed to create the partition map:\n%w", err)
			return
		}
		timestamp.StopEvent(nil) // creating delta disk
	}

	if isOfflineInstall {
		timestamp.StartEvent("create offline install env", nil)
		// Create setup chroot
		additionalExtraMountPoints := []*safechroot.MountPoint{
			safechroot.NewMountPoint(*localRepo, localRepoMountPoint, "", safechroot.BindMountPointFlags, ""),
			safechroot.NewMountPoint(filepath.Dir(*repoFile), repoFileMountPoint, "", safechroot.BindMountPointFlags, ""),
		}
		extraMountPoints = append(extraMountPoints, additionalExtraMountPoints...)

		setupChroot := safechroot.NewChroot(setupChrootDir, existingChrootDir)
		err = setupChroot.Initialize(*tdnfTar, extraDirectories, extraMountPoints, true)
		if err != nil {
			err = fmt.Errorf("failed to create setup chroot:\n%w", err)
			return
		}
		defer setupChroot.Close(leaveChrootOnDisk)

		// Before entering the chroot, copy in any and all host files needed and
		// fix up their paths to be in the tmp directory.
		err = fixupExtraFilesIntoChroot(setupChroot, &systemConfig)
		if err != nil {
			err = fmt.Errorf("failed to copy extra files into setup chroot:\n%w", err)
			return
		}

		timestamp.StopEvent(nil) // create offline install env

		err = setupChroot.Run(func() error {
			return buildImage(mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap, partIDToDevPathMap, partIDToFsTypeMap, mountPointToOverlayMap, packagesToInstall, systemConfig, diskDevPath, encryptedRoot, readOnlyRoot, diffDiskBuild, imgContentFile)
		})
		if err != nil {
			err = fmt.Errorf("failed to build image:\n%w", err)
			return
		}

		// Extract image package manifest from the 'setuproot' chroot
		err = setupChroot.MoveOutFile(installutils.PackageManifestRelativePath, imgContentFile)
		if err != nil {
			err = fmt.Errorf("failed to move files:\n%w", err)
			return
		}

		err = cleanupExtraFilesInChroot(setupChroot)
		if err != nil {
			err = fmt.Errorf("failed to cleanup extra files in setup chroot:\n%w", err)
			return
		}

		// Create any partition-based artifacts
		err = installutils.ExtractPartitionArtifacts(setupChrootDir, outputDir, defaultDiskIndex, disks[defaultDiskIndex], systemConfig, partIDToDevPathMap, mountPointToOverlayMap)
		if err != nil {
			return
		}

		// Copy disk artifact if necessary.
		// Currently only supports one disk config
		if !systemConfig.IsRootFS() {
			if disks[defaultDiskIndex].Artifacts != nil {
				input := filepath.Join(buildDir, defaultTempDiskName)
				output := filepath.Join(outputDir, fmt.Sprintf("disk%d.raw", defaultDiskIndex))
				err = file.Copy(input, output)
				if err != nil {
					return
				}
			}
		}
	} else {
		err = buildImage(mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap, partIDToDevPathMap, partIDToFsTypeMap, mountPointToOverlayMap, packagesToInstall, systemConfig, diskDevPath, encryptedRoot, readOnlyRoot, diffDiskBuild, imgContentFile)
		if err != nil {
			err = fmt.Errorf("failed to build image:\n%w", err)
			return
		}
	}

	// Cleanup encrypted disks
	if systemConfig.Encryption.Enable {
		err = diskutils.CleanupEncryptedDisks(encryptedRoot, isOfflineInstall)
		if err != nil {
			err = fmt.Errorf("failed to cleanup encrypted disks:\n%w", err)
			return
		}
	}

	return
}

func setupDiskEncryption(systemConfig *configuration.SystemConfig, encryptedRoot *diskutils.EncryptedRootDevice, keyFileDir string) (err error) {
	if systemConfig.Encryption.Enable {
		// Add a default keyfile for initramfs unlock
		encryptedRoot.HostKeyFile, err = diskutils.AddDefaultKeyfile(keyFileDir, encryptedRoot.Device, systemConfig.Encryption)
		if err != nil {
			err = fmt.Errorf("failed to add default keyfile:\n%w", err)
			return
		}

		// Copy the default keyfile into the image
		if len(systemConfig.AdditionalFiles) == 0 {
			systemConfig.AdditionalFiles = make(map[string]configuration.FileConfigList)
		}

		systemConfig.AdditionalFiles[encryptedRoot.HostKeyFile] = configuration.FileConfigList{{Path: diskutils.DefaultKeyFilePath}}
		logger.Log.Infof("Adding default key file to systemConfig additional files")
	}

	return
}

func setupRootFS(outputDir, installRoot string) (extraMountPoints []*safechroot.MountPoint, extraDirectories []string, err error) {
	const rootFSDirName = "rootfs"

	rootFSOutDir := filepath.Join(outputDir, rootFSDirName)

	// Ensure there is not already a directory at rootFSOutDir
	exists, err := file.DirExists(rootFSOutDir)
	logger.PanicOnError(err, "Failed while checking if directory (%s) exists.", rootFSOutDir)
	if exists {
		err = fmt.Errorf("output rootfs directory (%s) already exists", rootFSOutDir)
		return
	}

	err = os.MkdirAll(rootFSOutDir, os.ModePerm)
	if err != nil {
		return
	}

	// For a rootfs, bind-mount the output directory to the chroot directory being installed to
	rootFSMountPoint := safechroot.NewMountPoint(rootFSOutDir, installRoot, "", safechroot.BindMountPointFlags, "")
	extraMountPoints = []*safechroot.MountPoint{rootFSMountPoint}
	extraDirectories = []string{installRoot}

	return
}

func setupDisk(outputDir, diskName string, liveInstallFlag bool, diskConfig configuration.Disk, rootEncryption configuration.RootEncryption, readOnlyRootConfig configuration.ReadOnlyVerityRoot) (diskDevPath string, partIDToDevPathMap, partIDToFsTypeMap map[string]string, isLoopDevice bool, encryptedRoot diskutils.EncryptedRootDevice, readOnlyRoot diskutils.VerityDevice, err error) {
	const (
		realDiskType = "path"
	)
	if diskConfig.TargetDisk.Type == realDiskType {
		if liveInstallFlag {
			diskDevPath = diskConfig.TargetDisk.Value
			partIDToDevPathMap, partIDToFsTypeMap, encryptedRoot, readOnlyRoot, err = setupRealDisk(diskDevPath,
				diskConfig, rootEncryption, readOnlyRootConfig, false /*diskKnownToBeEmpty*/)
		} else {
			err = fmt.Errorf("target Disk Type is set but --live-install option is not set. Please check your config or enable the --live-install option")
			return
		}
	} else {
		diskDevPath, partIDToDevPathMap, partIDToFsTypeMap, encryptedRoot, readOnlyRoot, err = setupLoopDeviceDisk(outputDir, diskName, diskConfig, rootEncryption, readOnlyRootConfig)
		isLoopDevice = true
	}
	return
}

func setupLoopDeviceDisk(outputDir, diskName string, diskConfig configuration.Disk, rootEncryption configuration.RootEncryption, readOnlyRootConfig configuration.ReadOnlyVerityRoot) (diskDevPath string, partIDToDevPathMap, partIDToFsTypeMap map[string]string, encryptedRoot diskutils.EncryptedRootDevice, readOnlyRoot diskutils.VerityDevice, err error) {
	defer func() {
		// Detach the loopback device on failure
		if err != nil && diskDevPath != "" {
			detachErr := diskutils.DetachLoopbackDevice(diskDevPath)
			if detachErr != nil {
				logger.Log.Errorf("Failed to detach loopback device on failed initialization:\n%s", detachErr)
			}
		}
	}()

	// Create Raw Disk File
	rawDisk, err := diskutils.CreateEmptyDisk(outputDir, diskName, diskConfig.MaxSize)
	if err != nil {
		err = fmt.Errorf("failed to create empty disk file in (%s):\n%w", outputDir, err)
		return
	}

	diskDevPath, err = diskutils.SetupLoopbackDevice(rawDisk)
	if err != nil {
		err = fmt.Errorf("failed to mount raw disk (%s) as a loopback device:\n%w", rawDisk, err)
		return
	}

	partIDToDevPathMap, partIDToFsTypeMap, encryptedRoot, readOnlyRoot, err = setupRealDisk(diskDevPath, diskConfig,
		rootEncryption, readOnlyRootConfig, true /*diskKnownToBeEmpty*/)
	if err != nil {
		err = fmt.Errorf("failed to setup loopback disk partitions (%s):\n%w", rawDisk, err)
		return
	}

	return
}

func setupRealDisk(diskDevPath string, diskConfig configuration.Disk, rootEncryption configuration.RootEncryption,
	readOnlyRootConfig configuration.ReadOnlyVerityRoot, diskKnownToBeEmpty bool,
) (partIDToDevPathMap, partIDToFsTypeMap map[string]string, encryptedRoot diskutils.EncryptedRootDevice, readOnlyRoot diskutils.VerityDevice, err error) {
	// Set up partitions
	partIDToDevPathMap, partIDToFsTypeMap, encryptedRoot, readOnlyRoot, err = diskutils.CreatePartitions(diskDevPath,
		diskConfig, rootEncryption, readOnlyRootConfig, diskKnownToBeEmpty)
	if err != nil {
		err = fmt.Errorf("failed to create partitions on disk (%s):\n%w", diskDevPath, err)
		return
	}

	// Apply firmware
	err = diskutils.ApplyRawBinaries(diskDevPath, diskConfig)
	if err != nil {
		err = fmt.Errorf("failed to add add raw binaries to disk (%s):\n%w", diskDevPath, err)
		return
	}

	return
}

// fixupExtraFilesIntoChroot will copy extra files needed for the build
// into the chroot and alter the extra files in the config to point at their new paths.
func fixupExtraFilesIntoChroot(installChroot *safechroot.Chroot, config *configuration.SystemConfig) (err error) {
	var filesToCopy []safechroot.FileToCopy

	for i, user := range config.Users {
		for j, pubKey := range user.SSHPubKeyPaths {
			newFilePath := filepath.Join(sshPubKeysTempDirectory, pubKey)

			fileToCopy := safechroot.FileToCopy{
				Src:  pubKey,
				Dest: newFilePath,
			}

			config.Users[i].SSHPubKeyPaths[j] = newFilePath
			filesToCopy = append(filesToCopy, fileToCopy)
		}
	}

	fixedUpAdditionalFiles := make(map[string]configuration.FileConfigList)
	for srcFile, dstFileConfigs := range config.AdditionalFiles {
		newFilePath := filepath.Join(additionalFilesTempDirectory, srcFile)

		fileToCopy := safechroot.FileToCopy{
			Src:  srcFile,
			Dest: newFilePath,
		}

		fixedUpAdditionalFiles[newFilePath] = dstFileConfigs
		filesToCopy = append(filesToCopy, fileToCopy)
	}
	config.AdditionalFiles = fixedUpAdditionalFiles

	for i, script := range config.PostInstallScripts {
		newFilePath := filepath.Join(postInstallScriptTempDirectory, script.Path)

		fileToCopy := safechroot.FileToCopy{
			Src:  script.Path,
			Dest: newFilePath,
		}

		config.PostInstallScripts[i].Path = newFilePath
		filesToCopy = append(filesToCopy, fileToCopy)
	}

	for i, script := range config.FinalizeImageScripts {
		newFilePath := filepath.Join(finalizeImageScriptTempDirectory, script.Path)

		fileToCopy := safechroot.FileToCopy{
			Src:  script.Path,
			Dest: newFilePath,
		}

		config.FinalizeImageScripts[i].Path = newFilePath
		filesToCopy = append(filesToCopy, fileToCopy)
	}

	err = installChroot.AddFiles(filesToCopy...)
	return
}

func cleanupExtraFiles() (err error) {
	dirsToRemove := []string{additionalFilesTempDirectory, postInstallScriptTempDirectory, finalizeImageScriptTempDirectory, sshPubKeysTempDirectory}

	for _, dir := range dirsToRemove {
		logger.Log.Infof("Cleaning up directory %s", dir)
		err = os.RemoveAll(dir)
		if err != nil {
			err = fmt.Errorf("failed to cleanup directory (%s):\n%w", dir, err)
			return
		}
	}
	return
}

func cleanupExtraFilesInChroot(chroot *safechroot.Chroot) (err error) {
	logger.Log.Infof("Proceeding to cleanup extra files in chroot %s.", chroot.RootDir())
	err = chroot.Run(func() error {
		return cleanupExtraFiles()
	})
	return
}

func buildImage(mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap, partIDToDevPathMap, partIDToFsTypeMap map[string]string, mountPointToOverlayMap map[string]*installutils.Overlay, packagesToInstall []string, systemConfig configuration.SystemConfig, diskDevPath string, encryptedRoot diskutils.EncryptedRootDevice, readOnlyRoot diskutils.VerityDevice, diffDiskBuild bool, imgContentFile string) (err error) {
	timestamp.StartEvent("building image", nil)
	defer timestamp.StopEvent(nil)
	const (
		installRoot       = "/installroot"
		verityWorkingDir  = "verityworkingdir"
		emptyWorkerTar    = ""
		rootDir           = "/"
		existingChrootDir = true
		leaveChrootOnDisk = true
	)

	var mountList []string

	// Only invoke CreateInstallRoot for a raw disk. This call will result in mount points being created from a raw disk
	// into the install root. A rootfs will not have these.
	if !systemConfig.IsRootFS() {
		mountList, err = installutils.CreateInstallRoot(installRoot, mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap, mountPointToOverlayMap)
		if err != nil {
			err = fmt.Errorf("failed to create install root:\n%w", err)
			return
		}
		defer installutils.DestroyInstallRoot(installRoot, mountList, mountPointMap, mountPointToOverlayMap)
	}

	// Install any tools required for the setup root to function
	setupChrootPackages := []string{}
	toolingPackages := installutils.GetRequiredPackagesForInstall()
	for _, toolingPackage := range toolingPackages {
		setupChrootPackages = append(setupChrootPackages, toolingPackage.Name)
	}

	if systemConfig.ReadOnlyVerityRoot.Enable {
		// We will need the veritysetup package (and its dependencies) to manage the verity disk, add them to our
		// image setup environment (setuproot chroot or live installer).
		verityPackages := []string{"device-mapper", "veritysetup"}
		setupChrootPackages = append(setupChrootPackages, verityPackages...)
	}

	// Create new chroot for the new image
	installChroot := safechroot.NewChroot(installRoot, existingChrootDir)
	extraInstallMountPoints := []*safechroot.MountPoint{}
	extraDirectories := []string{}
	err = installChroot.Initialize(emptyWorkerTar, extraDirectories, extraInstallMountPoints, true)
	if err != nil {
		err = fmt.Errorf("failed to create install chroot:\n%w", err)
		return
	}
	defer installChroot.Close(leaveChrootOnDisk)

	// Update package repo files for upcoming package installation
	if len(systemConfig.PackageRepos) > 0 {
		if systemConfig.IsIsoInstall {
			err = configuration.UpdatePackageRepo(installChroot, systemConfig)
			if err != nil {
				return
			}
		} else {
			return fmt.Errorf("custom package repos should not be specified unless performing ISO installation")
		}
	}

	timestamp.StartEvent("install chroot packages", nil)
	for _, setupChrootPackage := range setupChrootPackages {
		_, err = installutils.TdnfInstall(setupChrootPackage, rootDir)
		if err != nil {
			err = fmt.Errorf("failed to install required setup chroot package (%s):\n%w", setupChrootPackage, err)
			return
		}
	}
	timestamp.StopEvent(nil) // install chroot packages

	// Configure rpm install macros for the setup environment. We run 'rpm' from outside the install chroot since it starts
	// empty. So the macros must be defined here before we install packages.
	logger.Log.Debugf("Adding setup environment customization macros if needed")
	err = customizationmacros.AddCustomizationMacros(rootDir, systemConfig.DisableRpmDocs,
		systemConfig.OverrideRpmLocales)
	if err != nil {
		err = fmt.Errorf("failed to add setup environment customization macros:\n%w", err)
		return
	}

	// Populate image contents
	err = installutils.PopulateInstallRoot(installChroot, packagesToInstall, systemConfig, mountList, mountPointMap,
		mountPointToFsTypeMap, mountPointToMountArgsMap, partIDToDevPathMap, partIDToFsTypeMap, encryptedRoot,
		diffDiskBuild)
	if err != nil {
		err = fmt.Errorf("failed to populate image contents:\n%w", err)
		return
	}

	err = installutils.AddImageIDFile(installChroot.RootDir(), *buildNumber)
	if err != nil {
		err = fmt.Errorf("failed to add image ID file:\n%w", err)
		return
	}

	// Configure the final image with the customized macros so that rpm continues to behave the same way in the final image
	logger.Log.Infof("Adding final image customization macros if needed")
	err = customizationmacros.AddCustomizationMacros(installChroot.RootDir(), systemConfig.DisableRpmDocs,
		systemConfig.OverrideRpmLocales)
	if err != nil {
		err = fmt.Errorf("failed to add final image customization macros:\n%w", err)
		return
	}

	// Only configure the bootloader or read only partitions for actual disks, a rootfs does not need these
	if !systemConfig.IsRootFS() {
		err = installutils.ConfigureDiskBootloader(systemConfig.BootType, systemConfig.Encryption.Enable,
			systemConfig.ReadOnlyVerityRoot.Enable, systemConfig.PartitionSettings, systemConfig.KernelCommandLine,
			installChroot, diskDevPath, mountPointMap, encryptedRoot, readOnlyRoot,
			systemConfig.EnableGrubMkconfig, false)
		if err != nil {
			err = fmt.Errorf("failed to configure boot loader:\n%w", err)
			return
		}
	}

	// Preconfigure SELinux labels now since all the changes to the filesystem should be done
	if systemConfig.KernelCommandLine.SELinux != configuration.SELinuxOff {
		err = installutils.SELinuxConfigure(systemConfig.KernelCommandLine.SELinux, installChroot,
			mountPointToFsTypeMap, systemConfig.IsRootFS())
		if err != nil {
			err = fmt.Errorf("failed to configure selinux:\n%w", err)
			return
		}
	}

	// Snapshot the root filesystem as a read-only verity disk and update the initramfs.
	if !systemConfig.IsRootFS() && systemConfig.ReadOnlyVerityRoot.Enable {
		timestamp.StartEvent("configure DM Verity", nil)
		var initramfsPathList []string
		err = readOnlyRoot.SwitchDeviceToReadOnly(mountPointMap["/"], mountPointToMountArgsMap["/"])
		if err != nil {
			err = fmt.Errorf("failed to switch root to read-only:\n%w", err)
			return
		}
		installutils.ReportAction("Hashing root for read-only with dm-verity, this may take a long time if error correction is enabled")
		initramfsPathList, err = filepath.Glob(filepath.Join(installRoot, "/boot/initramfs-*.img"))
		if err != nil || len(initramfsPathList) != 1 {
			return fmt.Errorf("could not find single initramfs (%v):\n%w", initramfsPathList, err)
		}
		err = readOnlyRoot.AddRootVerityFilesToInitramfs(verityWorkingDir, initramfsPathList[0])
		if err != nil {
			err = fmt.Errorf("failed to include read-only root files in initramfs:\n%w", err)
			return
		}
		timestamp.StopEvent(nil) // configure DM Verity
	}

	// Run finalize image scripts from within the installroot chroot
	err = installutils.RunFinalizeImageScripts(installChroot, systemConfig)
	if err != nil {
		err = fmt.Errorf("failed to run finalize image script:\n%w", err)
		return
	}

	return
}
