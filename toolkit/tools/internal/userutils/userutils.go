// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package userutils

import (
	"fmt"
	"path/filepath"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/randomization"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

const (
	RootUser          = "root"
	RootHomeDir       = "/root"
	UserHomeDirPrefix = "/home"
)

func HashPassword(password string) (string, error) {
	const postfixLength = 12

	salt, err := randomization.RandomString(postfixLength, randomization.LegalCharactersAlphaNum)
	if err != nil {
		return "", fmt.Errorf("failed to generate salt for hashed password:\n%w", err)
	}

	// Generate hashed password based on salt value provided.
	// -6 option indicates to use the SHA256/SHA512 algorithm
	stdout, _, err := shell.Execute("openssl", "passwd", "-6", "-salt", salt, password)
	if err != nil {
		return "", fmt.Errorf("failed to generate hashed password:\n%w", err)
	}

	hashedPassword := strings.TrimSpace(stdout)
	return hashedPassword, nil
}

func UserExists(username string, installChroot *safechroot.Chroot) (bool, error) {
	var userExists bool
	err := installChroot.UnsafeRun(func() error {
		_, stderr, err := shell.Execute("id", "-u", username)
		if err != nil {
			if !strings.Contains(stderr, "no such user") {
				return fmt.Errorf("failed to check if user exists (%s):\n%w", username, err)
			}

			userExists = false
		} else {
			userExists = true
		}

		return nil
	})
	if err != nil {
		return false, err
	}

	return userExists, nil
}

func AddUser(username string, hashedPassword string, uid string, installChroot *safechroot.Chroot) error {
	var args = []string{username, "-m", "-p", hashedPassword}
	if uid != "" {
		args = append(args, "-u", uid)
	}

	err := installChroot.UnsafeRun(func() error {
		return shell.ExecuteLive(false /*squashErrors*/, "useradd", args...)
	})
	if err != nil {
		return fmt.Errorf("failed to add user (%s):\n%w", username, err)
	}

	return nil
}

func UserHomeDirectory(username string) string {
	if username == RootUser {
		return RootHomeDir
	} else {
		return filepath.Join(UserHomeDirPrefix, username)
	}
}

// NameIsValid returns an error if the User name is empty
func NameIsValid(name string) (err error) {
	if strings.TrimSpace(name) == "" {
		return fmt.Errorf("invalid value for name (%s), name cannot be empty", name)
	}
	return
}

// UIDIsValid returns an error if the UID is outside bounds
// UIDs 1-999 are system users and 1000-60000 are normal users
// Bounds can be checked using:
// $grep -E '^UID_MIN|^UID_MAX' /etc/login.defs
func UIDIsValid(uid int) error {
	const (
		uidLowerBound = 0 // root user
		uidUpperBound = 60000
	)

	if uid < uidLowerBound || uid > uidUpperBound {
		return fmt.Errorf("invalid value for UID (%d), not within [%d, %d]", uid, uidLowerBound, uidUpperBound)
	}

	return nil
}

// PasswordExpiresDaysISValid returns an error if the expire days is not
// within bounds set by the chage -M command
func PasswordExpiresDaysIsValid(passwordExpiresDays int64) error {
	const (
		noExpiration    = -1 //no expiration
		upperBoundChage = 99999
	)
	if passwordExpiresDays < noExpiration || passwordExpiresDays > upperBoundChage {
		return fmt.Errorf("invalid value for PasswordExpiresDays (%d), not within [%d, %d]", passwordExpiresDays, noExpiration, upperBoundChage)
	}
	return nil
}
