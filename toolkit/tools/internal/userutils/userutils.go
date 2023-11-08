// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package userutils

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/randomization"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

const (
	RootUser          = "root"
	RootHomeDir       = "/root"
	UserHomeDirPrefix = "/home"

	ShadowFile = "/etc/shadow"
)

func HashPassword(password string) (string, error) {
	const postfixLength = 12

	if password == "" {
		return "", nil
	}

	salt, err := randomization.RandomString(postfixLength, randomization.LegalCharactersAlphaNum)
	if err != nil {
		return "", fmt.Errorf("failed to generate salt for hashed password:\n%w", err)
	}

	// Generate hashed password based on salt value provided.
	// -6 option indicates to use the SHA256/SHA512 algorithm
	stdout, _, err := shell.ExecuteWithStdin(password, "openssl", "passwd", "-6", "-salt", salt, "-stdin")
	if err != nil {
		return "", fmt.Errorf("failed to generate hashed password:\n%w", err)
	}

	hashedPassword := strings.TrimSpace(stdout)
	return hashedPassword, nil
}

func UserExists(username string, installChroot *safechroot.Chroot) (bool, error) {
	if installChroot == nil {
		return userExistsCore(username)
	}

	var userExists bool
	err := installChroot.UnsafeRun(func() error {
		exists, err := userExistsCore(username)
		userExists = exists
		return err
	})

	if err != nil {
		return false, err
	}
	return userExists, nil
}

func userExistsCore(username string) (bool, error) {
	_, stderr, err := shell.Execute("id", "-u", username)
	if err != nil {
		if strings.Contains(stderr, "no such user") {
			return false, nil
		}
		return false, fmt.Errorf("failed to check if user exists (%s):\n%w", username, err)
	}
	return true, nil
}

func AddUser(username string, hashedPassword string, uid string, installChroot *safechroot.Chroot) error {
	var execFunc func() error
	if installChroot != nil {
		execFunc = func() error {
			return installChroot.UnsafeRun(func() error {
				return addUserCore(username, hashedPassword, uid)
			})
		}
	} else {
		execFunc = func() error {
			return addUserCore(username, hashedPassword, uid)
		}
	}

	if err := execFunc(); err != nil {
		return fmt.Errorf("failed to add user (%s):\n%w", username, err)
	}

	return nil
}

func addUserCore(username, hashedPassword, uid string) error {
	var args = []string{username, "-m"}
	if hashedPassword != "" {
		args = append(args, "-p", hashedPassword)
	}
	if uid != "" {
		args = append(args, "-u", uid)
	}

	return shell.ExecuteLive(false, "useradd", args...)
}

func UpdateUserPassword(installRoot, username, hashedPassword string) error {
	shadowFilePath := filepath.Join(installRoot, ShadowFile)

	if hashedPassword == "" {
		// In the /etc/shadow file, the values `*` and `!` both mean the user's password login is disabled but the user
		// may login using other means (e.g. ssh, auto-login, etc.). This interpretation is also used by PAM. When sshd
		// has `UsePAM` set to `yes`, then sshd defers to PAM the decision on whether or not the user is disabled.
		// However, when `UsePAM` is set to `no`, then sshd must make this interpretation for itself. And the Mariner
		// build of sshd is configured to interpret the `!` in the shadow file to mean the user is fully disabled, even
		// for ssh login. But it interprets `*` to mean that only password login is disabled but sshd public/private key
		// login is fine.
		hashedPassword = "*"
	}

	// Find the line that starts with "<user>:<password>:..."
	findUserEntry, err := regexp.Compile(fmt.Sprintf("(?m)^%s:[^:]*:", regexp.QuoteMeta(username)))
	if err != nil {
		return fmt.Errorf("failed to compile user (%s) password update regex:\n%w", username, err)
	}

	// Read in existing /etc/shadow file.
	shadowFileBytes, err := os.ReadFile(shadowFilePath)
	if err != nil {
		return fmt.Errorf("failed to read shadow file (%s) to update user's (%s) password:\n%w", shadowFilePath, username, err)
	}

	shadowFile := string(shadowFileBytes)

	// Try to find the user's entry.
	entryIndexes := findUserEntry.FindStringIndex(shadowFile)
	if entryIndexes == nil {
		return fmt.Errorf("failed to find user (%s) in shadow file (%s)", username, shadowFilePath)
	}

	newShadowFile := fmt.Sprintf("%s%s:%s:%s", shadowFile[:entryIndexes[0]], username, hashedPassword, shadowFile[entryIndexes[1]:])

	// Write new /etc/shadow file.
	err = file.Write(newShadowFile, shadowFilePath)
	if err != nil {
		return fmt.Errorf("failed to write new shadow file (%s) to update user's (%s) password:\n%w", shadowFilePath, username, err)
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
