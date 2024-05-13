// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestPasswordIsValid(t *testing.T) {
	password := Password{
		Type:  PasswordTypeLocked,
		Value: "",
	}
	err := password.IsValid()
	assert.NoError(t, err)
}

func TestPasswordLockedHasValue(t *testing.T) {
	password := Password{
		Type:  PasswordTypeLocked,
		Value: "hello",
	}
	err := password.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "password value must be empty with type (locked)")
}

func TestPasswordInvalidType(t *testing.T) {
	password := Password{
		Type: "hello",
	}
	err := password.IsValid()
	assert.Error(t, err)
	assert.ErrorContains(t, err, "invalid password type (hello)")
}
