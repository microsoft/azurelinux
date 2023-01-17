// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
)

// CGroup sets the CGroup version
type CGroup string

const (
	// CGroupDefault enables cgroupv1
	CGroupDefault CGroup = ""
	// CGroupV1 enables cgroupv1
	CGroupV1 CGroup = "version_one"
	// CGroupV2 enables cgroupv2
	CGroupV2 CGroup = "version_two"
)

func (c CGroup) String() string {
	return fmt.Sprint(string(c))
}

// GetValidCGroup returns a list of all the supported
// cgroup version options
func (c *CGroup) GetValidCGroup() (types []CGroup) {
	return []CGroup{
		CGroupDefault,
		CGroupV1,
		CGroupV2,
	}
}

// IsValid returns an error if the CGroup is not valid
func (c *CGroup) IsValid() (err error) {
	for _, valid := range c.GetValidCGroup() {
		if *c == valid {
			return
		}
	}
	return fmt.Errorf("invalid value for CGroup (%s)", c)
}

// UnmarshalJSON Unmarshals a CGroup entry
func (c *CGroup) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypeCGroup CGroup
	err = json.Unmarshal(b, (*IntermediateTypeCGroup)(c))
	if err != nil {
		return fmt.Errorf("failed to parse [CGroup]: %w", err)
	}

	// Now validate the resulting unmarshaled object
	err = c.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [CGroup]: %w", err)
	}
	return
}
