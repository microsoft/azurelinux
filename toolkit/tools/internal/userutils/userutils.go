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
