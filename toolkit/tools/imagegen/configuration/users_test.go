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
			Name: "basicuser",
			Password: "abc",
		},
		{
			Name: "advancedSecureCoolUser",
			Password: "$6$7oFZAqiJ$EqnWLXsSLwX.wrIHDH8iDGou3BgFXxx0NgMJgJ5LSYjGA09BIUwjTNO31LrS2C9890P8SzYkyU6FYsYNihEgp0",
			PasswordHashed: true,
			PasswordExpiresDays: -1,
			UID: "105",
			PrimaryGroup: "testgroup",
			SecondaryGroups: []string {
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
)
//TestMain found in configuration_test.go.

func TestShouldPassParsingTestConfig(t *testing.T) {
	for _, b := range validUsers {
		assert.NoError(t, b.IsValid())
	}
}

//TestShouldFailParsingInvalidName
//validates that an empty user.name fails IsValid
func TestShouldFailParsingInvalidName(t *testing.T) {
	var test_user User
	test_user.Name = ""
	err := test_user.NameIsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for name ()", err.Error())
}

//TestShouldFailParsingInvalidUID
//validates that UID out of range fails IsValid
func TestShouldFailParsingInvalidUID(t *testing.T) {
	var test_user User
	test_user.UID = "-2"
	err := test_user.UIDIsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for UID (-2)", err.Error())

	test_user.UID = "60001"
	err = test_user.UIDIsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for UID (60001)", err.Error())
}

//TestShouldFailParsingInvalidPassword
//validates that an empty user.password fails IsValid
/* func TestShouldFailParsingInvalidPassword(t *testing.T) {
	var test_user User
	test_user.Password = ""
	err := test_user.PasswordIsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for Password ()", err.Error())
} */

//TestShouldFailParsingInvalidPasswordExpiresDays
//validates that -2 and 100000 fail IsValid as they are outside bounds
func TestShouldFailParsingInvalidPasswordExpiresDays(t *testing.T) {
	var test_user User
	test_user.PasswordExpiresDays = -2
	err := test_user.PasswordExpiresDaysIsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for PasswordExpiresDays (-2)", err.Error())

	test_user.PasswordExpiresDays = 100000
	err = test_user.PasswordExpiresDaysIsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for PasswordExpiresDays (100000)", err.Error())
}
