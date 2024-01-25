// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/userutils"
)

type User struct {
	Name                string   `yaml:"name"`
	UID                 *int     `yaml:"UID"`
	PasswordHashed      bool     `yaml:"passwordHashed"`
	Password            string   `yaml:"password"`
	PasswordPath        string   `yaml:"passwordPath"`
	PasswordExpiresDays *int64   `yaml:"passwordExpiresDays"`
	SSHPubKeyPaths      []string `yaml:"sshPubKeyPaths"`
	SSHPubKeys          []string `yaml:"SSHPubKeys"`
	PrimaryGroup        string   `yaml:"primaryGroup"`
	SecondaryGroups     []string `yaml:"secondaryGroups"`
	StartupCommand      string   `yaml:"startupCommand"`
}

func (u *User) IsValid() error {
	err := userutils.NameIsValid(u.Name)
	if err != nil {
		return fmt.Errorf("user (%s) is invalid:\n%w", u.Name, err)
	}

	if u.UID != nil {
		err := userutils.UIDIsValid(*u.UID)
		if err != nil {
			return fmt.Errorf("user (%s) is invalid:\n%w", u.Name, err)
		}
	}

	if u.Password != "" && u.PasswordPath != "" {
		return fmt.Errorf("user (%s) is invalid:\nfields Password and PasswordPath must not both be specified", u.Name)
	}

	if u.PasswordExpiresDays != nil {
		err := userutils.PasswordExpiresDaysIsValid(*u.PasswordExpiresDays)
		if err != nil {
			return fmt.Errorf("user (%s) is invalid:\n%w", u.Name, err)
		}
	}

	return nil
}
