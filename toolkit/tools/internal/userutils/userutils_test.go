// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package userutils

import (
	"os"
	"path/filepath"
	"strings"
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

func TestHashPasswordEmpty(t *testing.T) {
	hashedPassword, err := HashPassword("")
	assert.NoError(t, err, "hash password")
	assert.Equal(t, "", hashedPassword)
}

func TestHashPasswordNotEmpty(t *testing.T) {
	hashedPassword, err := HashPassword("password")
	assert.NoError(t, err, "hash password")
	assert.True(t, strings.HasPrefix(hashedPassword, "$6$"), "password prefix")
}

func TestUpdateUserPasswordEmptyToEmpty(t *testing.T) {
	testUpdateUserPassword(t, "root:*:19634:7:99999:7:::", "root:*:19634:7:99999:7:::", "root", "")
}

func TestUpdateUserPasswordSomethingToEmpty(t *testing.T) {
	testUpdateUserPassword(t,
		"root:$6$E0M9VkDvOLvO$nr9FjmIiSSP5C5V3Lhuqv4VzWmscABoiQ0mF.ZTbwKEN4nS60nsiU17qA/RGMbXHtJfci/DeLT1Zu2nhNFbwQ.:19634:7:99999:7:::",
		"root:*:19634:7:99999:7:::",
		"root",
		"")
}

func TestUpdateUserPassword(t *testing.T) {
	testUpdateUserPassword(t,
		"root:*:19634:7:99999:7:::",
		"root:$6$E0M9VkDvOLvO$nr9FjmIiSSP5C5V3Lhuqv4VzWmscABoiQ0mF.ZTbwKEN4nS60nsiU17qA/RGMbXHtJfci/DeLT1Zu2nhNFbwQ.:19634:7:99999:7:::",
		"root",
		"$6$E0M9VkDvOLvO$nr9FjmIiSSP5C5V3Lhuqv4VzWmscABoiQ0mF.ZTbwKEN4nS60nsiU17qA/RGMbXHtJfci/DeLT1Zu2nhNFbwQ.")
}

func testUpdateUserPassword(t *testing.T, originalShadowFile string, expectedShadowFile string, user string, hashedPassword string) {
	rootFilePath := tmpDir

	writeTestShadowFile(t, rootFilePath, originalShadowFile)

	err := UpdateUserPassword(rootFilePath, user, hashedPassword)
	if !assert.NoError(t, err, "update password") {
		return
	}

	actualShadowFileBytes, err := os.ReadFile(filepath.Join(rootFilePath, ShadowFile))
	if !assert.NoError(t, err, "read updated shadow file") {
		return
	}

	assert.Equal(t, expectedShadowFile, string(actualShadowFileBytes))
}

func TestUpdateUserPasswordMissingUser(t *testing.T) {
	rootFilePath := tmpDir

	writeTestShadowFile(t, rootFilePath, "root:!:19634:7:99999:7:::")

	err := UpdateUserPassword(rootFilePath, "test", "")
	if !assert.ErrorContains(t, err, "failed to find user", "update password") {
		return
	}
}

func writeTestShadowFile(t *testing.T, rootFilePath string, content string) {
	shadowFilePath := filepath.Join(rootFilePath, ShadowFile)

	err := os.MkdirAll(filepath.Join(rootFilePath, "/etc"), os.ModePerm)
	if !assert.NoError(t, err, "make /etc dir") {
		return
	}

	err = os.WriteFile(shadowFilePath, []byte(content), os.ModePerm)
	if !assert.NoError(t, err, "write sample shadow file") {
		return
	}
}
