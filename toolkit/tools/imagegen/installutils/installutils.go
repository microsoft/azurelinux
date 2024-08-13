// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package installutils

import (
	"fmt"
	"os"
	"os/exec"
	"path"
	"path/filepath"
	"runtime"
	"sort"
	"strconv"
	"strings"
	"syscall"
	"time"

	"github.com/google/uuid"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/diskutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/packagerepo/repocloner"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/resources"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/retry"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safemount"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/tdnf"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/timestamp"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/userutils"
	"github.com/sirupsen/logrus"
	"golang.org/x/sys/unix"
)

const (
	PackageManifestRelativePath = "image_pkg_manifest_installroot.json"

	// NullDevice represents the /dev/null device used as a mount device for overlay images.
	NullDevice = "/dev/null"

	// CmdlineSELinuxSecurityArg is the "security" arg needed for enabling SELinux.
	CmdlineSELinuxSecurityArg = "security=selinux"

	// CmdlineSELinuxEnabledArg is the "selinux" arg needed for disabling SELinux.
	CmdlineSELinuxDisabledArg = "selinux=0"

	// CmdlineSELinuxEnabledArg is the "selinux" arg needed for enabling SELinux.
	CmdlineSELinuxEnabledArg = "selinux=1"

	// CmdlineSELinuxEnforcingArg is the arg required for forcing SELinux to be in enforcing mode.
	CmdlineSELinuxEnforcingArg = "enforcing=1"

	// CmdlineSELinuxSettings is the kernel command-line args for enabling SELinux.
	CmdlineSELinuxSettings = CmdlineSELinuxSecurityArg + " " + CmdlineSELinuxEnabledArg

	// CmdlineSELinuxForceEnforcing is the kernel command-line args for enabling SELinux and force it to be in
	// enforcing mode.
	CmdlineSELinuxForceEnforcing = CmdlineSELinuxSettings + " " + CmdlineSELinuxEnforcingArg

	// SELinuxConfigFile is the file path of the SELinux config file.
	SELinuxConfigFile = "/etc/selinux/config"

	// SELinuxConfigEnforcing is the string value to set SELinux to enforcing in the /etc/selinux/config file.
	SELinuxConfigEnforcing = "enforcing"

	// SELinuxConfigPermissive is the string value to set SELinux to permissive in the /etc/selinux/config file.
	SELinuxConfigPermissive = "permissive"

	// SELinuxConfigDisabled is the string value to set SELinux to disabled in the /etc/selinux/config file.
	SELinuxConfigDisabled = "disabled"

	// GrubCfgFile is the filepath of the grub config file.
	GrubCfgFile = "/boot/grub2/grub.cfg"

	// GrubDefFile is the filepath of the config file used by grub-mkconfig.
	GrubDefFile = "/etc/default/grub"

	// CombinedBootPartitionBootPrefix is the grub.cfg boot prefix used when the boot partition is the same as the
	// rootfs partition.
	CombinedBootPartitionBootPrefix = "/boot"
)

const (
	overlay        = "overlay"
	rootMountPoint = "/"
	bootMountPoint = "/boot"

	// rpmDependenciesDirectory is the directory which contains RPM database. It is not required for images that do not contain RPM.
	rpmDependenciesDirectory = "/var/lib/rpm"

	// rpmManifestDirectory is the directory containing manifests of installed packages to support distroless vulnerability scanning tools.
	rpmManifestDirectory = "/var/lib/rpmmanifest"

	// /boot directory should be only accesible by root. The directories need the execute bit as well.
	bootDirectoryFileMode = 0400
	bootDirectoryDirMode  = 0700

	// Configuration files related to boot behavior. Users should be able to read these files, and root should have RW access.
	bootUsrConfigFileMode = 0644
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
		err = fmt.Errorf("failed to setup loop back device for mount (%s):\n%w", partitionSetting.OverlayBaseImage, err)
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
func CreateInstallRoot(installRoot string, mountPointMap, mountPointToFsTypeMap,
	mountPointToMountArgsMap map[string]string, mountPointToOverlayMap map[string]*Overlay,
) (mountList []string, err error) {
	for _, mountPoint := range sortMountPoints(&mountPointMap, false) {
		device := mountPointMap[mountPoint]
		err = mountSingleMountPoint(installRoot, mountPoint, device, mountPointToFsTypeMap[mountPoint],
			mountPointToMountArgsMap[mountPoint], mountPointToOverlayMap[mountPoint])
		if err != nil {
			return
		}

		// Add to the list 1-by-1 so that the we can safely unmount if mounting fails half-way through.
		// Note: The order of 'mountList' dictates the order the /etc/fstab file is written in.
		mountList = append(mountList, mountPoint)
	}
	return
}

// DestroyInstallRoot unmounts each of the installroot mountpoints in order, ensuring that the root mountpoint is last
// - installRoot is the path to the root where the mountpoints exist
// - mountPointMap is the map of mountpoints to partition device paths
// - mountPointToOverlayMap is the map of mountpoints to overlay devices
func DestroyInstallRoot(installRoot string, mountList []string, mountPointMap map[string]string,
	mountPointToOverlayMap map[string]*Overlay,
) (err error) {
	logger.Log.Trace("Destroying InstallRoot")

	defer OverlayUnmount(mountPointToOverlayMap)

	logger.Log.Trace("Destroying InstallRoot")

	// Reverse order for unmounting
	for i := len(mountList) - 1; i >= 0; i-- {
		mountPoint := mountList[i]

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
			return fmt.Errorf("failed to create mount for overlay device:\n%w", err)
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
				err = fmt.Errorf("failed to parse packages list from system config (%s):\n%w", systemCfg.Name, err)
				return
			}

			packages = append(packages, packageVer)
		}

		packageList = append(packageList, packages...)
	}

	return
}

// orderPackageInstallList updates the order we will install packages if needed. Installing each package one at a time
// can cause issues with ordering since we aren't doing a single transaction. For example, the initramfs regeneration is
// done as a post transaction step and only needs to be done once after all other packages are installed. Since we are
// not doing a single transaction it has an opportunity to trigger repeatedly. Moving it to the end of the list means it
// will only trigger once.
func orderPackageInstallList(packageList []string) []string {
	const initramfsPackagePrefix = "initramfs"

	initramfsPackages := []string{}
	orderedPackageList := []string{}
	for _, pkg := range packageList {
		// Search for initramfs, ignoring any version info at the end of the package name.
		if strings.HasPrefix(pkg, initramfsPackagePrefix) {
			initramfsPackages = append(initramfsPackages, pkg)
		} else {
			orderedPackageList = append(orderedPackageList, pkg)
		}
	}
	orderedPackageList = append(orderedPackageList, initramfsPackages...)
	return orderedPackageList
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
// - encryptedRoot stores information about the encrypted root device if root encryption is enabled
// - diffDiskBuild is a flag that denotes whether this is a diffdisk build or not
func PopulateInstallRoot(installChroot *safechroot.Chroot, packagesToInstall []string,
	config configuration.SystemConfig, mountList []string, installMap, mountPointToFsTypeMap, mountPointToMountArgsMap,
	partIDToDevPathMap, partIDToFsTypeMap map[string]string, encryptedRoot diskutils.EncryptedRootDevice,
	diffDiskBuild bool,
) (err error) {
	timestamp.StartEvent("populating install root", nil)
	defer timestamp.StopEvent(nil)

	const (
		filesystemPkg  = "filesystem"
		shadowUtilsPkg = "shadow-utils"
	)

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

	// Change the ordering if needed (ie make sure initramfs is last)
	packagesToInstall = orderPackageInstallList(packagesToInstall)

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

	// Keep a running total of how many packages have been installed through all the `TdnfInstallWithProgress` and
	// `TdnfInstallPriorityPackage` invocations
	packagesInstalled := 0

	timestamp.StartEvent("installing packages", nil)
	// Install filesystem package first
	packagesInstalled, packagesToInstall, err = TdnfInstallPriorityPackage(filesystemPkg, installRoot, packagesToInstall, packagesInstalled, totalPackages, true)
	if err != nil {
		err = fmt.Errorf("failed to install (%s) package in preparation for image creation:\n%w", filesystemPkg, err)
		return
	}

	// imageconfigvalidator should have ensured that we intend to install shadow-utils, so we can go ahead and do that here.
	if len(config.Users) > 0 || len(config.Groups) > 0 {
		if !sliceutils.ContainsValue(packagesToInstall, "shadow-utils") {
			err = fmt.Errorf("shadow-utils package must be added to the image's package lists when setting users or groups")
			return
		}

		packagesInstalled, packagesToInstall, err = TdnfInstallPriorityPackage(shadowUtilsPkg, installRoot, packagesToInstall, packagesInstalled, totalPackages, true)
		if err != nil {
			err = fmt.Errorf("failed to install (%s) package in preparation for modifying users/groups:\n%w", shadowUtilsPkg, err)
			return
		}
	}

	hostname := config.Hostname
	if !config.IsRootFS() && mountPointToFsTypeMap[rootMountPoint] != overlay {
		// Add /etc/hostname
		err = updateHostname(installChroot.RootDir(), hostname)
		if err != nil {
			return
		}
	}

	// Add groups
	err = addGroups(installChroot, config.Groups)
	if err != nil {
		return
	}

	// Add users
	err = addUsers(installChroot, config.Users)
	if err != nil {
		return
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

	if !config.IsRootFS() {
		// Configure system files
		err = configureSystemFiles(installChroot, hostname, config, mountList, installMap, mountPointToFsTypeMap,
			mountPointToMountArgsMap, partIDToDevPathMap, partIDToFsTypeMap, encryptedRoot)
		if err != nil {
			return
		}
	}

	// Configure machine-id and other systemd state files
	err = clearSystemdState(installChroot, config.EnableSystemdFirstboot)
	if err != nil {
		err = fmt.Errorf("failed to clean systemd files:\n%w", err)
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
	if err != nil {
		return
	}

	// The system should be fully populated with packages, we can clear the tdnf cache now to free up space.
	if !config.PreserveTdnfCache {
		err = cleanupTdnfCache(installChroot)
		if err != nil {
			return
		}
	}
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

// TdnfInstallPriorityPackage installs a specific package, removing it from the list of packages to install in future
// steps. This is useful for installing requirements for actual tooling operations that need to be installed before
// other packages.
func TdnfInstallPriorityPackage(priorityPackageName, installRoot string, packagesToInstall []string, currentPackagesInstalled, totalPackages int, reportProgress bool,
) (packagesInstalled int, updatedPackagesToInstall []string, err error) {
	packagesInstalled, err = TdnfInstallWithProgress(priorityPackageName, installRoot, currentPackagesInstalled, totalPackages, reportProgress)
	if err != nil {
		err = fmt.Errorf("failed to install priority package (%s):\n%w", priorityPackageName, err)
		return packagesInstalled, packagesToInstall, err
	}

	// Remove the package from the list of packages to install if present
	updatedPackagesToInstall = sliceutils.FindMatches(packagesToInstall, func(pkg string) bool { return pkg != priorityPackageName })

	return packagesInstalled, updatedPackagesToInstall, err
}

// TdnfInstallWithProgress installs a package in the current environment while optionally reporting progress
func TdnfInstallWithProgress(packageName, installRoot string, currentPackagesInstalled, totalPackages int, reportProgress bool) (packagesInstalled int, err error) {
	timestamp.StartEvent("installing"+packageName, nil)
	defer timestamp.StopEvent(nil)
	var (
		releaseverCliArg string
	)

	packagesInstalled = currentPackagesInstalled

	onStdout := func(line string) {
		const tdnfInstallPrefix = "Installing/Updating: "

		// Only process lines that match tdnfInstallPrefix
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
	err = shell.NewExecBuilder("tdnf", "-v", "install", packageName, "--installroot", installRoot, "--nogpgcheck",
		"--assumeyes", "--setopt", "reposdir=/etc/yum.repos.d/", releaseverCliArg).
		StdoutCallback(onStdout).
		LogLevel(logrus.TraceLevel, logrus.WarnLevel).
		WarnLogLines(shell.DefaultWarnLogLines).
		Execute()
	if err != nil {
		logger.Log.Warnf("Failed to tdnf install: %v. Package name: %v", err, packageName)
	}

	return
}

func configureSystemFiles(installChroot *safechroot.Chroot, hostname string, config configuration.SystemConfig,
	mountList []string, mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap, partIDToDevPathMap,
	partIDToFsTypeMap map[string]string, encryptedRoot diskutils.EncryptedRootDevice,
) (err error) {
	// Update hosts file
	err = updateHosts(installChroot.RootDir(), hostname)
	if err != nil {
		return
	}

	// Update fstab
	err = UpdateFstab(installChroot.RootDir(), config.PartitionSettings, mountList, mountPointMap,
		mountPointToFsTypeMap, mountPointToMountArgsMap, partIDToDevPathMap, partIDToFsTypeMap, config.EnableHidepid)
	if err != nil {
		return
	}

	// Update crypttab
	err = updateCrypttab(installChroot.RootDir(), mountPointMap, encryptedRoot)
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
				err = fmt.Errorf("%v", stderr)
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

// clearSystemdState clears the systemd state files that should be unique to each instance of the image. This is
// based on https://systemd.io/BUILDING_IMAGES/. Primarily, this function will ensure that /etc/machine-id is configured
// correctly, and that random seed and credential files are removed if they exist.
// - installChroot is the chroot to modify
// - enableSystemdFirstboot will set the machine-id file to "uninitialized" if true, and "" if false
func clearSystemdState(installChroot *safechroot.Chroot, enableSystemdFirstboot bool) (err error) {
	const (
		machineIDFile         = "/etc/machine-id"
		machineIDFirstBootOn  = "uninitialized\n"
		machineIDFirstbootOff = ""
		machineIDFilePerms    = 0444
	)

	// These state files are very unlikely to be present, but we should be thorough and check for them.
	// See https://systemd.io/BUILDING_IMAGES/ for more information.
	var otherFilesToRemove = []string{
		"/var/lib/systemd/random-seed",
		"/boot/efi/loader/random-seed",
		"/var/lib/systemd/credential.secret",
	}

	// From https://www.freedesktop.org/software/systemd/man/latest/machine-id.html#Initialization:
	// For operating system images which are created once and used on multiple
	// machines, for example for containers or in the cloud, /etc/machine-id
	// should be either missing or an empty file in the generic file system
	// image (the difference between the two options is described under
	// "First Boot Semantics" below). An ID will be generated during boot and
	// saved to this file if possible. Having an empty file in place is useful
	// because it allows a temporary file to be bind-mounted over the real file,
	// in case the image is used read-only
	//
	// From https://www.freedesktop.org/software/systemd/man/latest/machine-id.html#First%20Boot%20Semantics:
	//     etc/machine-id is used to decide whether a boot is the first one. The rules are as follows:
	//     1. The kernel command argument systemd.condition-first-boot= may be used to override the autodetection logic,
	//         see kernel-command-line(7).
	//     2. Otherwise, if /etc/machine-id does not exist, this is a first boot. During early boot, systemd will write
	//         "uninitialized\n" to this file and overmount a temporary file which contains the actual machine ID. Later
	//         (after first-boot-complete.target has been reached), the real machine ID will be written to disk.
	//     3. If /etc/machine-id contains the string "uninitialized", a boot is also considered the first boot. The same
	//         mechanism as above applies.
	//     4. If /etc/machine-id exists and is empty, a boot is not considered the first boot. systemd will still
	//         bind-mount a file containing the actual machine-id over it and later try to commit it to disk (if /etc/ is
	//         writable).
	//     5. If /etc/machine-id already contains a valid machine-id, this is not a first boot.
	//     If according to the above rules a first boot is detected, units with ConditionFirstBoot=yes will be run and
	//     systemd will perform additional initialization steps, in particular presetting units.
	//
	// We will use option 4) by default since AZL has traditionally not used firstboot mechanisms. All configuration
	// that systemd-firstboot would set should have already been configured by the imager tool. It is important to
	// create an empty file so that read-only configurations will work as expected. If the user requests that firstboot
	// be enabled we will set it to "uninitalized" as per option 3).

	ReportAction("Configuring systemd state files for first boot")

	// The systemd package will create this file, but if its not installed, we need to create it.
	exists, err := file.PathExists(filepath.Join(installChroot.RootDir(), machineIDFile))
	if err != nil {
		err = fmt.Errorf("failed to check if machine-id exists:\n%w", err)
		return
	}
	if !exists {
		logger.Log.Debug("Creating empty machine-id file")
		err = file.Create(filepath.Join(installChroot.RootDir(), machineIDFile), machineIDFilePerms)
		if err != nil {
			err = fmt.Errorf("failed to create empty machine-id:\n%w", err)
			return err
		}
	}

	if enableSystemdFirstboot {
		ReportAction("Enabling systemd firstboot")
		err = file.Write(machineIDFirstBootOn, filepath.Join(installChroot.RootDir(), machineIDFile))
	} else {
		ReportAction("Disabling systemd firstboot")
		err = file.Write(machineIDFirstbootOff, filepath.Join(installChroot.RootDir(), machineIDFile))
	}
	if err != nil {
		err = fmt.Errorf("failed to write empty machine-id:\n%w", err)
		return err
	}

	// These files should not be present in the image, but per https://systemd.io/BUILDING_IMAGES/ we should
	// be thorough and double-check.
	for _, filePath := range otherFilesToRemove {
		fullPath := filepath.Join(installChroot.RootDir(), filePath)
		exists, err = file.PathExists(fullPath)
		if err != nil {
			err = fmt.Errorf("failed to check if systemd state file (%s) exists:\n%w", filePath, err)
			return err
		}

		// Do an explicit check for existence so we can log the file removal.
		if exists {
			ReportActionf("Removing systemd state file (%s)", filePath)
			err = file.RemoveFileIfExists(fullPath)
			if err != nil {
				err = fmt.Errorf("failed to remove systemd state file (%s):\n%w", filePath, err)
				return err
			}
		}
	}

	return
}

// AddImageIDFile adds image-id file in the /etc directory of the install root.
// The file contains the following fields:
// BUILD_NUMBER: The build number of the image
// IMAGE_BUILD_DATE: The date when the image is built in format YYYYMMDDHHMMSS
// IMAGE_UUID: The UUID of the image
func AddImageIDFile(installChrootRootDir string, buildNumber string) (err error) {
	// Check if /etc directory exists and it does not, throw an error
	_, err = os.Stat(filepath.Join(installChrootRootDir, "/etc"))
	if err != nil {
		if os.IsNotExist(err) {
			err = fmt.Errorf("directory /etc does not exist in the install root")
		}
		return
	}

	// If buildNumber is empty, then default to "local"
	if buildNumber == "" {
		buildNumber = "local"
	}

	const (
		imageIDFile      = "/etc/image-id"
		imageIDFilePerms = 0444
	)

	ReportAction("Creating image-id file")

	// Get the current time in UTC and in format "YYYYMMDDHHMMSS"
	imageBuildDate := time.Now().UTC().Format("20060102150405")

	imageIDContent := fmt.Sprintf("BUILD_NUMBER=%s\nIMAGE_BUILD_DATE=%s\nIMAGE_UUID=%s\n", buildNumber, imageBuildDate, uuid.New().String())
	imageIDFilePath := filepath.Join(installChrootRootDir, imageIDFile)

	fileCreateErr := file.Create(imageIDFilePath, imageIDFilePerms)
	if fileCreateErr != nil {
		err = fmt.Errorf("failed to create image-id file: %v", fileCreateErr)
		return
	}

	ReportAction(fmt.Sprintf("Writing following content to image-id file: %s", imageIDContent))

	fileWriteErr := file.Write(imageIDContent, imageIDFilePath)
	if fileWriteErr != nil {
		err = fmt.Errorf("failed to write to image-id file: %v", fileWriteErr)
		return
	}

	return
}

func updateInitramfsForEncrypt(installChroot *safechroot.Chroot) (err error) {
	err = installChroot.UnsafeRun(func() (err error) {
		const (
			libModDir     = "/lib/modules"
			dracutModules = "dm crypt crypt-gpg crypt-loop lvm"
			initrdPrefix  = "/boot/initramfs-"
			initrdSuffix  = ".img"
			cryptTabPath  = "/etc/crypttab"
		)

		initrdPattern := fmt.Sprintf("%v*%v", initrdPrefix, initrdSuffix)
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
		kernel = strings.TrimSuffix(kernel, initrdSuffix)

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

func UpdateFstab(installRoot string, partitionSettings []configuration.PartitionSetting, mountList []string,
	mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap, partIDToDevPathMap, partIDToFsTypeMap map[string]string,
	hidepidEnabled bool,
) (err error) {
	const fstabPath = "/etc/fstab"

	fullFstabPath := filepath.Join(installRoot, fstabPath)

	return UpdateFstabFile(fullFstabPath, partitionSettings, mountList, mountPointMap,
		mountPointToFsTypeMap, mountPointToMountArgsMap, partIDToDevPathMap, partIDToFsTypeMap,
		hidepidEnabled)
}

func UpdateFstabFile(fullFstabPath string, partitionSettings []configuration.PartitionSetting, mountList []string,
	mountPointMap, mountPointToFsTypeMap, mountPointToMountArgsMap, partIDToDevPathMap, partIDToFsTypeMap map[string]string,
	hidepidEnabled bool,
) (err error) {
	const (
		doPseudoFsMount = true
	)
	ReportAction("Configuring fstab")

	for _, mountPoint := range mountList {
		devicePath := mountPointMap[mountPoint]

		if mountPoint != "" && devicePath != NullDevice {
			partSetting := configuration.FindMountpointPartitionSetting(partitionSettings, mountPoint)
			if partSetting == nil {
				err = fmt.Errorf("unable to find PartitionSetting for '%s", mountPoint)
				return
			}
			err = addEntryToFstab(fullFstabPath, mountPoint, devicePath, mountPointToFsTypeMap[mountPoint],
				mountPointToMountArgsMap[mountPoint], partSetting.MountIdentifier, !doPseudoFsMount)
			if err != nil {
				return
			}
		}
	}

	if hidepidEnabled {
		err = addEntryToFstab(fullFstabPath, "/proc", "proc", "proc", "rw,nosuid,nodev,noexec,relatime,hidepid=2", configuration.MountIdentifierNone, doPseudoFsMount)
		if err != nil {
			return
		}
	}

	// Add swap entry if there is one
	for partID, fstype := range partIDToFsTypeMap {
		if fstype == "linux-swap" {
			swapPartitionPath, exists := partIDToDevPathMap[partID]
			if exists {
				err = addEntryToFstab(fullFstabPath, "none", swapPartitionPath, "swap", "", "", doPseudoFsMount)
				if err != nil {
					return
				}
			}
		}
	}

	return
}

func addEntryToFstab(fullFstabPath, mountPoint, devicePath, fsType, mountArgs string, identifierType configuration.MountIdentifier, doPseudoFsMount bool) (err error) {
	const (
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

func ConfigureDiskBootloader(bootType string, encryptionEnable bool, readOnlyVerityRootEnable bool,
	partitionSettings []configuration.PartitionSetting, kernelCommandLine configuration.KernelCommandLine,
	installChroot *safechroot.Chroot, diskDevPath string, mountPointMap map[string]string,
	encryptedRoot diskutils.EncryptedRootDevice, readOnlyRoot diskutils.VerityDevice, enableGrubMkconfig bool,
	includeLegacyGrubCfg bool,
) (err error) {
	timestamp.StartEvent("configuring bootloader", nil)
	defer timestamp.StopEvent(nil)

	if mountPointMap[rootMountPoint] == NullDevice {
		// In case of overlay device being mounted at root, no need to change the bootloader.
		return
	}

	rootPartitionSetting := configuration.FindRootPartitionSetting(partitionSettings)
	if rootPartitionSetting == nil {
		err = fmt.Errorf("failed to find partition setting for root mountpoint")
		return
	}
	rootMountIdentifier := rootPartitionSetting.MountIdentifier

	return ConfigureDiskBootloaderWithRootMountIdType(bootType, encryptionEnable, readOnlyVerityRootEnable,
		rootMountIdentifier, kernelCommandLine, installChroot, diskDevPath, mountPointMap, encryptedRoot, readOnlyRoot,
		enableGrubMkconfig, includeLegacyGrubCfg)
}

func ConfigureDiskBootloaderWithRootMountIdType(bootType string, encryptionEnable bool, readOnlyVerityRootEnable bool,
	rootMountIdentifier configuration.MountIdentifier, kernelCommandLine configuration.KernelCommandLine,
	installChroot *safechroot.Chroot, diskDevPath string, mountPointMap map[string]string,
	encryptedRoot diskutils.EncryptedRootDevice, readOnlyRoot diskutils.VerityDevice, enableGrubMkconfig bool,
	includeLegacyGrubCfg bool,
) (err error) {
	// Add bootloader. Prefer a separate boot partition if one exists.
	bootDevice, isBootPartitionSeparate := mountPointMap[bootMountPoint]
	bootPrefix := ""
	if !isBootPartitionSeparate {
		bootDevice = mountPointMap[rootMountPoint]
		// If we do not have a separate boot partition we will need to add a prefix to all paths used in the configs.
		bootPrefix = CombinedBootPartitionBootPrefix
	}

	if mountPointMap[rootMountPoint] == NullDevice {
		// In case of overlay device being mounted at root, no need to change the bootloader.
		return
	}

	// Grub only accepts UUID, not PARTUUID or PARTLABEL
	bootUUID, err := GetUUID(bootDevice)
	if err != nil {
		err = fmt.Errorf("failed to get UUID: %s", err)
		return
	}

	err = InstallBootloader(installChroot, encryptionEnable, bootType, bootUUID, bootPrefix, diskDevPath)
	if err != nil {
		err = fmt.Errorf("failed to install bootloader: %s", err)
		return
	}

	// Add grub config to image
	var rootDevice string
	if encryptionEnable {
		// Encrypted devices don't currently support identifiers
		rootDevice = mountPointMap[rootMountPoint]
	} else if readOnlyVerityRootEnable {
		var partIdentifier string
		partIdentifier, err = FormatMountIdentifier(rootMountIdentifier, readOnlyRoot.BackingDevice)
		if err != nil {
			err = fmt.Errorf("failed to get partIdentifier: %s", err)
			return
		}
		rootDevice = fmt.Sprintf("verityroot:%v", partIdentifier)
	} else {
		var partIdentifier string
		partIdentifier, err = FormatMountIdentifier(rootMountIdentifier, mountPointMap[rootMountPoint])
		if err != nil {
			err = fmt.Errorf("failed to get partIdentifier: %s", err)
			return
		}

		rootDevice = partIdentifier
	}

	// Grub will always use filesystem UUID, never PARTUUID or PARTLABEL
	err = InstallGrubDefaults(installChroot.RootDir(), rootDevice, bootUUID, bootPrefix, encryptedRoot,
		kernelCommandLine, readOnlyRoot, isBootPartitionSeparate, includeLegacyGrubCfg)
	if err != nil {
		err = fmt.Errorf("failed to install main grub config file: %s", err)
		return
	}

	err = InstallGrubEnv(installChroot.RootDir())
	if err != nil {
		err = fmt.Errorf("failed to install grubenv file: %s", err)
		return
	}

	// Use grub mkconfig to replace the static template .cfg with a dynamically generated version if desired.
	if enableGrubMkconfig {
		err = CallGrubMkconfig(installChroot)
		if err != nil {
			err = fmt.Errorf("failed to generate grub.cfg via grub2-mkconfig: %s", err)
			return
		}
	}

	return
}

// InstallGrubEnv installs an empty grubenv f
func InstallGrubEnv(installRoot string) (err error) {
	const (
		assetGrubEnvFile = "assets/grub2/grubenv"
		grubEnvFile      = "boot/grub2/grubenv"
	)
	installGrubEnvFile := filepath.Join(installRoot, grubEnvFile)
	err = file.CopyResourceFile(resources.ResourcesFS, assetGrubEnvFile, installGrubEnvFile, bootDirectoryDirMode,
		bootDirectoryFileMode)
	if err != nil {
		logger.Log.Warnf("Failed to copy and change mode of grubenv: %v", err)
		return
	}

	return
}

// InstallGrubDefaults installs the main grub config to the rootfs partition
// - installRoot is the base install directory
// - rootDevice holds the root partition
// - bootUUID is the UUID for the boot partition
// - bootPrefix is the path to the /boot grub configs based on the mountpoints (i.e., if /boot is a separate partition from the rootfs partition, bootPrefix="").
// - encryptedRoot holds the encrypted root information if encrypted root is enabled
// - kernelCommandLine contains additional kernel parameters which may be optionally set
// - readOnlyRoot holds the dm-verity read-only root partition information if dm-verity is enabled.
// - isBootPartitionSeparate is a boolean value which is true if the /boot partition is separate from the root partition
// - includeLegacyCfg specifies if the legacy grub.cfg from Azure Linux should also be added.
// Note: this boot partition could be different than the boot partition specified in the bootloader.
// This boot partition specifically indicates where to find the kernel, config files, and initrd
func InstallGrubDefaults(installRoot, rootDevice, bootUUID, bootPrefix string,
	encryptedRoot diskutils.EncryptedRootDevice, kernelCommandLine configuration.KernelCommandLine,
	readOnlyRoot diskutils.VerityDevice, isBootPartitionSeparate bool, includeLegacyCfg bool,
) (err error) {
	// Copy the bootloader's /etc/default/grub and set the file permission
	err = installGrubTemplateFile(resources.AssetsGrubDefFile, GrubDefFile, installRoot, rootDevice, bootUUID,
		bootPrefix, encryptedRoot, kernelCommandLine, readOnlyRoot, isBootPartitionSeparate)
	if err != nil {
		logger.Log.Warnf("Failed to install (%s): %v", GrubDefFile, err)
		return
	}

	if includeLegacyCfg {
		// Add the legacy /boot/grub2/grub.cfg file, which was used in Azure Linux 2.0.
		err = installGrubTemplateFile(resources.AssetsGrubCfgFile, GrubCfgFile, installRoot, rootDevice, bootUUID,
			bootPrefix, encryptedRoot, kernelCommandLine, readOnlyRoot, isBootPartitionSeparate)
		if err != nil {
			logger.Log.Warnf("Failed to install (%s): %v", GrubCfgFile, err)
			return
		}
	}

	return
}

func installGrubTemplateFile(assetFile, targetFile, installRoot, rootDevice, bootUUID, bootPrefix string,
	encryptedRoot diskutils.EncryptedRootDevice, kernelCommandLine configuration.KernelCommandLine,
	readOnlyRoot diskutils.VerityDevice, isBootPartitionSeparate bool,
) (err error) {
	installGrubDefFile := filepath.Join(installRoot, targetFile)

	err = file.CopyResourceFile(resources.ResourcesFS, assetFile, installGrubDefFile, bootDirectoryDirMode,
		bootUsrConfigFileMode)
	if err != nil {
		return
	}

	// Add in bootUUID
	err = setGrubCfgBootUUID(bootUUID, installGrubDefFile)
	if err != nil {
		logger.Log.Warnf("Failed to set bootUUID in %s: %v", installGrubDefFile, err)
		return
	}

	// Add in bootPrefix
	err = setGrubCfgBootPrefix(bootPrefix, installGrubDefFile)
	if err != nil {
		logger.Log.Warnf("Failed to set bootPrefix in %s: %v", installGrubDefFile, err)
		return
	}

	// Add in rootDevice
	err = setGrubCfgRootDevice(rootDevice, installGrubDefFile, encryptedRoot.LuksUUID)
	if err != nil {
		logger.Log.Warnf("Failed to set rootDevice in %s: %v", installGrubDefFile, err)
		return
	}

	// Add in rootLuksUUID
	err = setGrubCfgLuksUUID(installGrubDefFile, encryptedRoot.LuksUUID)
	if err != nil {
		logger.Log.Warnf("Failed to set luksUUID in %s: %v", installGrubDefFile, err)
		return
	}

	// Add in logical volumes to active
	err = setGrubCfgLVM(installGrubDefFile, encryptedRoot.LuksUUID)
	if err != nil {
		logger.Log.Warnf("Failed to set lvm.lv in %s: %v", installGrubDefFile, err)
		return
	}

	// Configure IMA policy
	err = setGrubCfgIMA(installGrubDefFile, kernelCommandLine)
	if err != nil {
		logger.Log.Warnf("Failed to set ima_policy in in %s: %v", installGrubDefFile, err)
		return
	}

	err = setGrubCfgReadOnlyVerityRoot(installGrubDefFile, readOnlyRoot)
	if err != nil {
		logger.Log.Warnf("Failed to set verity root in in %s: %v", installGrubDefFile, err)
		return
	}

	err = setGrubCfgSELinux(installGrubDefFile, kernelCommandLine)
	if err != nil {
		logger.Log.Warnf("Failed to set SELinux in %s: %v", installGrubDefFile, err)
		return
	}

	// Configure FIPS
	err = setGrubCfgFIPS(isBootPartitionSeparate, bootUUID, installGrubDefFile, kernelCommandLine)
	if err != nil {
		logger.Log.Warnf("Failed to set FIPS in %s: %v", installGrubDefFile, err)
		return
	}

	err = setGrubCfgCGroup(installGrubDefFile, kernelCommandLine)
	if err != nil {
		logger.Log.Warnf("Failed to set CGroup configuration in %s: %v", installGrubDefFile, err)
		return
	}

	// Append any additional command line parameters
	err = setGrubCfgAdditionalCmdLine(installGrubDefFile, kernelCommandLine)
	if err != nil {
		logger.Log.Warnf("Failed to append extra command line parameters in %s: %v", installGrubDefFile, err)
		return
	}

	return
}

func CallGrubMkconfig(installChroot *safechroot.Chroot) (err error) {
	squashErrors := false

	ReportActionf("Running grub2-mkconfig...")
	err = installChroot.UnsafeRun(func() error {
		return shell.ExecuteLive(squashErrors, "grub2-mkconfig", "-o", GrubCfgFile)
	})

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
		if err != nil {
			return fmt.Errorf("failed to add group (%s):\n%w", group.Name, err)
		}
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

		// Primary group will have already been set when the user was created so we don't need to set it again
		err = ConfigureUserSecondaryGroupMembership(installChroot, user.Name, user.SecondaryGroups)
		if err != nil {
			return
		}

		err = ProvisionUserSSHCerts(installChroot, user.Name, user.SSHPubKeyPaths, user.SSHPubKeys,
			false /*includeExistingKeys*/)
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
			return fmt.Errorf("failed to access shadow file:\n%w", ferr)
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

	// Create the user with the given hashed password
	if user.Name == userutils.RootUser {
		if user.UID != "" {
			logger.Log.Warnf("Ignoring UID for (%s) user, using default", userutils.RootUser)
		}

		if exists, ferr := file.PathExists(installChrootShadowFile); ferr != nil {
			err = fmt.Errorf("failed to access shadow file:\n%w", ferr)
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
		err = userutils.AddUser(user.Name, user.HomeDirectory, user.PrimaryGroup, hashedPassword, user.UID, installChroot)
		if err != nil {
			return
		}
	}

	// Update password expiration
	if user.PasswordExpiresDays != 0 {
		// Ignore updating if there is no shadow file to update
		if exists, ferr := file.PathExists(installChrootShadowFile); ferr != nil {
			err = fmt.Errorf("failed to access shadow file:\n%w", ferr)
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
func Chage(installChroot safechroot.ChrootInterface, passwordExpirationInDays int64, username string) (err error) {
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

func ConfigureUserPrimaryGroupMembership(installChroot safechroot.ChrootInterface, username string, primaryGroup string,
) (err error) {
	const squashErrors = false

	if primaryGroup != "" {
		err = installChroot.UnsafeRun(func() error {
			return shell.ExecuteLive(squashErrors, "usermod", "-g", primaryGroup, username)
		})

		if err != nil {
			return
		}
	}

	return
}

func ConfigureUserSecondaryGroupMembership(installChroot safechroot.ChrootInterface, username string, secondaryGroups []string,
) (err error) {
	const squashErrors = false

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

func ConfigureUserStartupCommand(installChroot safechroot.ChrootInterface, username string, startupCommand string) (err error) {
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

func ProvisionUserSSHCerts(installChroot safechroot.ChrootInterface, username string, sshPubKeyPaths []string,
	sshPubKeys []string, includeExistingKeys bool,
) (err error) {
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
	if len(sshPubKeyPaths) == 0 && len(sshPubKeys) == 0 {
		return
	}

	userSSHKeyDir := userutils.UserSSHDirectory(username)
	authorizedKeysFile := filepath.Join(userSSHKeyDir, userutils.SSHAuthorizedKeysFileName)

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

	allSSHKeys := []string(nil)

	if includeExistingKeys {
		authorizedKeysFileFullPath := filepath.Join(installChroot.RootDir(), authorizedKeysFile)

		fileExists, err := file.PathExists(authorizedKeysFileFullPath)
		if err != nil {
			return fmt.Errorf("failed to check if authorized_keys file (%s) exists:\n%w", authorizedKeysFileFullPath, err)
		}

		if fileExists {
			pubKeyData, err = file.ReadLines(authorizedKeysFileFullPath)
			if err != nil {
				return fmt.Errorf("failed to read existing authorized_keys (%s) file:\n%w", authorizedKeysFileFullPath, err)
			}

			allSSHKeys = append(allSSHKeys, pubKeyData...)
		}
	}

	// Add SSH keys from sshPubKeyPaths
	for _, pubKey := range sshPubKeyPaths {
		relativeDst := filepath.Join(userSSHKeyDir, filepath.Base(pubKey))

		fileToCopy := safechroot.FileToCopy{
			Src:  pubKey,
			Dest: relativeDst,
		}

		err = installChroot.AddFiles(fileToCopy)
		if err != nil {
			return
		}

		pubKeyData, err = file.ReadLines(pubKey)
		if err != nil {
			logger.Log.Warnf("Failed to read from SSHPubKey : %v", err)
			return
		}

		allSSHKeys = append(allSSHKeys, pubKeyData...)
	}

	// Add direct SSH keys
	allSSHKeys = append(allSSHKeys, sshPubKeys...)

	for _, pubKey := range allSSHKeys {
		logger.Log.Infof("Adding ssh key (%s) to user (%s) .ssh/authorized_users", filepath.Base(pubKey), username)
		pubKey += "\n"

		err = file.Append(pubKey, authorizedKeysTempFile)
		if err != nil {
			logger.Log.Warnf("Failed to append to %s : %v", authorizedKeysTempFile, err)
			return
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
func SELinuxConfigure(selinuxMode configuration.SELinux, installChroot *safechroot.Chroot,
	mountPointToFsTypeMap map[string]string, isRootFS bool,
) (err error) {
	timestamp.StartEvent("SELinux", nil)
	defer timestamp.StopEvent(nil)
	logger.Log.Infof("Preconfiguring SELinux policy in %s mode", selinuxMode)

	err = SELinuxUpdateConfig(selinuxMode, installChroot)
	if err != nil {
		err = fmt.Errorf("failed to update SELinux config:\n%w", err)
		return
	}
	err = SELinuxRelabelFiles(installChroot, mountPointToFsTypeMap, isRootFS)
	if err != nil {
		err = fmt.Errorf("failed to label SELinux files:\n%w", err)
		return
	}
	return
}

func SELinuxUpdateConfig(selinuxMode configuration.SELinux, installChroot *safechroot.Chroot) (err error) {
	const (
		selinuxPattern = "^SELINUX=.*"
	)
	var mode string

	switch selinuxMode {
	case configuration.SELinuxEnforcing, configuration.SELinuxForceEnforcing:
		mode = SELinuxConfigEnforcing
	case configuration.SELinuxPermissive:
		mode = SELinuxConfigPermissive
	case configuration.SELinuxOff:
		mode = SELinuxConfigDisabled
	}

	selinuxConfigPath := filepath.Join(installChroot.RootDir(), SELinuxConfigFile)
	selinuxProperty := fmt.Sprintf("SELINUX=%s", mode)
	err = sed(selinuxPattern, selinuxProperty, "`", selinuxConfigPath)
	return
}

func SELinuxRelabelFiles(installChroot *safechroot.Chroot, mountPointToFsTypeMap map[string]string, isRootFS bool,
) (err error) {
	const (
		fileContextBasePath = "etc/selinux/%s/contexts/files/file_contexts"
	)
	var listOfMountsToLabel []string

	if isRootFS {
		listOfMountsToLabel = append(listOfMountsToLabel, "/")
	} else {
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
	}

	// Find the type of policy we want to label with
	selinuxConfigPath := filepath.Join(installChroot.RootDir(), SELinuxConfigFile)
	stdout, stderr, err := shell.Execute("sed", "-n", "s/^SELINUXTYPE=\\(.*\\)$/\\1/p", selinuxConfigPath)
	if err != nil {
		err = fmt.Errorf("failed to find an SELINUXTYPE in (%s):\n%w\n%v", selinuxConfigPath, err, stderr)
		return
	}
	selinuxType := strings.TrimSpace(stdout)
	fileContextPath := fmt.Sprintf(fileContextBasePath, selinuxType)

	targetRootPath := "/mnt/_bindmountroot"
	targetRootFullPath := filepath.Join(installChroot.RootDir(), targetRootPath)

	for _, mountToLabel := range listOfMountsToLabel {
		logger.Log.Debugf("Running setfiles to apply SELinux labels on mount points: %v", mountToLabel)

		// The chroot environment has a bunch of special filesystems (e.g. /dev, /proc, etc.) mounted within the OS
		// image. In addition, an image may have placed system directories on separate partitions, and these partitions
		// will also be mounted within the OS image. These mounts hide the underlying directory that is used as a mount
		// point, which prevents that directory from receiving an SELinux label from the setfiles command. A well known
		// way to get an unobstructed view of a filesystem, free from other mount-points, is to create a bind-mount for
		// that filesystem. Therefore, bind mounts are used to ensure that all directories receive an SELinux label.
		sourceFullPath := filepath.Join(installChroot.RootDir(), mountToLabel)
		targetPath := filepath.Join(targetRootPath, mountToLabel)
		targetFullPath := filepath.Join(installChroot.RootDir(), targetPath)

		bindMount, err := safemount.NewMount(sourceFullPath, targetFullPath, "", unix.MS_BIND, "", true)
		if err != nil {
			return fmt.Errorf("failed to bind mount (%s) while SELinux labeling:\n%w", mountToLabel, err)
		}
		defer bindMount.Close()

		err = installChroot.UnsafeRun(func() error {
			// We only want to print basic info, filter out the real output unless at trace level (Execute call handles that)
			files := 0
			lastFile := ""
			onStdout := func(line string) {
				files++
				lastFile = line
				if (files % 1000) == 0 {
					ReportActionf("SELinux: labelled %d files", files)
				}
			}
			err := shell.NewExecBuilder("setfiles", "-m", "-v", "-r", targetRootPath, fileContextPath, targetPath).
				StdoutCallback(onStdout).
				LogLevel(logrus.TraceLevel, logrus.WarnLevel).
				Execute()
			if err != nil {
				return fmt.Errorf("failed while labeling files (last file: %s) %w", lastFile, err)
			}
			ReportActionf("SELinux: labelled %d files", files)
			return err
		})
		if err != nil {
			return err
		}

		err = bindMount.CleanClose()
		if err != nil {
			return err
		}

		// Cleanup the temporary directory.
		// Note: This is intentionally done within the for loop to ensure the directory is always empty for the next
		// mount. For example, if a parent directory mount is processed after a nested child directory mount.
		err = os.RemoveAll(targetRootFullPath)
		if err != nil {
			return fmt.Errorf("failed to remove temporary bind mount directory:\n%w", err)
		}
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
func InstallBootloader(installChroot *safechroot.Chroot, encryptEnabled bool, bootType, bootUUID, bootPrefix,
	bootDevPath string,
) (err error) {
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
		err = installEfiBootloader(encryptEnabled, efiPath, bootUUID, bootPrefix)
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
		squashErrors     = false
		bootDir          = "/boot"
		bootDirArg       = "--boot-directory"
		grub2BootDir     = "/boot/grub2"
		grub2InstallName = "grub2-install"
		grubInstallName  = "grub-install"
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

	installName := grub2InstallName
	grub2InstallExists, err := file.CommandExists(grub2InstallName)
	if err != nil {
		return
	}

	if !grub2InstallExists {
		grubInstallExists, err := file.CommandExists(grubInstallName)
		if err != nil {
			return err
		}

		if !grubInstallExists {
			return fmt.Errorf("neither 'grub2-install' command nor 'grub-install' command found")
		}

		installName = grubInstallName
	}

	err = shell.ExecuteLive(squashErrors, installName, "--target=i386-pc", grub2InstallBootDirArg, bootDevPath)
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
		err = fmt.Errorf("unknown mount identifier: (%v)", identifier)
	}
	return
}

// enableCryptoDisk enables Grub to boot from an encrypted disk
// - installChroot is the installation chroot
func enableCryptoDisk() (err error) {
	const (
		grubCryptoDisk     = "GRUB_ENABLE_CRYPTODISK=y\n"
		grubPreloadModules = `GRUB_PRELOAD_MODULES="lvm"`
	)

	err = file.Append(grubCryptoDisk, GrubDefFile)
	if err != nil {
		logger.Log.Warnf("Failed to add grub cryptodisk: %v", err)
		return
	}
	err = file.Append(grubPreloadModules, GrubDefFile)
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
func installEfiBootloader(encryptEnabled bool, installRoot, bootUUID, bootPrefix string) (err error) {
	const (
		defaultCfgFilename = "grub.cfg"
		grubAssetDir       = "assets/efi/grub"
		grubFinalDir       = "boot/grub2"
	)

	// Copy the bootloader's grub.cfg
	grubAssetPath := filepath.Join(grubAssetDir, defaultCfgFilename)
	grubFinalPath := filepath.Join(installRoot, grubFinalDir, defaultCfgFilename)
	err = file.CopyResourceFile(resources.ResourcesFS, grubAssetPath, grubFinalPath, bootDirectoryDirMode,
		bootDirectoryFileMode)
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

	// Set the boot prefix path
	prefixPath := filepath.Join("/", bootPrefix, "grub2")
	err = setGrubCfgPrefixPath(prefixPath, grubFinalPath)
	if err != nil {
		logger.Log.Warnf("Failed to set prefixPath in grub.cfg: %v", err)
		return
	}

	// Add in encrypted volume mount command if needed
	err = setGrubCfgEncryptedVolume(grubFinalPath, encryptEnabled)
	if err != nil {
		logger.Log.Warnf("Failed to set encrypted volume in grub.cfg: %v", err)
		return
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
		err = fmt.Errorf("failed to remove RPM database (%s):\n%w", rpmDir, err)
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
				err = fmt.Errorf("failed to cleanup post-install script (%s):\n%w", scriptPath, err)
			}

			return err
		})

		if err != nil {
			return
		}
	}

	return
}

// cleanupTdnfCache runs 'tdnf clean all' and removes the contents of the tdnf cache directory.
// If 'tdnf' is not installed, the function will skip the cleanup.
// If /var/cache/tdnf does not exist, the function will skip removing its contents.
func cleanupTdnfCache(installChroot *safechroot.Chroot) error {
	const (
		squashErrors      = false
		rpmCacheDirectory = "/var/cache/tdnf"
	)

	ReportActionf("Cleaning tdnf cache")
	err := installChroot.UnsafeRun(func() error {
		// Check if 'tdnf' is in the chroot's PATH, some images may have removed it.
		_, chrootErr := exec.LookPath("tdnf")
		if chrootErr != nil {
			logger.Log.Debugf("Skipping tdnf cache cleanup since 'tdnf' is not installed")
			return nil
		}
		logger.Log.Infof("Cleaning tdnf cache")
		chrootErr = shell.ExecuteLive(squashErrors, "tdnf", "clean", "all")
		return chrootErr
	})

	if err != nil {
		err = fmt.Errorf("failed to cleanup tdnf cache:\n%w", err)
		return err
	}

	// Remove all files and subdirectories in the tdnf cache directory, but leave
	// the directory since it's owned by the tdnf package.
	cacheDir := filepath.Join(installChroot.RootDir(), rpmCacheDirectory)
	// Skip if directory is missing already
	exists, err := file.DirExists(cacheDir)
	if err != nil {
		return fmt.Errorf("failed to check if tdnf cache directory exists (%s):\n%w", cacheDir, err)
	}
	if !exists {
		logger.Log.Debugf("Skipping tdnf cache cleanup since directory does not exist (%s)", cacheDir)
		return nil
	}

	logger.Log.Infof("Removing contents of (%s)", cacheDir)
	err = file.RemoveDirectoryContents(cacheDir)
	if err != nil {
		err = fmt.Errorf("failed to remove tdnf cache contents (%s/*):\n%w", cacheDir, err)
		return err
	}
	return nil
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
				err = fmt.Errorf("failed to cleanup finalize image script (%s):\n%w", scriptPath, err)
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
		selinuxPattern = "{{.SELinux}}"
	)
	var selinux string

	switch kernelCommandline.SELinux {
	case configuration.SELinuxForceEnforcing:
		selinux = CmdlineSELinuxForceEnforcing
	case configuration.SELinuxPermissive, configuration.SELinuxEnforcing:
		selinux = CmdlineSELinuxSettings
	case configuration.SELinuxOff:
		selinux = CmdlineSELinuxDisabledArg
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

func setGrubCfgPrefixPath(prefixPath string, grubPath string) (err error) {
	const (
		prefixPathPattern = "{{.PrefixPath}}"
	)
	var cmdline configuration.KernelCommandLine

	err = sed(prefixPathPattern, prefixPath, cmdline.GetSedDelimeter(), grubPath)
	if err != nil {
		logger.Log.Warnf("Failed to set grub.cfg's prefixPath: %v", err)
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

func setGrubCfgEncryptedVolume(grubPath string, enableEncryptedVolume bool) (err error) {
	const (
		encryptedVolPattern = "{{.CryptoMountCommand}}"
		cryptoMountCommand  = "cryptomount -a"
	)
	var (
		cmdline         configuration.KernelCommandLine
		encryptedVolArg = ""
	)

	if enableEncryptedVolume {
		encryptedVolArg = cryptoMountCommand
	}

	logger.Log.Debugf("Adding CryptoMountCommand('%s') to '%s'", encryptedVolArg, grubPath)
	err = sed(encryptedVolPattern, encryptedVolArg, cmdline.GetSedDelimeter(), grubPath)
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
