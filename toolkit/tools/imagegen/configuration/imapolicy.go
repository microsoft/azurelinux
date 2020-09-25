// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
)

// ImaPolicy sets the ima_policy kernel command line option
type ImaPolicy string

const (
	// ImaPolicyTcb selects the tcb IMA policy
	ImaPolicyTcb ImaPolicy = "tcb"
	// ImaPolicyAppraiseTcb selects the appraise_tcb IMA policy
	ImaPolicyAppraiseTcb ImaPolicy = "appraise_tcb"
	// ImaPolicySecureBoot selects the secure_boot IMA policy
	ImaPolicySecureBoot ImaPolicy = "secure_boot"
	// ImaPolicyNone selects no IMA policy
	ImaPolicyNone ImaPolicy = ""
)

func (i ImaPolicy) String() string {
	return fmt.Sprint(string(i))
}

// GetValidImaPolicies returns a list of all the supported
// disk partition types
func (i *ImaPolicy) GetValidImaPolicies() (types []ImaPolicy) {
	return []ImaPolicy{
		ImaPolicyTcb,
		ImaPolicyAppraiseTcb,
		ImaPolicySecureBoot,
		ImaPolicyNone,
	}
}

// IsValid returns an error if the ImaPolicy is not valid
func (i *ImaPolicy) IsValid() (err error) {
	for _, valid := range i.GetValidImaPolicies() {
		if *i == valid {
			return
		}
	}
	return fmt.Errorf("invalid value for ImaPolicy (%s)", i)
}

// UnmarshalJSON Unmarshals an ImaPolicy entry
func (i *ImaPolicy) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypeImaPolicy ImaPolicy
	err = json.Unmarshal(b, (*IntermediateTypeImaPolicy)(i))
	if err != nil {
		return fmt.Errorf("failed to parse [ImaPolicy]: %w", err)
	}

	// Now validate the resulting unmarshaled object
	err = i.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [ImaPolicy]: %w", err)
	}
	return
}
