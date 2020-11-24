// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

//TestMain found in configuration_test.go.

func TestShouldFailParsingInvalidPasswordExpire(t *testing.T) {
	var test_user User
	test_user.PasswordExpiresDays = -2
	err := test_user.IsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for PasswordExpiresDays (-2)", err.Error())
}