// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"strconv"
	"time"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/installutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/sliceutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/userutils"
)

const (
	configDirMountPathInChroot = "/_imageconfigs"
	resolveConfPath            = "/etc/resolv.conf"
	defaultFilePermissions     = 0o755
)

func doCustomizations(buildDir string, baseConfigPath string, config *imagecustomizerapi.Config,
	imageConnection *ImageConnection, rpmsSources []string, useBaseImageRpmRepos bool, partitionsCustomized bool,
) error {
	var err error

	imageChroot := imageConnection.Chroot()

	buildTime := time.Now().Format("2006-01-02T15:04:05Z")

	err = overrideResolvConf(imageChroot)
	if err != nil {
		return err
	}

	err = addRemoveAndUpdatePackages(buildDir, baseConfigPath, config.OS, imageChroot, rpmsSources,
		useBaseImageRpmRepos)
	if err != nil {
		return err
	}

	err = UpdateHostname(config.OS.Hostname, imageChroot)
	if err != nil {
		return err
	}

	err = copyAdditionalDirs(baseConfigPath, config.OS.AdditionalDirs, imageChroot)
	if err != nil {
		return err
	}

	err = copyAdditionalFiles(baseConfigPath, config.OS.AdditionalFiles, imageChroot)
	if err != nil {
		return err
	}

	err = AddOrUpdateUsers(config.OS.Users, baseConfigPath, imageChroot)
	if err != nil {
		return err
	}

	err = enableOrDisableServices(config.OS.Services, imageChroot)
	if err != nil {
		return err
	}

	err = loadOrDisableModules(config.OS.Modules, imageChroot.RootDir())
	if err != nil {
		return err
	}

	err = addCustomizerRelease(imageChroot, ToolVersion, buildTime)
	if err != nil {
		return err
	}

	err = handleBootLoader(baseConfigPath, config, imageConnection)
	if err != nil {
		return err
	}

	selinuxMode, err := handleSELinux(config.OS.SELinux.Mode, config.OS.ResetBootLoaderType,
		imageChroot)
	if err != nil {
		return err
	}

	overlayUpdated, err := enableOverlays(config.OS.Overlays, imageChroot)
	if err != nil {
		return err
	}

	verityUpdated, err := enableVerityPartition(buildDir, config.OS.Verity, imageChroot)
	if err != nil {
		return err
	}

	if partitionsCustomized || overlayUpdated || verityUpdated {
		err = regenerateInitrd(imageChroot)
		if err != nil {
			return err
		}
	}

	if config.Scripts != nil {
		err = runUserScripts(baseConfigPath, config.Scripts.PostCustomization, "postCustomization", imageChroot)
		if err != nil {
			return err
		}
	}

	err = selinuxSetFiles(selinuxMode, imageChroot)
	if err != nil {
		return err
	}

	err = deleteResolvConf(imageChroot)
	if err != nil {
		return err
	}

	if config.Scripts != nil {
		err = runUserScripts(baseConfigPath, config.Scripts.FinalizeCustomization, "finalizeCustomization", imageChroot)
		if err != nil {
			return err
		}
	}

	return nil
}

// Override the resolv.conf file, so that in-chroot processes can access the network.
// For example, to install packages from packages.microsoft.com.
func overrideResolvConf(imageChroot *safechroot.Chroot) error {
	logger.Log.Infof("Overriding resolv.conf file")

	imageResolveConfPath := filepath.Join(imageChroot.RootDir(), resolveConfPath)

	// Remove the existing resolv.conf file, if it exists.
	// Note: It is assumed that the image will have a process that runs on boot that will override the resolv.conf
	// file. For example, systemd-resolved. So, it isn't neccessary to make a back-up of the existing file.
	err := os.RemoveAll(imageResolveConfPath)
	if err != nil {
		return fmt.Errorf("failed to delete existing resolv.conf file: %w", err)
	}

	err = file.Copy(resolveConfPath, imageResolveConfPath)
	if err != nil {
		return fmt.Errorf("failed to override resolv.conf file with host's resolv.conf: %w", err)
	}

	return nil
}

// Delete the overridden resolv.conf file.
// Note: It is assumed that the image will have a process that runs on boot that will override the resolv.conf
// file. For example, systemd-resolved.
func deleteResolvConf(imageChroot *safechroot.Chroot) error {
	logger.Log.Infof("Deleting overridden resolv.conf file")

	imageResolveConfPath := filepath.Join(imageChroot.RootDir(), resolveConfPath)

	err := os.RemoveAll(imageResolveConfPath)
	if err != nil {
		return fmt.Errorf("failed to delete overridden resolv.conf file: %w", err)
	}

	return err
}

func UpdateHostname(hostname string, imageChroot safechroot.ChrootInterface) error {
	if hostname == "" {
		return nil
	}

	logger.Log.Infof("Setting hostname (%s)", hostname)

	hostnameFilePath := filepath.Join(imageChroot.RootDir(), "etc/hostname")
	err := file.Write(hostname, hostnameFilePath)
	if err != nil {
		return fmt.Errorf("failed to write hostname file: %w", err)
	}

	return nil
}

func copyAdditionalFiles(baseConfigPath string, additionalFiles imagecustomizerapi.AdditionalFilesMap, imageChroot *safechroot.Chroot) error {
	for sourceFile, fileConfigs := range additionalFiles {
		absSourceFile := file.GetAbsPathWithBase(baseConfigPath, sourceFile)
		for _, fileConfig := range fileConfigs {
			logger.Log.Infof("Copying: %s", fileConfig.Path)

			fileToCopy := safechroot.FileToCopy{
				Src:         absSourceFile,
				Dest:        fileConfig.Path,
				Permissions: (*fs.FileMode)(fileConfig.Permissions),
			}

			err := imageChroot.AddFiles(fileToCopy)
			if err != nil {
				return err
			}
		}
	}

	return nil
}

func copyAdditionalDirs(baseConfigPath string, additionalDirs imagecustomizerapi.DirConfigList, imageChroot *safechroot.Chroot) error {
	for _, dirConfigElement := range additionalDirs {
		absSourceDir := file.GetAbsPathWithBase(baseConfigPath, dirConfigElement.SourcePath)
		logger.Log.Infof("Copying %s into %s", absSourceDir, dirConfigElement.DestinationPath)

		// Setting permissions values. They are set to a default value if they have not been specified.
		newDirPermissionsValue := fs.FileMode(defaultFilePermissions)
		if dirConfigElement.NewDirPermissions != nil {
			newDirPermissionsValue = *(*fs.FileMode)(dirConfigElement.NewDirPermissions)
		}
		childFilePermissionsValue := fs.FileMode(defaultFilePermissions)
		if dirConfigElement.ChildFilePermissions != nil {
			childFilePermissionsValue = *(*fs.FileMode)(dirConfigElement.ChildFilePermissions)
		}

		dirToCopy := safechroot.DirToCopy{
			Src:                  absSourceDir,
			Dest:                 dirConfigElement.DestinationPath,
			NewDirPermissions:    newDirPermissionsValue,
			ChildFilePermissions: childFilePermissionsValue,
			MergedDirPermissions: (*fs.FileMode)(dirConfigElement.MergedDirPermissions),
		}
		err := imageChroot.AddDirs(dirToCopy)
		if err != nil {
			return err
		}
	}
	return nil
}

func AddOrUpdateUsers(users []imagecustomizerapi.User, baseConfigPath string, imageChroot safechroot.ChrootInterface) error {
	for _, user := range users {
		err := addOrUpdateUser(user, baseConfigPath, imageChroot)
		if err != nil {
			return err
		}
	}

	return nil
}

func addOrUpdateUser(user imagecustomizerapi.User, baseConfigPath string, imageChroot safechroot.ChrootInterface) error {
	var err error

	logger.Log.Infof("Adding/updating user (%s)", user.Name)

	hashedPassword := ""
	if user.Password != nil {
		passwordIsFile := user.Password.Type == imagecustomizerapi.PasswordTypePlainTextFile ||
			user.Password.Type == imagecustomizerapi.PasswordTypeHashedFile

		passwordIsHashed := user.Password.Type == imagecustomizerapi.PasswordTypeHashed ||
			user.Password.Type == imagecustomizerapi.PasswordTypeHashedFile

		password := user.Password.Value
		if passwordIsFile {
			// Read password from file.
			passwordFullPath := file.GetAbsPathWithBase(baseConfigPath, user.Password.Value)

			passwordFileContents, err := os.ReadFile(passwordFullPath)
			if err != nil {
				return fmt.Errorf("failed to read password file (%s): %w", passwordFullPath, err)
			}

			password = string(passwordFileContents)
		}

		hashedPassword = password
		if !passwordIsHashed {
			// Hash the password.
			hashedPassword, err = userutils.HashPassword(password)
			if err != nil {
				return err
			}
		}
	}

	// Check if the user already exists.
	userExists, err := userutils.UserExists(user.Name, imageChroot)
	if err != nil {
		return err
	}

	if userExists {
		if user.UID != nil {
			return fmt.Errorf("cannot set UID (%d) on a user (%s) that already exists", *user.UID, user.Name)
		}

		// Update the user's password.
		err = userutils.UpdateUserPassword(imageChroot.RootDir(), user.Name, hashedPassword)
		if err != nil {
			return err
		}
	} else {
		var uidStr string
		if user.UID != nil {
			uidStr = strconv.Itoa(*user.UID)
		}

		// Add the user.
		err = userutils.AddUser(user.Name, hashedPassword, uidStr, imageChroot)
		if err != nil {
			return err
		}
	}

	// Set user's password expiry.
	if user.PasswordExpiresDays != nil {
		err = installutils.Chage(imageChroot, *user.PasswordExpiresDays, user.Name)
		if err != nil {
			return err
		}
	}

	// Set user's groups.
	err = installutils.ConfigureUserGroupMembership(imageChroot, user.Name, user.PrimaryGroup, user.SecondaryGroups)
	if err != nil {
		return err
	}

	// Set user's SSH keys.
	for i, _ := range user.SSHPublicKeyPaths {
		user.SSHPublicKeyPaths[i] = file.GetAbsPathWithBase(baseConfigPath, user.SSHPublicKeyPaths[i])
	}

	err = installutils.ProvisionUserSSHCerts(imageChroot, user.Name, user.SSHPublicKeyPaths, user.SSHPublicKeys,
		userExists)
	if err != nil {
		return err
	}

	// Set user's startup command.
	err = installutils.ConfigureUserStartupCommand(imageChroot, user.Name, user.StartupCommand)
	if err != nil {
		return err
	}

	return nil
}

func enableOrDisableServices(services imagecustomizerapi.Services, imageChroot *safechroot.Chroot) error {
	var err error

	// Handle enabling services
	for _, service := range services.Enable {
		logger.Log.Infof("Enabling service (%s)", service)

		err = imageChroot.UnsafeRun(func() error {
			return shell.ExecuteLiveWithErr(1, "systemctl", "enable", service)
		})
		if err != nil {
			return fmt.Errorf("failed to enable service (%s):\n%w", service, err)
		}
	}

	// Handle disabling services
	for _, service := range services.Disable {
		logger.Log.Infof("Disabling service (%s)", service)

		err = imageChroot.UnsafeRun(func() error {
			return shell.ExecuteLiveWithErr(1, "systemctl", "disable", service)
		})
		if err != nil {
			return fmt.Errorf("failed to disable service (%s):\n%w", service, err)
		}
	}

	return nil
}

func addCustomizerRelease(imageChroot *safechroot.Chroot, toolVersion string, buildTime string) error {
	var err error

	logger.Log.Infof("Creating image customizer release file")

	customizerReleaseFilePath := filepath.Join(imageChroot.RootDir(), "/etc/mariner-customizer-release")
	lines := []string{
		fmt.Sprintf("%s=\"%s\"", "TOOL_VERSION", toolVersion),
		fmt.Sprintf("%s=\"%s\"", "BUILD_DATE", buildTime),
		"",
	}

	err = file.WriteLines(lines, customizerReleaseFilePath)
	if err != nil {
		return fmt.Errorf("error writing customizer release file (%s): %w", customizerReleaseFilePath, err)
	}

	return nil
}

func handleBootLoader(baseConfigPath string, config *imagecustomizerapi.Config, imageConnection *ImageConnection,
) error {
	bootCustomizer, err := NewBootCustomizer(imageConnection.Chroot())
	if err != nil {
		return err
	}

	currentSelinuxMode, err := bootCustomizer.GetSELinuxMode(imageConnection.Chroot())
	if err != nil {
		return fmt.Errorf("failed to get existing SELinux mode:\n%w", err)
	}

	switch config.OS.ResetBootLoaderType {
	case imagecustomizerapi.ResetBootLoaderTypeHard:
		logger.Log.Infof("Resetting bootloader config")

		if config.Storage == nil {
			return fmt.Errorf("failed to configure bootloader. Missing 'storage' configuration.")
		}
		// Hard-reset the grub config.
		err := configureDiskBootLoader(imageConnection, config.Storage.FileSystems,
			config.Storage.BootType, config.OS.SELinux, config.OS.KernelCommandLine, currentSelinuxMode)
		if err != nil {
			return fmt.Errorf("failed to configure bootloader:\n%w", err)
		}

	default:
		// Append the kernel command-line args to the existing grub config.
		err := addKernelCommandLine(config.OS.KernelCommandLine.ExtraCommandLine, imageConnection.Chroot())
		if err != nil {
			return fmt.Errorf("failed to add extra kernel command line:\n%w", err)
		}
	}

	return nil
}

// Inserts new kernel command-line args into the grub config file.
func addKernelCommandLine(kernelExtraArguments imagecustomizerapi.KernelExtraArguments,
	imageChroot *safechroot.Chroot,
) error {
	var err error

	if kernelExtraArguments == "" {
		// Nothing to do.
		return nil
	}

	logger.Log.Infof("Setting KernelCommandLine.ExtraCommandLine")

	bootCustomizer, err := NewBootCustomizer(imageChroot)
	if err != nil {
		return err
	}

	err = bootCustomizer.AddKernelCommandLine(string(kernelExtraArguments))
	if err != nil {
		return err
	}

	err = bootCustomizer.WriteToFile(imageChroot)
	if err != nil {
		return err
	}

	return nil
}

func handleSELinux(selinuxMode imagecustomizerapi.SELinuxMode, resetBootLoaderType imagecustomizerapi.ResetBootLoaderType,
	imageChroot *safechroot.Chroot,
) (imagecustomizerapi.SELinuxMode, error) {
	var err error

	bootCustomizer, err := NewBootCustomizer(imageChroot)
	if err != nil {
		return selinuxMode, err
	}

	currentSELinuxMode, err := bootCustomizer.GetSELinuxMode(imageChroot)
	if err != nil {
		return selinuxMode, fmt.Errorf("failed to get current SELinux mode:\n%w", err)
	}

	if selinuxMode == imagecustomizerapi.SELinuxModeDefault || selinuxMode == currentSELinuxMode {
		// Don't need to change the configured SELinux mode.
		return currentSELinuxMode, nil
	}

	logger.Log.Infof("Configuring SELinux mode")

	switch resetBootLoaderType {
	case imagecustomizerapi.ResetBootLoaderTypeHard:
		// The grub.cfg file has been recreated from scratch and therefore the SELinux args will already be correct and
		// don't need to be updated.

	default:
		// Update the SELinux kernel command-line args.
		err := bootCustomizer.UpdateSELinuxCommandLine(selinuxMode)
		if err != nil {
			return selinuxMode, err
		}

		err = bootCustomizer.WriteToFile(imageChroot)
		if err != nil {
			return selinuxMode, err
		}
	}

	if selinuxMode != imagecustomizerapi.SELinuxModeDisabled {
		err = updateSELinuxModeInConfigFile(selinuxMode, imageChroot)
		if err != nil {
			return selinuxMode, err
		}
	}

	return selinuxMode, nil
}

func updateSELinuxModeInConfigFile(selinuxMode imagecustomizerapi.SELinuxMode, imageChroot *safechroot.Chroot) error {
	if selinuxMode == imagecustomizerapi.SELinuxModeDisabled {
		// SELinux is disabled in the kernel command line.
		// So, no need to update the SELinux config file.
		return nil
	}

	imagerSELinuxMode, err := selinuxModeToImager(selinuxMode)
	if err != nil {
		return err
	}

	// Ensure an SELinux policy has been installed.
	// Typically, this is provided by the 'selinux-policy' package.
	selinuxConfigFileFullPath := filepath.Join(imageChroot.RootDir(), installutils.SELinuxConfigFile)
	selinuxConfigFileExists, err := file.PathExists(selinuxConfigFileFullPath)
	if err != nil {
		return fmt.Errorf("failed to check if (%s) file exists:\n%w", installutils.SELinuxConfigFile, err)
	}

	if !selinuxConfigFileExists {
		return fmt.Errorf("SELinux is enabled but the (%s) file is missing:\n"+
			"please ensure an SELinux policy is installed:\n"+
			"the '%s' package provides the default policy",
			installutils.SELinuxConfigFile, configuration.SELinuxPolicyDefault)
	}

	err = installutils.SELinuxUpdateConfig(imagerSELinuxMode, imageChroot)
	if err != nil {
		return fmt.Errorf("failed to set SELinux mode in config file:\n%w", err)
	}

	return nil
}

func selinuxSetFiles(selinuxMode imagecustomizerapi.SELinuxMode, imageChroot *safechroot.Chroot) error {
	if selinuxMode == imagecustomizerapi.SELinuxModeDisabled {
		// SELinux is disabled in the kernel command line.
		// So, no need to call setfiles.
		return nil
	}

	logger.Log.Infof("Setting file SELinux labels")

	// Get the list of mount points.
	mountPointToFsTypeMap := make(map[string]string, 0)
	for _, mountPoint := range getNonSpecialChrootMountPoints(imageChroot) {
		mountPointToFsTypeMap[mountPoint.GetTarget()] = mountPoint.GetFSType()
	}

	// Set the SELinux config file and relabel all the files.
	err := installutils.SELinuxRelabelFiles(imageChroot, mountPointToFsTypeMap, false)
	if err != nil {
		return fmt.Errorf("failed to set SELinux file labels:\n%w", err)
	}

	return nil
}

func getNonSpecialChrootMountPoints(imageChroot *safechroot.Chroot) []*safechroot.MountPoint {
	return sliceutils.FindMatches(imageChroot.GetMountPoints(),
		func(mountPoint *safechroot.MountPoint) bool {
			switch mountPoint.GetTarget() {
			case "/dev", "/proc", "/sys", "/run", "/dev/pts":
				// Skip special directories.
				return false

			default:
				return true
			}
		},
	)
}
