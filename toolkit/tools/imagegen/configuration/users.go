// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package configuration

import (
	"fmt"
)

// IsValid returns an error if the User struct is not valid
func (p *User) IsValid() (err error) {
	if p.PasswordExpiresDays < -1 || p.PasswordExpiresDays > 99999 {
		return fmt.Errorf("invalid value for PasswordExpiresDays (%d)", p.PasswordExpiresDays)
	}
	return
}
