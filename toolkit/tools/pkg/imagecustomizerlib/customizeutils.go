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

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/configuration"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/installutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safemount"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/userutils"
	"golang.org/x/sys/unix"
)

const (
	configDirMountPathInChroot = "/_imageconfigs"
	resolveConfPath            = "/etc/resolv.conf"
)

func doCustomizations(buildDir string, baseConfigPath string, config *imagecustomizerapi.Config,
	imageChroot *safechroot.Chroot, rpmsSources []string, useBaseImageRpmRepos bool, partitionsCustomized bool,
) error {
	var err error

	// Note: The ordering of the customization steps here should try to mirror the order of the equivalent steps in imager
	// tool as closely as possible.

	buildTime := time.Now().Format("2006-01-02T15:04:05Z")

	err = overrideResolvConf(imageChroot)
	if err != nil {
		return err
	}

	err = addRemoveAndUpdatePackages(buildDir, baseConfigPath, &config.SystemConfig, imageChroot, rpmsSources,
		useBaseImageRpmRepos, partitionsCustomized)
	if err != nil {
		return err
	}

	err = updateHostname(config.SystemConfig.Hostname, imageChroot)
	if err != nil {
		return err
	}

	err = copyAdditionalFiles(baseConfigPath, config.SystemConfig.AdditionalFiles, imageChroot)
	if err != nil {
		return err
	}

	err = AddOrUpdateUsers(config.SystemConfig.Users, baseConfigPath, imageChroot)
	if err != nil {
		return err
	}

	err = enableOrDisableServices(config.SystemConfig.Services, imageChroot)
	if err != nil {
		return err
	}

	err = loadOrDisableModules(config.SystemConfig.Modules, imageChroot)
	if err != nil {
		return err
	}

	err = addCustomizerRelease(imageChroot, ToolVersion, buildTime)
	if err != nil {
		return err
	}

	err = runScripts(baseConfigPath, config.SystemConfig.PostInstallScripts, imageChroot)
	if err != nil {
		return err
	}

	err = handleKernelCommandLine(config.SystemConfig.KernelCommandLine.ExtraCommandLine, imageChroot,
		partitionsCustomized)
	if err != nil {
		return fmt.Errorf("failed to add extra kernel command line: %w", err)
	}

	err = handleSELinux(config.SystemConfig.KernelCommandLine.SELinux, partitionsCustomized, imageChroot)
	if err != nil {
		return err
	}

	err = runScripts(baseConfigPath, config.SystemConfig.FinalizeImageScripts, imageChroot)
	if err != nil {
		return err
	}

	err = deleteResolvConf(imageChroot)
	if err != nil {
		return err
	}

	err = enableVerityPartition(config.SystemConfig.Verity, imageChroot)
	if err != nil {
		return err
	}

	return nil
}

// Override the resolv.conf file, so that in-chroot processes can access the network.
// For example, to install packages from packages.microsoft.com.
func overrideResolvConf(imageChroot *safechroot.Chroot) error {
	logger.Log.Debugf("Overriding resolv.conf file")

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
	logger.Log.Debugf("Deleting overridden resolv.conf file")

	imageResolveConfPath := filepath.Join(imageChroot.RootDir(), resolveConfPath)

	err := os.RemoveAll(imageResolveConfPath)
	if err != nil {
		return fmt.Errorf("failed to delete overridden resolv.conf file: %w", err)
	}

	return err
}

func updateHostname(hostname string, imageChroot *safechroot.Chroot) error {
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
		absSourceFile := filepath.Join(baseConfigPath, sourceFile)
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

func runScripts(baseConfigPath string, scripts []imagecustomizerapi.Script, imageChroot *safechroot.Chroot) error {
	if len(scripts) <= 0 {
		return nil
	}

	configDirMountPath := filepath.Join(imageChroot.RootDir(), configDirMountPathInChroot)

	// Bind mount the config directory so that the scripts can access any required resources.
	mount, err := safemount.NewMount(baseConfigPath, configDirMountPath, "", unix.MS_BIND|unix.MS_RDONLY, "", true)
	if err != nil {
		return err
	}
	defer mount.Close()

	for _, script := range scripts {
		scriptPathInChroot := filepath.Join(configDirMountPathInChroot, script.Path)
		command := fmt.Sprintf("%s %s", scriptPathInChroot, script.Args)
		logger.Log.Infof("Running script (%s)", script.Path)

		// Run the script.
		err = imageChroot.UnsafeRun(func() error {
			return shell.ExecuteLiveWithErr(1, shell.ShellProgram, "-c", command)
		})
		if err != nil {
			return fmt.Errorf("script (%s) failed:\n%w", script.Path, err)
		}
	}

	err = mount.CleanClose()
	if err != nil {
		return err
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

	password := user.Password
	if user.PasswordPath != "" {
		// Read password from file.
		passwordFullPath := filepath.Join(baseConfigPath, user.PasswordPath)

		passwordFileContents, err := os.ReadFile(passwordFullPath)
		if err != nil {
			return fmt.Errorf("failed to read password file (%s): %w", passwordFullPath, err)
		}

		password = string(passwordFileContents)
	}

	// Hash the password.
	hashedPassword := password
	if !user.PasswordHashed {
		hashedPassword, err = userutils.HashPassword(password)
		if err != nil {
			return err
		}
	}

	// Check if the user already exists.
	userExists, err := userutils.UserExists(user.Name, imageChroot)
	if err != nil {
		return err
	}

	if userExists {
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
	for i, _ := range user.SSHPubKeyPaths {
		// If absolute path is not provided, then append baseConfigPath.
		if !filepath.IsAbs(user.SSHPubKeyPaths[i]) {
			user.SSHPubKeyPaths[i] = filepath.Join(baseConfigPath, user.SSHPubKeyPaths[i])
		}
	}

	err = installutils.ProvisionUserSSHCerts(imageChroot, user.Name, user.SSHPubKeyPaths, user.SSHPubKeys)
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
		logger.Log.Infof("Enabling service (%s)", service.Name)

		err = imageChroot.UnsafeRun(func() error {
			return shell.ExecuteLiveWithErr(1, "systemctl", "enable", service.Name)
		})
		if err != nil {
			return fmt.Errorf("failed to enable service (%s):\n%w", service.Name, err)
		}
	}

	// Handle disabling services
	for _, service := range services.Disable {
		logger.Log.Infof("Disabling service (%s)", service.Name)

		err = imageChroot.UnsafeRun(func() error {
			return shell.ExecuteLiveWithErr(1, "systemctl", "disable", service.Name)
		})
		if err != nil {
			return fmt.Errorf("failed to disable service (%s):\n%w", service.Name, err)
		}
	}

	return nil
}

func loadOrDisableModules(modules imagecustomizerapi.Modules, imageChroot *safechroot.Chroot) error {
	var err error

	for _, module := range modules.Load {
		logger.Log.Infof("Loading kernel module (%s)", module.Name)
		moduleFileName := module.Name + ".conf"
		moduleFilePath := filepath.Join(imageChroot.RootDir(), "/etc/modules-load.d/", moduleFileName)
		err = file.Write(module.Name, moduleFilePath)
		if err != nil {
			return fmt.Errorf("failed to write module load configuration: %w", err)
		}
	}

	for _, module := range modules.Disable {
		logger.Log.Infof("Disabling kernel module (%s)", module.Name)
		moduleFileName := module.Name + ".conf"
		moduleFilePath := filepath.Join(imageChroot.RootDir(), "/etc/modprobe.d/", moduleFileName)
		data := fmt.Sprintf("blacklist %s\n", module.Name)
		err = file.Write(data, moduleFilePath)
		if err != nil {
			return fmt.Errorf("failed to write module disable configuration: %w", err)
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

func handleSELinux(selinuxMode imagecustomizerapi.SELinux, partitionsCustomized bool, imageChroot *safechroot.Chroot,
) error {
	var err error

	// Resolve the default SELinux mode.
	if selinuxMode == imagecustomizerapi.SELinuxDefault {
		selinuxMode, err = getCurrentSELinuxMode(imageChroot)
		if err != nil {
			return err
		}
	}

	// If the partitions were customized, then the grub.cfg file will have been recreated from scratch and therefore
	// the SELinux args will already be correct and don't need to be updated.
	if !partitionsCustomized {
		// Update the SELinux kernel command-line args.
		err := updateSELinuxCommandLine(selinuxMode, imageChroot)
		if err != nil {
			return fmt.Errorf("failed to update SELinux args in grub.cfg:\n%w", err)
		}
	}

	if selinuxMode != imagecustomizerapi.SELinuxDisabled {
		err = updateSELinuxMode(selinuxMode, imageChroot)
		if err != nil {
			return err
		}
	}

	return nil
}

func updateSELinuxMode(selinuxMode imagecustomizerapi.SELinux, imageChroot *safechroot.Chroot) error {
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

	// Get the list of mount points.
	mountPointToFsTypeMap := make(map[string]string, 0)
	for _, mountPoint := range imageChroot.GetMountPoints() {
		switch mountPoint.GetTarget() {
		case "/dev", "/proc", "/sys", "/run", "/dev/pts":
			// Skip special directories.
			continue
		}

		mountPointToFsTypeMap[mountPoint.GetTarget()] = mountPoint.GetFSType()
	}

	// Set the SELinux config file and relabel all the files.
	err = installutils.SELinuxConfigure(imagerSELinuxMode, imageChroot, mountPointToFsTypeMap, false)
	if err != nil {
		return err
	}

	return nil
}
