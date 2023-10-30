// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package installutils

import (
	"fmt"
	"os"
	"path"
	"path/filepath"
	"runtime"
	"sort"
	"strconv"
	"strings"
	"syscall"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repocloner"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/retry"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/tdnf"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/timestamp"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/userutils"
)

const (
	PackageManifestRelativePath = "image_pkg_manifest_installroot.json"

	// NullDevice represents the /dev/null device used as a mount device for overlay images.
	NullDevice     = "/dev/null"
	overlay        = "overlay"
	rootMountPoint = "/"

	// rpmDependenciesDirectory is the directory which contains RPM database. It is not required for images that do not contain RPM.
	rpmDependenciesDirectory = "/var/lib/rpm"

	// rpmManifestDirectory is the directory containing manifests of installed packages to support distroless vulnerability scanning tools.
	rpmManifestDirectory = "/var/lib/rpmmanifest"

	// /boot directory should be only accesible by root. The directories need the execute bit as well.
	bootDirectoryFileMode = 0400
	bootDirectoryDirMode  = 0700
)

// PackageList represents the list of packages to install into an image
type PackageList struct {
	Packages []string `json:"packages"`
}

// GetRequiredPackagesForInstall returns the list of packages required for
// the tooling to install an image
func GetRequiredPackagesForInstall() []*pkgjson.PackageVer {
	packageList := []*pkgjson.PackageVer{}

	// grub2-pc package is needed for the install tools to build/install the legacy grub bootloader
	// Note: only required on x86_64 installs
	if runtime.GOARCH == "amd64" {
		packageList = append(packageList, &pkgjson.PackageVer{Name: "grub2-pc"})
	}

	return packageList
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
// - diffDiskBuild is a flag that denotes whether this is a diffdisk build or not
func CreateMountPointPartitionMap(partDevPathMap, partIDToFsTypeMap map[string]string, partitionSettings []configuration.PartitionSetting) (mountPointDevPathMap, mountPointToFsTypeMap, mountPointToMountArgsMap map[string]string, diffDiskBuild bool) {
	mountPointDevPathMap = make(map[string]string)
	mountPointToFsTypeMap = make(map[string]string)
	mountPointToMountArgsMap = make(map[string]string)

	// Go through each PartitionSetting
	for _, partitionSetting := range partitionSettings {
		logger.Log.Tracef("%v[%v]", partitionSetting.ID, partitionSetting.MountPoint)
		partDevPath, ok := partDevPathMap[partitionSetting.ID]
		if ok {
			if partitionSetting.OverlayBaseImage == "" {
				mountPointDevPathMap[partitionSetting.MountPoint] = partDevPath
				mountPointToFsTypeMap[partitionSetting.MountPoint] = partIDToFsTypeMap[partitionSetting.ID]
				mountPointToMountArgsMap[partitionSetting.MountPoint] = partitionSetting.MountOptions
			} else {
				diffDiskBuild = true
			}
		}
		logger.Log.Tracef("%v", mountPointDevPathMap)
	}
	return
}

// sortMountPoints will return a slice of mount points sorted either forward (for mounting)
// or backwards (for unmounting)
// - mountPointMap is the map of mountpoint to partition device path
// - sortForUnmount reverses the sorting order so mounts are unmounted most nested to least nested
func sortMountPoints(mountPointMap *map[string]string, sortForUnmount bool) (remainingMounts []string) {
	// Convert the installMap into a slice of mount points so it can be sorted
	for mountPoint := range *mountPointMap {
		// Skip empty mount points
		if mountPoint == "" {
			continue
		}
		remainingMounts = append(remainingMounts, mountPoint)
	}

	// We need to make sure we sort the mount points so we don't mount things in the wrong order
	// e.g.: /dev is mounted before /dev/pts is.
	if !sortForUnmount {
		sort.Sort(sort.StringSlice(remainingMounts))
	} else {
		// Reverse the sorting so we unmount in the opposite order
		sort.Sort(sort.Reverse(sort.StringSlice(remainingMounts)))
	}
	return
}

// UpdatePartitionMapWithOverlays Creates Overlay map and updates the partition map with required parameters.
// - partDevPathMap is a map of partition IDs to partition device paths
// - partIDToFsTypeMap is a map of partition IDs to filesystem type
// - mountPointDevPathMap is a map of mountpoint to partition device path
// - mountPointToFsTypeMap is a map of mountpoint to filesystem type
// - mountPointToMountArgsMap is a map of mountpoint to mount arguments to be passed on a call to mount
// - config is the SystemConfig from a config file
// Output
// - mountPointToOverlayMap is a map of mountpoint to overlay data
func UpdatePartitionMapWithOverlays(partDevPathMap, partIDToFsTypeMap, mountPointDevPathMap, mountPointToFsTypeMap, mountPointToMountArgsMap map[string]string, config configuration.SystemConfig) (mountPointToOverlayMap map[string]*Overlay, err error) {
	mountPointToOverlayMap = make(map[string]*Overlay)

	// Go through each PartitionSetting
	for _, partitionSetting := range config.PartitionSettings {
		logger.Log.Tracef("%v[%v]", partitionSetting.ID, partitionSetting.MountPoint)
		if partitionSetting.OverlayBaseImage != "" {
			err = createOverlayPartition(partitionSetting, mountPointDevPathMap, mountPointToMountArgsMap, mountPointToFsTypeMap, mountPointToOverlayMap)
			if err != nil {
				return
			}
		}
	}
	return
}

func createOverlayPartition(partitionSetting configuration.PartitionSetting, mountPointDevPathMap, mountPointToMountArgsMap, mountPointToFsTypeMap map[string]string, mountPointToOverlayMap map[string]*Overlay) (err error) {
	//Mount the base image
	//Create a temp upper dir
	//Add to the mount args
	devicePath, err := diskutils.SetupLoopbackDevice(partitionSetting.OverlayBaseImage)

	if err != nil {
		logger.Log.Errorf("Could not setup loop back device for mount (%s)", partitionSetting.OverlayBaseImage)

		return
	}

	overlayMount := NewOverlay(devicePath)

	mountPointToOverlayMap[partitionSetting.MountPoint] = &overlayMount

	// For overlays the device to be mounted is /dev/null. The actual device is synthesized from the lower and upper dir args
	// These args are passed to the mount command using -o
	mountPointDevPathMap[partitionSetting.MountPoint] = NullDevice
	mountPointToMountArgsMap[partitionSetting.MountPoint] = overlayMount.getMountArgs()
	mountPointToFsTypeMap[partitionSetting.MountPoint] = overlay
	return
}

// CreateInstallRoot walks through the map of mountpoints and mounts the partitions into installroot
// - installRoot is the destination path to mount these partitions
// - mountPointMap is the map of mountpoint to partition device path
// - mountPointToFsTypeMap is the map of mountpoint to the file type
// - mountPointToMountArgsMap is the map of mountpoint to the parameters sent to
// - mountPointToOverlayMap is the map of mountpoint to the overlay structure containing the base image
func CreateInstallRoot(installRoot string, mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap map[string]string, mountPointToOverlayMap map[string]*Overlay) (installMap map[string]string, err error) {
	installMap = make(map[string]string)
	for _, mountPoint := range sortMountPoints(&mountPointMap, false) {
		device := mountPointMap[mountPoint]
		err = mountSingleMountPoint(installRoot, mountPoint, device, mountPointToFsTypeMap[mountPoint], mountPointToMountArgsMap[mountPoint], mountPointToOverlayMap[mountPoint])
		if err != nil {
			return
		}
		installMap[mountPoint] = device
	}
	return
}

// DestroyInstallRoot unmounts each of the installroot mountpoints in order, ensuring that the root mountpoint is last
// - installRoot is the path to the root where the mountpoints exist
// - mountPointMap is the map of mountpoints to partition device paths
// - mountPointToOverlayMap is the map of mountpoints to overlay devices
func DestroyInstallRoot(installRoot string, mountPointMap map[string]string, mountPointToOverlayMap map[string]*Overlay) (err error) {
	logger.Log.Trace("Destroying InstallRoot")

	defer OverlayUnmount(mountPointToOverlayMap)

	logger.Log.Trace("Destroying InstallRoot")
	// Reverse order for unmounting
	for _, mountPoint := range sortMountPoints(&mountPointMap, true) {
		err = diskutils.BlockOnDiskIO(mountPointMap[mountPoint])
		if err != nil {
			logger.Log.Errorf("DestroyInstallRoot flush IO Error: %s", err.Error())
		}
		err = unmountSingleMountPoint(installRoot, mountPoint)
		if err != nil {
			logger.Log.Errorf("DestroyInstallRoot Error: %s", err.Error())
			return
		}
	}

	return
}

// OverlayUnmount unmounts the overlay devices that are stored in the map, It ignores the errors and returns the last error.
// - mountPointToOverlayMap is the map of mountpoints to overlay devices
func OverlayUnmount(mountPointToOverlayMap map[string]*Overlay) (err error) {
	for _, overlay := range mountPointToOverlayMap {
		temperr := overlay.unmount()
		if temperr != nil {
			// Log a warning on error. Return the last error.
			logger.Log.Warnf("Failed to unmount the overlay (%+v). Continuing without unmounting: (%v)", overlay, temperr)
			err = temperr
		}
	}
	return
}

func mountSingleMountPoint(installRoot, mountPoint, device, fsType, extraOptions string, overlayDevice *Overlay) (err error) {
	mountPath := filepath.Join(installRoot, mountPoint)
	err = os.MkdirAll(mountPath, os.ModePerm)
	if err != nil {
		logger.Log.Warnf("Failed to create mountpoint: %v", err)
		return
	}

	if overlayDevice != nil {
		err = overlayDevice.setupFolders()
		if err != nil {
			logger.Log.Errorf("Failed to create mount for overlay device: %v", err)
			return
		}
	}
	err = mount(mountPath, device, fsType, extraOptions)
	return
}

func unmountSingleMountPoint(installRoot, mountPoint string) (err error) {

	mountPath := filepath.Join(installRoot, mountPoint)
	err = umount(mountPath)
	return
}

func mount(path, device, fsType, extraOptions string) (err error) {
	const squashErrors = false

	var mountArgs []string

	if fsType != "" {
		mountArgs = append(mountArgs, "-t", fsType)
	}

	if extraOptions != "" {
		mountArgs = append(mountArgs, "-o", extraOptions)
	}

	mountArgs = append(mountArgs, device, path)

	err = shell.ExecuteLive(squashErrors, "mount", mountArgs...)
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

// PackageNamesFromSingleSystemConfig goes through the "PackageLists" and "Packages" fields in the "SystemConfig" object, extracting
// from packageList JSONs and packages listed in config itself to create one comprehensive package list.
// NOTE: the package list contains the versions restrictions for the packages, if present, in the form "[package][condition][version]".
//
//	Example: gcc=9.1.0
//
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

	logger.Log.Tracef("Processing inline packages")
	finalPkgList = append(finalPkgList, systemConfig.Packages...)

	logger.Log.Tracef("finalPkgList = %v", finalPkgList)
	return
}

// SelectKernelPackage selects the kernel to use for the current installation
// based on the KernelOptions field of the system configuration.
func SelectKernelPackage(systemConfig configuration.SystemConfig, isLiveInstall bool) (kernelPkg string, err error) {
	const defaultOption = "default"

	optionToUse := defaultOption

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
			var packageVer *pkgjson.PackageVer

			packageVer, err = pkgjson.PackageStringToPackageVer(pkg)
			if err != nil {
				logger.Log.Errorf("Failed to parse packages list from system config \"%s\".", systemCfg.Name)
				return
			}

			packages = append(packages, packageVer)
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
// - partIDToDevPathMap is a map of partition IDs to physical device paths
// - partIDToFsTypeMap is a map of partition IDs to filesystem type
// - isRootFS specifies if the installroot is either backed by a directory (rootfs) or a raw disk
// - encryptedRoot stores information about the encrypted root device if root encryption is enabled
// - diffDiskBuild is a flag that denotes whether this is a diffdisk build or not
// - hidepidEnabled is a flag that denotes whether /proc will be mounted with the hidepid option
func PopulateInstallRoot(installChroot *safechroot.Chroot, packagesToInstall []string, config configuration.SystemConfig, installMap, mountPointToFsTypeMap, mountPointToMountArgsMap, partIDToDevPathMap, partIDToFsTypeMap map[string]string, isRootFS bool, encryptedRoot diskutils.EncryptedRootDevice, diffDiskBuild, hidepidEnabled bool) (err error) {
	timestamp.StartEvent("populating install root", nil)
	defer timestamp.StopEvent(nil)

	const (
		filesystemPkg = "filesystem"
	)

	defer stopGPGAgent(installChroot)

	ReportAction("Initializing RPM Database")

	installRoot := filepath.Join(rootMountPoint, installChroot.RootDir())

	// Initialize RPM Database so we can install RPMs into the installroot
	err = initializeRpmDatabase(installRoot, diffDiskBuild)
	if err != nil {
		return
	}

	if !config.RemoveRpmDb {
		// User wants to avoid removing the RPM database.
		logger.Log.Debug("RemoveRpmDb is not turned on. Skipping RPM database cleanup.")
	} else {
		defer func() {
			// Signal an error if cleanup fails; don't overwrite the previous error though.
			// Failure to clean up the RPM database constitutes a build break.
			cleanupErr := cleanupRpmDatabase(installRoot)
			if err == nil {
				err = cleanupErr
			}
		}()
	}

	// Calculate how many packages need to be installed so an accurate percent complete can be reported
	installedPackages, err := calculateTotalPackages(packagesToInstall, installRoot)
	if err != nil {
		return
	}
	totalPackages := len(installedPackages.Repo)

	// Write out JSON file with list of packages included in the image
	packageManifestPath := filepath.Join("/", PackageManifestRelativePath)
	err = jsonutils.WriteJSONFile(packageManifestPath, installedPackages)
	if err != nil {
		return
	}

	// Keep a running total of how many packages have been installed through all the `TdnfInstallWithProgress` invocations
	packagesInstalled := 0

	timestamp.StartEvent("installing packages", nil)
	// Install filesystem package first
	packagesInstalled, err = TdnfInstallWithProgress(filesystemPkg, installRoot, packagesInstalled, totalPackages, true)
	if err != nil {
		return
	}

	hostname := config.Hostname
	if !isRootFS && mountPointToFsTypeMap[rootMountPoint] != overlay {
		// Add /etc/hostname
		err = updateHostname(installChroot.RootDir(), hostname)
		if err != nil {
			return
		}
	}

	// Install packages one-by-one to avoid exhausting memory
	// on low resource systems
	for _, pkg := range packagesToInstall {
		packagesInstalled, err = TdnfInstallWithProgress(pkg, installRoot, packagesInstalled, totalPackages, true)
		if err != nil {
			return
		}
	}

	timestamp.StopEvent(nil) // installing packages
	timestamp.StartEvent("final image configuration", nil)

	// Copy additional files
	err = copyAdditionalFiles(installChroot, config)
	if err != nil {
		return
	}

	if !isRootFS {
		// Configure system files
		err = configureSystemFiles(installChroot, hostname, config, installMap, mountPointToFsTypeMap, mountPointToMountArgsMap, partIDToDevPathMap, partIDToFsTypeMap, encryptedRoot, hidepidEnabled)
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

	if config.RemoveRpmDb {
		// When the RemoveRpmDb flag is true, generate a list of installed packages since they cannot be queiried at runtime
		logger.Log.Info("Generating manifest with package information since RemoveRpmDb is enabled.")
		generateContainerManifests(installChroot)
	}

	if len(config.Networks) > 0 {
		err = configuration.ConfigureNetwork(installChroot, config)
		if err != nil {
			return
		}
	}

	timestamp.StopEvent(nil) // final image configuration

	// Run post-install scripts from within the installroot chroot
	err = runPostInstallScripts(installChroot, config)
	return
}

func generateContainerManifests(installChroot *safechroot.Chroot) {
	installRoot := filepath.Join(rootMountPoint, installChroot.RootDir())
	rpmDir := filepath.Join(installRoot, rpmDependenciesDirectory)
	rpmManifestDir := filepath.Join(installRoot, rpmManifestDirectory)
	manifest1Path := filepath.Join(rpmManifestDir, "container-manifest-1")
	manifest2Path := filepath.Join(rpmManifestDir, "container-manifest-2")

	os.MkdirAll(rpmManifestDir, os.ModePerm)

	// Please contact Qualys before changing the following rpm query.
	shell.ExecuteAndLogToFile(manifest1Path, "rpm", "--dbpath", rpmDir, "-qa")
	// Please contact Qualys, AquaSec (trivy) and other supported scanning vendors before changing the following rpm query.
	shell.ExecuteAndLogToFile(manifest2Path, "rpm", "--dbpath", rpmDir, "-qa", "--qf", "%{NAME}\t%{VERSION}-%{RELEASE}\t%{INSTALLTIME}\t%{BUILDTIME}\t%{VENDOR}\t(none)\t%{SIZE}\t%{ARCH}\t%{EPOCHNUM}\t%{SOURCERPM}\n")

	return
}

func initializeRpmDatabase(installRoot string, diffDiskBuild bool) (err error) {
	if !diffDiskBuild {
		var (
			stdout string
			stderr string
		)

		stdout, stderr, err = shell.Execute("rpm", "--root", installRoot, "--initdb")
		if err != nil {
			logger.Log.Warnf("Failed to create rpm database: %v", err)
			logger.Log.Warn(stdout)
			logger.Log.Warn(stderr)
			return err
		}
	}
	return
}

// TdnfInstall installs a package into the current environment without calculating progress
func TdnfInstall(packageName, installRoot string) (packagesInstalled int, err error) {
	packagesInstalled, err = TdnfInstallWithProgress(packageName, installRoot, 0, 0, false)
	return
}

// TdnfInstallWithProgress installs a package in the current environment while optionally reporting progress
func TdnfInstallWithProgress(packageName, installRoot string, currentPackagesInstalled, totalPackages int, reportProgress bool) (packagesInstalled int, err error) {
	timestamp.StartEvent("installing"+packageName, nil)
	defer timestamp.StopEvent(nil)
	var (
		releaseverCliArg string
	)

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
		if reportProgress {
			ReportAction(status)
		} else {
			// ReportAction() logs at debug level
			logger.Log.Debug(status)
		}

		packagesInstalled++

		if reportProgress {
			// Calculate and report what percentage of packages have been installed
			percentOfPackagesInstalled := float32(packagesInstalled) / float32(totalPackages)
			progress := int(percentOfPackagesInstalled * 100)
			ReportPercentComplete(progress)
		}
	}

	releaseverCliArg, err = tdnf.GetReleaseverCliArg()
	if err != nil {
		return
	}

	// TDNF 3.x uses repositories from installchroot instead of host. Passing setopt for repo files directory to use local repo for installroot installation
	err = shell.ExecuteLiveWithCallback(onStdout, logger.Log.Warn, true, "tdnf", "-v", "install", packageName,
		"--installroot", installRoot, "--nogpgcheck", "--assumeyes", "--setopt", "reposdir=/etc/yum.repos.d/",
		releaseverCliArg)
	if err != nil {
		logger.Log.Warnf("Failed to tdnf install: %v. Package name: %v", err, packageName)
	}

	return
}

func configureSystemFiles(installChroot *safechroot.Chroot, hostname string, config configuration.SystemConfig, installMap, mountPointToFsTypeMap, mountPointToMountArgsMap, partIDToDevPathMap, partIDToFsTypeMap map[string]string, encryptedRoot diskutils.EncryptedRootDevice, hidepidEnabled bool) (err error) {
	// Update hosts file
	err = updateHosts(installChroot.RootDir(), hostname)
	if err != nil {
		return
	}

	// Update fstab
	err = UpdateFstab(installChroot.RootDir(), config.PartitionSettings, installMap, mountPointToFsTypeMap, mountPointToMountArgsMap, partIDToDevPathMap, partIDToFsTypeMap, hidepidEnabled)
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

// calculateTotalPackages will simulate installing the provided list of packages in the installRoot.
// all packages that will be installed are returned in installedPackages, and a manifest with these packages
// is generated under build/imagegen/$config_name/image_pkg_manifest.json
func calculateTotalPackages(packages []string, installRoot string) (installedPackages *repocloner.RepoContents, err error) {
	var (
		releaseverCliArg string
	)
	installedPackages = &repocloner.RepoContents{}
	const tdnfAssumeNoStdErr = "Error(1032) : Operation aborted.\n"

	releaseverCliArg, err = tdnf.GetReleaseverCliArg()
	if err != nil {
		return
	}

	// For every package calculate what dependencies would also be installed from it.
	// checkedPackageSet contains a mapping of all package IDs (name, version, etc) to avoid calculating duplicates
	checkedPackageSet := make(map[string]bool)
	for _, pkg := range packages {
		var (
			stdout string
			stderr string
		)

		// Issue an install request but stop right before actually performing the install (assumeno)
		stdout, stderr, err = shell.Execute("tdnf", "install", releaseverCliArg, "--assumeno", "--nogpgcheck", pkg, "--installroot", installRoot)
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
		for _, line := range splitStdout {
			matches := tdnf.InstallPackageRegex.FindStringSubmatch(line)
			if len(matches) != tdnf.InstallMaxMatchLen {
				// This line contains output other than a package information; skip it
				continue
			}

			pkg := &repocloner.RepoPackage{
				Name:         matches[tdnf.InstallPackageName],
				Version:      matches[tdnf.InstallPackageVersion],
				Architecture: matches[tdnf.InstallPackageArch],
				Distribution: matches[tdnf.InstallPackageDist],
			}

			pkgID := pkg.ID()
			if checkedPackageSet[pkgID] {
				logger.Log.Tracef("Skipping duplicate package: %s", line)
				continue
			}
			checkedPackageSet[pkgID] = true

			logger.Log.Debugf("Added installedPackages entry for: %v", pkgID)

			installedPackages.Repo = append(installedPackages.Repo, pkg)
		}
	}

	logger.Log.Debugf("Total number of packages to be installed: %d", len(installedPackages.Repo))

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
		machineIDFilePerms = 0444
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

func UpdateFstab(installRoot string, partitionSettings []configuration.PartitionSetting, installMap, mountPointToFsTypeMap, mountPointToMountArgsMap, partIDToDevPathMap, partIDToFsTypeMap map[string]string, hidepidEnabled bool) (err error) {
	const (
		doPseudoFsMount = true
	)
	ReportAction("Configuring fstab")

	for mountPoint, devicePath := range installMap {
		if mountPoint != "" && devicePath != NullDevice {
			partSetting := configuration.FindMountpointPartitionSetting(partitionSettings, mountPoint)
			if partSetting == nil {
				err = fmt.Errorf("unable to find PartitionSetting for '%s", mountPoint)
				return
			}
			err = addEntryToFstab(installRoot, mountPoint, devicePath, mountPointToFsTypeMap[mountPoint], mountPointToMountArgsMap[mountPoint], partSetting.MountIdentifier, !doPseudoFsMount)
			if err != nil {
				return
			}
		}
	}

	if hidepidEnabled {
		err = addEntryToFstab(installRoot, "/proc", "proc", "proc", "rw,nosuid,nodev,noexec,relatime,hidepid=2", configuration.MountIdentifierNone, doPseudoFsMount)
		if err != nil {
			return
		}
	}

	// Add swap entry if there is one
	for partID, fstype := range partIDToFsTypeMap {
		if fstype == "linux-swap" {
			swapPartitionPath, exists := partIDToDevPathMap[partID]
			if exists {
				err = addEntryToFstab(installRoot, "none", swapPartitionPath, "swap", "", "", doPseudoFsMount)
				if err != nil {
					return
				}
			}
		}
	}

	return
}

func addEntryToFstab(installRoot, mountPoint, devicePath, fsType, mountArgs string, identifierType configuration.MountIdentifier, doPseudoFsMount bool) (err error) {
	const (
		fstabPath        = "/etc/fstab"
		rootfsMountPoint = "/"
		defaultOptions   = "defaults"
		swapFsType       = "swap"
		swapOptions      = "sw"
		readOnlyOptions  = "ro"
		defaultDump      = "0"
		disablePass      = "0"
		rootPass         = "1"
		defaultPass      = "2"
	)

	var options string

	if mountArgs == "" {
		options = defaultOptions
		if diskutils.IsReadOnlyDevice(devicePath) {
			options = fmt.Sprintf("%s,%s", options, readOnlyOptions)
		}
	} else {
		options = mountArgs
	}

	if fsType == swapFsType {
		options = swapOptions
	}

	fullFstabPath := filepath.Join(installRoot, fstabPath)

	// Get the block device
	var device string
	if diskutils.IsEncryptedDevice(devicePath) || diskutils.IsReadOnlyDevice(devicePath) || doPseudoFsMount {
		device = devicePath
	} else {
		device, err = FormatMountIdentifier(identifierType, devicePath)
		if err != nil {
			logger.Log.Warnf("Failed to get mount identifier for block device %v", devicePath)
			return err
		}
	}

	// Note: Rootfs should always have a pass number of 1. All other mountpoints are either 0 or 2
	pass := defaultPass
	if mountPoint == rootfsMountPoint {
		pass = rootPass
	} else if doPseudoFsMount {
		pass = disablePass
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
	// Encrypted root will always use UUID rather than the PartitionSetting.MountIdentifier
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

// InstallGrubEnv installs an empty grubenv f
func InstallGrubEnv(installRoot, assetsDir string) (err error) {
	const (
		assetGrubEnvFile = "grub2/grubenv"
		grubEnvFile      = "boot/grub2/grubenv"
	)
	assetGrubEnvFileFullPath := filepath.Join(assetsDir, assetGrubEnvFile)
	installGrubEnvFile := filepath.Join(installRoot, grubEnvFile)
	err = file.CopyAndChangeMode(assetGrubEnvFileFullPath, installGrubEnvFile, bootDirectoryDirMode, bootDirectoryFileMode)
	if err != nil {
		logger.Log.Warnf("Failed to copy and change mode of grubenv: %v", err)
		return
	}

	return
}

// InstallGrubCfg installs the main grub config to the boot partition
// - installRoot is the base install directory
// - rootDevice holds the root partition
// - bootUUID is the UUID for the boot partition
// - bootPrefix is the path to the /boot grub configs based on the mountpoints (i.e., if /boot is a separate partition from the rootfs partition, bootPrefix="").
// - encryptedRoot holds the encrypted root information if encrypted root is enabled
// - kernelCommandLine contains additional kernel parameters which may be optionally set
// - readOnlyRoot holds the dm-verity read-only root partition information if dm-verity is enabled.
// - isBootPartitionSeparate is a boolean value which is true if the /boot partition is separate from the root partition
// Note: this boot partition could be different than the boot partition specified in the bootloader.
// This boot partition specifically indicates where to find the kernel, config files, and initrd
func InstallGrubCfg(installRoot, rootDevice, bootUUID, bootPrefix, assetsDir string, encryptedRoot diskutils.EncryptedRootDevice, kernelCommandLine configuration.KernelCommandLine, readOnlyRoot diskutils.VerityDevice, isBootPartitionSeparate bool) (err error) {
	const (
		assetGrubcfgFile = "grub2/grub.cfg"
		grubCfgFile      = "boot/grub2/grub.cfg"
		assetGrubDefFile = "grub2/grub"
		grubDefFile      = "etc/default/grub"
	)

	// Copy the bootloader's grub.cfg and set the file permission
	assetGrubcfgFileFullPath := filepath.Join(assetsDir, assetGrubcfgFile)
	installGrubCfgFile := filepath.Join(installRoot, grubCfgFile)

	assetGrubDefFileFullPath := filepath.Join(assetsDir, assetGrubDefFile)
	installGrubDefFile := filepath.Join(installRoot, grubDefFile)

	err = file.CopyAndChangeMode(assetGrubcfgFileFullPath, installGrubCfgFile, bootDirectoryDirMode, bootDirectoryFileMode)
	if err != nil {
		return
	}
	err = file.CopyAndChangeMode(assetGrubDefFileFullPath, installGrubDefFile, bootDirectoryDirMode, 0755)
	if err != nil {
		return
	}

	for _, installedFile := range []string{installGrubCfgFile, installGrubDefFile} {
		// Add in bootUUID
		err = setGrubCfgBootUUID(bootUUID, installedFile)
		if err != nil {
			logger.Log.Warnf("Failed to set bootUUID in grub.cfg: %v", err)
			return
		}

		// Add in bootPrefix
		err = setGrubCfgBootPrefix(bootPrefix, installedFile)
		if err != nil {
			logger.Log.Warnf("Failed to set bootPrefix in grub.cfg: %v", err)
			return
		}

		// Add in rootDevice
		err = setGrubCfgRootDevice(rootDevice, installedFile, encryptedRoot.LuksUUID)
		if err != nil {
			logger.Log.Warnf("Failed to set rootDevice in grub.cfg: %v", err)
			return
		}

		// Add in rootLuksUUID
		err = setGrubCfgLuksUUID(installedFile, encryptedRoot.LuksUUID)
		if err != nil {
			logger.Log.Warnf("Failed to set luksUUID in grub.cfg: %v", err)
			return
		}

		// Add in logical volumes to active
		err = setGrubCfgLVM(installedFile, encryptedRoot.LuksUUID)
		if err != nil {
			logger.Log.Warnf("Failed to set lvm.lv in grub.cfg: %v", err)
			return
		}

		// Configure IMA policy
		err = setGrubCfgIMA(installedFile, kernelCommandLine)
		if err != nil {
			logger.Log.Warnf("Failed to set ima_policy in grub.cfg: %v", err)
			return
		}

		err = setGrubCfgReadOnlyVerityRoot(installedFile, readOnlyRoot)
		if err != nil {
			logger.Log.Warnf("Failed to set verity root in grub.cfg: %v", err)
			return
		}

		err = setGrubCfgSELinux(installedFile, kernelCommandLine)
		if err != nil {
			logger.Log.Warnf("Failed to set SELinux in grub.cfg: %v", err)
			return
		}

		// Configure FIPS
		err = setGrubCfgFIPS(isBootPartitionSeparate, bootUUID, installedFile, kernelCommandLine)
		if err != nil {
			logger.Log.Warnf("Failed to set FIPS in grub.cfg: %v", err)
			return
		}

		err = setGrubCfgCGroup(installedFile, kernelCommandLine)
		if err != nil {
			logger.Log.Warnf("Failed to set CGroup configuration in grub.cfg: %v", err)
			return
		}

		// Append any additional command line parameters
		err = setGrubCfgAdditionalCmdLine(installedFile, kernelCommandLine)
		if err != nil {
			logger.Log.Warnf("Failed to append extra command line parameters in grub.cfg: %v", err)
			return
		}
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
	rootUserAdded := false

	for _, user := range users {
		logger.Log.Infof("Adding user (%s)", user.Name)
		ReportActionf("Adding user: %s", user.Name)

		var (
			isRoot bool
		)

		isRoot, err = createUserWithPassword(installChroot, user)
		if err != nil {
			return
		}
		if isRoot {
			rootUserAdded = true
		}

		err = ConfigureUserGroupMembership(installChroot, user.Name, user.PrimaryGroup, user.SecondaryGroups)
		if err != nil {
			return
		}

		err = ProvisionUserSSHCerts(installChroot, user.Name, user.SSHPubKeyPaths)
		if err != nil {
			return
		}

		err = ConfigureUserStartupCommand(installChroot, user.Name, user.StartupCommand)
		if err != nil {
			return
		}
	}

	// If no root entry was specified in the config file, never expire the root password
	if !rootUserAdded {
		logger.Log.Debugf("No root user entry found in config file. Setting root password to never expire.")

		// Ignore updating if there is no shadow file to update in the target image
		installChrootShadowFile := filepath.Join(installChroot.RootDir(), userutils.ShadowFile)
		if exists, ferr := file.PathExists(installChrootShadowFile); ferr != nil {
			logger.Log.Error("Error accessing shadow file.")
			return ferr
		} else if !exists {
			logger.Log.Debugf("No shadow file to update. Skipping setting password to never expire.")
			return
		}
		err = Chage(installChroot, -1, "root")
	}
	return
}

func createUserWithPassword(installChroot *safechroot.Chroot, user configuration.User) (isRoot bool, err error) {
	var (
		hashedPassword          string
		installChrootShadowFile = filepath.Join(installChroot.RootDir(), userutils.ShadowFile)
	)

	// Get the hashed password for the user
	if user.PasswordHashed {
		hashedPassword = user.Password
	} else {
		hashedPassword, err = userutils.HashPassword(user.Password)
		if err != nil {
			return
		}
	}
	logger.Log.Tracef("hashed password: %v", hashedPassword)

	if strings.TrimSpace(hashedPassword) == "" {
		err = fmt.Errorf("empty password for user (%s) is not allowed", user.Name)
		return
	}

	// Create the user with the given hashed password
	if user.Name == userutils.RootUser {
		if user.UID != "" {
			logger.Log.Warnf("Ignoring UID for (%s) user, using default", userutils.RootUser)
		}

		if exists, ferr := file.PathExists(installChrootShadowFile); ferr != nil {
			logger.Log.Error("Error accessing shadow file.")
			err = ferr
			return
		} else if !exists {
			logger.Log.Debugf("No shadow file to update. Skipping updating user password..")
		} else {
			// Update shadow file
			err = userutils.UpdateUserPassword(installChroot.RootDir(), user.Name, hashedPassword)
			if err != nil {
				logger.Log.Warnf("Encountered a problem when updating root user password: %s", err)
				return
			}
		}
		isRoot = true
	} else {
		err = userutils.AddUser(user.Name, hashedPassword, user.UID, installChroot)
		if err != nil {
			return
		}
	}

	// Update password expiration
	if user.PasswordExpiresDays != 0 {
		// Ignore updating if there is no shadow file to update
		if exists, ferr := file.PathExists(installChrootShadowFile); ferr != nil {
			logger.Log.Error("Error accessing shadow file.")
			err = ferr
			return
		} else if !exists {
			logger.Log.Debugf("No shadow file to update. Skipping updating password expiration.")
			return
		}

		err = Chage(installChroot, user.PasswordExpiresDays, user.Name)
	}

	return
}

// chage works in the same way as invoking "chage -M passwordExpirationInDays username"
// i.e. it sets the maximum password expiration date.
func Chage(installChroot *safechroot.Chroot, passwordExpirationInDays int64, username string) (err error) {
	var (
		shadow            []string
		usernameWithColon = fmt.Sprintf("%s:", username)
	)

	installChrootShadowFile := filepath.Join(installChroot.RootDir(), userutils.ShadowFile)

	shadow, err = file.ReadLines(installChrootShadowFile)
	if err != nil {
		return
	}

	for n, entry := range shadow {
		done := false
		// Entries in shadow are separated by colon and start with a username
		// Finding one that starts like that means we've found our entry
		if strings.HasPrefix(entry, usernameWithColon) {
			// Each line in shadow contains 9 fields separated by colon ("") in the following order:
			// login name, encrypted password, date of last password change,
			// minimum password age, maximum password age, password warning period,
			// password inactivity period, account expiration date, reserved field for future use
			const (
				passwordNeverExpiresValue = -1
				loginNameField            = 0
				encryptedPasswordField    = 1
				passwordChangedField      = 2
				minPasswordAgeField       = 3
				maxPasswordAgeField       = 4
				warnPeriodField           = 5
				inactivityPeriodField     = 6
				expirationField           = 7
				reservedField             = 8
				totalFieldsCount          = 9
			)

			fields := strings.Split(entry, ":")
			// Any value other than totalFieldsCount indicates error in parsing
			if len(fields) != totalFieldsCount {
				return fmt.Errorf("invalid shadow entry (%v) for user (%s): %d fields expected, but %d found", fields, username, totalFieldsCount, len(fields))
			}

			if passwordExpirationInDays == passwordNeverExpiresValue {
				// If passwordExpirationInDays is equal to -1, it means that password never expires.
				// This is expressed by leaving account expiration date field (and fields after it) empty.
				for _, fieldToChange := range []int{maxPasswordAgeField, warnPeriodField, inactivityPeriodField, expirationField, reservedField} {
					fields[fieldToChange] = ""
				}
				// Each user appears only once, since we found one, we are finished; save the changes and exit.
				done = true
			} else if passwordExpirationInDays < passwordNeverExpiresValue {
				// Values smaller than -1 make no sense
				return fmt.Errorf("invalid value for maximum user's (%s) password expiration: %d; should be greater than %d", username, passwordExpirationInDays, passwordNeverExpiresValue)
			} else {
				// If passwordExpirationInDays has any other value, it's the maximum expiration date: set it accordingly
				// To do so, we need to ensure that passwordChangedField holds a valid value and then sum it with passwordExpirationInDays.
				var (
					passwordAge     int64
					passwordChanged = fields[passwordChangedField]
				)

				if passwordChanged == "" {
					// Set to the number of days since epoch
					fields[passwordChangedField] = fmt.Sprintf("%d", int64(time.Since(time.Unix(0, 0)).Hours()/24))
				}
				passwordAge, err = strconv.ParseInt(fields[passwordChangedField], 10, 64)
				if err != nil {
					return
				}
				fields[expirationField] = fmt.Sprintf("%d", passwordAge+passwordExpirationInDays)

				// Each user appears only once, since we found one, we are finished; save the changes and exit.
				done = true
			}
			if done {
				// Create and save new shadow file including potential changes from above.
				shadow[n] = strings.Join(fields, ":")
				err = file.Write(strings.Join(shadow, "\n"), installChrootShadowFile)
				return
			}
		}
	}

	return fmt.Errorf(`user "%s" not found when trying to change the password expiration date`, username)
}

func ConfigureUserGroupMembership(installChroot *safechroot.Chroot, username string, primaryGroup string,
	secondaryGroups []string,
) (err error) {
	const squashErrors = false

	// Update primary group
	if primaryGroup != "" {
		err = installChroot.UnsafeRun(func() error {
			return shell.ExecuteLive(squashErrors, "usermod", "-g", primaryGroup, username)
		})

		if err != nil {
			return
		}
	}

	// Update secondary groups
	if len(secondaryGroups) != 0 {
		allGroups := strings.Join(secondaryGroups, ",")
		err = installChroot.UnsafeRun(func() error {
			return shell.ExecuteLive(squashErrors, "usermod", "-a", "-G", allGroups, username)
		})

		if err != nil {
			return
		}
	}

	return
}

func ConfigureUserStartupCommand(installChroot *safechroot.Chroot, username string, startupCommand string) (err error) {
	const (
		passwdFilePath = "etc/passwd"
		sedDelimiter   = "|"
	)

	if startupCommand == "" {
		return
	}

	logger.Log.Debugf("Updating user '%s' startup command to '%s'.", username, startupCommand)

	findPattern := fmt.Sprintf(`^\(%s.*\):[^:]*$`, username)
	replacePattern := fmt.Sprintf(`\1:%s`, startupCommand)
	filePath := filepath.Join(installChroot.RootDir(), passwdFilePath)
	err = sed(findPattern, replacePattern, sedDelimiter, filePath)
	if err != nil {
		err = fmt.Errorf("failed to update user's (%s) startup command (%s):\n%w", username, startupCommand, err)
		return
	}

	return
}

func ProvisionUserSSHCerts(installChroot *safechroot.Chroot, username string, sshPubKeyPaths []string) (err error) {
	var (
		pubKeyData []string
		exists     bool
	)
	const squashErrors = false
	const authorizedKeysTempFilePerms = 0644
	const authorizedKeysTempFile = "/tmp/authorized_keys"
	const sshDirectoryPermission = "0700"

	// Skip user SSH directory generation when not provided with public keys
	// Let SSH handle the creation of this folder on its first use
	if len(sshPubKeyPaths) == 0 {
		return
	}

	homeDir := userutils.UserHomeDirectory(username)
	userSSHKeyDir := filepath.Join(homeDir, ".ssh")
	authorizedKeysFile := filepath.Join(userSSHKeyDir, "authorized_keys")

	exists, err = file.PathExists(authorizedKeysTempFile)
	if err != nil {
		logger.Log.Warnf("Error accessing %s file : %v", authorizedKeysTempFile, err)
		return
	}
	if !exists {
		logger.Log.Debugf("File %s does not exist. Creating file...", authorizedKeysTempFile)
		err = file.Create(authorizedKeysTempFile, authorizedKeysTempFilePerms)
		if err != nil {
			logger.Log.Warnf("Failed to create %s file : %v", authorizedKeysTempFile, err)
			return
		}
	} else {
		err = os.Truncate(authorizedKeysTempFile, 0)
		if err != nil {
			logger.Log.Warnf("Failed to truncate %s file : %v", authorizedKeysTempFile, err)
			return
		}
	}
	defer os.Remove(authorizedKeysTempFile)

	for _, pubKey := range sshPubKeyPaths {
		logger.Log.Infof("Adding ssh key (%s) to user (%s)", filepath.Base(pubKey), username)
		relativeDst := filepath.Join(userSSHKeyDir, filepath.Base(pubKey))

		fileToCopy := safechroot.FileToCopy{
			Src:  pubKey,
			Dest: relativeDst,
		}

		err = installChroot.AddFiles(fileToCopy)
		if err != nil {
			return
		}

		logger.Log.Infof("Adding ssh key (%s) to user (%s) .ssh/authorized_users", filepath.Base(pubKey), username)
		pubKeyData, err = file.ReadLines(pubKey)
		if err != nil {
			logger.Log.Warnf("Failed to read from SSHPubKey : %v", err)
			return
		}

		// Append to the tmp/authorized_users file
		for _, sshkey := range pubKeyData {
			sshkey += "\n"
			err = file.Append(sshkey, authorizedKeysTempFile)
			if err != nil {
				logger.Log.Warnf("Failed to append to %s : %v", authorizedKeysTempFile, err)
				return
			}
		}
	}

	fileToCopy := safechroot.FileToCopy{
		Src:  authorizedKeysTempFile,
		Dest: authorizedKeysFile,
	}

	err = installChroot.AddFiles(fileToCopy)
	if err != nil {
		return
	}

	// Change ownership of the folder to belong to the user and their primary group
	err = installChroot.UnsafeRun(func() (err error) {
		// Find the primary group of the user
		stdout, stderr, err := shell.Execute("id", "-g", username)
		if err != nil {
			logger.Log.Warnf(stderr)
			return
		}

		primaryGroup := strings.TrimSpace(stdout)
		logger.Log.Debugf("Primary group for user (%s) is (%s)", username, primaryGroup)

		ownership := fmt.Sprintf("%s:%s", username, primaryGroup)
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

	return
}

// SELinuxConfigure pre-configures SELinux file labels and configuration files
func SELinuxConfigure(systemConfig configuration.SystemConfig, installChroot *safechroot.Chroot, mountPointToFsTypeMap map[string]string) (err error) {
	timestamp.StartEvent("SELinux", nil)
	defer timestamp.StopEvent(nil)
	logger.Log.Infof("Preconfiguring SELinux policy in %s mode", systemConfig.KernelCommandLine.SELinux)

	err = selinuxUpdateConfig(systemConfig, installChroot)
	if err != nil {
		logger.Log.Errorf("Failed to update SELinux config")
		return
	}
	err = selinuxRelabelFiles(systemConfig, installChroot, mountPointToFsTypeMap)
	if err != nil {
		logger.Log.Errorf("Failed to label SELinux files")
		return
	}
	return
}

func selinuxUpdateConfig(systemConfig configuration.SystemConfig, installChroot *safechroot.Chroot) (err error) {
	const (
		configFile     = "etc/selinux/config"
		selinuxPattern = "^SELINUX=.*"
	)
	var mode string

	switch systemConfig.KernelCommandLine.SELinux {
	case configuration.SELinuxEnforcing, configuration.SELinuxForceEnforcing:
		mode = configuration.SELinuxEnforcing.String()
	case configuration.SELinuxPermissive:
		mode = configuration.SELinuxPermissive.String()
	}

	selinuxConfigPath := filepath.Join(installChroot.RootDir(), configFile)
	selinuxMode := fmt.Sprintf("SELINUX=%s", mode)
	err = sed(selinuxPattern, selinuxMode, "`", selinuxConfigPath)
	return
}

func selinuxRelabelFiles(systemConfig configuration.SystemConfig, installChroot *safechroot.Chroot, mountPointToFsTypeMap map[string]string) (err error) {
	const (
		squashErrors        = false
		configFile          = "etc/selinux/config"
		fileContextBasePath = "etc/selinux/%s/contexts/files/file_contexts"
	)
	var listOfMountsToLabel []string

	// Search through all our mount points for supported filesystem types
	// Note for the future: SELinux can support any of {btrfs, encfs, ext2-4, f2fs, jffs2, jfs, ubifs, xfs, zfs}, but the build system currently
	//     only supports the below cases:
	for mount, fsType := range mountPointToFsTypeMap {
		switch fsType {
		case "ext2", "ext3", "ext4", "xfs":
			listOfMountsToLabel = append(listOfMountsToLabel, mount)
		case "fat32", "fat16", "vfat":
			logger.Log.Debugf("SELinux will not label mount at (%s) of type (%s), skipping", mount, fsType)
		default:
			err = fmt.Errorf("unknown fsType (%s) for mount (%s), cannot configure SELinux", fsType, mount)
			return
		}
	}

	// Find the type of policy we want to label with
	selinuxConfigPath := filepath.Join(installChroot.RootDir(), configFile)
	stdout, stderr, err := shell.Execute("sed", "-n", "s/^SELINUXTYPE=\\(.*\\)$/\\1/p", selinuxConfigPath)
	if err != nil {
		logger.Log.Errorf("Could not find an SELINUXTYPE in %s", selinuxConfigPath)
		logger.Log.Error(stderr)
		return
	}
	selinuxType := strings.TrimSpace(stdout)
	fileContextPath := fmt.Sprintf(fileContextBasePath, selinuxType)

	logger.Log.Debugf("Running setfiles to apply SELinux labels on mount points: %v", listOfMountsToLabel)
	err = installChroot.UnsafeRun(func() error {
		args := []string{"-m", "-v", fileContextPath}
		args = append(args, listOfMountsToLabel...)

		// We only want to print basic info, filter out the real output unless at trace level (Execute call handles that)
		files := 0
		lastFile := ""
		onStdout := func(args ...interface{}) {
			if len(args) > 0 {
				files++
				lastFile = fmt.Sprintf("%v", args)
			}
			if (files % 1000) == 0 {
				ReportActionf("SELinux: labelled %d files", files)
			}
		}
		err := shell.ExecuteLiveWithCallback(onStdout, logger.Log.Warn, squashErrors, "setfiles", args...)
		if err != nil {
			return fmt.Errorf("failed while labeling files (last file: %s) %w", lastFile, err)
		}
		return err
	})

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
func InstallBootloader(installChroot *safechroot.Chroot, encryptEnabled bool, bootType, bootUUID, bootPrefix, bootDevPath, assetsDir string) (err error) {
	const (
		efiMountPoint  = "/boot/efi"
		efiBootType    = "efi"
		legacyBootType = "legacy"
		noneBootType   = "none"
	)

	ReportAction("Configuring bootloader")

	switch bootType {
	case legacyBootType:
		err = installLegacyBootloader(installChroot, bootDevPath, encryptEnabled)
		if err != nil {
			return
		}
	case efiBootType:
		efiPath := filepath.Join(installChroot.RootDir(), efiMountPoint)
		err = installEfiBootloader(encryptEnabled, efiPath, bootUUID, bootPrefix, assetsDir)
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
func installLegacyBootloader(installChroot *safechroot.Chroot, bootDevPath string, encryptEnabled bool) (err error) {
	const (
		squashErrors = false
		bootDir      = "/boot"
		bootDirArg   = "--boot-directory"
		grub2BootDir = "/boot/grub2"
	)

	// Add grub cryptodisk settings
	if encryptEnabled {
		err = enableCryptoDisk()
		if err != nil {
			return
		}
	}
	installBootDir := filepath.Join(installChroot.RootDir(), bootDir)
	grub2InstallBootDirArg := fmt.Sprintf("%s=%s", bootDirArg, installBootDir)
	err = shell.ExecuteLive(squashErrors, "grub2-install", "--target=i386-pc", grub2InstallBootDirArg, bootDevPath)
	if err != nil {
		return
	}
	installGrub2BootDir := filepath.Join(installChroot.RootDir(), grub2BootDir)
	err = shell.ExecuteLive(squashErrors, "chmod", "-R", "go-rwx", installGrub2BootDir)
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

// GetPartLabel queries the PARTLABEL of the given partition
// - device is the device path of the desired partition
func GetPartLabel(device string) (stdout string, err error) {
	stdout, _, err = shell.Execute("blkid", device, "-s", "PARTLABEL", "-o", "value")
	if err != nil {
		return
	}
	logger.Log.Trace(stdout)
	stdout = strings.TrimSpace(stdout)
	return
}

// FormatMountIdentifier finds the requested identifier type for the given device, and formats it for use
//
//	ie "UUID=12345678-abcd..."
func FormatMountIdentifier(identifier configuration.MountIdentifier, device string) (identifierString string, err error) {
	var id string
	switch identifier {
	case configuration.MountIdentifierUuid:
		id, err = GetUUID(device)
		if err != nil {
			return
		}
		identifierString = fmt.Sprintf("UUID=%s", id)
	case configuration.MountIdentifierPartUuid:
		id, err = GetPartUUID(device)
		if err != nil {
			return
		}
		identifierString = fmt.Sprintf("PARTUUID=%s", id)
	case configuration.MountIdentifierPartLabel:
		id, err = GetPartLabel(device)
		if err != nil {
			return
		}
		identifierString = fmt.Sprintf("PARTLABEL=%s", id)
	case configuration.MountIdentifierNone:
		err = fmt.Errorf("must select a mount identifier for device (%s)", device)
	default:
		err = fmt.Errorf("unknown mount identifier: '%v'", identifier)
	}
	return
}

// enableCryptoDisk enables Grub to boot from an encrypted disk
// - installChroot is the installation chroot
func enableCryptoDisk() (err error) {
	const (
		grubPath           = "/etc/default/grub"
		grubCryptoDisk     = "GRUB_ENABLE_CRYPTODISK=y\n"
		grubPreloadModules = `GRUB_PRELOAD_MODULES="lvm"`
	)

	err = file.Append(grubCryptoDisk, grubPath)
	if err != nil {
		logger.Log.Warnf("Failed to add grub cryptodisk: %v", err)
		return
	}
	err = file.Append(grubPreloadModules, grubPath)
	if err != nil {
		logger.Log.Warnf("Failed to add grub preload modules: %v", err)
		return
	}
	return
}

// installEfi copies the efi binaries and grub configuration to the appropriate
// installRoot/boot/efi folder
// It is expected that shim (bootx64.efi) and grub2 (grub2.efi) are installed
// into the EFI directory via the package list installation mechanism.
func installEfiBootloader(encryptEnabled bool, installRoot, bootUUID, bootPrefix, assetsDir string) (err error) {
	const (
		defaultCfgFilename = "grub.cfg"
		encryptCfgFilename = "grubEncrypt.cfg"
		grubAssetDir       = "efi/grub"
		grubFinalDir       = "boot/grub2"
	)

	// Copy the bootloader's grub.cfg
	grubAssetPath := filepath.Join(assetsDir, grubAssetDir, defaultCfgFilename)
	if encryptEnabled {
		grubAssetPath = filepath.Join(assetsDir, grubAssetDir, encryptCfgFilename)
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

	// Set the boot prefix
	err = setGrubCfgBootPrefix(bootPrefix, grubFinalPath)
	if err != nil {
		logger.Log.Warnf("Failed to set bootPrefix in grub.cfg: %v", err)
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
	return copyAdditionalFilesHelper(installChroot, config.AdditionalFiles)
}

func copyAdditionalFilesHelper(installChroot *safechroot.Chroot, additionalFiles map[string]configuration.FileConfigList) (err error) {
	ReportAction("Copying additional files")
	timestamp.StartEvent("Copying additional files", nil)
	defer timestamp.StopEvent(nil)

	for srcFile, dstFileConfigs := range additionalFiles {
		for _, dstFileConfig := range dstFileConfigs {
			fileToCopy := safechroot.FileToCopy{
				Src:         srcFile,
				Dest:        dstFileConfig.Path,
				Permissions: (*os.FileMode)(dstFileConfig.Permissions),
			}

			err = installChroot.AddFiles(fileToCopy)
			if err != nil {
				return
			}
		}
	}

	return
}

// cleanupRpmDatabase removes RPM database if the image does not require a package manager.
// rootPrefix is prepended to the RPM database path - useful when RPM database resides in a chroot and cleanupRpmDatabase can't be called from within the chroot.
func cleanupRpmDatabase(rootPrefix string) (err error) {
	logger.Log.Info("Attempting RPM database cleanup...")
	rpmDir := filepath.Join(rootPrefix, rpmDependenciesDirectory)
	err = os.RemoveAll(rpmDir)
	if err != nil {
		logger.Log.Errorf("Failed to remove RPM database (%s). Error: %s", rpmDir, err)
		err = fmt.Errorf("failed to remove RPM database (%s): %s", rpmDir, err)
	} else {
		logger.Log.Infof("Cleaned up RPM database (%s)", rpmDir)
	}
	return
}

func RunPreInstallScripts(config configuration.SystemConfig) (err error) {
	const squashErrors = false

	for _, script := range config.PreInstallScripts {
		ReportActionf("Running pre-install script: %s", path.Base(script.Path))

		err = shell.ExecuteLive(squashErrors, shell.ShellProgram, "-c", fmt.Sprintf("%s %s", script.Path, script.Args))
		if err != nil {
			return
		}
	}

	return
}

func runPostInstallScripts(installChroot *safechroot.Chroot, config configuration.SystemConfig) (err error) {
	timestamp.StartEvent("post install scripts", nil)
	defer timestamp.StopEvent(nil)
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
			err := shell.ExecuteLive(squashErrors, shell.ShellProgram, "-c", fmt.Sprintf("%s %s", scriptPath, script.Args))

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

func RunFinalizeImageScripts(installChroot *safechroot.Chroot, config configuration.SystemConfig) (err error) {
	const squashErrors = false

	for _, script := range config.FinalizeImageScripts {
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

		ReportActionf("Running finalize image script: %s", path.Base(script.Path))
		logger.Log.Infof("Running finalize image script: %s", script.Path)
		err = installChroot.UnsafeRun(func() error {
			err := shell.ExecuteLive(squashErrors, shell.ShellProgram, "-c", fmt.Sprintf("%s %s", scriptPath, script.Args))

			if err != nil {
				return err
			}

			err = os.Remove(scriptPath)
			if err != nil {
				logger.Log.Errorf("Failed to cleanup finalize image script (%s). Error: %s", scriptPath, err)
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

	logger.Log.Debugf("Adding ExtraCommandLine('%s') to '%s'", kernelCommandline.ExtraCommandLine, grubPath)
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

	logger.Log.Debugf("Adding ImaPolicy('%s') to '%s'", ima, grubPath)
	err = sed(imaPattern, ima, kernelCommandline.GetSedDelimeter(), grubPath)
	if err != nil {
		logger.Log.Warnf("Failed to set grub.cfg's IMA setting: %v", err)
	}

	return
}

func setGrubCfgSELinux(grubPath string, kernelCommandline configuration.KernelCommandLine) (err error) {
	const (
		selinuxPattern        = "{{.SELinux}}"
		selinuxSettings       = "security=selinux selinux=1"
		selinuxForceEnforcing = "enforcing=1"
	)
	var selinux string

	switch kernelCommandline.SELinux {
	case configuration.SELinuxForceEnforcing:
		selinux = fmt.Sprintf("%s %s", selinuxSettings, selinuxForceEnforcing)
	case configuration.SELinuxPermissive, configuration.SELinuxEnforcing:
		selinux = selinuxSettings
	case configuration.SELinuxOff:
		selinux = ""
	}

	logger.Log.Debugf("Adding SELinuxConfiguration('%s') to '%s'", selinux, grubPath)
	err = sed(selinuxPattern, selinux, kernelCommandline.GetSedDelimeter(), grubPath)
	if err != nil {
		logger.Log.Warnf("Failed to set grub.cfg's SELinux setting: %v", err)
	}

	return
}

func setGrubCfgFIPS(isBootPartitionSeparate bool, bootUUID, grubPath string, kernelCommandline configuration.KernelCommandLine) (err error) {
	const (
		enableFIPSPattern = "{{.FIPS}}"
		enableFIPS        = "fips=1"
		bootPrefix        = "boot="
		uuidPrefix        = "UUID="
	)

	// If EnableFIPS is set, always add "fips=1" to the kernel cmdline.
	// If /boot is a dedicated partition from the root partition, add "boot=UUID=<bootUUID value>" as well to the kernel cmdline in grub.cfg.
	// This second step is required for fips boot-time self tests to find the kernel's .hmac file in the /boot partition.
	fipsKernelArgument := ""
	if kernelCommandline.EnableFIPS {
		fipsKernelArgument = fmt.Sprintf("%s", enableFIPS)
		if isBootPartitionSeparate {
			fipsKernelArgument = fmt.Sprintf("%s %s%s%s", fipsKernelArgument, bootPrefix, uuidPrefix, bootUUID)
		}
	}

	logger.Log.Debugf("Adding EnableFIPS('%s') to '%s'", fipsKernelArgument, grubPath)
	err = sed(enableFIPSPattern, fipsKernelArgument, kernelCommandline.GetSedDelimeter(), grubPath)
	if err != nil {
		logger.Log.Warnf("Failed to set grub.cfg's EnableFIPS setting: %v", err)
	}
	return
}

func setGrubCfgCGroup(grubPath string, kernelCommandline configuration.KernelCommandLine) (err error) {
	const (
		cgroupPattern     = "{{.CGroup}}"
		cgroupv1FlagValue = "systemd.unified_cgroup_hierarchy=0"
		cgroupv2FlagValue = "systemd.unified_cgroup_hierarchy=1"
	)
	var cgroup string

	switch kernelCommandline.CGroup {
	case configuration.CGroupV2:
		cgroup = fmt.Sprintf("%s", cgroupv2FlagValue)
	case configuration.CGroupV1:
		cgroup = fmt.Sprintf("%s", cgroupv1FlagValue)
	case configuration.CGroupDefault:
		cgroup = ""
	}

	logger.Log.Debugf("Adding CGroupConfiguration('%s') to '%s'", cgroup, grubPath)
	err = sed(cgroupPattern, cgroup, kernelCommandline.GetSedDelimeter(), grubPath)
	if err != nil {
		logger.Log.Warnf("Failed to set grub.cfg's CGroup setting: %v", err)
	}

	return
}

// setGrubCfgReadOnlyVerityRoot populates the arguments needed to boot with a dm-verity read-only root partition
func setGrubCfgReadOnlyVerityRoot(grubPath string, readOnlyRoot diskutils.VerityDevice) (err error) {
	var (
		verityMountArg          = fmt.Sprintf("rd.verityroot.devicename=%s", readOnlyRoot.MappedName)
		verityHashArg           = fmt.Sprintf("rd.verityroot.hashtree=/%s.hashtree", readOnlyRoot.MappedName)
		verityRootHashArg       = fmt.Sprintf("rd.verityroot.roothashfile=/%s.roothash", readOnlyRoot.MappedName)
		verityRootHashSigArg    = fmt.Sprintf("rd.verityroot.roothashsig=/%s.p7", readOnlyRoot.MappedName)
		verityFECDataArg        = fmt.Sprintf("rd.verityroot.fecdata=/%s.fec", readOnlyRoot.MappedName)
		verityFECRootsArg       = fmt.Sprintf("rd.verityroot.fecroots=%d", readOnlyRoot.FecRoots)
		verityErrorHandling     = fmt.Sprintf("rd.verityroot.verityerrorhandling=%s", readOnlyRoot.ErrorBehavior)
		verityValidateOnBootArg = fmt.Sprintf("rd.verityroot.validateonboot=%v", readOnlyRoot.ValidateOnBoot)
		verityOverlaysArg       = fmt.Sprintf("rd.verityroot.overlays=\"%s\"", strings.Join(readOnlyRoot.TmpfsOverlays, " "))
		verityOverlaySizeArg    = fmt.Sprintf("rd.verityroot.overlaysize=\"%s\"", readOnlyRoot.TmpfsOverlaySize)
		verityDebugMountsArg    = fmt.Sprintf("rd.verityroot.overlays_debug_mount=%s", readOnlyRoot.TmpfsOverlaysDebugMount)
		verityPattern           = "{{.ReadOnlyVerityRoot}}"
		verityArgs              = ""

		cmdline configuration.KernelCommandLine
	)

	if readOnlyRoot.MappedName != "" {
		// Basic set of verity arguments common to all use cases
		verityArgs = fmt.Sprintf("%s %s %s %s %s %s %s %s",
			verityMountArg,
			verityHashArg,
			verityRootHashArg,
			verityErrorHandling,
			verityValidateOnBootArg,
			verityOverlaysArg,
			verityOverlaySizeArg,
			verityDebugMountsArg,
		)
		// Only include the FEC arguments if we have FEC enabled
		if readOnlyRoot.FecRoots > 0 {
			verityArgs = fmt.Sprintf("%s %s %s", verityArgs, verityFECDataArg, verityFECRootsArg)
		}
		if readOnlyRoot.UseRootHashSignature {
			verityArgs = fmt.Sprintf("%s %s", verityArgs, verityRootHashSigArg)
		}
	}

	logger.Log.Debugf("Adding Verity Root ('%s') to %s", verityArgs, grubPath)
	err = sed(verityPattern, verityArgs, cmdline.GetSedDelimeter(), grubPath)
	if err != nil {
		logger.Log.Warnf("Failed to set grub.cfg's Verity Root setting: %v", err)
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

	logger.Log.Debugf("Adding lvm('%s') to '%s'", lvm, grubPath)
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

	logger.Log.Debugf("Adding luks('%s') to '%s'", luksUUID, grubPath)
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

	logger.Log.Debugf("Adding UUID('%s') to '%s'", bootUUID, grubPath)
	err = sed(bootUUIDPattern, bootUUID, cmdline.GetSedDelimeter(), grubPath)
	if err != nil {
		logger.Log.Warnf("Failed to set grub.cfg's bootUUID: %v", err)
		return
	}
	return
}

func setGrubCfgBootPrefix(bootPrefix, grubPath string) (err error) {
	const (
		bootPrefixPattern = "{{.BootPrefix}}"
	)
	var cmdline configuration.KernelCommandLine

	logger.Log.Debugf("Adding BootPrefix('%s') to '%s'", bootPrefix, grubPath)
	err = sed(bootPrefixPattern, bootPrefix, cmdline.GetSedDelimeter(), grubPath)
	if err != nil {
		logger.Log.Warnf("Failed to set grub.cfg's bootPrefix: %v", err)
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
	logger.Log.Debugf("Adding EncryptedVolume('%s') to '%s'", encryptedVol, grubPath)
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

	logger.Log.Debugf("Adding RootDevice('%s') to '%s'", rootDevice, grubPath)
	err = sed(rootDevicePattern, rootDevice, cmdline.GetSedDelimeter(), grubPath)
	if err != nil {
		logger.Log.Warnf("Failed to set grub.cfg's rootDevice: %v", err)
		return
	}
	return
}

// ExtractPartitionArtifacts scans through the SystemConfig and generates all the partition-based artifacts specified.
// - setupChrootDirPath is the path to the setup root dir where the build takes place
// - workDirPath is the directory to place the artifacts
// - diskIndex is the index of the disk this is added to the parition artifact generated
// - disk configuration settings for the disk
// - systemConfig system configration corresponding to the disk configuration
// - partIDToDevPathMap is a map of partition IDs to partition device paths
// - mountPointToOverlayMap is a map of mountpoints to the overlay details for this mount if any
func ExtractPartitionArtifacts(setupChrootDirPath, workDirPath string, diskIndex int, disk configuration.Disk, systemConfig configuration.SystemConfig, partIDToDevPathMap map[string]string, mountPointToOverlayMap map[string]*Overlay) (err error) {
	timestamp.StartEvent("create partition artifacts", nil)
	defer timestamp.StopEvent(nil)

	const (
		ext4ArtifactType  = "ext4"
		diffArtifactType  = "diff"
		rdiffArtifactType = "rdiff"
	)
	// Scan each partition for Artifacts
	for i, partition := range disk.Partitions {
		for _, artifact := range partition.Artifacts {
			devPath := partIDToDevPathMap[partition.ID]

			switch artifact.Type {
			case ext4ArtifactType:
				// Ext4 artifact type output is a .raw of the partition
				finalName := fmt.Sprintf("disk%d.partition%d.raw", diskIndex, i)
				err = createRawArtifact(workDirPath, devPath, finalName)
				if err != nil {
					return err
				}
			case diffArtifactType:
				for _, setting := range systemConfig.PartitionSettings {
					if setting.ID == partition.ID {
						if setting.OverlayBaseImage != "" {
							// Diff artifact type output
							finalName := fmt.Sprintf("disk%d.partition%d.diff", diskIndex, i)
							err = createDiffArtifact(setupChrootDirPath, workDirPath, finalName, mountPointToOverlayMap[setting.MountPoint])
						}
						break
					}
				}

			case rdiffArtifactType:
				for _, setting := range systemConfig.PartitionSettings {
					if setting.ID == partition.ID {
						if setting.RdiffBaseImage != "" {
							// Diff artifact type output
							finalName := fmt.Sprintf("disk%d.partition%d.rdiff", diskIndex, i)
							err = createRDiffArtifact(workDirPath, devPath, setting.RdiffBaseImage, finalName)
						}
						break
					}
				}
			}
		}
	}
	return
}

func createDiffArtifact(setupChrootDirPath, workDirPath, name string, overlay *Overlay) (err error) {
	const (
		squashErrors = true
	)

	fullPath := filepath.Join(workDirPath, name)

	upperDir := overlay.getUpperDir()
	upperDir = filepath.Join(setupChrootDirPath, upperDir)
	tarArgs := []string{
		"cvf",
		fullPath,
		"-C",
		upperDir,
		"."}

	return shell.ExecuteLive(squashErrors, "tar", tarArgs...)
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

func createRDiffArtifact(workDirPath, devPath, rDiffBaseImage, name string) (err error) {
	const (
		signatureFileName = "./signature"
		squashErrors      = true
	)

	fullPath := filepath.Join(workDirPath, name)

	// rdiff expectes the signature file path to be relative.
	rdiffArgs := []string{
		"signature",
		rDiffBaseImage,
		signatureFileName,
	}

	err = shell.ExecuteLive(squashErrors, "rdiff", rdiffArgs...)
	if err != nil {
		return
	}

	signatureFileFullPath := filepath.Join(workDirPath, signatureFileName)
	defer os.Remove(signatureFileFullPath)

	rdiffArgs = []string{
		"delta",
		signatureFileName,
		devPath,
		fullPath,
	}

	return shell.ExecuteLive(squashErrors, "rdiff", rdiffArgs...)
}

// KernelPackages returns a list of kernel packages obtained from KernelOptions in the config's SystemConfigs
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
			// This is non-fatal, as there is no guarantee the image has gpg agent started.
			logger.Log.Warnf("Failed to stop gpg-agent. This is expected if it is not installed: %s", err)
		}

		return nil
	})
}
