// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
	"os"
	"strconv"

	"gopkg.in/yaml.v3"
)

// The file permissions to set on the file.
//
// Accepted formats:
//
// - Octal string (e.g. "660")
type FilePermissions os.FileMode

func (p *FilePermissions) IsValid() error {
	// Check if there are set bits outside of the permissions bits.
	if *p & ^FilePermissions(os.ModePerm) != 0 {
		return fmt.Errorf("0o%o contains non-permission bits", *p)
	}

	return nil
}

func (p *FilePermissions) UnmarshalYAML(value *yaml.Node) error {
	var err error

	// Try to parse as a string.
	var strValue string
	err = value.Decode(&strValue)
	if err != nil {
		return fmt.Errorf("failed to parse FilePermissions:\n%w", err)
	}

	// Try to parse the string as an octal number.
	fileModeUint, err := strconv.ParseUint(strValue, 8, 32)
	if err != nil {
		return fmt.Errorf("failed to parse FilePermissions:\n%w", err)
	}

	*p = (FilePermissions)(fileModeUint)
	return nil
}
