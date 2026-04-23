// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"fmt"
	"os"
	"strconv"

	"github.com/microsoft/azurelinux/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/azurelinux/toolkit/tools/imagegen/installutils"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/userutils"
)

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
	// Check if the user already exists.
	userExists, err := userutils.UserExists(user.Name, imageChroot)
	if err != nil {
		return err
	}

	if userExists {
		logger.Log.Infof("Updating user (%s)", user.Name)
	} else {
		logger.Log.Infof("Adding user (%s)", user.Name)
	}

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

	if userExists {
		if user.UID != nil {
			return fmt.Errorf("cannot set UID (%d) on a user (%s) that already exists", *user.UID, user.Name)
		}

		if user.HomeDirectory != "" {
			return fmt.Errorf("cannot set home directory (%s) on a user (%s) that already exists",
				user.HomeDirectory, user.Name)
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
		err = userutils.AddUser(user.Name, user.HomeDirectory, user.PrimaryGroup, hashedPassword, uidStr, imageChroot)
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

	// Update an existing user's primary group. A new user's primary group will have already been set by AddUser().
	if userExists {
		err = installutils.ConfigureUserPrimaryGroupMembership(imageChroot, user.Name, user.PrimaryGroup)
		if err != nil {
			return err
		}
	}
	// Set user's secondary groups.
	err = installutils.ConfigureUserSecondaryGroupMembership(imageChroot, user.Name, user.SecondaryGroups)
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

	// Set user's sudo access.
	err = UpdateSudoAccess(imageChroot, user.Name, user.Sudo)
	if err != nil {
		return err
	}

	return nil
}

func UpdateSudoAccess(installChroot safechroot.ChrootInterface, username string, enableSudo bool) error {
	if enableSudo {

		// Define the sudo configuration file path for the user
		sudoersFile := fmt.Sprintf("/etc/sudoers.d/%s", username)

		// Content for sudo configuration
		content := fmt.Sprintf("%s ALL=(ALL) NOPASSWD:ALL", username)

		// Permissions for the sudoers file (read-only for root)
		permissions := imagecustomizerapi.FilePermissions(0440)

		// Create the AdditionalFile object
		additionalFiles := imagecustomizerapi.AdditionalFileList{
			imagecustomizerapi.AdditionalFile{
				Destination: fmt.Sprintf("/etc/sudoers.d/%s", username),
				Content:     &content,
				Permissions: &permissions,
			},
		}

		err := CopyAdditionalFiles(sudoersFile, additionalFiles, installChroot)
		if err != nil {
			return err
		}
	}
	return nil
}
