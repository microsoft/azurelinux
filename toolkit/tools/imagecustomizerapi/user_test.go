// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/ptrutils"
	"github.com/stretchr/testify/assert"
)

func TestUserIsValid(t *testing.T) {
	user := User{
		Name: "test",
		UID:  ptrutils.PtrTo(1000),
		Password: &Password{
			Type:  "plain-text",
			Value: "hello",
		},
		PasswordExpiresDays: ptrutils.PtrTo(int64(10)),
		SSHPublicKeyPaths: []string{
			"/home/test/.ssh/id_ed25519.pub",
		},
		PrimaryGroup: "test",
		SecondaryGroups: []string{
			"sudo", "docker",
		},
		StartupCommand: "/bin/bash",
	}

	err := user.IsValid()
	assert.NoError(t, err)
}

func TestUserIsValidBadUid(t *testing.T) {
	user := User{
		Name: "test",
		UID:  ptrutils.PtrTo(-1),
	}

	err := user.IsValid()
	assert.ErrorContains(t, err, "user (test) is invalid")
	assert.ErrorContains(t, err, "invalid value for UID (-1), not within [0, 60000]")
}

func TestUserIsValidBadPassword(t *testing.T) {
	user := User{
		Name: "test",
		Password: &Password{
			Type:  "cat",
			Value: "dog",
		},
	}

	err := user.IsValid()
	assert.ErrorContains(t, err, "user (test) is invalid")
	assert.ErrorContains(t, err, "invalid password type (cat)")
}

func TestUserIsValidBadPasswordExpiry(t *testing.T) {
	user := User{
		Name:                "test",
		PasswordExpiresDays: ptrutils.PtrTo(int64(-2)),
	}

	err := user.IsValid()
	assert.ErrorContains(t, err, "user (test) is invalid")
	assert.ErrorContains(t, err, "invalid value for PasswordExpiresDays (-2), not within [-1, 99999]")
}
