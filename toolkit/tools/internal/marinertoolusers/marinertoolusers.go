// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Defines functions for getting the mariner builder user, and changing ownership of files and directories to the user.
// The file change functions are defined here since they are used in the logging package and will create circular dependencies
// in the file package if defined there.
package marinertoolusers

import (
	"fmt"
	"io/fs"
	"os"
	"os/user"
	"path/filepath"
	"strconv"
)

const userEnvName = "MARINER_BUILDER_USER"

// GetMarinerBuildUser will return the mariner builder user if set, otherwise will return nil
func GetMarinerBuildUser() (marinerBuilderUser *user.User) {
	marinerBuilderUser = nil
	userName := os.Getenv(userEnvName)
	if userName != "" {
		builderUser, err := user.Lookup(userName)
		if err == nil {
			marinerBuilderUser = builderUser
		}
	}
	return
}

// GiveSinglePathToMarinerUser will change ownership of a file or directory to the calling user (MARINER_BUILDER_USER) instead of root, if
// the user is set. Otherwise will do nothing.
func GiveSinglePathToUser(path string, user *user.User) (err error) {
	if user != nil {
		var uid, gid int
		uid, err = convertUserUIDInt(user)
		if err != nil {
			err = fmt.Errorf("unable to change ownership of path '%s':\n%w", path, err)
			return
		}
		gid, err = convertUserGIDInt(user)
		if err != nil {
			err = fmt.Errorf("unable to change ownership of path '%s':\n%w", path, err)
			return
		}
		err = os.Chown(path, uid, gid)
		if err != nil {
			err = fmt.Errorf("unable to change ownership of path '%s':\n%w", path, err)
		}
	}
	return
}

// GiveDirToUserRecursive will change ownership of a directory to the calling user (MARINER_BUILDER_USER) instead of root, if
// the user is set. Otherwise will do nothing.
func GiveDirToUserRecursive(path string, user *user.User) (err error) {
	// Walk the directory and change ownership of all files and directories
	err = filepath.WalkDir(path, func(path string, info fs.DirEntry, err error) error {
		if err != nil {
			return err
		}
		return GiveSinglePathToUser(path, user)
	})

	if err != nil {
		err = fmt.Errorf("unable to recursively change ownership of directory '%s':\n%w", path, err)
	}
	return
}

// Get the mariner builder UID
func convertUserUIDInt(user *user.User) (uid int, err error) {
	if user == nil {
		err = fmt.Errorf("user is nil")
		return
	}
	uid, err = strconv.Atoi(user.Uid)
	if err != nil {
		err = fmt.Errorf("unable to convert UID to int:\n%w", err)
	}
	return
}

// Get the mariner builder GID
func convertUserGIDInt(user *user.User) (gid int, err error) {
	if user == nil {
		err = fmt.Errorf("user is nil")
		return
	}
	gid, err = strconv.Atoi(user.Gid)
	if err != nil {
		err = fmt.Errorf("unable to convert GID to int:\n%w", err)
	}
	return
}
