// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
)

// VerityErrorBehavior sets the error behavior for the root FS verity disk
type VerityErrorBehavior string

const (
	// VerityErrorBehaviorIgnore ignores corruption
	VerityErrorBehaviorIgnore VerityErrorBehavior = "ignore"
	// VerityErrorBehaviorRestart restarts the device when corrupt blocks are found
	VerityErrorBehaviorRestart VerityErrorBehavior = "restart"
	// VerityErrorBehaviorPanic panics the kernel when corrupt blocks are found
	VerityErrorBehaviorPanic VerityErrorBehavior = "panic"
	// VerityErrorBehaviorDefault does not explicitly set the error behavior
	VerityErrorBehaviorDefault VerityErrorBehavior = ""
)

func (v VerityErrorBehavior) String() string {
	return fmt.Sprint(string(v))
}

// GetValidVerityErrorBehaviors returns a list of all the supported
// verity error handling behaviors
func (v *VerityErrorBehavior) GetValidVerityErrorBehaviors() (types []VerityErrorBehavior) {
	return []VerityErrorBehavior{
		VerityErrorBehaviorIgnore,
		VerityErrorBehaviorRestart,
		VerityErrorBehaviorPanic,
		VerityErrorBehaviorDefault,
	}
}

// IsValid returns an error if the VerityErrorBehavior is not valid
func (v *VerityErrorBehavior) IsValid() (err error) {
	for _, valid := range v.GetValidVerityErrorBehaviors() {
		if *v == valid {
			return
		}
	}
	return fmt.Errorf("invalid value for VerityErrorBehavior (%s)", v)
}

// UnmarshalJSON Unmarshals an VerityErrorBehavior entry
func (v *VerityErrorBehavior) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypeVerityErrorBehavior VerityErrorBehavior
	err = json.Unmarshal(b, (*IntermediateTypeVerityErrorBehavior)(v))
	if err != nil {
		return fmt.Errorf("failed to parse [VerityErrorBehavior]: %w", err)
	}

	// Now validate the resulting unmarshaled object
	err = v.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [VerityErrorBehavior]: %w", err)
	}
	return
}
