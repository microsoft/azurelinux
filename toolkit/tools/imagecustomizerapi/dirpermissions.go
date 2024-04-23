// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

//

package imagecustomizerapi

import (
	"fmt"
	"os"
)

// The file permissions to set on the directory.
//
// Accepted formats:
//
// - Octal string (e.g. "660")
type DirPermissions os.FileMode

func (p *DirPermissions) IsValid() (err error) {
	// Check if there are set bits outside of the permissions bits.
	if *p & ^DirPermissions(os.ModePerm) != 0 {
		return fmt.Errorf("0o%o contains non-permission bits", *p)
	}

	return nil
}
