// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's Users configuration schema.

package configuration

import (
	"encoding/json"
	"fmt"
	"strconv"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/userutils"
)

type User struct {
	Name                string   `json:"Name"`
	UID                 string   `json:"UID"`
	PasswordHashed      bool     `json:"PasswordHashed"`
	Password            string   `json:"Password"`
	PasswordExpiresDays int64    `json:"PasswordExpiresDays"`
	SSHPubKeyPaths      []string `json:"SSHPubKeyPaths"`
	SSHPubKeys          []string `json:"SSHPubKeys"`
	PrimaryGroup        string   `json:"PrimaryGroup"`
	SecondaryGroups     []string `json:"SecondaryGroups"`
	StartupCommand      string   `json:"StartupCommand"`
}

// UnmarshalJSON Unmarshals a User entry
func (u *User) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypeUser User
	err = json.Unmarshal(b, (*IntermediateTypeUser)(u))
	if err != nil {
		return fmt.Errorf("failed to parse [User]: %w", err)
	}

	// Now validate the resulting unmarshaled object
	err = u.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [User]: %w", err)
	}
	return
}

// IsValid returns an error if the User struct is not valid
func (p *User) IsValid() (err error) {
	err = p.NameIsValid()
	if err != nil {
		return
	}
	err = p.UIDIsValid()
	if err != nil {
		return
	}
	err = p.PasswordExpiresDaysIsValid()
	if err != nil {
		return
	}
	return
}

// NameIsValid returns an error if the User name is empty
func (p *User) NameIsValid() (err error) {
	return userutils.NameIsValid(p.Name)
}

// UIDIsValid returns an error if the UID is outside bounds.
func (p *User) UIDIsValid() (err error) {
	if strings.TrimSpace(p.UID) != "" {
		uidNum, err := strconv.Atoi(p.UID)
		if err != nil {
			return fmt.Errorf("failed to convert UID (%s) to a number", p.UID)
		}

		err = userutils.UIDIsValid(uidNum)
		if err != nil {
			return err
		}
	}
	return
}

// PasswordExpiresDaysISValid returns an error if the expire days is not
// within bounds set by the chage -M command
func (p *User) PasswordExpiresDaysIsValid() (err error) {
	return userutils.PasswordExpiresDaysIsValid(p.PasswordExpiresDays)
}
