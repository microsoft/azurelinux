// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
)

// SELinux sets the SELinux mode
type SELinux string

const (
	// SELinuxOff disables SELinux
	SELinuxOff SELinux = ""
	// SELinuxEnforcing sets SELinux to enforcing
	SELinuxEnforcing SELinux = "enforcing"
	// SELinuxPermissive sets SELinux to permissive
	SELinuxPermissive SELinux = "permissive"
	// SELinuxForceEnforcing both sets SELinux to enforcing, and forces it via the kernel command line
	SELinuxForceEnforcing SELinux = "force_enforcing"
)

func (s SELinux) String() string {
	return fmt.Sprint(string(s))
}

// GetValidImaPolicies returns a list of all the supported
// disk partition types
func (s *SELinux) GetValidSELinux() (types []SELinux) {
	return []SELinux{
		SELinuxOff,
		SELinuxEnforcing,
		SELinuxForceEnforcing,
		SELinuxPermissive,
	}
}

// IsValid returns an error if the SELinux is not valid
func (s *SELinux) IsValid() (err error) {
	for _, valid := range s.GetValidSELinux() {
		if *s == valid {
			return
		}
	}
	return fmt.Errorf("invalid value for SELinux (%s)", s)
}

// UnmarshalJSON Unmarshals an SELinux entry
func (s *SELinux) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypeSELinux SELinux
	err = json.Unmarshal(b, (*IntermediateTypeSELinux)(s))
	if err != nil {
		return fmt.Errorf("failed to parse [SELinux]: %w", err)
	}

	// Now validate the resulting unmarshaled object
	err = s.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [SELinux]: %w", err)
	}
	return
}
