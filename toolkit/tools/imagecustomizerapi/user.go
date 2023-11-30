// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/userutils"
)

type User struct {
	Name                string   `yaml:"Name"`
	UID                 *int     `yaml:"UID"`
	PasswordHashed      bool     `yaml:"PasswordHashed"`
	Password            string   `yaml:"Password"`
	PasswordPath        string   `yaml:"PasswordPath"`
	PasswordExpiresDays *int64   `yaml:"PasswordExpiresDays"`
	SSHPubKeyPaths      []string `yaml:"SSHPubKeyPaths"`
	PrimaryGroup        string   `yaml:"PrimaryGroup"`
	SecondaryGroups     []string `yaml:"SecondaryGroups"`
	StartupCommand      string   `yaml:"StartupCommand"`
	HomeDirectory       string   `yaml:"HomeDirectory"`
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
