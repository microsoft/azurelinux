// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.
package marineruser

import (
	"os"
	"os/user"
	"strconv"
)

const userEnvName = "MARINER_BUILDER_USER"

var marinerBuilderUser *MarinerBuilderUser

type MarinerBuilderUser struct {
	user *user.User
}

func GetUser() *MarinerBuilderUser {
	if marinerBuilderUser == nil {
		getMarinerBuilderUser()
	}
	return marinerBuilderUser
}

// Optionally set a user if present in the environment
func getMarinerBuilderUser() {
	userName := os.Getenv(userEnvName)
	if userName != "" {
		userName, err := user.Lookup(userName)
		if err == nil {
			marinerBuilderUser = &MarinerBuilderUser{user: userName}
		}
	} else {
		marinerBuilderUser = nil
	}
}

// Get the mariner builder user
func (m *MarinerBuilderUser) GetMarinerBuilderUser() string {
	if m.user != nil {
		return m.user.Username
	}
	return ""
}

// Get the mariner builder UID
func (m *MarinerBuilderUser) GetMarinerBuilderUID() int {
	if m.user != nil {
		uid, err := strconv.Atoi(m.user.Uid)
		if err != nil {
			return -1
		}
		return uid
	}
	return -1
}

// Get the mariner builder GID
func (m *MarinerBuilderUser) GetMarinerBuilderGID() int {
	if m.user != nil {
		gid, err := strconv.Atoi(m.user.Gid)
		if err != nil {
			return -1
		}
		return gid
	}
	return -1
}

// GiveFileToMarinerUser will change ownership of a file to the calling user (MARINER_BUILDER_USER) instead of root, if
// the user is set. Otherwise will do nothing.
func GiveFileToMarinerUser(path string) (err error) {
	if GetUser() != nil {
		err = os.Chown(path, GetUser().GetMarinerBuilderUID(), GetUser().GetMarinerBuilderGID())
		if err != nil {
			return
		}
	}
	return
}
