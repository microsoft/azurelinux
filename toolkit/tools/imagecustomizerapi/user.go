// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/userutils"
)

type User struct {
	Name                string    `yaml:"name"`
	UID                 *int      `yaml:"uid"`
	Password            *Password `yaml:"password"`
	PasswordExpiresDays *int64    `yaml:"passwordExpiresDays"`
	SSHPublicKeyPaths   []string  `yaml:"sshPublicKeyPaths"`
	SSHPublicKeys       []string  `yaml:"sshPublicKeys"`
	PrimaryGroup        string    `yaml:"primaryGroup"`
	SecondaryGroups     []string  `yaml:"secondaryGroups"`
	StartupCommand      string    `yaml:"startupCommand"`
	HomeDirectory       string    `yaml:"homeDirectory"`
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

	if u.Password != nil {
		err := u.Password.IsValid()
		if err != nil {
			return fmt.Errorf("user (%s) is invalid:\n%w", u.Name, err)
		}
	}

	if u.PasswordExpiresDays != nil {
		err := userutils.PasswordExpiresDaysIsValid(*u.PasswordExpiresDays)
		if err != nil {
			return fmt.Errorf("user (%s) is invalid:\n%w", u.Name, err)
		}
	}

	return nil
}
