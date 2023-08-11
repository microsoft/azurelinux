// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for valid options for the fips image config setting

package configuration

import (
	"encoding/json"
	"fmt"
)

type FIPSMode string

const (
	// FIPSModeDefaultOff disables fips mode
	FIPSModeDefaultOff FIPSMode = ""
	// FIPSModeDisable disables fips mode
	FIPSModeDisable FIPSMode = "disable"
	// FIPSModeEnable enables fips mode
	FIPSModeEnable FIPSMode = "enable"
)

func (f FIPSMode) String() string {
	return fmt.Sprint(string(f))
}

// GetValidFIPSMode returns a list of all the supported
// FIPSMode values
func (f *FIPSMode) GetValidFIPSMode() (types []FIPSMode) {
	return []FIPSMode{
		FIPSModeDefaultOff,
		FIPSModeDisable,
		FIPSModeEnable,
	}
}

// IsValid returns an error if the FIPSMode is not valid
func (f *FIPSMode) IsValid() (err error) {
	for _, valid := range f.GetValidFIPSMode() {
		if *f == valid {
			return
		}
	}
	return fmt.Errorf("invalid value for FIPSMode (%s)", f)
}

// UnmarshalJSON Unmarshals an FIPSMode entry
func (f *FIPSMode) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypeFIPSMode FIPSMode
	err = json.Unmarshal(b, (*IntermediateTypeFIPSMode)(f))
	if err != nil {
		return fmt.Errorf("failed to parse [FIPSMode]: %w", err)
	}

	// Validate the resulting unmarshaled object
	err = f.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [FIPSMode]: %w", err)
	}
	return
}
