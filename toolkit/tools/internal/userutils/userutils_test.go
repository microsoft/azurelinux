// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package userutils

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestUserHomeDirectoryNormalUser(t *testing.T) {
	homeDir := UserHomeDirectory("test")
	assert.Equal(t, "/home/test", homeDir)
}

func TestUserHomeDirectoryRoot(t *testing.T) {
	homeDir := UserHomeDirectory("root")
	assert.Equal(t, "/root", homeDir)
}

func TestNameIsValidRoot(t *testing.T) {
	err := NameIsValid("root")
	assert.NoError(t, err)
}

func TestNameIsValidEmpty(t *testing.T) {
	err := NameIsValid("   ")
	assert.ErrorContains(t, err, "invalid")
	assert.ErrorContains(t, err, "name")
}

func TestUIDIsValidRoot(t *testing.T) {
	err := UIDIsValid(0)
	assert.NoError(t, err)
}

func TestUIDIsValidNegative(t *testing.T) {
	err := UIDIsValid(-1)
	assert.ErrorContains(t, err, "invalid")
	assert.ErrorContains(t, err, "UID")
}

func TestUIDIsValidTooLarge(t *testing.T) {
	err := UIDIsValid(60001)
	assert.ErrorContains(t, err, "invalid")
	assert.ErrorContains(t, err, "UID")
}

func TestPasswordExpiresDaysIsValidNoExpiry(t *testing.T) {
	err := PasswordExpiresDaysIsValid(-1)
	assert.NoError(t, err)
}

func TestPasswordExpiresDaysIsValidNegative(t *testing.T) {
	err := PasswordExpiresDaysIsValid(-2)
	assert.ErrorContains(t, err, "invalid")
	assert.ErrorContains(t, err, "PasswordExpiresDays")
}

func TestPasswordExpiresDaysIsValidTooLarge(t *testing.T) {
	err := PasswordExpiresDaysIsValid(100000)
	assert.ErrorContains(t, err, "invalid")
	assert.ErrorContains(t, err, "PasswordExpiresDays")
}
