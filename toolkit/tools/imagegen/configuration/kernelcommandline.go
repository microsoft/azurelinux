// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
	"strings"
)

const (
	SELinuxPolicyDefault = "selinux-policy"
)

// KernelCommandLine holds extra command line parameters which can be
// added to the grub config file.
//   - ImaPolicy: A list of IMA policies which will be used together
//   - ExtraCommandLine: Arbitrary parameters which will be appended to the
//     end of the kernel command line
type KernelCommandLine struct {
	CGroup           CGroup      `json:"CGroup"`
	ImaPolicy        []ImaPolicy `json:"ImaPolicy"`
	SELinux          SELinux     `json:"SELinux"`
	SELinuxPolicy    string      `json:"SELinuxPolicy"`
	EnableFIPS       bool        `json:"EnableFIPS"`
	ExtraCommandLine string      `json:"ExtraCommandLine"`
}

// GetSedDelimeter returns the delimeter which should be used with sed
// to find/replace the command line strings.
func (k *KernelCommandLine) GetSedDelimeter() (delimeter string) {
	return "`"
}

// IsValid returns an error if the KernelCommandLine is not valid
func (k *KernelCommandLine) IsValid() (err error) {
	err = k.CGroup.IsValid()
	if err != nil {
		return err
	}

	for _, ima := range k.ImaPolicy {
		if err = ima.IsValid(); err != nil {
			return
		}
	}

	err = k.SELinux.IsValid()
	if err != nil {
		return err
	}

	// A character needs to be set aside for use as the sed delimiter, make sure it isn't included in the provided string
	if strings.Contains(k.ExtraCommandLine, k.GetSedDelimeter()) {
		return fmt.Errorf("the 'ExtraCommandLine' field contains the %s character which is reserved for use by sed", k.GetSedDelimeter())
	}

	return
}

// UnmarshalJSON Unmarshals a KernelCommandLine entry
func (k *KernelCommandLine) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypeKernelCommandLine KernelCommandLine
	err = json.Unmarshal(b, (*IntermediateTypeKernelCommandLine)(k))
	if err != nil {
		return fmt.Errorf("failed to parse [KernelCommandLine]: %w", err)
	}

	// Now validate the resulting unmarshaled object
	err = k.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [KernelCommandLine]: %w", err)
	}
	return
}
