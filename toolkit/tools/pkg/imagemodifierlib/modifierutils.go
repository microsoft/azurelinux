// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagemodifierlib

import (
	"strconv"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagecustomizerapi"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/imagegen/installutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/userutils"
)

func doModifications(baseConfigPath string, config *imagecustomizerapi.Config) error {
	err := addOrUpdateUsers(config.SystemConfig.Users, baseConfigPath)
	if err != nil {
		return err
	}

	return nil
}

func addOrUpdateUsers(users []imagecustomizerapi.User, baseConfigPath string) error {
	for _, user := range users {
		err := addOrUpdateUser(user, baseConfigPath)
		if err != nil {
			return err
		}
	}

	return nil
}

func addOrUpdateUser(user imagecustomizerapi.User, baseConfigPath string) error {
	var err error
	logger.Log.Infof("Adding/updating user (%s)", user.Name)

	password := user.Password

	// Hash the password.
	hashedPassword := password
	if !user.PasswordHashed {
		hashedPassword, err = userutils.HashPassword(password)
		if err != nil {
			return err
		}
	}

	// Check if the user already exists.
	userExists, err := userutils.UserExists(user.Name, nil)
	if err != nil {
		return err
	}

	if userExists {
		// Update the user's password.
		err = userutils.UpdateUserPassword("", user.Name, hashedPassword)
		if err != nil {
			return err
		}
	} else {
		var uidStr string
		if user.UID != nil {
			uidStr = strconv.Itoa(*user.UID)
		}

		// Add the user.
		err = userutils.AddUser(user.Name, hashedPassword, uidStr, nil)
		if err != nil {
			return err
		}
	}

	// TODO: update Chage to allow empty chroot to set user's password expiry.
	// if user.PasswordExpiresDays != nil {
	// 	err = installutils.Chage(nil, *user.PasswordExpiresDays, user.Name)
	// 	if err != nil {
	// 		return err
	// 	}
	// }

	// Set user's groups.
	err = installutils.ConfigureUserGroupMembership(nil, user.Name, user.PrimaryGroup, user.SecondaryGroups)
	if err != nil {
		return err
	}

	// Set user's SSH keys.
	err = installutils.ProvisionUserSSHCertsWithPubKeys(user.Name, user.SSHPubKeys)
	if err != nil {
		return err
	}

	// TODO: update ConfigureUserStartupCommand to allow empty chroot to set user's startup command.
	// err = installutils.ConfigureUserStartupCommand(nil, user.Name, user.StartupCommand)
	// if err != nil {
	// 	return err
	// }

	return nil
}
