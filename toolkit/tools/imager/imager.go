// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Tool to create and install images

package main

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/installutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"

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
	liveInstallFlag = app.Flag("live-install", "Enable to perform a live install to the disk specified in config file.").Bool()
	emitProgress    = app.Flag("emit-progress", "Write progress updates to stdout, such as percent complete and current action.").Bool()
	logFile         = exe.LogFileFlag(app)
	logLevel        = exe.LogLevelFlag(app)
)

const (
	// additionalFilesTempDirectory is the location where installutils expects to pick up any additional files
	// to add to the install directory
	additionalFilesTempDirectory = "/tmp/additionalfiles"

	// postInstallScriptTempDirectory is the directory where installutils expects to pick up any post install scripts
	// to run inside the install directory environment
	postInstallScriptTempDirectory = "/tmp/postinstall"

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

	logger.InitBestEffort(*logFile, *logLevel)

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
	}

	err = buildSystemConfig(systemConfig, config.Disks, *outputDir, *buildDir)
	logger.PanicOnError(err, "Failed to build system configuration")

}

func buildSystemConfig(systemConfig configuration.SystemConfig, disks []configuration.Disk, outputDir, buildDir string) (err error) {
	logger.Log.Infof("Building system configuration (%s)", systemConfig.Name)

	const (
		assetsMountPoint    = "/installer"
		localRepoMountPoint = "/mnt/cdrom/RPMS"
		repoFileMountPoint  = "/etc/yum.repos.d"
		setupRoot           = "/setuproot"
		installRoot         = "/installroot"
		rootID              = "rootfs"
		defaultDiskIndex    = 0
		defaultTempDiskName = "disk.raw"
		existingChrootDir   = false
		leaveChrootOnDisk   = false
	)

	var (
		isRootFS               bool
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
		logger.Log.Error("Failed to import packages from package lists in config file")
		return
	}

	isRootFS = len(systemConfig.PartitionSettings) == 0
	if isRootFS {
		logger.Log.Infof("Creating rootfs")
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
		logger.Log.Info("Creating raw disk in build directory")
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
			logger.Log.Errorf("Failed to select a suitable kernel to install in config (%s)", systemConfig.Name)
			return
		}

		logger.Log.Infof("Selected (%s) for the kernel", kernelPkg)
		packagesToInstall = append([]string{kernelPkg}, packagesToInstall...)
	}

	setupChrootDir := filepath.Join(buildDir, setupRoot)

	// Create Parition to Mountpoint map
	mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap, diffDiskBuild := installutils.CreateMountPointPartitionMap(partIDToDevPathMap, partIDToFsTypeMap, systemConfig)
	if diffDiskBuild {
		mountPointToOverlayMap, err = installutils.UpdatePartitionMapWithOverlays(partIDToDevPathMap, partIDToFsTypeMap, mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap, systemConfig)
		// Schedule unmount of overlays after the upper layers are unmounted.
		defer installutils.OverlayUnmount(mountPointToOverlayMap)
		if err != nil {
			logger.Log.Error("Failed to create the partition map")
			return
		}
	}

	if isOfflineInstall {
		// Create setup chroot
		additionalExtraMountPoints := []*safechroot.MountPoint{
			safechroot.NewMountPoint(*assets, assetsMountPoint, "", safechroot.BindMountPointFlags, ""),
			safechroot.NewMountPoint(*localRepo, localRepoMountPoint, "", safechroot.BindMountPointFlags, ""),
			safechroot.NewMountPoint(filepath.Dir(*repoFile), repoFileMountPoint, "", safechroot.BindMountPointFlags, ""),
		}
		extraMountPoints = append(extraMountPoints, additionalExtraMountPoints...)

		setupChroot := safechroot.NewChroot(setupChrootDir, existingChrootDir)
		err = setupChroot.Initialize(*tdnfTar, extraDirectories, extraMountPoints)
		if err != nil {
			logger.Log.Error("Failed to create setup chroot")
			return
		}
		defer setupChroot.Close(leaveChrootOnDisk)

		// Before entering the chroot, copy in any and all host files needed and
		// fix up their paths to be in the tmp directory.
		err = fixupExtraFilesIntoChroot(setupChroot, &systemConfig)
		if err != nil {
			logger.Log.Error("Failed to copy extra files into setup chroot")
			return
		}

		err = setupChroot.Run(func() error {
			return buildImage(mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap, partIDToDevPathMap, mountPointToOverlayMap, packagesToInstall, systemConfig, diskDevPath, isRootFS, encryptedRoot, readOnlyRoot, diffDiskBuild)
		})
		if err != nil {
			logger.Log.Error("Failed to build image")
			return
		}

		err = cleanupExtraFilesInChroot(setupChroot)
		if err != nil {
			logger.Log.Error("Failed to cleanup extra files in setup chroot")
			return
		}

		// Create any partition-based artifacts
		err = installutils.ExtractPartitionArtifacts(setupChrootDir, outputDir, defaultDiskIndex, disks[defaultDiskIndex], systemConfig, partIDToDevPathMap, mountPointToOverlayMap)
		if err != nil {
			return
		}

		// Copy disk artifact if necessary.
		// Currently only supports one disk config
		if !isRootFS {
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
		err = buildImage(mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap, partIDToDevPathMap, mountPointToOverlayMap, packagesToInstall, systemConfig, diskDevPath, isRootFS, encryptedRoot, readOnlyRoot, diffDiskBuild)
		if err != nil {
			logger.Log.Error("Failed to build image")
			return
		}
	}

	// Cleanup encrypted disks
	if systemConfig.Encryption.Enable {
		err = diskutils.CleanupEncryptedDisks(encryptedRoot, isOfflineInstall)
		if err != nil {
			logger.Log.Warn("Failed to cleanup encrypted disks")
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
			logger.Log.Warnf("Failed to add default keyfile: %v", err)
			return
		}

		// Copy the default keyfile into the image
		if len(systemConfig.AdditionalFiles) == 0 {
			systemConfig.AdditionalFiles = make(map[string]string)
		}

		systemConfig.AdditionalFiles[encryptedRoot.HostKeyFile] = diskutils.DefaultKeyFilePath
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
			partIDToDevPathMap, partIDToFsTypeMap, encryptedRoot, readOnlyRoot, err = setupRealDisk(diskDevPath, diskConfig, rootEncryption, readOnlyRootConfig)
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
				logger.Log.Errorf("Failed to detach loopback device on failed initialization. Error: %s", detachErr)
			}
		}
	}()

	// Create Raw Disk File
	rawDisk, err := diskutils.CreateEmptyDisk(outputDir, diskName, diskConfig)
	if err != nil {
		logger.Log.Errorf("Failed to create empty disk file in (%s)", outputDir)
		return
	}

	diskDevPath, err = diskutils.SetupLoopbackDevice(rawDisk)
	if err != nil {
		logger.Log.Errorf("Failed to mount raw disk (%s) as a loopback device", rawDisk)
		return
	}

	partIDToDevPathMap, partIDToFsTypeMap, encryptedRoot, readOnlyRoot, err = setupRealDisk(diskDevPath, diskConfig, rootEncryption, readOnlyRootConfig)
	if err != nil {
		logger.Log.Errorf("Failed to setup loopback disk partitions (%s)", rawDisk)
		return
	}

	return
}

func setupRealDisk(diskDevPath string, diskConfig configuration.Disk, rootEncryption configuration.RootEncryption, readOnlyRootConfig configuration.ReadOnlyVerityRoot) (partIDToDevPathMap, partIDToFsTypeMap map[string]string, encryptedRoot diskutils.EncryptedRootDevice, readOnlyRoot diskutils.VerityDevice, err error) {
	const (
		defaultBlockSize = diskutils.MiB
		noMaxSize        = 0
	)

	// Set up partitions
	partIDToDevPathMap, partIDToFsTypeMap, encryptedRoot, readOnlyRoot, err = diskutils.CreatePartitions(diskDevPath, diskConfig, rootEncryption, readOnlyRootConfig)
	if err != nil {
		logger.Log.Errorf("Failed to create partitions on disk (%s)", diskDevPath)
		return
	}

	// Apply firmware
	err = diskutils.ApplyRawBinaries(diskDevPath, diskConfig)
	if err != nil {
		logger.Log.Errorf("Failed to add add raw binaries to disk (%s)", diskDevPath)
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

	fixedUpAdditionalFiles := make(map[string]string)
	for srcFile, dstFile := range config.AdditionalFiles {
		newFilePath := filepath.Join(additionalFilesTempDirectory, srcFile)

		fileToCopy := safechroot.FileToCopy{
			Src:  srcFile,
			Dest: newFilePath,
		}

		fixedUpAdditionalFiles[newFilePath] = dstFile
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

	err = installChroot.AddFiles(filesToCopy...)
	return
}

func cleanupExtraFiles() (err error) {
	dirsToRemove := []string{additionalFilesTempDirectory, postInstallScriptTempDirectory, sshPubKeysTempDirectory}

	for _, dir := range dirsToRemove {
		logger.Log.Infof("Cleaning up directory %s", dir)
		err = os.RemoveAll(dir)
		if err != nil {
			logger.Log.Warnf("Failed to cleanup directory (%s). Error: %s", dir, err)
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
func buildImage(mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap, partIDToDevPathMap map[string]string, mountPointToOverlayMap map[string]*installutils.Overlay, packagesToInstall []string, systemConfig configuration.SystemConfig, diskDevPath string, isRootFS bool, encryptedRoot diskutils.EncryptedRootDevice, readOnlyRoot diskutils.VerityDevice, diffDiskBuild bool) (err error) {
	const (
		installRoot       = "/installroot"
		verityWorkingDir  = "verityworkingdir"
		emptyWorkerTar    = ""
		rootDir           = "/"
		existingChrootDir = true
		leaveChrootOnDisk = true
	)

	var installMap map[string]string

	// Only invoke CreateInstallRoot for a raw disk. This call will result in mount points being created from a raw disk
	// into the install root. A rootfs will not have these.
	if !isRootFS {
		installMap, err = installutils.CreateInstallRoot(installRoot, mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap, mountPointToOverlayMap)
		if err != nil {
			err = fmt.Errorf("failed to create install root: %s", err)
			return
		}
		defer installutils.DestroyInstallRoot(installRoot, installMap, mountPointToOverlayMap)
	}

	// Install any tools required for the setup root to function
	setupChrootPackages := []string{}
	toolingPackages := installutils.GetRequiredPackagesForInstall()
	for _, toolingPackage := range toolingPackages {
		setupChrootPackages = append(setupChrootPackages, toolingPackage.Name)
	}

	logger.Log.Infof("HidepidDisabled is %v.", systemConfig.HidepidDisabled)
	hidepidEnabled := !systemConfig.HidepidDisabled

	if systemConfig.ReadOnlyVerityRoot.Enable {
		// We will need the veritysetup package (and its dependencies) to manage the verity disk, add them to our
		// image setup environment (setuproot chroot or live installer).
		verityPackages := []string{"device-mapper", "veritysetup"}
		setupChrootPackages = append(setupChrootPackages, verityPackages...)
	}

	for _, setupChrootPackage := range setupChrootPackages {
		_, err = installutils.TdnfInstall(setupChrootPackage, rootDir)
		if err != nil {
			err = fmt.Errorf("failed to install required setup chroot package '%s': %w", setupChrootPackage, err)
			return
		}
	}

	// Create new chroot for the new image
	installChroot := safechroot.NewChroot(installRoot, existingChrootDir)
	extraInstallMountPoints := []*safechroot.MountPoint{}
	extraDirectories := []string{}
	err = installChroot.Initialize(emptyWorkerTar, extraDirectories, extraInstallMountPoints)
	if err != nil {
		err = fmt.Errorf("failed to create install chroot: %s", err)
		return
	}
	defer installChroot.Close(leaveChrootOnDisk)

	// Populate image contents
	err = installutils.PopulateInstallRoot(installChroot, packagesToInstall, systemConfig, installMap, mountPointToFsTypeMap, mountPointToMountArgsMap, partIDToDevPathMap, isRootFS, encryptedRoot, diffDiskBuild, hidepidEnabled)
	if err != nil {
		err = fmt.Errorf("failed to populate image contents: %s", err)
		return
	}

	// Only configure the bootloader or read only partitions for actual disks, a rootfs does not need these
	if !isRootFS {
		err = configureDiskBootloader(systemConfig, installChroot, diskDevPath, installMap, encryptedRoot, readOnlyRoot)
		if err != nil {
			err = fmt.Errorf("failed to configure boot loader: %w", err)
			return
		}

		// Preconfigure SELinux labels now since all the changes to the filesystem should be done
		if systemConfig.KernelCommandLine.SELinux != configuration.SELinuxOff {
			err = installutils.SELinuxConfigure(systemConfig, installChroot, mountPointToFsTypeMap)
			if err != nil {
				err = fmt.Errorf("failed to configure selinux: %w", err)
				return
			}
		}

		// Snapshot the root filesystem as a read-only verity disk and update the initramfs.
		if systemConfig.ReadOnlyVerityRoot.Enable {
			var initramfsPathList []string
			err = readOnlyRoot.SwitchDeviceToReadOnly(mountPointMap["/"], mountPointToMountArgsMap["/"])
			if err != nil {
				err = fmt.Errorf("failed to switch root to read-only: %w", err)
				return
			}
			installutils.ReportAction("Hashing root for read-only with dm-verity, this may take a long time if error correction is enabled")
			initramfsPathList, err = filepath.Glob(filepath.Join(installRoot, "/boot/initrd.img*"))
			if err != nil || len(initramfsPathList) != 1 {
				return fmt.Errorf("could not find single initramfs (%v): %w", initramfsPathList, err)
			}
			err = readOnlyRoot.AddRootVerityFilesToInitramfs(verityWorkingDir, initramfsPathList[0])
			if err != nil {
				err = fmt.Errorf("failed to include read-only root files in initramfs: %w", err)
				return
			}
		}
	}

	return
}

func configureDiskBootloader(systemConfig configuration.SystemConfig, installChroot *safechroot.Chroot, diskDevPath string, installMap map[string]string, encryptedRoot diskutils.EncryptedRootDevice, readOnlyRoot diskutils.VerityDevice) (err error) {
	const rootMountPoint = "/"
	const bootMountPoint = "/boot"

	var rootDevice string

	// Add bootloader. Prefer a separate boot partition if one exists.
	bootDevice, ok := installMap[bootMountPoint]
	bootPrefix := ""
	if !ok {
		bootDevice = installMap[rootMountPoint]
		// If we do not have a separate boot partition we will need to add a prefix to all paths used in the configs.
		bootPrefix = "/boot"
	}

	if installMap[rootMountPoint] == installutils.NullDevice {
		// In case of overlay device being mounted at root, no need to change the bootloader.
		return
	}

	// Grub only accepts UUID, not PARTUUID or PARTLABEL
	bootUUID, err := installutils.GetUUID(bootDevice)
	if err != nil {
		err = fmt.Errorf("failed to get UUID: %s", err)
		return
	}

	bootType := systemConfig.BootType
	err = installutils.InstallBootloader(installChroot, systemConfig.Encryption.Enable, bootType, bootUUID, bootPrefix, diskDevPath)
	if err != nil {
		err = fmt.Errorf("failed to install bootloader: %s", err)
		return
	}

	// Add grub config to image
	rootPartitionSetting := systemConfig.GetRootPartitionSetting()
	if rootPartitionSetting == nil {
		err = fmt.Errorf("failed to find partition setting for root mountpoint")
		return
	}
	rootMountIdentifier := rootPartitionSetting.MountIdentifier
	if systemConfig.Encryption.Enable {
		// Encrypted devices don't currently support identifiers
		rootDevice = installMap[rootMountPoint]
	} else if systemConfig.ReadOnlyVerityRoot.Enable {
		var partIdentifier string
		partIdentifier, err = installutils.FormatMountIdentifier(rootMountIdentifier, readOnlyRoot.BackingDevice)
		if err != nil {
			err = fmt.Errorf("failed to get partIdentifier: %s", err)
			return
		}
		rootDevice = fmt.Sprintf("verityroot:%v", partIdentifier)
	} else {
		var partIdentifier string
		partIdentifier, err = installutils.FormatMountIdentifier(rootMountIdentifier, installMap[rootMountPoint])
		if err != nil {
			err = fmt.Errorf("failed to get partIdentifier: %s", err)
			return
		}

		rootDevice = partIdentifier
	}

	// Grub will always use filesystem UUID, never PARTUUID or PARTLABEL
	err = installutils.InstallGrubCfg(installChroot.RootDir(), rootDevice, bootUUID, bootPrefix, encryptedRoot, systemConfig.KernelCommandLine, readOnlyRoot)
	if err != nil {
		err = fmt.Errorf("failed to install main grub config file: %s", err)
		return
	}

	return
}
