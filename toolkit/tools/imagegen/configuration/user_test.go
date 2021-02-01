// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

var (
	validUsers = []User{
		{
			Name:     "basicUser",
			Password: "abc",
		},
		{
			Name:                "advancedSecureCoolUser",
			Password:            "$6$7oFZAqiJ$EqnWLXsSLwX.wrIHDH8iDGou3BgFXxx0NgMJgJ5LSYjGA09BIUwjTNO31LrS2C9890P8SzYkyU6FYsYNihEgp0",
			PasswordHashed:      true,
			PasswordExpiresDays: -1,
			UID:                 "105",
			PrimaryGroup:        "testgroup",
			SecondaryGroups: []string{
				"groupa",
				"groupb",
			},
			SSHPubKeyPaths: []string{
				"firstSSHKey.pub",
				"secondSSHKey.pub",
			},
			StartupCommand: "/usr/bin/somescript",
		},
	}
	invalidUserNoPassword = []User{
		{
			Name: "badUser",
		},
	}
)

// TestMain found in configuration_test.go.

func TestShouldPassParsingTestConfig_User(t *testing.T) {
	for _, b := range validUsers {
		var checkedUser User
		assert.NoError(t, b.IsValid())
		err := remarshalJSON(b, &checkedUser)
		assert.NoError(t, err)
		assert.Equal(t, b, checkedUser)
	}
}

// TestShouldFailParsingInvalidName
// validates that an empty user.name fails IsValid
func TestShouldFailParsingInvalidName_User(t *testing.T) {
	var checkedUser User
	testUser := validUsers[1]
	testUser.Name = ""

	err := testUser.NameIsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for name (), name cannot be empty", err.Error())

	err = remarshalJSON(testUser, &checkedUser)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [User]: invalid value for name (), name cannot be empty", err.Error())
}

// TestShouldFailParsingInvalidUID
// validates that UID out of range fails IsValid
func TestShouldFailParsingInvalidUIDLowerBound_User(t *testing.T) {
	var checkedUser User
	testUser := validUsers[1]
	testUser.UID = "-2"
	err := testUser.UIDIsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for UID (-2), not within [0, 60000]", err.Error())

	err = testUser.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for UID (-2), not within [0, 60000]", err.Error())

	err = remarshalJSON(testUser, &checkedUser)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [User]: invalid value for UID (-2), not within [0, 60000]", err.Error())
}

// TestShouldFailParsingInvalidUID
// validates that UID out of range fails IsValid
func TestShouldFailParsingInvalidUIDUpperBound_User(t *testing.T) {
	var checkedUser User
	testUser := validUsers[1]
	testUser.UID = "60001"
	err := testUser.UIDIsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for UID (60001), not within [0, 60000]", err.Error())

	err = testUser.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for UID (60001), not within [0, 60000]", err.Error())

	err = remarshalJSON(testUser, &checkedUser)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [User]: invalid value for UID (60001), not within [0, 60000]", err.Error())
}

// TestShouldFailParsingInvalidPasswordSet
// validates that empty password field fails if not root
func TestShouldFailParsingInvalidPasswordSet(t *testing.T) {
	var checkedUser User
	testUser := validUsers[1]
	testUser.Password = ""
	err := testUser.PasswordIsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for Password (empty)", err.Error())

	err = testUser.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for Password (empty)", err.Error())

	err = remarshalJSON(testUser, &checkedUser)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [User]: invalid value for Password (empty)", err.Error())
}

// TestShouldFailParsingInvalidPasswordMissingField
// validates that empty password field fails if not root
func TestShouldFailParsingInvalidPasswordMissingField(t *testing.T) {
	var checkedUser User
	testUser := invalidUserNoPassword[0]

	err := testUser.PasswordIsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for Password (empty)", err.Error())

	err = testUser.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for Password (empty)", err.Error())

	err = remarshalJSON(testUser, &checkedUser)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [User]: invalid value for Password (empty)", err.Error())
}

// TestShouldPassParsingRootPassword
// validates that empty password passes if root
func TestShouldPassParsingRootPassword(t *testing.T) {
	var checkedUser User
	testUser := validUsers[1]
	testUser.Name = "root"
	testUser.Password = ""
	err := testUser.PasswordIsValid()
	assert.NoError(t, err)

	err = remarshalJSON(testUser, &checkedUser)
	assert.NoError(t, err)
}

// TestShouldFailParsingInvalidPasswordExpiresDays
// validates that -2 fails IsValid as it is outside bounds
func TestShouldFailParsingInvalidPasswordExpiresDaysLowerBound_User(t *testing.T) {
	var checkedUser User
	testUser := validUsers[1]
	testUser.PasswordExpiresDays = -2
	err := testUser.PasswordExpiresDaysIsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for PasswordExpiresDays (-2), not within [-1, 99999]", err.Error())

	err = testUser.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for PasswordExpiresDays (-2), not within [-1, 99999]", err.Error())

	err = remarshalJSON(testUser, &checkedUser)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [User]: invalid value for PasswordExpiresDays (-2), not within [-1, 99999]", err.Error())
}

// TestShouldFailParsingInvalidPasswordExpiresDays
// validates that 100000 fails IsValid as it is outside bounds
func TestShouldFailParsingInvalidPasswordExpiresDayUpperBound_User(t *testing.T) {
	var checkedUser User
	testUser := validUsers[1]
	testUser.PasswordExpiresDays = 100000
	err := testUser.PasswordExpiresDaysIsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for PasswordExpiresDays (100000), not within [-1, 99999]", err.Error())

	err = testUser.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for PasswordExpiresDays (100000), not within [-1, 99999]", err.Error())

	err = remarshalJSON(testUser, &checkedUser)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [User]: invalid value for PasswordExpiresDays (100000), not within [-1, 99999]", err.Error())
}
