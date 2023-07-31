// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

//

package configuration

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
)

// The file permissions to set on the file.
//
// Accepted formats:
//
// - Octal string (e.g. "660")
type FilePermissions os.FileMode

func (p *FilePermissions) IsValid() (err error) {
	// Check if there are set bits outside of the permissions bits.
	if *p & ^FilePermissions(os.ModePerm) != 0 {
		return fmt.Errorf("0o%o contains non-permission bits", *p)
	}

	return nil
}

func (p *FilePermissions) UnmarshalJSON(b []byte) error {
	var err error

	// Try to parse as a string.
	var strValue string
	err = json.Unmarshal(b, &strValue)
	if err != nil {
		return fmt.Errorf("failed to parse [FilePermissions]: %w", err)
	}

	// Try to parse the string as an octal number.
	fileModeUint, err := strconv.ParseUint(strValue, 8, 32)
	if err != nil {
		return fmt.Errorf("failed to parse [FilePermissions]: %w", err)
	}

	*p = (FilePermissions)(fileModeUint)

	// Validate the unmarshaled object.
	err = p.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [FilePermissions]: %w", err)
	}

	return nil
}

func (p FilePermissions) MarshalJSON() ([]byte, error) {
	strValue := strconv.FormatUint(uint64(p), 8)
	return json.Marshal(strValue)
}
