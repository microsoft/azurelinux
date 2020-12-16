// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Tool to create and install images

package main

import (
	"fmt"
	"os"
	"path/filepath"

	"gopkg.in/alecthomas/kingpin.v2"
	"microsoft.com/pkggen/imagegen/configuration"
	"microsoft.com/pkggen/imagegen/diskutils"
	"microsoft.com/pkggen/imagegen/installutils"
	"microsoft.com/pkggen/internal/exe"
	"microsoft.com/pkggen/internal/file"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/safechroot"
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
		isRootFS           bool
		isLoopDevice       bool
		isOfflineInstall   bool
		diskDevPath        string
		kernelPkg          string
		encryptedRoot      diskutils.EncryptedRootDevice
		partIDToDevPathMap map[string]string
		partIDToFsTypeMap  map[string]string
		extraMountPoints   []*safechroot.MountPoint
		extraDirectories   []string
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
	} else {
		logger.Log.Info("Creating raw disk in build directory")
		diskConfig := disks[defaultDiskIndex]
		diskDevPath, partIDToDevPathMap, partIDToFsTypeMap, isLoopDevice, encryptedRoot, err = setupDisk(buildDir, defaultTempDiskName, *liveInstallFlag, diskConfig, systemConfig.Encryption)
		if err != nil {
			return
		}

		// Add additional system settings for root encryption
		err = setupDiskEncryption(&systemConfig, &encryptedRoot, buildDir)
		if err != nil {
			return
		}

		if isLoopDevice {
			isOfflineInstall = true
			defer diskutils.DetachLoopbackDevice(diskDevPath)
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

	// Create Parition to Mountpoint map
	mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap := installutils.CreateMountPointPartitionMap(partIDToDevPathMap, partIDToFsTypeMap, systemConfig)

	if isOfflineInstall {
		// Create setup chroot
		additionalExtraMountPoints := []*safechroot.MountPoint{
			safechroot.NewMountPoint(*assets, assetsMountPoint, "", safechroot.BindMountPointFlags, ""),
			safechroot.NewMountPoint(*localRepo, localRepoMountPoint, "", safechroot.BindMountPointFlags, ""),
			safechroot.NewMountPoint(filepath.Dir(*repoFile), repoFileMountPoint, "", safechroot.BindMountPointFlags, ""),
		}
		extraMountPoints = append(extraMountPoints, additionalExtraMountPoints...)

		setupChrootDir := filepath.Join(buildDir, setupRoot)
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
			return buildImage(mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap, packagesToInstall, systemConfig, diskDevPath, isRootFS, encryptedRoot)
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
		err = installutils.ExtractPartitionArtifacts(outputDir, defaultDiskIndex, disks[defaultDiskIndex], partIDToDevPathMap)
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
		err = buildImage(mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap, packagesToInstall, systemConfig, diskDevPath, isRootFS, encryptedRoot)
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

func setupDisk(outputDir, diskName string, liveInstallFlag bool, diskConfig configuration.Disk, rootEncryption configuration.RootEncryption) (diskDevPath string, partIDToDevPathMap, partIDToFsTypeMap map[string]string, isLoopDevice bool, encryptedRoot diskutils.EncryptedRootDevice, err error) {
	const (
		realDiskType = "path"
	)
	if diskConfig.TargetDisk.Type == realDiskType {
		if liveInstallFlag {
			diskDevPath = diskConfig.TargetDisk.Value
			partIDToDevPathMap, partIDToFsTypeMap, encryptedRoot, err = setupRealDisk(diskDevPath, diskConfig, rootEncryption)
		} else {
			err = fmt.Errorf("target Disk Type is set but --live-install option is not set. Please check your config or enable the --live-install option")
			return
		}
	} else {
		diskDevPath, partIDToDevPathMap, partIDToFsTypeMap, encryptedRoot, err = setupLoopDeviceDisk(outputDir, diskName, diskConfig, rootEncryption)
		isLoopDevice = true
	}
	return
}

func setupLoopDeviceDisk(outputDir, diskName string, diskConfig configuration.Disk, rootEncryption configuration.RootEncryption) (diskDevPath string, partIDToDevPathMap, partIDToFsTypeMap map[string]string, encryptedRoot diskutils.EncryptedRootDevice, err error) {
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

	partIDToDevPathMap, partIDToFsTypeMap, encryptedRoot, err = setupRealDisk(diskDevPath, diskConfig, rootEncryption)
	if err != nil {
		logger.Log.Errorf("Failed to setup loopback disk partitions (%s)", rawDisk)
		return
	}

	return
}

func setupRealDisk(diskDevPath string, diskConfig configuration.Disk, rootEncryption configuration.RootEncryption) (partIDToDevPathMap, partIDToFsTypeMap map[string]string, encryptedRoot diskutils.EncryptedRootDevice, err error) {
	const (
		defaultBlockSize = diskutils.MiB
		noMaxSize        = 0
	)

	// Set up partitions
	partIDToDevPathMap, partIDToFsTypeMap, encryptedRoot, err = diskutils.CreatePartitions(diskDevPath, diskConfig, rootEncryption)
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

func buildImage(mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap map[string]string, packagesToInstall []string, systemConfig configuration.SystemConfig, diskDevPath string, isRootFS bool, encryptedRoot diskutils.EncryptedRootDevice) (err error) {
	const (
		installRoot       = "/installroot"
		emptyWorkerTar    = ""
		existingChrootDir = true
		leaveChrootOnDisk = true
	)

	var installMap map[string]string

	// Only invoke CreateInstallRoot for a raw disk. This call will result in mount points being created from a raw disk
	// into the install root. A rootfs will not have these.
	if !isRootFS {
		installMap, err = installutils.CreateInstallRoot(installRoot, mountPointMap, mountPointToMountArgsMap)
		if err != nil {
			err = fmt.Errorf("failed to create install root: %s", err)
			return
		}
		defer installutils.DestroyInstallRoot(installRoot, installMap)
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
	err = installutils.PopulateInstallRoot(installChroot, packagesToInstall, systemConfig, installMap, mountPointToFsTypeMap, mountPointToMountArgsMap, isRootFS, encryptedRoot)
	if err != nil {
		err = fmt.Errorf("failed to populate image contents: %s", err)
		return
	}

	// Only configure the bootloader for actual disks, a rootfs does not need one
	if !isRootFS {
		err = configureDiskBootloader(systemConfig, installChroot, diskDevPath, installMap, encryptedRoot)
	}

	return
}

func configureDiskBootloader(systemConfig configuration.SystemConfig, installChroot *safechroot.Chroot, diskDevPath string, installMap map[string]string, encryptedRoot diskutils.EncryptedRootDevice) (err error) {
	const rootMountPoint = "/"
	const bootMountPoint = "/boot"

	var rootDevice string

	// Add bootloader. Prefer a seperate boot partition if one exists.
	bootDevice, ok := installMap[bootMountPoint]
	bootPrefix := ""
	if !ok {
		bootDevice = installMap[rootMountPoint]
		// If we do not have a seperate boot partition we will need to add a prefix to all paths used in the configs.
		bootPrefix = "/boot"
	}
	bootUUID, err := installutils.GetUUID(bootDevice)
	if err != nil {
		err = fmt.Errorf("failed to get UUID: %s", err)
		return
	}

	bootType := systemConfig.BootType
	if systemConfig.Encryption.Enable && bootType == "legacy" {
		err = installutils.EnableCryptoDisk(installChroot)
		if err != nil {
			err = fmt.Errorf("Unable to enable crypto disk: %s", err)
			return
		}
	}

	err = installutils.InstallBootloader(installChroot, systemConfig.Encryption.Enable, bootType, bootUUID, bootPrefix, diskDevPath)
	if err != nil {
		err = fmt.Errorf("failed to install bootloader: %s", err)
		return
	}

	// Add grub config to image
	if systemConfig.Encryption.Enable {
		rootDevice = installMap[rootMountPoint]
	} else {
		var partUUID string
		partUUID, err = installutils.GetPartUUID(installMap[rootMountPoint])
		if err != nil {
			err = fmt.Errorf("failed to get PARTUUID: %s", err)
			return
		}

		rootDevice = fmt.Sprintf("PARTUUID=%v", partUUID)
	}

	err = installutils.InstallGrubCfg(installChroot.RootDir(), rootDevice, bootUUID, bootPrefix, encryptedRoot, systemConfig.KernelCommandLine)
	if err != nil {
		err = fmt.Errorf("failed to install main grub config file: %s", err)
		return
	}

	return
}
