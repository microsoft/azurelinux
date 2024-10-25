// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"time"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
)

func doOsCustomizations(buildDir string, baseConfigPath string, config *imagecustomizerapi.Config,
	imageConnection *ImageConnection, rpmsSources []string, useBaseImageRpmRepos bool, partitionsCustomized bool,
	imageUuid string) error {
	var err error

	imageChroot := imageConnection.Chroot()

	buildTime := time.Now().Format("2006-01-02T15:04:05Z")

	resolvConf, err := overrideResolvConf(imageChroot)
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

	err = addCustomizerRelease(imageChroot, ToolVersion, buildTime, imageUuid)
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

	overlayUpdated, err := enableOverlays(config.OS.Overlays, selinuxMode, imageChroot)
	if err != nil {
		return err
	}

	verityUpdated, err := enableVerityPartition(config.OS.Verity, imageChroot)
	if err != nil {
		return err
	}

	if partitionsCustomized || overlayUpdated || verityUpdated {
		err = regenerateInitrd(imageChroot)
		if err != nil {
			return err
		}
	}

	err = runUserScripts(baseConfigPath, config.Scripts.PostCustomization, "postCustomization", imageChroot)
	if err != nil {
		return err
	}

	err = restoreResolvConf(resolvConf, imageChroot)
	if err != nil {
		return err
	}

	err = selinuxSetFiles(selinuxMode, imageChroot)
	if err != nil {
		return err
	}

	err = runUserScripts(baseConfigPath, config.Scripts.FinalizeCustomization, "finalizeCustomization", imageChroot)
	if err != nil {
		return err
	}

	err = checkForInstalledKernel(imageChroot)
	if err != nil {
		return err
	}

	return nil
}
