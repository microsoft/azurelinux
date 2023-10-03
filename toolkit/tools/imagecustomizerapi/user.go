// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type User struct {
	Name                string   `json:"Name"`
	UID                 string   `json:"UID"`
	PasswordHashed      bool     `json:"PasswordHashed"`
	Password            string   `json:"Password"`
	PasswordPath        string   `json:"PasswordPath"`
	PasswordExpiresDays int64    `json:"PasswordExpiresDays"`
	SSHPubKeyPaths      []string `json:"SSHPubKeyPaths"`
	PrimaryGroup        string   `json:"PrimaryGroup"`
	SecondaryGroups     []string `json:"SecondaryGroups"`
	StartupCommand      string   `json:"StartupCommand"`
}

func (u *User) IsValid() error {
	if u.Password != "" && u.PasswordPath != "" {
		return fmt.Errorf("fields Password and PasswordPath must not both be specified")
	}

	return nil
}
