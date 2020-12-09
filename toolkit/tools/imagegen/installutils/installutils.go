// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package installutils

import (
	"crypto/rand"
	"fmt"
	"os"
	"path"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
	"syscall"
	"time"

	"microsoft.com/pkggen/imagegen/configuration"
	"microsoft.com/pkggen/imagegen/diskutils"
	"microsoft.com/pkggen/internal/file"
	"microsoft.com/pkggen/internal/jsonutils"
	"microsoft.com/pkggen/internal/logger"
	"microsoft.com/pkggen/internal/pkgjson"
	"microsoft.com/pkggen/internal/retry"
	"microsoft.com/pkggen/internal/safechroot"
	"microsoft.com/pkggen/internal/shell"
)

const (
	rootMountPoint = "/"
	rootUser       = "root"

	// /boot directory should be only accesible by root. The directories need the execute bit as well.
	bootDirectoryFileMode = 0600
	bootDirectoryDirMode  = 0700
)

// PackageList represents the list of packages to install into an image
type PackageList struct {
	Packages []string `json:"packages"`
}

// CreateMountPointPartitionMap creates a map between the mountpoint supplied in the config file and the device path
// of the partition
// - partDevPathMap is a map of partition IDs to partition device paths
// - partIDToFsTypeMap is a map of partition IDs to filesystem type
// - config is the SystemConfig from a config file
// Output
// - mountPointDevPathMap is a map of mountpoint to partition device path
// - mountPointToFsTypeMap is a map of mountpoint to filesystem type
// - mountPointToMountArgsMap is a map of mountpoint to mount arguments to be passed on a call to mount
func CreateMountPointPartitionMap(partDevPathMap, partIDToFsTypeMap map[string]string, config configuration.SystemConfig) (mountPointDevPathMap, mountPointToFsTypeMap, mountPointToMountArgsMap map[string]string) {
	mountPointDevPathMap = make(map[string]string)
	mountPointToFsTypeMap = make(map[string]string)
	mountPointToMountArgsMap = make(map[string]string)

	// Go through each PartitionSetting
	for _, partitionSetting := range config.PartitionSettings {
		logger.Log.Tracef("%v[%v]", partitionSetting.ID, partitionSetting.MountPoint)
		partDevPath, ok := partDevPathMap[partitionSetting.ID]
		if ok {
			mountPointDevPathMap[partitionSetting.MountPoint] = partDevPath
			mountPointToFsTypeMap[partitionSetting.MountPoint] = partIDToFsTypeMap[partitionSetting.ID]
			mountPointToMountArgsMap[partitionSetting.MountPoint] = partitionSetting.MountOptions
		}
		logger.Log.Tracef("%v", mountPointDevPathMap)
	}
	return
}

// CreateInstallRoot walks through the map of mountpoints and mounts the partitions into installroot
// - installRoot is the destination path to mount these partitions
// - mountPointMap is the map of mountpoint to partition device path
func CreateInstallRoot(installRoot string, mountPointMap, mountPointToMountArgsMap map[string]string) (installMap map[string]string, err error) {
	installMap = make(map[string]string)

	// Always mount root first
	err = mountSingleMountPoint(installRoot, rootMountPoint, mountPointMap[rootMountPoint], mountPointToMountArgsMap[rootMountPoint])
	if err != nil {
		return
	}
	installMap[rootMountPoint] = mountPointMap[rootMountPoint]

	// Mount rest of the mountpoints
	for mountPoint, device := range mountPointMap {
		if mountPoint != "" && mountPoint != rootMountPoint {
			err = mountSingleMountPoint(installRoot, mountPoint, device, mountPointToMountArgsMap[mountPoint])
			if err != nil {
				return
			}
			installMap[mountPoint] = device
		}
	}
	return
}

// DestroyInstallRoot unmounts each of the installroot mountpoints in order, ensuring that the root mountpoint is last
// - installRoot is the path to the root where the mountpoints exist
// - installMap is the map of mountpoints to partition device paths
func DestroyInstallRoot(installRoot string, installMap map[string]string) (err error) {
	logger.Log.Trace("Destroying InstallRoot")

	// Convert the installMap into a slice of mount points so it can be sorted
	var allMountsToUnmount []string
	for mountPoint := range installMap {
		// Skip empty mount points
		if mountPoint == "" {
			continue
		}

		allMountsToUnmount = append(allMountsToUnmount, mountPoint)
	}

	// Sort the mount points
	// This way nested mounts will be handled correctly:
	// e.g.: /dev/pts is unmounted and then /dev is.
	sort.Sort(sort.Reverse(sort.StringSlice(allMountsToUnmount)))
	for _, mountPoint := range allMountsToUnmount {
		err = unmountSingleMountPoint(installRoot, mountPoint)
		if err != nil {
			return
		}
	}

	return
}

func mountSingleMountPoint(installRoot, mountPoint, device, extraOptions string) (err error) {
	mountPath := filepath.Join(installRoot, mountPoint)
	err = os.MkdirAll(mountPath, os.ModePerm)
	if err != nil {
		logger.Log.Warnf("Failed to create mountpoint: %v", err)
		return
	}
	err = mount(mountPath, device, extraOptions)
	return
}

func unmountSingleMountPoint(installRoot, mountPoint string) (err error) {
	mountPath := filepath.Join(installRoot, mountPoint)
	err = umount(mountPath)
	return
}

func mount(path, device, extraOptions string) (err error) {
	const squashErrors = false

	if extraOptions == "" {
		err = shell.ExecuteLive(squashErrors, "mount", device, path)
	} else {
		err = shell.ExecuteLive(squashErrors, "mount", "-o", extraOptions, device, path)
	}

	if err != nil {
		return
	}
	return
}

func umount(path string) (err error) {
	const (
		retryAttempts = 3
		retryDuration = time.Second
		unmountFlags  = 0
	)
	err = retry.Run(func() error {
		return syscall.Unmount(path, unmountFlags)
	}, retryAttempts, retryDuration)
	return
}

// PackageNamesFromSingleSystemConfig goes through the packageslist field in the systemconfig and extracts the list of packages
// from each of the packagelists
// - systemConfig is the systemconfig field from the config file
// Since kernel is not part of the packagelist, it is added separately from KernelOptions.
func PackageNamesFromSingleSystemConfig(systemConfig configuration.SystemConfig) (finalPkgList []string, err error) {
	var packages PackageList

	for _, packageList := range systemConfig.PackageLists {
		// Read json
		logger.Log.Tracef("Processing packages from packagelist %v", packageList)
		packages, err = getPackagesFromJSON(packageList)
		if err != nil {
			return
		}
		logger.Log.Tracef("packages %v", packages)
		finalPkgList = append(finalPkgList, packages.Packages...)
	}
	logger.Log.Tracef("finalPkgList = %v", finalPkgList)
	return
}

// SelectKernelPackage selects the kernel to use for the current installation
// based on the KernelOptions field of the system configuration.
func SelectKernelPackage(systemConfig configuration.SystemConfig, isLiveInstall bool) (kernelPkg string, err error) {
	const (
		defaultOption = "default"
		hypervOption  = "hyperv"
	)

	optionToUse := defaultOption

	// Only consider Hyper-V for an ISO
	if isLiveInstall {
		// Only check if running on Hyper V if there's a kernel option for it
		_, found := systemConfig.KernelOptions[hypervOption]
		if found {
			isHyperV, err := isRunningInHyperV()
			if err != nil {
				logger.Log.Warnf("Unable to detect if the current system is Hyper-V, using the default kernel")
			} else if isHyperV {
				optionToUse = hypervOption
			}
		}
	}

	kernelPkg = systemConfig.KernelOptions[optionToUse]
	if kernelPkg == "" {
		err = fmt.Errorf("no kernel for option (%s) set", optionToUse)
		return
	}

	return
}

// PackageNamesFromConfig takes the union of top level package names for every system configuration in a top level
// config file.
// - config is the config file to proccess
func PackageNamesFromConfig(config configuration.Config) (packageList []*pkgjson.PackageVer, err error) {
	// For each system config, clone all packages that go into it
	for _, systemCfg := range config.SystemConfigs {
		var packagesToInstall []string
		// Get list of packages to install into image
		packagesToInstall, err = PackageNamesFromSingleSystemConfig(systemCfg)
		if err != nil {
			return
		}

		packages := make([]*pkgjson.PackageVer, 0, len(packagesToInstall))
		for _, pkg := range packagesToInstall {
			packages = append(packages, &pkgjson.PackageVer{
				Name: pkg,
			})
		}

		packageList = append(packageList, packages...)
	}
	return
}

// PopulateInstallRoot fills the installroot with packages and configures the image for boot
// - installChroot is a pointer to the install Chroot object
// - packagesToInstall is a slice of packages to install
// - config is the systemconfig field from the config file
// - installMap is a map of mountpoints to physical device paths
// - mountPointToFsTypeMap is a map of mountpoints to filesystem type
// - mountPointToMountArgsMap is a map of mountpoints to mount options
// - isRootFS specifies if the installroot is either backed by a directory (rootfs) or a raw disk
// - encryptedRoot stores information about the encrypted root device if root encryption is enabled
func PopulateInstallRoot(installChroot *safechroot.Chroot, packagesToInstall []string, config configuration.SystemConfig, installMap, mountPointToFsTypeMap, mountPointToMountArgsMap map[string]string, isRootFS bool, encryptedRoot diskutils.EncryptedRootDevice) (err error) {
	const (
		filesystemPkg = "filesystem"
	)

	defer stopGPGAgent(installChroot)

	ReportAction("Initializing RPM Database")

	installRoot := filepath.Join(rootMountPoint, installChroot.RootDir())

	// Initialize RPM Database so we can install RPMs into the installroot
	err = initializeRpmDatabase(installRoot)
	if err != nil {
		return
	}

	// Calculate how many packages need to be installed so an accurate percent complete can be reported
	totalPackages, err := calculateTotalPackages(packagesToInstall, installRoot)
	if err != nil {
		return
	}

	// Keep a running total of how many packages have be installed through all the `tdnfInstall` invocations
	packagesInstalled := 0

	// Install filesystem package first
	packagesInstalled, err = tdnfInstall(filesystemPkg, installRoot, packagesInstalled, totalPackages)
	if err != nil {
		return
	}

	hostname := config.Hostname
	if !isRootFS {
		// Add /etc/hostname
		err = updateHostname(installChroot.RootDir(), hostname)
		if err != nil {
			return
		}
	}

	// Install packages one-by-one to avoid exhausting memory
	// on low resource systems
	for _, pkg := range packagesToInstall {
		packagesInstalled, err = tdnfInstall(pkg, installRoot, packagesInstalled, totalPackages)
		if err != nil {
			return
		}
	}

	// Copy additional files
	err = copyAdditionalFiles(installChroot, config)
	if err != nil {
		return
	}

	if !isRootFS {
		// Configure system files
		err = configureSystemFiles(installChroot, hostname, installMap, mountPointToFsTypeMap, mountPointToMountArgsMap, encryptedRoot)
		if err != nil {
			return
		}

		// Add groups
		err = addGroups(installChroot, config.Groups)
		if err != nil {
			return
		}
	}

	// Add users
	err = addUsers(installChroot, config.Users)
	if err != nil {
		return
	}

	// Add machine-id
	err = addMachineID(installChroot)
	if err != nil {
		return
	}

	// Configure for encryption
	if config.Encryption.Enable {
		err = updateInitramfsForEncrypt(installChroot)
		if err != nil {
			return
		}
	}

	// Run post-install scripts from within the installroot chroot
	err = runPostInstallScripts(installChroot, config)
	return
}

func initializeRpmDatabase(installRoot string) (err error) {
	stdout, stderr, err := shell.Execute("rpm", "--root", installRoot, "--initdb")
	if err != nil {
		logger.Log.Warnf("Failed to create rpm database: %v", err)
		logger.Log.Warn(stdout)
		logger.Log.Warn(stderr)
		return
	}

	err = initializeTdnfConfiguration(installRoot)
	return
}

// initializeTdnfConfiguration installs the 'mariner-release' package
// into the clean RPM root. The package is used by tdnf to properly set
// the default values for its variables and internal configuration.
func initializeTdnfConfiguration(installRoot string) (err error) {
	const (
		squashErrors   = false
		releasePackage = "mariner-release"
	)

	logger.Log.Debugf("Downloading '%s' package to a clean RPM root under '%s'.", releasePackage, installRoot)

	err = shell.ExecuteLive(squashErrors, "tdnf", "download", "--alldeps", "--destdir", installRoot, releasePackage)
	if err != nil {
		logger.Log.Errorf("Failed to prepare the RPM database on downloading the 'mariner-release' package: %v", err)
		return
	}

	rpmSearch := filepath.Join(installRoot, "*.rpm")
	rpmFiles, err := filepath.Glob(rpmSearch)
	if err != nil {
		logger.Log.Errorf("Failed to prepare the RPM database while searching for RPM files: %v", err)
		return
	}

	defer func() {
		logger.Log.Tracef("Cleaning up leftover RPM files after installing 'mariner-release' package under '%s'.", installRoot)
		for _, file := range rpmFiles {
			err = os.Remove(file)
			if err != nil {
				logger.Log.Errorf("Failed to prepare the RPM database on removing leftover file (%s): %v", file, err)
				return
			}
		}
	}()

	logger.Log.Debugf("Installing 'mariner-release' package to a clean RPM root under '%s'.", installRoot)

	rpmArgs := []string{"-i", "--root", installRoot}
	rpmArgs = append(rpmArgs, rpmFiles...)
	err = shell.ExecuteLive(squashErrors, "rpm", rpmArgs...)
	if err != nil {
		logger.Log.Errorf("Failed to prepare the RPM database on installing the 'mariner-release' package: %v", err)
		return
	}

	return
}

func configureSystemFiles(installChroot *safechroot.Chroot, hostname string, installMap, mountPointToFsTypeMap, mountPointToMountArgsMap map[string]string, encryptedRoot diskutils.EncryptedRootDevice) (err error) {
	// Update hosts file
	err = updateHosts(installChroot.RootDir(), hostname)
	if err != nil {
		return
	}

	// Update fstab
	err = updateFstab(installChroot.RootDir(), installMap, mountPointToFsTypeMap, mountPointToMountArgsMap)
	if err != nil {
		return
	}

	// Update crypttab
	err = updateCrypttab(installChroot.RootDir(), installMap, encryptedRoot)
	if err != nil {
		return
	}

	return
}

func calculateTotalPackages(packages []string, installRoot string) (totalPackages int, err error) {
	allPackageNames := make(map[string]bool)
	const tdnfAssumeNoStdErr = "Error(1032) : Operation aborted.\n"

	// For every package calculate what dependencies would also be installed from it.
	for _, pkg := range packages {
		var (
			stdout string
			stderr string
		)

		// Issue an install request but stop right before actually performing the install (assumeno)
		stdout, stderr, err = shell.Execute("tdnf", "install", "--assumeno", "--nogpgcheck", pkg, "--installroot", installRoot)
		if err != nil {
			// tdnf aborts the process when it detects an install with --assumeno.
			if stderr == tdnfAssumeNoStdErr {
				err = nil
			} else {
				logger.Log.Error(stderr)
				return
			}
		}

		splitStdout := strings.Split(stdout, "\n")

		// Search for the list of packages to be installed,
		// it will be prefixed with a line "Installing:" and will
		// end with an empty line.
		inPackageList := false
		for _, line := range splitStdout {
			const (
				packageListPrefix    = "Installing:"
				packageNameDelimiter = " "
			)

			const (
				packageNameIndex      = iota
				extraInformationIndex = iota
				totalPackageNameParts = iota
			)

			if !inPackageList {
				inPackageList = strings.HasPrefix(line, packageListPrefix)
				continue
			} else if strings.TrimSpace(line) == "" {
				break
			}

			// Each package to be installed will list its name, followed by a space and then various extra information
			pkgSplit := strings.SplitN(line, packageNameDelimiter, totalPackageNameParts)
			if len(pkgSplit) != totalPackageNameParts {
				err = fmt.Errorf("unexpected TDNF package name output: %s", line)
				return
			}

			allPackageNames[pkgSplit[packageNameIndex]] = true
		}
	}

	totalPackages = len(allPackageNames)
	logger.Log.Debugf("All packages to be installed (%d): %v", totalPackages, allPackageNames)
	return
}

// addMachineID creates the /etc/machine-id file in the installChroot
func addMachineID(installChroot *safechroot.Chroot) (err error) {
	// From https://www.freedesktop.org/software/systemd/man/machine-id.html:
	// For operating system images which are created once and used on multiple
	// machines, for example for containers or in the cloud, /etc/machine-id
	// should be an empty file in the generic file system image. An ID will be
	// generated during boot and saved to this file if possible.

	const (
		machineIDFile      = "/etc/machine-id"
		machineIDFilePerms = 0644
	)

	ReportAction("Configuring machine id")

	err = installChroot.UnsafeRun(func() error {
		return file.Create(machineIDFile, machineIDFilePerms)
	})
	return
}

func updateInitramfsForEncrypt(installChroot *safechroot.Chroot) (err error) {
	err = installChroot.UnsafeRun(func() (err error) {
		const (
			libModDir     = "/lib/modules"
			dracutModules = "dm crypt crypt-gpg crypt-loop lvm"
			initrdPrefix  = "/boot/initrd.img-"
			cryptTabPath  = "/etc/crypttab"
		)

		initrdPattern := fmt.Sprintf("%v%v", initrdPrefix, "*")
		initrdImageSlice, err := filepath.Glob(initrdPattern)
		if err != nil {
			logger.Log.Warnf("Unable to get initrd image: %v", err)
			return
		}

		// Assume only one initrd image present
		if len(initrdImageSlice) != 1 {
			logger.Log.Warn("Unable to find one initrd image")
			logger.Log.Warnf("Initrd images found: %v", initrdImageSlice)
			err = fmt.Errorf("unable to find one intird image: %v", initrdImageSlice)
			return
		}

		initrdImage := initrdImageSlice[0]

		// Get the kernel version
		kernel := strings.TrimPrefix(initrdImage, initrdPrefix)

		// Construct list of files to install in initramfs
		installFiles := fmt.Sprintf("%v %v", cryptTabPath, diskutils.DefaultKeyFilePath)

		// Regenerate initramfs via Dracut
		dracutArgs := []string{
			"-f",
			"--no-hostonly",
			"--fstab",
			"--kmoddir", filepath.Join(libModDir, kernel),
			"--add", dracutModules,
			"-I", installFiles,
			initrdImage, kernel,
		}
		_, stderr, err := shell.Execute("dracut", dracutArgs...)

		if err != nil {
			logger.Log.Warnf("Unable to execute dracut: %v", stderr)
			return
		}

		return
	})

	return
}

func updateFstab(installRoot string, installMap, mountPointToFsTypeMap, mountPointToMountArgsMap map[string]string) (err error) {
	ReportAction("Configuring fstab")

	for mountPoint, devicePath := range installMap {
		if mountPoint != "" {
			err = addEntryToFstab(installRoot, mountPoint, devicePath, mountPointToFsTypeMap[mountPoint], mountPointToMountArgsMap[mountPoint])
			if err != nil {
				return
			}
		}
	}
	return
}

func addEntryToFstab(installRoot, mountPoint, devicePath, fsType, mountArgs string) (err error) {
	const (
		uuidPrefix       = "UUID="
		fstabPath        = "/etc/fstab"
		rootfsMountPoint = "/"
		defaultOptions   = "defaults"
		defaultDump      = "0"
		disablePass      = "0"
		rootPass         = "1"
		defaultPass      = "2"
	)

	var options string

	if mountArgs == "" {
		options = defaultOptions
	} else {
		options = mountArgs
	}

	fullFstabPath := filepath.Join(installRoot, fstabPath)

	// Get the block device
	var device string
	if diskutils.IsEncryptedDevice(devicePath) {
		device = devicePath
	} else {
		uuid, err := GetUUID(devicePath)
		if err != nil {
			logger.Log.Warnf("Failed to get UUID for block device %v", devicePath)
			return err
		}

		device = fmt.Sprintf("%v%v", uuidPrefix, uuid)
	}

	// Note: Rootfs should always have a pass number of 1. All other mountpoints are either 0 or 2
	pass := defaultPass
	if mountPoint == rootfsMountPoint {
		pass = rootPass
	}

	// Construct fstab entry and append to fstab file
	newEntry := fmt.Sprintf("%v %v %v %v %v %v\n", device, mountPoint, fsType, options, defaultDump, pass)
	err = file.Append(newEntry, fullFstabPath)
	if err != nil {
		logger.Log.Warnf("Failed to append to fstab file")
		return
	}
	return
}

func updateCrypttab(installRoot string, installMap map[string]string, encryptedRoot diskutils.EncryptedRootDevice) (err error) {
	ReportAction("Configuring Crypttab")

	for _, devicePath := range installMap {
		if diskutils.IsEncryptedDevice(devicePath) {
			err = addEntryToCrypttab(installRoot, devicePath, encryptedRoot)
			if err != nil {
				return
			}
		}
	}

	return
}

// Add an encryption mapping to crypttab
func addEntryToCrypttab(installRoot string, devicePath string, encryptedRoot diskutils.EncryptedRootDevice) (err error) {
	const (
		cryptTabPath = "/etc/crypttab"
		Options      = "luks,discard"
		uuidPrefix   = "UUID="
	)

	fullCryptTabPath := filepath.Join(installRoot, cryptTabPath)
	uuid := encryptedRoot.LuksUUID
	blockDevice := diskutils.GetLuksMappingName(uuid)
	encryptedUUID := fmt.Sprintf("%v%v", uuidPrefix, uuid)
	encryptionPassword := diskutils.DefaultKeyFilePath

	// Construct crypttab entry and append crypttab file
	newEntry := fmt.Sprintf("%v %v %v %v\n", blockDevice, encryptedUUID, encryptionPassword, Options)
	err = file.Append(newEntry, fullCryptTabPath)
	if err != nil {
		logger.Log.Warnf("Failed to append crypttab")
		return
	}
	return
}

// InstallGrubCfg installs the main grub config to the boot partition
// - installRoot is the base install directory
// - rootDevice holds the root partition
// - bootUUID is the UUID for the boot partition
// - encryptedRoot holds the encrypted root information if encrypted root is enabled
// - kernelCommandLine contains additional kernel parameters which may be optionally set
// Note: this boot partition could be different than the boot partition specified in the bootloader.
// This boot partition specifically indicates where to find the kernel, config files, and initrd
func InstallGrubCfg(installRoot, rootDevice, bootUUID string, encryptedRoot diskutils.EncryptedRootDevice, kernelCommandLine configuration.KernelCommandLine) (err error) {
	const (
		assetGrubcfgFile = "/installer/grub2/grub.cfg"
		grubCfgFile      = "boot/grub2/grub.cfg"
	)

	// Copy the bootloader's grub.cfg and set the file permission
	installGrubCfgFile := filepath.Join(installRoot, grubCfgFile)
	err = file.CopyAndChangeMode(assetGrubcfgFile, installGrubCfgFile, bootDirectoryDirMode, bootDirectoryFileMode)
	if err != nil {
		return
	}

	// Add in bootUUID
	err = setGrubCfgBootUUID(bootUUID, installGrubCfgFile)
	if err != nil {
		logger.Log.Warnf("Failed to set bootUUID in grub.cfg: %v", err)
		return
	}

	// Add in rootDevice
	err = setGrubCfgRootDevice(rootDevice, installGrubCfgFile, encryptedRoot.LuksUUID)
	if err != nil {
		logger.Log.Warnf("Failed to set rootDevice in grub.cfg: %v", err)
		return
	}

	// Add in rootLuksUUID
	err = setGrubCfgLuksUUID(installGrubCfgFile, encryptedRoot.LuksUUID)
	if err != nil {
		logger.Log.Warnf("Failed to set luksUUID in grub.cfg: %v", err)
		return
	}

	// Add in logical volumes to active
	err = setGrubCfgLVM(installGrubCfgFile, encryptedRoot.LuksUUID)
	if err != nil {
		logger.Log.Warnf("Failed to set lvm.lv in grub.cfg: %v", err)
		return
	}

	// Configure IMA policy
	err = setGrubCfgIMA(installGrubCfgFile, kernelCommandLine)
	if err != nil {
		logger.Log.Warnf("Failed to set ima_policy in grub.cfg: %v", err)
		return
	}

	// Append any additional command line parameters
	err = setGrubCfgAdditionalCmdLine(installGrubCfgFile, kernelCommandLine)
	if err != nil {
		logger.Log.Warnf("Failed to append extra command line parameterse in grub.cfg: %v", err)
		return
	}

	return
}

func updateHostname(installRoot, hostname string) (err error) {
	ReportAction("Configuring hostname")

	// Update the environment variables to use the new hostname.
	env := append(shell.CurrentEnvironment(), fmt.Sprintf("HOSTNAME=%s", hostname))
	shell.SetEnvironment(env)

	hostnameFilePath := filepath.Join(installRoot, "etc/hostname")
	err = file.Write(hostname, hostnameFilePath)
	if err != nil {
		logger.Log.Warnf("Failed to write hostname")
		return
	}
	return
}

func updateHosts(installRoot, hostname string) (err error) {
	const (
		lineNumber = "6"
		hostsFile  = "etc/hosts"
	)

	ReportAction("Configuring hosts file")

	newHost := fmt.Sprintf("127.0.0.1   %v", hostname)
	hostsFilePath := filepath.Join(installRoot, hostsFile)
	err = sedInsert(lineNumber, newHost, hostsFilePath)
	if err != nil {
		logger.Log.Warnf("Failed to write hosts file")
		return
	}
	return
}

func addGroups(installChroot *safechroot.Chroot, groups []configuration.Group) (err error) {
	const squashErrors = false

	for _, group := range groups {
		logger.Log.Infof("Adding group (%s)", group.Name)
		ReportActionf("Adding group: %s", group.Name)

		var args = []string{group.Name}
		if group.GID != "" {
			args = append(args, "-g", group.GID)
		}

		err = installChroot.UnsafeRun(func() error {
			return shell.ExecuteLive(squashErrors, "groupadd", args...)
		})
	}

	return
}

func addUsers(installChroot *safechroot.Chroot, users []configuration.User) (err error) {
	const (
		squashErrors = false
	)

	rootUserAdded := false

	for _, user := range users {
		logger.Log.Infof("Adding user (%s)", user.Name)
		ReportActionf("Adding user: %s", user.Name)

		var (
			homeDir string
			isRoot  bool
		)

		homeDir, isRoot, err = createUserWithPassword(installChroot, user)
		if err != nil {
			return
		}
		if isRoot {
			rootUserAdded = true
		}

		err = configureUserGroupMembership(installChroot, user)
		if err != nil {
			return
		}

		err = provisionUserSSHCerts(installChroot, user, homeDir)
		if err != nil {
			return
		}

		err = configureUserStartupCommand(installChroot, user)
		if err != nil {
			return
		}
	}

	// If no root entry was specified in the config file, never expire the root password
	if !rootUserAdded {
		logger.Log.Debugf("No root user entry found in config file. Setting root password to never expire.")
		err = installChroot.UnsafeRun(func() error {
			return shell.ExecuteLive(squashErrors, "chage", "-M", "-1", "root")
		})
	}
	return
}

func createUserWithPassword(installChroot *safechroot.Chroot, user configuration.User) (homeDir string, isRoot bool, err error) {
	const (
		squashErrors        = false
		rootHomeDir         = "/root"
		userHomeDirPrefix   = "/home"
		passwordExpiresBase = 10
		postfixLength       = 12
		alphaNumeric        = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	)

	var (
		hashedPassword string
		stdout         string
		stderr         string
		salt           string
	)

	// Get the hashed password for the user
	if user.PasswordHashed {
		hashedPassword = user.Password
	} else {
		salt, err = randomString(postfixLength, alphaNumeric)
		if err != nil {
			return
		}
		// Generate hashed password based on salt value provided.
		// -6 option indicates to use the SHA256/SHA512 algorithm
		stdout, stderr, err = shell.Execute("openssl", "passwd", "-6", "-salt", salt, user.Password)
		if err != nil {
			logger.Log.Warnf("Failed to generate hashed password")
			logger.Log.Warn(stderr)
			return
		}
		hashedPassword = strings.TrimSpace(stdout)
	}
	logger.Log.Tracef("hashed password: %v", hashedPassword)

	if strings.TrimSpace(hashedPassword) == "" {
		err = fmt.Errorf("empty password for user (%s) is not allowed", user.Name)
		return
	}

	// Create the user with the given hashed password
	if user.Name == rootUser {
		homeDir = rootHomeDir

		if user.UID != "" {
			logger.Log.Warnf("Ignoring UID for (%s) user, using default", rootUser)
		}

		// Update shadow file
		err = updateUserPassword(installChroot.RootDir(), user.Name, hashedPassword)
		isRoot = true
	} else {
		homeDir = filepath.Join(userHomeDirPrefix, user.Name)

		var args = []string{user.Name, "-m", "-p", hashedPassword}
		if user.UID != "" {
			args = append(args, "-u", user.UID)
		}

		err = installChroot.UnsafeRun(func() error {
			return shell.ExecuteLive(squashErrors, "useradd", args...)
		})
	}

	if err != nil {
		return
	}

	err = user.PasswordExpiresDaysIsValid()
	if err != nil {
		return
	}

	// Update password expiration
	if user.PasswordExpiresDays != 0 {
		err = installChroot.UnsafeRun(func() error {
			return shell.ExecuteLive(squashErrors, "chage", "-M", strconv.FormatInt(user.PasswordExpiresDays, passwordExpiresBase), user.Name)
		})
	}

	return
}

func configureUserGroupMembership(installChroot *safechroot.Chroot, user configuration.User) (err error) {
	const squashErrors = false

	// Update primary group
	if user.PrimaryGroup != "" {
		err = installChroot.UnsafeRun(func() error {
			return shell.ExecuteLive(squashErrors, "usermod", "-g", user.PrimaryGroup, user.Name)
		})

		if err != nil {
			return
		}
	}

	// Update secondary groups
	if len(user.SecondaryGroups) != 0 {
		allGroups := strings.Join(user.SecondaryGroups, ",")
		err = installChroot.UnsafeRun(func() error {
			return shell.ExecuteLive(squashErrors, "usermod", "-a", "-G", allGroups, user.Name)
		})

		if err != nil {
			return
		}
	}

	return
}

func configureUserStartupCommand(installChroot *safechroot.Chroot, user configuration.User) (err error) {
	const (
		passwdFilePath = "etc/passwd"
		sedDelimiter   = "|"
	)

	if user.StartupCommand == "" {
		return
	}

	logger.Log.Debugf("Updating user '%s' startup command to '%s'.", user.Name, user.StartupCommand)

	findPattern := fmt.Sprintf(`^\(%s.*\):[^:]*$`, user.Name)
	replacePattern := fmt.Sprintf(`\1:%s`, user.StartupCommand)
	filePath := filepath.Join(installChroot.RootDir(), passwdFilePath)
	err = sed(findPattern, replacePattern, sedDelimiter, filePath)
	if err != nil {
		logger.Log.Errorf("Failed to update user's startup command.")
		return
	}
	return
}

func provisionUserSSHCerts(installChroot *safechroot.Chroot, user configuration.User, homeDir string) (err error) {
	const squashErrors = false

	userSSHKeyDir := filepath.Join(homeDir, ".ssh")

	for _, pubKey := range user.SSHPubKeyPaths {
		logger.Log.Infof("Adding ssh key (%s) to user (%s)", filepath.Base(pubKey), user.Name)
		relativeDst := filepath.Join(userSSHKeyDir, filepath.Base(pubKey))

		fileToCopy := safechroot.FileToCopy{
			Src:  pubKey,
			Dest: relativeDst,
		}

		err = installChroot.AddFiles(fileToCopy)
		if err != nil {
			return
		}
	}

	if len(user.SSHPubKeyPaths) != 0 {
		const sshDirectoryPermission = "0700"

		// Change ownership of the folder to belong to the user and their primary group
		err = installChroot.UnsafeRun(func() (err error) {
			// Find the primary group of the user
			stdout, stderr, err := shell.Execute("id", "-g", user.Name)
			if err != nil {
				logger.Log.Warnf(stderr)
				return
			}

			primaryGroup := strings.TrimSpace(stdout)
			logger.Log.Debugf("Primary group for user (%s) is (%s)", user.Name, primaryGroup)

			ownership := fmt.Sprintf("%s:%s", user.Name, primaryGroup)
			err = shell.ExecuteLive(squashErrors, "chown", "-R", ownership, userSSHKeyDir)
			if err != nil {
				return
			}

			err = shell.ExecuteLive(squashErrors, "chmod", "-R", sshDirectoryPermission, userSSHKeyDir)
			return
		})

		if err != nil {
			return
		}
	}

	return
}

func updateUserPassword(installRoot, username, password string) (err error) {
	const (
		shadowFilePath = "etc/shadow"
		sedDelimiter   = "|"
	)

	findPattern := fmt.Sprintf("%v:x:", username)
	replacePattern := fmt.Sprintf("%v:%v:", username, password)
	filePath := filepath.Join(installRoot, shadowFilePath)
	err = sed(findPattern, replacePattern, sedDelimiter, filePath)
	if err != nil {
		logger.Log.Warnf("Failed to write hashed password to shadow file")
		return
	}
	return
}

func tdnfInstall(packageName, installRoot string, currentPackagesInstalled, totalPackages int) (packagesInstalled int, err error) {
	packagesInstalled = currentPackagesInstalled

	onStdout := func(args ...interface{}) {
		const tdnfInstallPrefix = "Installing/Updating: "

		// Only process lines that match tdnfInstallPrefix
		if len(args) == 0 {
			return
		}

		line := args[0].(string)
		if !strings.HasPrefix(line, tdnfInstallPrefix) {
			return
		}

		status := fmt.Sprintf("Installing: %s", strings.TrimPrefix(line, tdnfInstallPrefix))
		ReportAction(status)

		packagesInstalled++

		// Calculate and report what percentage of packages have been installed
		percentOfPackagesInstalled := float32(packagesInstalled) / float32(totalPackages)
		progress := int(percentOfPackagesInstalled * 100)
		ReportPercentComplete(progress)
	}

	err = shell.ExecuteLiveWithCallback(onStdout, logger.Log.Warn, true, "tdnf", "install", packageName, "--installroot", installRoot, "--nogpgcheck", "--assumeyes")
	if err != nil {
		logger.Log.Warnf("Failed to tdnf install: %v. Package name: %v", err, packageName)
	}

	return
}

func sed(find, replace, delimiter, file string) (err error) {
	const squashErrors = false

	replacement := fmt.Sprintf("s%s%s%s%s%s", delimiter, find, delimiter, replace, delimiter)
	return shell.ExecuteLive(squashErrors, "sed", "-i", replacement, file)
}

func sedInsert(line, replace, file string) (err error) {
	const squashErrors = false

	insertAtLine := fmt.Sprintf("%si%s", line, replace)
	return shell.ExecuteLive(squashErrors, "sed", "-i", insertAtLine, file)
}

func getPackagesFromJSON(file string) (pkgList PackageList, err error) {
	err = jsonutils.ReadJSONFile(file, &pkgList)
	if err != nil {
		logger.Log.Warnf("Could not read JSON file: %v", err)
		return
	}
	return
}

// InstallBootloader installs the proper bootloader for this type of image
// - installChroot is a pointer to the install Chroot object
// - bootType indicates the type of boot loader to add.
// - bootUUID is the UUID of the boot partition
// Note: this boot partition could be different than the boot partition specified in the main grub config.
// This boot partition specifically indicates where to find the main grub cfg
func InstallBootloader(installChroot *safechroot.Chroot, encryptEnabled bool, bootType, bootUUID, bootDevPath string) (err error) {
	const (
		efiMountPoint  = "/boot/efi"
		efiBootType    = "efi"
		legacyBootType = "legacy"
		noneBootType   = "none"
	)

	ReportAction("Configuring bootloader")

	switch bootType {
	case legacyBootType:
		err = installLegacyBootloader(installChroot, bootDevPath)
		if err != nil {
			return
		}
	case efiBootType:
		efiPath := filepath.Join(installChroot.RootDir(), efiMountPoint)
		err = installEfiBootloader(encryptEnabled, efiPath, bootUUID)
		if err != nil {
			return
		}
	case noneBootType:
		// Nothing to do here
	default:
		err = fmt.Errorf("unknown boot type: %v", bootType)
		return
	}
	return
}

// Note: We assume that the /boot directory is present. Whether it is backed by an explicit "boot" partition or present
// as part of a general "root" partition is assumed to have been done already.
func installLegacyBootloader(installChroot *safechroot.Chroot, bootDevPath string) (err error) {
	const (
		squashErrors = false
	)

	// Since we do not have grub2-pc installed in the setup environment, we need to generate the legacy grub bootloader
	// inside of the install environment. This assumes the install environment has the grub2-pc package installed
	err = installChroot.UnsafeRun(func() (err error) {
		err = shell.ExecuteLive(squashErrors, "grub2-install", "--target=i386-pc", "--boot-directory=/boot", bootDevPath)
		err = shell.ExecuteLive(squashErrors, "chmod", "-R", "go-rwx", "/boot/grub2/")
		return
	})

	return
}

// EnableCryptoDisk enables Grub to boot from an encrypted disk
// - installChroot is the installation chroot
func EnableCryptoDisk(installChroot *safechroot.Chroot) (err error) {
	const (
		grubPath           = "/etc/default/grub"
		grubCryptoDisk     = "GRUB_ENABLE_CRYPTODISK=y\n"
		grubPreloadModules = `GRUB_PRELOAD_MODULES="lvm"`
	)

	err = installChroot.UnsafeRun(func() error {
		err := file.Append(grubCryptoDisk, grubPath)
		if err != nil {
			logger.Log.Warnf("Failed to add grub cryptodisk: %v", err)
			return err
		}

		err = file.Append(grubPreloadModules, grubPath)
		if err != nil {
			logger.Log.Warnf("Failed to add grub preload modules: %v", err)
			return err
		}

		return err
	})

	return
}

// GetUUID queries the UUID of the given partition
// - device is the device path of the desired partition
func GetUUID(device string) (stdout string, err error) {
	stdout, _, err = shell.Execute("blkid", device, "-s", "UUID", "-o", "value")
	if err != nil {
		return
	}
	logger.Log.Trace(stdout)
	stdout = strings.TrimSpace(stdout)
	return
}

// GetPartUUID queries the PARTUUID of the given partition
// - device is the device path of the desired partition
func GetPartUUID(device string) (stdout string, err error) {
	stdout, _, err = shell.Execute("blkid", device, "-s", "PARTUUID", "-o", "value")
	if err != nil {
		return
	}
	logger.Log.Trace(stdout)
	stdout = strings.TrimSpace(stdout)
	return
}

// installEfi copies the efi binaries and grub configuration to the appropriate
// installRoot/boot/efi folder
// It is expected that shim (bootx64.efi) and grub2 (grub2.efi) are installed
// into the EFI directory via the package list installation mechanism.
func installEfiBootloader(encryptEnabled bool, installRoot, bootUUID string) (err error) {
	const (
		defaultCfgFilename = "grub.cfg"
		encryptCfgFilename = "grubEncrypt.cfg"
		efiAssetDir        = "/installer/efi/x86_64"
		grubAssetDir       = "/installer/efi/grub"
		efiFinalDir        = "EFI/BOOT"
		grubFinalDir       = "boot/grub2"
	)

	// Copy the bootloader's grub.cfg
	grubAssetPath := filepath.Join(grubAssetDir, defaultCfgFilename)
	if encryptEnabled {
		grubAssetPath = filepath.Join(grubAssetDir, encryptCfgFilename)
	}
	grubFinalPath := filepath.Join(installRoot, grubFinalDir, defaultCfgFilename)
	err = file.CopyAndChangeMode(grubAssetPath, grubFinalPath, bootDirectoryDirMode, bootDirectoryFileMode)
	if err != nil {
		logger.Log.Warnf("Failed to copy grub.cfg: %v", err)
		return
	}

	// Add in bootUUID
	err = setGrubCfgBootUUID(bootUUID, grubFinalPath)
	if err != nil {
		logger.Log.Warnf("Failed to set bootUUID in grub.cfg: %v", err)
		return
	}

	// Add in encrypted volume
	if encryptEnabled {
		err = setGrubCfgEncryptedVolume(grubFinalPath)
		if err != nil {
			logger.Log.Warnf("Failed to set encrypted volume in grub.cfg: %v", err)
			return
		}
	}

	return
}

func copyAdditionalFiles(installChroot *safechroot.Chroot, config configuration.SystemConfig) (err error) {
	ReportAction("Copying additional files")

	for srcFile, dstFile := range config.AdditionalFiles {
		fileToCopy := safechroot.FileToCopy{
			Src:  srcFile,
			Dest: dstFile,
		}

		err = installChroot.AddFiles(fileToCopy)
		if err != nil {
			return
		}
	}

	return
}

func runPostInstallScripts(installChroot *safechroot.Chroot, config configuration.SystemConfig) (err error) {
	const squashErrors = false

	for _, script := range config.PostInstallScripts {
		// Copy the script from this chroot into the install chroot before running it
		scriptPath := script.Path
		fileToCopy := safechroot.FileToCopy{
			Src:  scriptPath,
			Dest: scriptPath,
		}

		installChroot.AddFiles(fileToCopy)
		if err != nil {
			return
		}

		ReportActionf("Running post-install script: %s", path.Base(script.Path))
		logger.Log.Infof("Running post-install script: %s", script.Path)
		err = installChroot.UnsafeRun(func() error {
			err := shell.ExecuteLive(squashErrors, shell.ShellProgram, "-c", scriptPath, script.Args)
			if err != nil {
				return err
			}

			err = os.Remove(scriptPath)
			if err != nil {
				logger.Log.Errorf("Failed to cleanup post-install script (%s). Error: %s", scriptPath, err)
			}

			return err
		})

		if err != nil {
			return
		}
	}

	return
}

func setGrubCfgAdditionalCmdLine(grubPath string, kernelCommandline configuration.KernelCommandLine) (err error) {
	const (
		extraPattern = "{{.ExtraCommandLine}}"
	)

	logger.Log.Debugf("Adding ExtraCommandLine('%s') to %s", kernelCommandline.ExtraCommandLine, grubPath)
	err = sed(extraPattern, kernelCommandline.ExtraCommandLine, kernelCommandline.GetSedDelimeter(), grubPath)
	if err != nil {
		logger.Log.Warnf("Failed to append extra paramters to grub.cfg: %v", err)
	}

	return
}

func setGrubCfgIMA(grubPath string, kernelCommandline configuration.KernelCommandLine) (err error) {
	const (
		imaPrefix  = "ima_policy="
		imaPattern = "{{.IMAPolicy}}"
	)

	var ima string

	for _, policy := range kernelCommandline.ImaPolicy {
		ima += fmt.Sprintf("%v%v ", imaPrefix, policy)
	}

	logger.Log.Debugf("Adding ImaPolicy('%s') to %s", ima, grubPath)
	err = sed(imaPattern, ima, kernelCommandline.GetSedDelimeter(), grubPath)
	if err != nil {
		logger.Log.Warnf("Failed to set grub.cfg's IMA setting: %v", err)
	}

	return
}

func setGrubCfgLVM(grubPath, luksUUID string) (err error) {
	const (
		lvmPrefix  = "rd.lvm.lv="
		lvmPattern = "{{.LVM}}"
	)
	var cmdline configuration.KernelCommandLine

	var lvm string
	if luksUUID != "" {
		lvm = fmt.Sprintf("%v%v", lvmPrefix, diskutils.GetEncryptedRootVolPath())
	}

	logger.Log.Debugf("Adding lvm('%s') to %s", lvm, grubPath)
	err = sed(lvmPattern, lvm, cmdline.GetSedDelimeter(), grubPath)
	if err != nil {
		logger.Log.Warnf("Failed to set grub.cfg's LVM setting: %v", err)
	}

	return
}

func setGrubCfgLuksUUID(grubPath, uuid string) (err error) {
	const (
		luksUUIDPrefix  = "luks.uuid="
		luksUUIDPattern = "{{.LuksUUID}}"
	)
	var (
		cmdline  configuration.KernelCommandLine
		luksUUID string
	)
	if uuid != "" {
		luksUUID = fmt.Sprintf("%v%v", luksUUIDPrefix, uuid)
	}

	logger.Log.Debugf("Adding luks('%s') to %s", luksUUID, grubPath)
	err = sed(luksUUIDPattern, luksUUID, cmdline.GetSedDelimeter(), grubPath)
	if err != nil {
		logger.Log.Warnf("Failed to set grub.cfg's luksUUID: %v", err)
		return
	}

	return
}

func setGrubCfgBootUUID(bootUUID, grubPath string) (err error) {
	const (
		bootUUIDPattern = "{{.BootUUID}}"
	)
	var cmdline configuration.KernelCommandLine

	logger.Log.Debugf("Adding UUID('%s') to %s", bootUUID, grubPath)
	err = sed(bootUUIDPattern, bootUUID, cmdline.GetSedDelimeter(), grubPath)
	if err != nil {
		logger.Log.Warnf("Failed to set grub.cfg's bootUUID: %v", err)
		return
	}
	return
}

func setGrubCfgEncryptedVolume(grubPath string) (err error) {
	const (
		encryptedVolPattern = "{{.EncryptedVolume}}"
		lvmPrefix           = "lvm/"
	)
	var cmdline configuration.KernelCommandLine

	encryptedVol := fmt.Sprintf("%v%v%v%v", "(", lvmPrefix, diskutils.GetEncryptedRootVol(), ")")
	logger.Log.Debugf("Adding EncryptedVolume('%s') to %s", encryptedVol, grubPath)
	err = sed(encryptedVolPattern, encryptedVol, cmdline.GetSedDelimeter(), grubPath)
	if err != nil {
		logger.Log.Warnf("Failed to grub.cfg's encryptedVolume: %v", err)
		return
	}
	return
}

func setGrubCfgRootDevice(rootDevice, grubPath, luksUUID string) (err error) {
	const (
		rootDevicePattern = "{{.RootPartition}}"
	)
	var cmdline configuration.KernelCommandLine

	if luksUUID != "" {
		rootDevice = diskutils.GetEncryptedRootVolMapping()
	}

	logger.Log.Debugf("Adding RootDevice('%s') to %s", rootDevice, grubPath)
	err = sed(rootDevicePattern, rootDevice, cmdline.GetSedDelimeter(), grubPath)
	if err != nil {
		logger.Log.Warnf("Failed to set grub.cfg's rootDevice: %v", err)
		return
	}
	return
}

// ExtractPartitionArtifacts scans through the SystemConfig and generates all the partition-based artifacts specified.
// - workDirPath is the directory to place the artifacts
// - partIDToDevPathMap is a map of partition IDs to partition device paths
func ExtractPartitionArtifacts(workDirPath string, diskIndex int, disk configuration.Disk, partIDToDevPathMap map[string]string) (err error) {
	const (
		ext4ArtifactType = "ext4"
	)

	// Scan each partition for Artifacts
	for i, partition := range disk.Partitions {
		for _, artifact := range partition.Artifacts {
			if artifact.Type == ext4ArtifactType {
				devPath := partIDToDevPathMap[partition.ID]

				// Ext4 artifact type output is a .raw of the partition
				finalName := fmt.Sprintf("disk%d.partition%d.raw", diskIndex, i)
				err = createRawArtifact(workDirPath, devPath, finalName)
				if err != nil {
					return err
				}
			}
		}
	}
	return
}

func createRawArtifact(workDirPath, devPath, name string) (err error) {
	const (
		defaultBlockSize = 1024 * 1024 // 1MB
		squashErrors     = true
	)

	fullPath := filepath.Join(workDirPath, name)

	ddArgs := []string{
		fmt.Sprintf("if=%s", devPath),          // Input file.
		fmt.Sprintf("of=%s", fullPath),         // Output file.
		fmt.Sprintf("bs=%d", defaultBlockSize), // Size of one copied block.
	}

	return shell.ExecuteLive(squashErrors, "dd", ddArgs...)
}

// randomString generates a random string of the length specified
// using the provided legalCharacters.  crypto.rand is more secure
// than math.rand and does not need to be seeded.
func randomString(length int, legalCharacters string) (output string, err error) {
	b := make([]byte, length)
	_, err = rand.Read(b)
	if err != nil {
		return
	}

	count := byte(len(legalCharacters))
	for i := range b {
		idx := b[i] % count
		b[i] = legalCharacters[idx]
	}

	output = string(b)
	return
}

// isRunningInHyperV checks if the program is running in a Hyper-V Virtual Machine.
func isRunningInHyperV() (isHyperV bool, err error) {
	const (
		dmesgHypervTag = "Hyper-V"
	)

	stdout, stderr, err := shell.Execute("dmesg")
	if err != nil {
		logger.Log.Warnf("stderr: %v", stderr)
		return
	}
	logger.Log.Debugf("dmesg system: %s", stdout)

	// dmesg will print information about Hyper-V if it detects that Hyper-V is the hypervisor.
	// There will be multiple mentions of Hyper-V in the output (entry for BIOS as well as hypervisor)
	// and diagnostic information about hypervisor version.
	// Outside of Hyper-V, this name will not be reported.
	if strings.Contains(stdout, dmesgHypervTag) {
		logger.Log.Infof("Detected Hyper-V Host")
		isHyperV = true
	}
	return
}

//KernelPackages returns a list of kernel packages obtained from KernelOptions in the config's SystemConfigs
func KernelPackages(config configuration.Config) []*pkgjson.PackageVer {
	var packageList []*pkgjson.PackageVer
	// Add all the provided kernels to the package list
	for _, cfg := range config.SystemConfigs {
		for name, kernelPath := range cfg.KernelOptions {
			// Ignore comments
			if name[0] == '_' {
				continue
			}
			kernelName := filepath.Base(kernelPath)
			logger.Log.Tracef("Processing kernel %s derived from %s (required for option %s)", kernelName, kernelPath, name)
			packageList = append(packageList, &pkgjson.PackageVer{Name: kernelName})
		}
	}
	return packageList
}

// stopGPGAgent stops gpg-agent if it is running inside the installChroot.
//
// It is possible that one of the packages or post-install scripts started a GPG agent.
// e.g. when installing the mariner-repos SPEC, a GPG import occurs. This starts the gpg-agent process inside the chroot.
// To be able to cleanly exit the setup chroot, we must stop it.
func stopGPGAgent(installChroot *safechroot.Chroot) {
	installChroot.UnsafeRun(func() error {
		err := shell.ExecuteLiveWithCallback(logger.Log.Debug, logger.Log.Warn, false, "gpgconf", "--kill", "gpg-agent")
		if err != nil {
			// This is non-fatal, as there is no guarentee the image has gpg agent started.
			logger.Log.Warnf("Failed to stop gpg-agent. This is expected if it is not installed: %s", err)
		}

		return nil
	})
}
