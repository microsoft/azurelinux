// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

//TestMain found in configuration_test.go.

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
//validates that an empty user.password fails IsValid
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
func TestShouldFailParsingInvalidPassword(t *testing.T) {
	var test_user User
	test_user.Password = ""
	err := test_user.PasswordIsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for Password ()", err.Error())
}

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
