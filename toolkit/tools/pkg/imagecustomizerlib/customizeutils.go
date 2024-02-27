// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"bufio"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerapi"
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

func copyAdditionalFiles(baseConfigPath string, additionalFiles map[string]imagecustomizerapi.FileConfigList, imageChroot *safechroot.Chroot) error {
	for sourceFile, fileConfigs := range additionalFiles {
		for _, fileConfig := range fileConfigs {
			logger.Log.Infof("Copying: %s", fileConfig.Path)

			fileToCopy := safechroot.FileToCopy{
				Src:         filepath.Join(baseConfigPath, sourceFile),
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

func loadOrDisableModules(modules []imagecustomizerapi.Module, imageChroot *safechroot.Chroot) error {
	var err error
	var modulesToLoad []string
	var modulesToDisable []string
	var moduleOptionsUpdates map[string]map[string]string = make(map[string]map[string]string)
	moduleDisableFilePath := filepath.Join(imageChroot.RootDir(), "/etc/modprobe.d/modules-disabled.conf")
	moduleLoadFilePath := filepath.Join(imageChroot.RootDir(), "/etc/modules-load.d/modules-load.conf")
	moduleOptionsFilePath := filepath.Join(imageChroot.RootDir(), "/etc/modprobe.d/module-options.conf")

	for i, module := range modules {
		switch module.LoadMode {
		case "boot":
			// If a module is disabled, remove it. Add the module to modules-load.d/. Write options if provided.
			err = removeModuleFromDisableList(module.Name, moduleDisableFilePath)
			if err != nil {
				logger.Log.Infof("Error removing module %s from the disabled list", module.Name)
				return err
			}
			modulesToLoad = append(modulesToLoad, module.Name)

			if len(module.Options) > 0 {
				moduleOptionsUpdates[module.Name] = module.Options
			}

		case "auto":
			// If a module is disabled, enable it. Write options if provided
			err = removeModuleFromDisableList(module.Name, moduleDisableFilePath)
			if err != nil {
				logger.Log.Infof("Error removing module %s from the disabled list", module.Name)
				return err
			}

			if len(module.Options) > 0 {
				moduleOptionsUpdates[module.Name] = module.Options
			}

		case "disable":
			// Disable a module, throw error if options are provided
			if len(module.Options) > 0 {
				return fmt.Errorf("cannot add options for disabled module %s at index %d. Specify auto or boot as loadMode to override setting in base image", module.Name, i)
			}

			modulesToDisable = append(modulesToDisable, module.Name)

		case "inherit", "":
			// inherits the behavior of the base image, modify the options without changing the loading state
			if len(module.Options) > 0 {
				disabled, err := isModuleDisabled(module.Name, moduleDisableFilePath)
				if err != nil {
					logger.Log.Infof("Error checking %s", moduleDisableFilePath)
					return err
				}

				if disabled {
					return fmt.Errorf("cannot add options for disabled module %s at index %d. Specify auto or boot as loadMode to override setting in base image", module.Name, i)
				}

				if len(module.Options) > 0 {
					moduleOptionsUpdates[module.Name] = module.Options
				}
			}
		}
	}

	// Batch process module to load
	err = ensureModulesLoaded(modulesToLoad, moduleLoadFilePath)
	if err != nil {
		return err
	}

	// Batch process module to disable
	err = ensureModulesDisabled(modulesToDisable, moduleLoadFilePath)
	if err != nil {
		return err
	}

	// Batch process module options
	aggregatedOptions := []string{}
	if len(moduleOptionsUpdates) > 0 {
		for moduleName, options := range moduleOptionsUpdates {
			for key, value := range options {
				logger.Log.Infof("Writing module options %s=%s for module %s", key, value, moduleName)
				aggregatedOptions, err = aggregateModuleOptions(aggregatedOptions, moduleOptionsFilePath, moduleName, key, value)
				if err != nil {
					return fmt.Errorf("failed to append module option for module %s: %w", moduleName, err)
				}
			}
		}

		file, err := os.OpenFile(moduleOptionsFilePath, os.O_WRONLY|os.O_CREATE|os.O_APPEND, 0644)
		if err != nil {
			return fmt.Errorf("failed to open %s: %w", moduleOptionsFilePath, err)
		}
		defer file.Close()

		content := strings.Join(aggregatedOptions, "\n") + "\n"
		// Append the content to the file.
		if _, err := file.WriteString(content); err != nil {
			return fmt.Errorf("failed to write module options to %s: %w", moduleOptionsFilePath, err)
		}
	}

	return nil
}

func ensureModulesLoaded(moduleNames []string, moduleLoadFilePath string) error {
    content, err := os.ReadFile(moduleLoadFilePath)
    if err != nil {
        if !os.IsNotExist(err) {
            return fmt.Errorf("failed to read module load configuration: %w", err)
        }
        // If the file does not exist, initialize content as empty
        content = []byte{}
    }

    needUpdate := false

	for _, moduleName := range moduleNames {
		if !strings.Contains(string(content), moduleName+"\n") {
			content = append(content, (moduleName + "\n")...)
			needUpdate = true
			logger.Log.Infof("Loading module %s", moduleName)
		} else {
			logger.Log.Infof("Module %s is already loaded", moduleName)
		}
	}

	if needUpdate {
		err = os.WriteFile(moduleLoadFilePath, content, 0644)
		if err != nil {
			return fmt.Errorf("failed to update module load configuration: %w", err)
		}
	}
    return nil
}

func ensureModulesDisabled(moduleNames []string, moduleDisableFilePath string) error {
    content, err := os.ReadFile(moduleDisableFilePath)
    if err != nil {
        if !os.IsNotExist(err) {
            return fmt.Errorf("failed to read disable configuration: %w", err)
        }
        // If the file does not exist, initialize content as empty
        content = []byte{}
    }

    contentString := string(content)
    needUpdate := false

    for _, moduleName := range moduleNames {
        blacklistEntry := "blacklist " + moduleName
        if !strings.Contains(string(content), blacklistEntry+"\n") {
            // Module is not disabled, append it
            contentString += blacklistEntry + "\n"
            needUpdate = true
            logger.Log.Infof("Disabling module %s", moduleName)
        } else {
			logger.Log.Infof("Module %s is already disabled\n", moduleName)
		}
    }

    if needUpdate {
        err = os.WriteFile(moduleDisableFilePath, []byte(contentString), 0644)
        if err != nil {
            return fmt.Errorf("failed to update disable configuration: %w", err)
        }
    }

    return nil
}

func isModuleDisabled(moduleName, moduleDisableFilePath string) (bool, error) {
	_, err := os.Stat(moduleDisableFilePath)
	if os.IsNotExist(err) {
		// File doesn't exist, treat as not disabled.
		return false, nil
	} else if err != nil {
		return false, err
	}

	file, err := os.Open(moduleDisableFilePath)
	if err != nil {
		return false, err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		if strings.TrimSpace(scanner.Text()) == moduleName {
			return true, nil
		}
	}

	if err := scanner.Err(); err != nil {
		logger.Log.Errorf("Failed to scan file %s with error %s", moduleDisableFilePath, err)
		return false, err
	}

	return false, nil
}

func removeModuleFromDisableList(moduleName, moduleDisableFilePath string) error {
	disabled, err := isModuleDisabled(moduleName, moduleDisableFilePath)
	if err != nil {
		logger.Log.Infof("Error checking %s", moduleDisableFilePath)
		return err
	}

	if disabled {
		logger.Log.Infof("Module %s found in the disabled list. Removing...", moduleName)
		lines, err := os.ReadFile(moduleDisableFilePath)
		if err != nil {
			return err
		}

		// Filter out the line that contains the module name.
		var updatedLines []string
		for _, line := range strings.Split(string(lines), "\n") {
			if !strings.Contains(line, moduleName) {
				updatedLines = append(updatedLines, line)
			}
		}

		return os.WriteFile(moduleDisableFilePath, []byte(strings.Join(updatedLines, "\n")), 0644)
	}

	return nil
}


func aggregateModuleOptions(aggregatedOptions []string, moduleOptionsFilePath string, moduleName string, optionKey string, optionValue string) ([]string, error) {
    found := false

    if _, err := os.Stat(moduleOptionsFilePath); err != nil {
        if os.IsNotExist(err) {
            // If the file does not exist, append the new option and return the options
            return append(aggregatedOptions, fmt.Sprintf("options %s %s=%s", moduleName, optionKey, optionValue)), nil
        }
        return nil, err
    }

    // File exists, if the option exists in the file, directly update the file, otherwise, append it and return the options
    file, err := os.Open(moduleOptionsFilePath)
    if err != nil {
        return nil, err
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
		var updatedLines []string
        line := scanner.Text()
        if strings.HasPrefix(line, "options "+moduleName) {
            fields := strings.Fields(line)
            updatedLine := fields[:1]
            for _, field := range fields[1:] {
                if strings.HasPrefix(field, optionKey+"=") {
                    // Update the existing option value
                    updatedLine = append(updatedLine, optionKey+"="+optionValue)
                } else {
                    // Keep other options as they are
                    updatedLine = append(updatedLine, field)
                }
            }
            line = strings.Join(updatedLine, " ")
            found = true
        }
        updatedLines = append(updatedLines, line)
		// Directly write back to file as this is updating existing option
		os.WriteFile(moduleOptionsFilePath, []byte(strings.Join(updatedLines, "\n")), 0644)
    }

    if err := scanner.Err(); err != nil {
        return nil, err
    }

    if !found {
        // If not found, append this new option
        aggregatedOptions = append(aggregatedOptions, fmt.Sprintf("options %s %s=%s", moduleName, optionKey, optionValue))
    }

    return aggregatedOptions, nil
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
